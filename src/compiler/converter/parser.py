from src.globals import (
    INSTRUCTION_MARKER, PARAMETER_MARKER, ASSIGNMENT_MARKER, LOCATE
)

class ParameterParser():
    def __init__(self, instructions: str) -> None:
        self.instructions = instructions.split(INSTRUCTION_MARKER)
        self.commands = []
        self.locate_commands = []

    def cmd_seq(self):
        return self.commands, self.locate_commands

    def parse(self):
        for instruct in self.instructions:
            command, parameters = self._split(instruction=instruct)
            
            if command == LOCATE:
                obj = parameters["object"].strip('"').strip("'")
                self.locate_commands.append(obj)
                continue

            self.commands.append((command, parameters))
    
    def print_cmds(self):
        for c, p in self.commands:
            print(c)
            for key in p:
                print(f"\t{key}: {p[key]}")
        
        print()

        for obj in self.locate_commands:
            print(obj)

    def _split(self, instruction: str):
        split_instruc = instruction.split(PARAMETER_MARKER)
        command = split_instruc[0].lower()

        if len(split_instruc) == 1:
            return command, {}
        
        parameters = {}
        for param in split_instruc[1:]:
            if ASSIGNMENT_MARKER not in param:
                return None, None
            
            p, v = param.split(ASSIGNMENT_MARKER)

            parameters[p] = v.lower()
        
        return command, parameters

# Example usage
if __name__ == "__main__":
    example1 = "takeoff, distance_move forward_distance=4 up_distance=3, locate object=table"

    parser = ParameterParser(instructions=example1)
    parser.parse()
    parser.print_cmds()

    commands, locate_commands = parser.cmd_seq()
    print(commands)
    print(locate_commands)