class Robot:
    dirs = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
    MIN_COORD = 0
    MAX_COORD = 100

    def __init__(self, coordinates: tuple):
        self.x, self.y = coordinates
        self.path_list = [coordinates]

    def move(self, step_commands: str):
        self.path_list = [self.path_list[-1]]
        for command in step_commands:
            step = Robot.dirs.get(command, (0, 0))
            self.x += step[0]
            self.y += step[1]
            self.check_borders()
            self.path_list.append((self.x, self.y))
        return self.x, self.y

    def check_borders(self):
        self.x = max(min(self.x, Robot.MAX_COORD), Robot.MIN_COORD)
        self.y = max(min(self.y, Robot.MAX_COORD), Robot.MIN_COORD)

    def path(self):
        return self.path_list
