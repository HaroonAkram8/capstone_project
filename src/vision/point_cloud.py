import cv2
import numpy as np
import open3d as o3d

class PointCloud:
    def __init__(self, ):
        self.pcd = o3d.geometry.PointCloud()
        self.intrinsic = o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)
    
    def map_3d(self, rgb_image, depth_image, bboxes):
        curr_pcd = self._pcd_from_img(rgb_image=rgb_image, depth_image=depth_image)
        self._merge_pcds(curr_pcd=curr_pcd)

        square_2d = self._normalize_bbox_to_pcd(bboxes=bboxes, depth_image=depth_image)

        # Connect points to form edges (square is a closed loop)
        lines = [
            [0, 1],  # Bottom edge
            [1, 2],  # Right edge
            [2, 3],  # Top edge
            [3, 0],  # Left edge
        ]

        # Define the colors for the lines
        colors = [[1, 0, 0] for _ in lines]  # Red color for all edges

        # Create a LineSet for the square
        line_set = o3d.geometry.LineSet()
        line_set.points = o3d.utility.Vector3dVector(square_2d[0])
        line_set.lines = o3d.utility.Vector2iVector(lines)
        line_set.colors = o3d.utility.Vector3dVector(colors)

        # Visualize point cloud and square
        o3d.visualization.draw_geometries([self.pcd, line_set], zoom=0.5)
    
    def show_env(self,):
        o3d.visualization.draw_geometries([self.pcd], zoom=0.5)
    
    def _pcd_from_img(self, rgb_image, depth_image):
        depth_image = depth_image.astype(np.float32) / 1000.0

        rgb_o3d = o3d.geometry.Image(rgb_image)
        depth_o3d = o3d.geometry.Image(depth_image)

        rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(rgb_o3d, depth_o3d)

        curr_pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, self.intrinsic)
        curr_pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]) # Flip it, otherwise the pointcloud will be upside down

        return curr_pcd
    
    def _merge_pcds(self, curr_pcd):
        # UNFINISHED
        # Currently, the points will overlap on top of each other
        # Either use Visual Odometry or SLAM to keep track of camera position to dynamically map environment
        self.pcd += curr_pcd
    
    def _normalize_bbox_to_pcd(self, bboxes, depth_image):
        normalized_bboxes = []
        fx = self.intrinsic.intrinsic_matrix[0, 0]
        fy = self.intrinsic.intrinsic_matrix[1, 1]
        cx = self.intrinsic.intrinsic_matrix[0, 2]
        cy = self.intrinsic.intrinsic_matrix[1, 2]

        height, width = depth_image.shape  # Get depth image dimensions

        for bbox in bboxes:
            normalized_bbox = []
            for corner in bbox:
                u, v = corner[:2]  # Pixel coordinates
                
                # Ensure the coordinates are within the valid range
                if 0 <= u < width and 0 <= v < height:
                    Z = depth_image[int(v), int(u)] / 1000.0  # Convert to meters
                    if Z > 0:  # Valid depth value
                        X = (u - cx) * Z / fx
                        Y = (v - cy) * Z / fy
                        normalized_bbox.append([X, Y, Z])
                    else:
                        print(f"Skipping invalid depth at ({u}, {v})")
                else:
                    print(f"Skipping out-of-bounds corner: ({u}, {v})")
            if normalized_bbox:
                normalized_bboxes.append(normalized_bbox)
        return normalized_bboxes



if __name__ == "__main__":
    from ultralytics import YOLOWorld

    # Initialize a YOLO-World model
    model = YOLOWorld("yolov8s-world.pt")  # or select yolov8m/l-world.pt for different sizes

    # Execute inference with the YOLOv8s-world model on the specified image
    results = model.predict("./choi/livingroom1-color/01385.jpg")

    class_names = model.names
    bboxes = []

    # Extract bounding boxes
    for result in results:
        boxes = result.boxes.xyxy  # Bounding boxes in [x_min, y_min, x_max, y_max] format
        confidences = result.boxes.conf  # Confidence scores
        classes = result.boxes.cls  # Class indices

        # Print all bounding box information
        for box, confidence, cls in zip(boxes, confidences, classes):
            box = box.tolist()
            print(f"Box: {box}, Confidence: {confidence:.2f}, Class: {class_names[int(cls)]}")

            bbox = [
                [int(box[0]), int(box[1]), 0],  # Bottom-left
                [int(box[2]), int(box[1]), 0],  # Bottom-right
                [int(box[2]), int(box[3]), 0],  # Top-right
                [int(box[0]), int(box[3]), 0],  # Top-left
            ]

            bboxes.append(bbox)
    
    print(bboxes)


    pcd = PointCloud()

    rgb_image = cv2.imread("./choi/livingroom1-color/01385.jpg")
    depth_image = cv2.imread("./choi/livingroom1-depth-clean/01385.png", cv2.IMREAD_UNCHANGED)

    pcd.map_3d(rgb_image=rgb_image, depth_image=depth_image, bboxes=bboxes)

    # rgb_image = cv2.imread("./choi/livingroom1-color/01355.jpg")
    # depth_image = cv2.imread("./choi/livingroom1-depth-clean/01355.png", cv2.IMREAD_UNCHANGED)

    # pcd.map_3d(rgb_image=rgb_image, depth_image=depth_image)

    # pcd.show_env()
