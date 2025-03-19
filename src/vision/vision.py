import math
from ultralytics import YOLOWorld

from src.vision.object import Object

class VisionModel:
    def __init__(self, model_name: str="yolov8s-world.pt", simulation: bool=True, current_position=None, camera_intrinsics=None):
        self.model_name = model_name
        self.vision_model = YOLOWorld(self.model_name)
        self.class_names = self.vision_model.names

        self.current_position = current_position
        self.object_states = {}

        self.camera_intrinsics = camera_intrinsics

        self.locate = self._sim_locate
        if not simulation:
            self.locate = self._irl_locate
    
    def set_current_location(self, current_position):
        self.current_position = current_position
    
    def set_camera_intrinsics(self, camera_intrinsics):
        self.camera_intrinsics = camera_intrinsics
    
    def find_objects(self, rgb_image, depth_image, classes: list=None):
        results = self.predict(image=rgb_image, classes=classes)
        self.parse_results(results=results, depth_data=depth_image)
    
    def get_object_states(self):
        return self.object_states

    def predict(self, image, classes: list=None):
        if classes is not None:
            self.vision_model.set_classes(classes)
            self.class_names = self.vision_model.names

        results = self.vision_model.predict(image)

        return results
    
    def reset_model_classes(self,):
        self.vision_model = YOLOWorld(self.model_name)
        self.class_names = self.vision_model.names
    
    def parse_results(self, results, depth_data):
        curr_pos = self.current_position()

        for result in results:
            boxes = result.boxes.xyxy
            confidences = result.boxes.conf
            classes = result.boxes.cls

            for box, confidence, cls in zip(boxes, confidences, classes):
                x_min, y_min, x_max, y_max = box.tolist()

                x_centre = int((x_min + x_max) / 2)
                y_centre = int((y_min + y_max) / 2)

                location = self.locate(depth_data=depth_data, x_centre=x_centre, y_centre=y_centre, curr_pos=curr_pos)
                name = self.class_names[int(cls)]

                obj = Object(name=name, confidence=confidence, location=location)

                if obj.name not in self.object_states or self.object_states[obj.name].confidence < obj.confidence:
                    self.object_states[obj.name] = obj
    
    def _sim_locate(self, depth_data, x_centre: int, y_centre: int, curr_pos: dict):
        relative_location = self._relative_locate(depth_data=depth_data, x_centre=x_centre, y_centre=y_centre)
        location = self._transform_location(relative_location=relative_location, curr_pos=curr_pos)
        return location
    
    def _transform_location(self, relative_location: dict, curr_pos: dict):
        X = curr_pos["x"] + relative_location["x"] * math.sin(curr_pos["yaw"]) + relative_location["z"] * math.cos(curr_pos["yaw"])
        Y = curr_pos["y"] + relative_location["x"] * math.cos(curr_pos["yaw"]) - relative_location["z"] * math.sin(curr_pos["yaw"])
        Z = curr_pos["z"] - relative_location["y"] # z is negative

        location = {
            "x": round(X, 2),
            "y": round(Y, 2),
            "z": round(Z, 2)
        }

        return location
    
    def _relative_locate(self, depth_data, x_centre: int, y_centre: int):
        fx, fy, cx, cy = self.camera_intrinsics

        Z = depth_data[y_centre, x_centre]
        if Z == 0:
            return None

        X = (x_centre - cx) * Z / fx
        Y = (y_centre - cy) * Z / fy

        return {
            "x": float(X),
            "y": float(Y),
            "z": float(Z)
        }

    def _irl_locate(self, depth_data, x_centre: int, y_centre: int, curr_pos: dict):
        pass

if __name__ == "__main__":
    vision_model = VisionModel()

    results = vision_model.predict(image="./class.jpg", classes=["clock", "chair"])
    vision_model.parse_results(results=results)

    vision_model.reset_model_classes()

    results = vision_model.predict(image="./class.jpg")
    vision_model.parse_results(results=results)