from ultralytics import YOLOWorld

from src.vision.object import Object

class VisionModel:
    def __init__(self, model_name: str="yolov8s-world.pt", simulation: bool=True, curr_loc: list=[0.0, 0.0, 0.0]):
        self.model_name = model_name
        self.vision_model = YOLOWorld(self.model_name)
        self.class_names = self.vision_model.names

        self.curr_loc = curr_loc
        self.object_states = {}

        self.camera_intrinsics = None

        self.locate = self._sim_locate
        if not simulation:
            self.locate = self._irl_locate
    
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
        for result in results:
            boxes = result.boxes.xyxy
            confidences = result.boxes.conf
            classes = result.boxes.cls

            for box, confidence, cls in zip(boxes, confidences, classes):
                x_min, y_min, x_max, y_max = box.tolist()

                x_centre = int((x_min + x_max) / 2)
                y_centre = int((y_min + y_max) / 2)

                location = self.locate(depth_data=depth_data, x_centre=x_centre, y_centre=y_centre)
                name = self.class_names[int(cls)]

                obj = Object(name=name, confidence=confidence, location=location)

                if obj.name not in self.object_states or self.object_states[obj.name].confidence < obj.confidence:
                    self.object_states[obj.name] = obj
    
    def _sim_locate(self, depth_data, x_centre: int, y_centre: int):
        location = self._relative_locate(depth_data=depth_data, x_centre=x_centre, y_centre=y_centre)
        return location
    
    def _relative_locate(self, depth_data, x_centre: int, y_centre: int):
        fx, fy, cx, cy = self.camera_intrinsics

        Z = depth_data[y_centre, x_centre]
        if Z == 0:
            return None

        X = (x_centre - cx) * Z / fx
        Y = (y_centre - cy) * Z / fy

        return {
            "relative_x": float(X),
            "relative_y": float(Y),
            "relative_z": float(Z)
        }

    def _irl_locate(self, depth_data, x_centre: int, y_centre: int):
        pass

if __name__ == "__main__":
    vision_model = VisionModel()

    results = vision_model.predict(image="./class.jpg", classes=["clock", "chair"])
    vision_model.parse_results(results=results)

    vision_model.reset_model_classes()

    results = vision_model.predict(image="./class.jpg")
    vision_model.parse_results(results=results)