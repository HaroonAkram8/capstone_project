import cv2
import numpy as np
import open3d as o3d

class PointCloud:
    def __init__(self, ):
        self.pcd = o3d.geometry.PointCloud()
        self.intrinsic = o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)
    
    def map_3d(self, rgb_image, depth_image):
        curr_pcd = self._pcd_from_img(rgb_image=rgb_image, depth_image=depth_image)
        self._merge_pcds(curr_pcd=curr_pcd)
    
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


if __name__ == "__main__":
    pcd = PointCloud()

    rgb_image = cv2.imread("./choi/livingroom1-color/00000.jpg")
    depth_image = cv2.imread("./choi/livingroom1-depth-clean/00000.png", cv2.IMREAD_UNCHANGED)

    pcd.map_3d(rgb_image=rgb_image, depth_image=depth_image)

    # rgb_image = cv2.imread("./choi/livingroom1-color/00105.jpg")
    # depth_image = cv2.imread("./choi/livingroom1-depth-clean/00105.png", cv2.IMREAD_UNCHANGED)

    # pcd.map_3d(rgb_image=rgb_image, depth_image=depth_image)

    pcd.show_env()
