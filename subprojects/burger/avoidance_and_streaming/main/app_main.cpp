/* combined_app.cpp */

#include <sys/param.h>
#include <cstdio>
#include <cstdint>
#include <cstddef>
#include <cstring>
#include <chrono>
#include <cmath>
#include <mutex>
#include <condition_variable>
#include <vector>
#include <unistd.h>

// ESP-IDF includes
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "esp_netif.h"
#include "protocol_examples_common.h"

// FreeRTOS includes
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// Application-specific includes
#include "esp32_spi_impl.h"
#include "spi_api.hpp"

// Define the obstacle message rate if not already defined
#ifndef OBSTACLE_SEND_RATE_HZ
#define OBSTACLE_SEND_RATE_HZ 15
#endif

//------------------------------------------------------------------------------
// Global variables for MJPEG streaming
//------------------------------------------------------------------------------
static const char* PREVIEWSTREAM = "spipreview";
uint32_t example_chunk_recv_size = 0;
std::mutex receiverSocketsMtx;
std::vector<int> receiverSockets;
std::condition_variable receiverSocketsCv;

//------------------------------------------------------------------------------
// HTTP MJPEG streaming GET request handler
//------------------------------------------------------------------------------
esp_err_t get_frame_handler(httpd_req_t *req) {
    const char INITIAL[] =
        "HTTP/1.1 200 OK\r\n"
        "Content-type: multipart/x-mixed-replace; boundary=--jpgboundary\r\n"
        "\r\n";
    httpd_send(req, INITIAL, strlen(INITIAL));

    int socket = httpd_req_to_sockfd(req);
    {
        std::unique_lock<std::mutex> lock(receiverSocketsMtx);
        receiverSockets.push_back(socket);
        receiverSocketsCv.notify_all();
    }
    return ESP_OK;
}

//------------------------------------------------------------------------------
// Callback for SPI data chunk streaming (used by both functionalities)
//------------------------------------------------------------------------------
void mjpeg_streaming_message(void* received_packet, uint32_t packet_size, uint32_t message_size) {
    std::unique_lock<std::mutex> lock(receiverSocketsMtx);
    for(auto it = receiverSockets.begin(); it != receiverSockets.end(); ) {
        bool socketError = false;
        // At start of a new message, send headers
        if(example_chunk_recv_size == 0){
            printf("Sending out new mjpeg image..., message size: %d\n", message_size);
            const char ITERATION[] =
                "--jpgboundary\r\n"
                "Content-type: image/jpeg\r\n";
            char contentLength[256];
            memset(contentLength, 0, sizeof(contentLength));
            snprintf(contentLength, sizeof(contentLength), "Content-length: %d\r\n\r\n", message_size);

            if(write(*it, ITERATION, sizeof(ITERATION) - 1) <= 0){
                socketError = true;
            }
            if(write(*it, contentLength, strlen(contentLength)) <= 0){
                socketError = true;
            }
        }
        // Send the current packet
        if(write(*it, (const char*) received_packet, packet_size) <= 0){
            socketError = true;
        }
        // If this is the last packet, send the trailing blank line
        if(example_chunk_recv_size + packet_size >= message_size){
            const char END_HEADERS[] = "\r\n";
            if(write(*it, END_HEADERS, strlen(END_HEADERS)) <= 0){
                socketError = true;
            }
        }
        if(socketError){
            it = receiverSockets.erase(it);
        } else {
            ++it;
        }
    }
    example_chunk_recv_size += packet_size;
    if(example_chunk_recv_size >= message_size){
        example_chunk_recv_size = 0;
    }
}

//------------------------------------------------------------------------------
// Task for MJPEG streaming functionality
//------------------------------------------------------------------------------
static void mjpeg_streaming_task(void *arg) {
    dai::SpiApi mySpiApi;
    mySpiApi.set_send_spi_impl(&esp32_send_spi);
    mySpiApi.set_recv_spi_impl(&esp32_recv_spi);
    mySpiApi.set_chunk_packet_cb(&mjpeg_streaming_message);

    std::vector<uint8_t> temporaryBuffer;
    temporaryBuffer.resize(64 * 1024);

    while(1) {
        // Wait until at least one client is connected
        {
            std::unique_lock<std::mutex> lock(receiverSocketsMtx);
            receiverSocketsCv.wait(lock, []{ return !receiverSockets.empty(); });
        }

        if(mySpiApi.chunk_message_buffer(PREVIEWSTREAM, temporaryBuffer.data(), temporaryBuffer.size())) {
            printf("Correctly sent out mjpeg\n");
            uint8_t req_success = mySpiApi.spi_pop_messages();
        } else {
            usleep(100);
        }
    }
    vTaskDelete(NULL);
}

//------------------------------------------------------------------------------
// Obstacle Avoidance functionality
//------------------------------------------------------------------------------
// Here we define an obstacle_avoidance class (its declaration might normally be in a header).
// It uses SPI to receive spatial data, sends heartbeat messages, and publishes obstacle data.
// Note: The actual implementations of serial_comm, MAVLink functions, and associated types 
// (such as mavlink_message_t, MAV_FRAME_BODY_FRD) are assumed to be defined elsewhere.

class obstacle_avoidance {
public:
    void send_obs_dist_3d(uint32_t time, float x, float y, float z);
    void main_loop();
};

void obstacle_avoidance::send_obs_dist_3d(uint32_t time, float x, float y, float z) {
    const float obstacle_vector[3] = { z * 0.001f, x * 0.001f, -y * 0.001f };
    uint8_t buf[2041];
    mavlink_message_t mav_msg;
    mavlink_msg_obstacle_distance_3d_pack(1, 93, &mav_msg, time, 0, MAV_FRAME_BODY_FRD, 65535,
                                            obstacle_vector[0], obstacle_vector[1], obstacle_vector[2],
                                            0.3f, 10.0f);
    uint16_t len = mavlink_msg_to_send_buffer(buf, &mav_msg);
    serial_comm.send_message(len, buf);
}

void obstacle_avoidance::main_loop() {
    dai::SpiApi mySpiApi;
    mySpiApi.set_send_spi_impl(&esp32_send_spi);
    mySpiApi.set_recv_spi_impl(&esp32_recv_spi);
    mySpiApi.set_chunk_packet_cb(&mjpeg_streaming_message);

    std::vector<uint8_t> temporaryBuffer;
    temporaryBuffer.resize(64 * 1024);

    while(true) {
        // Send a heartbeat to the autopilot
        serial_comm.send_heartbeat();

        dai::Message spatialDataMsg;
        bool receivedAnyMessage = false;

        if(mySpiApi.req_message(&spatialDataMsg, "spatialData")){
            const uint32_t msg_ms = serial_comm.get_millis_ms();
            dai::RawSpatialLocations rawSpatialLocations;
            mySpiApi.parse_metadata(&spatialDataMsg.raw_meta, rawSpatialLocations);

            static uint32_t last_obstacle_msg_ms = 0;
            if ((msg_ms - last_obstacle_msg_ms) > (1000 / OBSTACLE_SEND_RATE_HZ)) {
                last_obstacle_msg_ms = msg_ms;
                for(const auto& spatialData : rawSpatialLocations.spatialLocations){
                    auto x = spatialData.spatialCoordinates.x;
                    auto y = spatialData.spatialCoordinates.y;
                    auto z = spatialData.spatialCoordinates.z;
                    send_obs_dist_3d(msg_ms, x, y, z);
                    auto euclideanDistance = std::sqrt(x*x + y*y + z*z);
                    printf("Euclidean distance %d mm, X: %d mm, Y: %d mm, Z: %d mm \n",
                           (int)euclideanDistance, (int)x, (int)y, (int)z);
                }
            }
            mySpiApi.free_message(&spatialDataMsg);
            mySpiApi.spi_pop_message("spatialData");
            receivedAnyMessage = true;
        }

        if(!receivedAnyMessage) {
            usleep(1000);
        }
    }
}

//------------------------------------------------------------------------------
// Task for obstacle avoidance functionality
//------------------------------------------------------------------------------
static void obstacle_avoidance_task(void *arg) {
    obstacle_avoidance avoidance_grid;
    avoidance_grid.main_loop();
    vTaskDelete(NULL);
}

//------------------------------------------------------------------------------
// Combined app_main entry point
//------------------------------------------------------------------------------
extern "C" void app_main() {
    // Initialize NVS, network interface, event loop, etc.
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    ESP_ERROR_CHECK(example_connect());
    ESP_ERROR_CHECK(start_file_server());
    init_esp32_spi();

    // Launch the MJPEG streaming and obstacle avoidance tasks concurrently
    xTaskCreate(mjpeg_streaming_task, "mjpeg_task", 8192, NULL, 5, NULL);
    xTaskCreate(obstacle_avoidance_task, "obstacle_task", 8192, NULL, 5, NULL);

    // The main task can loop indefinitely (or optionally perform other work)
    while(1) {
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
    // deinit_esp32_spi();  // Not reached
}
