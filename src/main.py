from src.drone_manager import DroneManager

def main():
    drone = DroneManager(model_name="llama3")    # Use "phi3:mini" or "llama3" tto switch between models
    drone.listen()

if __name__ == "__main__":
    main()