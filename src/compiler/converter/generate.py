import math

from src.globals import MOVE_POS, MOVE_DIST, MOVE_VEL, ROTATE, WAIT, KEY_WORDS

class ParameterGenerator():
    def __init__(self, current_position) -> None:
        self.current_position = current_position
        self.mappings = {
            MOVE_POS: self._move_positionally,
            MOVE_DIST: self._move_distance,
            MOVE_VEL: self._move_velocity,
            ROTATE: self._rotate,
            WAIT: self._wait,
        }

    def generate(self, cmd, parameters):
        if cmd not in self.mappings:
            return parameters
        
        gen_p = self.mappings[cmd](parameters=parameters)

        for key in gen_p:
            gen_p[key] = round(gen_p[key], 2)

        return gen_p
    
    def _wait(self, parameters):
        duration = KEY_WORDS["intermediate"]
        if "duration" in parameters:
            duration = self._get_val(parameter_value=parameters["duration"])

        gen_p = {
            "duration": duration,
        }

        return gen_p
    
    def _rotate(self, parameters):
        duration = KEY_WORDS["intermediate"]
        if "duration" in parameters:
            duration = self._get_val(parameter_value=parameters["duration"])

        yaw_rate = self._get_val(parameter_value=parameters["yaw"]) / duration

        gen_p = {
            "yaw_rate": yaw_rate,
            "duration": duration,
        }

        return gen_p

    def _move_positionally(self, parameters):
        curr_pos = self.current_position()
        gen_p = {}

        for dir in ["x", "y", "z"]:
            if dir not in parameters:
                gen_p[dir] = curr_pos[dir]
                continue

            gen_p[dir] = self._get_val(parameter_value=parameters[dir])

        gen_p = self._velocity(parameters=parameters, curr_pos=curr_pos, gen_p=gen_p)
        return gen_p
    
    def _move_distance(self, parameters):
        curr_pos = self.current_position()

        gen_p = self._project_to_xy(parameters=parameters, yaw=curr_pos['yaw'], p_names=["forward_distance", "right_distance", "up_distance"], out_names=['x', 'y', 'z'])        
        gen_p = self._velocity(parameters=parameters, curr_pos=curr_pos, gen_p=gen_p)
        
        gen_p["x"] += curr_pos["x"]
        gen_p["y"] += curr_pos["y"]
        gen_p["z"] += curr_pos["z"]

        return gen_p
    
    def _move_velocity(self, parameters):
        curr_pos = self.current_position()

        gen_p = self._project_to_xy(parameters=parameters, yaw=curr_pos['yaw'], p_names=["forward_velocity", "right_velocity", "up_velocity"], out_names=['vx', 'vy', 'vz']) 
        gen_p = self._distance(parameters=parameters, gen_p=gen_p)

        return gen_p
    
    def _project_to_xy(self, parameters, yaw, p_names, out_names):
        for dir in p_names:
            if dir not in parameters:
                parameters[dir] = 0.0
                continue

            parameters[dir] = self._get_val(parameter_value=parameters[dir])
        
        gen_p = {
            out_names[0]: parameters[p_names[0]] * math.cos(yaw) + parameters[p_names[1]] * math.cos(math.pi / 2 - yaw),
            out_names[1]: parameters[p_names[0]] * math.sin(yaw) - parameters[p_names[1]] * math.sin(math.pi / 2 - yaw),
            out_names[2]: parameters[p_names[2]],
        }

        return gen_p
    
    def _get_val(self, parameter_value):
        try:
            value = float(parameter_value)
        except ValueError:
            if parameter_value in KEY_WORDS:
                value = KEY_WORDS[parameter_value]
            else:
                value = 1
        
        if value == 0:
            value = 1

        return value
    
    def _distance(self, parameters, gen_p):
        if "duration" in parameters:
            gen_p["duration"] = self._get_val(parameter_value=parameters["duration"])
        elif "distance" in parameters:
            gen_p["duration"] = self._get_val(parameter_value=parameters["distance"]) / self._velocity_magnitude(gen_p=gen_p)
        else:
            gen_p["duration"] = KEY_WORDS["intermediate"]
        
        return gen_p
    
    def _velocity(self, parameters, curr_pos, gen_p):
        if "velocity" in parameters:
            gen_p["velocity"] = self._get_val(parameter_value=parameters["velocity"])
        elif "duration" in parameters:
            distance = self._distance_magnitude(curr_pos=curr_pos, gen_p=gen_p)
            gen_p["velocity"] = distance / self._get_val(parameter_value=parameters["duration"])
        else:
            gen_p["velocity"] = KEY_WORDS["moderate"]
        
        return gen_p
    
    def _velocity_magnitude(self, gen_p):
        velocity = pow(gen_p["vx"] ** 2 + gen_p["vy"] ** 2 + gen_p["vz"] ** 2, 0.5)
        return velocity
    
    def _distance_magnitude(self, curr_pos, gen_p):
        distance = pow((curr_pos["x"] - gen_p["x"]) ** 2 + (curr_pos["y"] - gen_p["y"]) ** 2 + (curr_pos["z"] - gen_p["z"]) ** 2, 0.5)
        return distance

# Example usage
if __name__ == "__main__":
    def test_position():
        return {
            'x': 0.0,
            'y': 0.0,
            'z': 0.0,
            'yaw': 0
        }

    example1 = {
        "right_distance": '7',
        "velocity": '4',
    }

    generator = ParameterGenerator(current_position=test_position)

    gen_p = generator.generate(cmd=MOVE_DIST, parameters=example1)
    print(gen_p)