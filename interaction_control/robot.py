from component import *
import time


class RobotComponent(Component):
    whos_playing = None

    def run_function(self, action):
        print(self.name, action[0], action[1:])
        try:
            if action[1]:
                getattr(self, action[0])(action[1])
            else:
                getattr(self, action[0])()
            return True
        except:
            self.express(action)
        return False

    def express(self, action):
        self.current_state = action[0]
        if action[1]:
            self.current_param = action[1:]
        time.sleep(1)

    def after_called(self):
        if self.current_param:
            if isinstance(self.current_param, list):
                if 'done' in self.current_param:
                    self.current_state = 'idle'
                    self.current_param = None

    def set_playing(self, action):
        self.current_param = action[1:]
        self.whos_playing = action[0]
        print(self.whos_playing, self.current_param)

    def set_selection(self, action):
        # set the possible treasures to select from
        if self.whos_playing == 'demo':
            self.current_param = 1
        if self.whos_playing == 'robot':
            self.current_state = 'select_treasure'
            self.current_param = 2

    def win(self):
        print(self.name, self.whos_playing, 'wins!')
        if self.whos_playing == 'child':
            self.run_function(['child_win_happy', None])
        else:
            self.run_function(['robot_win_happy', None])

    def play_game(self, action):
        print(self.whos_playing, 'playing the game')