import math

from src.globals import CMD_KEY_WORDS, KEY_WORDS

class ParameterGenerator():
    def __init__(self, current_position) -> None:
        self.current_position = current_position
        self.mappings = {
            CMD_KEY_WORDS["MOVE_POS"]: self._move_positionally,
            CMD_KEY_WORDS["MOVE_DIST"]: self._move_distance,
            CMD_KEY_WORDS["MOVE_VEL"]: self._move_velocity,
        }

    def generate(self, cmd, parameters):
        if cmd not in self.mappings:
            return {}
        
        gen_p = self.mappings[cmd](parameters=parameters)
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

        for dir in ["forward_distance", "right_distance", "up_distance"]:
            if dir not in parameters:
                parameters[dir] = 0.0
                continue

            parameters[dir] = self._get_val(parameter_value=parameters[dir])
        
        gen_p = {
            'x': parameters["forward_distance"] * math.cos(curr_pos['yaw']) + parameters["right_distance"] * math.cos(math.pi / 2 - curr_pos['yaw']),
            'y': parameters["forward_distance"] * math.sin(curr_pos['yaw']) - parameters["right_distance"] * math.sin(math.pi / 2 - curr_pos['yaw']),
            'z': parameters["up_distance"],
        }
        
        gen_p = self._velocity(parameters=parameters, curr_pos=curr_pos, gen_p=gen_p)
        return gen_p
    
    def _move_velocity(self, parameters):
        curr_pos = self.current_position()
        gen_p = {}

        for dir in ["x", "y", "z"]:
            gen_p[dir] = curr_pos[dir]

            if dir not in parameters:
                continue

            gen_p[dir] += self._get_val(parameter_value=parameters[dir])
        
        gen_p = self._velocity(parameters=parameters, curr_pos=curr_pos, gen_p=gen_p)
        return gen_p
    
    def _get_val(self, parameter_value):
        try:
            value = float(parameter_value)
        except ValueError:
            value = KEY_WORDS[parameter_value]
        
        return value
    
    def _velocity(self, parameters, curr_pos, gen_p):
        if "velocity" in parameters:
            gen_p["velocity"] = self._get_val(parameter_value=parameters["velocity"])
        elif "duration" in parameters:
            distance = self._distance(curr_pos=curr_pos, gen_p=gen_p)
            gen_p["velocity"] = distance / self._get_val(parameter_value=parameters["duration"])
        else:
            gen_p["velocity"] = KEY_WORDS["MODERATE"]
        
        return gen_p
    
    def _distance(self, curr_pos, gen_p):
        distance = pow((curr_pos["x"] - gen_p["x"]) ** 2 + (curr_pos["y"] - gen_p["y"]) ** 2 + (curr_pos["z"] - gen_p["z"]) ** 2, 0.5)
        return distance

# Example usage
if __name__ == "__main__":
    def test_position():
        return {
            'x': 0.0,
            'y': 0.0,
            'z': 0.0,
            'yaw': math.pi / 3
        }

    example1 = {
        "forward_distance": '7',
        "right_distance": '4',
        "up_distance": '5',
        "velocity": '2'
    }

    generator = ParameterGenerator(current_position=test_position)

    gen_p = generator.generate(cmd=CMD_KEY_WORDS["MOVE_DIST"], parameters=example1)
    print(gen_p)