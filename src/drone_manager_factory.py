from enum import Enum

import src.drone_manager
from src.llm.llm import Models

class DroneManagerTypes(Enum):
    TestDrone = "TestDrone"
    ConcreteDrone = "ConcreteDrone"


class DroneManagerFactory:
    def create(self, drone_type: DroneManagerTypes, model: Models, system_prompt: str) -> src.drone_manager.IDroneManager:
        match drone_type:
            case DroneManagerTypes.TestDrone:
                return src.drone_manager.TestDroneManager(model, system_prompt)
            case DroneManagerTypes.ConcreteDrone:
                return src.drone_manager.DroneManager(model, system_prompt)
