from ultralytics import YOLOWorld

from src.vision.locate import sim_locate, irl_locate
from src.vision.object import Object

class VisionModel:
    def __init__(self, model_name: str="yolov8s-world.pt", simulation: bool=True, current_position=None, camera_intrinsics=None):
        self.model_name = model_name
        self.vision_model = YOLOWorld(self.model_name)
        self.class_names = self.vision_model.names

        self.current_position = current_position
        self.object_states = {}

        self.camera_intrinsics = camera_intrinsics

        self.locate = sim_locate
        if not simulation:
            self.locate = irl_locate
    
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

                location, _ = self.locate(depth_data=depth_data, camera_intrinsics=self.camera_intrinsics, x_centre=x_centre, y_centre=y_centre, curr_pos=curr_pos)
                name = self.class_names[int(cls)]

                obj = Object(name=name, confidence=confidence, location=location)

                if obj.name not in self.object_states or self.object_states[obj.name].confidence < obj.confidence:
                    self.object_states[obj.name] = obj

if __name__ == "__main__":
    vision_model = VisionModel()

    results = vision_model.predict(image="./class.jpg", classes=["clock", "chair"])
    vision_model.parse_results(results=results)

    vision_model.reset_model_classes()

    results = vision_model.predict(image="./class.jpg")
    vision_model.parse_results(results=results)