from interaction_control import *
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import Layout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.app import App
from kivy.animation import Animation
from kivy.core.window import Window
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader
from tangram_game import *


class SolveTangramRoom(Screen):
    task_json = None
    the_app = None

    def __init__(self, **kwargs):
        print("solveTangramRoom")
        super(Screen, self).__init__(**kwargs)

    def on_enter(self, *args):
        print("on_enter solve_tangram_room")
        # self.load_sounds()
        # self.play_sound("TangramOpen_myFriend")

    def init_task(self,x,the_app):
        self.task_json = x[0]
        self.the_app = the_app
        print("Solve Tangram Room init_task ", self.task_json)

        #shade:
        game_task_layout = GameTaskLayout()
        game_task_layout.reset(str(0))
        game_task_layout.import_json_task(self.task_json)
        game_task_layout.update_selection_task_shade()

        #pieces:
        self.update_task_pieces()

        tangram_game_widget = self.ids['tangram_game_widget']
        tangram_game_widget.reset() #clear the pieces from previous run
        tangram_game_widget.add_widget(game_task_layout)

        # button
        button_rotate = Rotate(self)
        button_rotate.size_hint_x = 0.1
        button_rotate.size_hint_y = 0.1
        button_rotate.pos = [15 * TangramGame.SCALE, 5 * TangramGame.SCALE]
        tangram_game_widget.add_widget(button_rotate)


    def update_task_pieces(self):
        # pieces
        self.pieces = {}
        for p in TangramPiece.tangram_list:
            self.pieces[p] = TangramPiece(self)
            self.pieces[p].name = p

        for key, value in self.pieces.items():
            value.init_position()
            value.set_shape()
            self.add_widget(value)

    def is_selected(self):
        for k, p in self.pieces.items():
            if p.selected:
                return True
        return False

    def reset_sizes(self):
        for k, p in self.pieces.items():
            p.size = [TangramPiece.piece_size[p.name][0] * TangramGame.SCALE,
                      TangramPiece.piece_size[p.name][1] * TangramGame.SCALE]

    def check_solution(self):
        "print check_solution"
        solution_json = self.export_task()
        print ("solution_json", solution_json)
        self.the_app.check_solution(solution_json)

    def export_task(self):
        # export current pieces to json string in Task format
        task_dict = {}
        task_dict['size'] = '5 5'
        task_dict['pieces'] = []

        for p in self.pieces:
            name = self.pieces[p].name
            rot = self.pieces[p].rot
            pos = [self.pieces[p].pos[0], self.pieces[p].pos[1]]

            # print 'pieces:'
            # print  [self.pieces[p].name, self.pieces[p].rot,self.pieces[p].pos[0], self.pieces[p].pos[1] ]

            # pos[0] += -13 * TangramGame.SCALE
            # pos[1] += -20 * TangramGame.SCALE

            pos[0] += -21 * TangramGame.SCALE
            pos[1] += -14 * TangramGame.SCALE

            if 'small triangle' in name:
                pos = [(-0.5 * (pos[1] / TangramGame.SCALE - 1)) - 0.5, (0.5 * (pos[0] / TangramGame.SCALE - 1)) + 0.5]
            elif 'medium triangle' in name:
                if rot == '0':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE - 1) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 2) + 1]
                elif rot == '90':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 1) + 1]
                elif rot == '180':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE - 1) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 2) + 1]
                elif rot == '270':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 1) + 1]
            elif 'large triangle' in name:
                pos = [-0.5 * (pos[1] / TangramGame.SCALE) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 2) + 1]
            elif 'square' in name:
                pos = [-0.5 * (pos[1] / TangramGame.SCALE - 1) - 0.5, 0.5 * (pos[0] / TangramGame.SCALE - 1) + 0.5]
            elif 'parrallelogram' in name:
                if rot == '0':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 1) + 1]
                elif rot == '90':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE - 1) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 2) + 1]
                elif rot == '180':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 1) + 1]
                elif rot == '270':
                    pos = [-0.5 * (pos[1] / TangramGame.SCALE - 1) - 1, 0.5 * (pos[0] / TangramGame.SCALE - 2) + 1]
                    # print 'new pos:'
            # print [name, rot, pos]
            task_dict['pieces'].append((name, rot, str(pos[0]) + ' ' + str(pos[1])))
        json_str = json.dumps(task_dict)
        # print json_str
        return json_str


class Rotate(Button):

    def __init__(self, the_app):
        super(Rotate,self).__init__()
        self.the_app = the_app
        self.background_normal = 'buttons/arrow_rotate.png'
        self.size = (TangramGame.SCALE * 4, TangramGame.SCALE * 4)

    def on_press(self):
        if self.the_app.current is not None:
            self.the_app.current.rot = str(int(self.the_app.current.rot) + 90)
            if self.the_app.current.rot == '360':
                self.the_app.current.rot = '0'
            self.the_app.current.set_shape()
        self.the_app.check_solution()

class GameTaskLayout(Button, TaskLayout):
    # inherits from TaskLayout which is in tangram_game.py

    def __init__(self):
        super(GameTaskLayout, self).__init__()
        print("GameTaskLayout __init__")
        self.size = [300,300]
        self.update_position()
        with self.canvas.before:
            print ("self.canvas.before")
            Color(234/255.0,226/255.0,139/255.0,1)
            self.rect = Rectangle()
            self.rect.pos = self.pos
            self.rect.size = self.size
            print (self.rect.size)

    def update_position(self, *args):
        print('GameTaskLayout update_position')
        self.pos = [Window.width * 0.28, Window.height * 0.23]
        self.size = [Window.width * 0.36, Window.height * 0.28]
        #self.update_selection_task_pos()

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        print('GameTaskLayout self.size ',self.size, 'self.pos ', self.pos)
        self.rect.size = self.size

    def on_press(self, *args):
        super(Button, self).on_press()
        # self.incorrect_pos()
        # self.the_app.selected_task(self.original_task)
        print("Selection Task Layout: on_press" , self.name)

    def update_selection_task_shade(self):
        print ('update_selection_task_shade ')
        print('TangramGame.SCALE ', TangramGame.SCALE)
        print('update_selection_task_pos ', self.pos, self.size)
        for p in self.pieces:
            print("p[pos] ", p['pos'], p['name'])
            print("update_selection_task_shade", self.x,self.y)
            p['pos'][0] += self.x + 3.5 * TangramGame.SCALE
            p['pos'][1] += self.y + 3.5 * TangramGame.SCALE
        self.update_task()


    def get_color(self, index):
        modulo = index % 3
        if (modulo == 0):
            my_color = Color(1,0,0,1)
        elif (modulo == 1):
            my_color = Color(0,1,0,1)
        elif (modulo == 2):
            my_color = Color(0,0,1,1)
        return my_color



class Background(Widget):
    pass

class TreasureBox(Widget):
    def rotate_shape(self, *kwargs):
        print("rotate shape")


class TangramGameWidget(Widget):
    def __init__(self, **kwargs):
        print("TangramGameWidget __init__")
        super(TangramGameWidget, self).__init__(**kwargs)
        self.canvas.clear()
        self.clear_widgets()

    def reset(self):
        self.clear_widgets()

class HourGlassWidget (Widget):
    def __init__(self, **kwargs):
        super(HourGlassWidget, self).__init__(**kwargs)
        self.delta=0
        #self.animate_sand()
        Clock.schedule_interval(self.after_init,0.01)  #only after init is done ids can be accessed

    def after_init(self, *args):
        print ('HourGlassWidget: after init')
        self.hourglass = self.ids['hourglass']
        self.topSand = self.ids['topSand']
        self.middleSand = self.ids['middleSand']
        self.bottomSand = self.ids['bottomSand']
        self.init = False
        self.do_layout()
        # self.start_hourglass(120)
        return False

    def do_layout(self, *args):
        print ("do_layout")
        print (self)
        if (not self.init):
            self.size = Window.width * 0.08, Window.height * 0.2
            self.pos = Window.width * 0.85, Window.height * 0.25
            sandWidth = self.width
            sandHeight = self.height * 0.25
            self.sandHeight = sandHeight
            self.hourglass.size = self.width, self.height
            self.hourglass.pos = self.x, self.y
            self.topSand.size = sandWidth, sandHeight
            self.topSand.pos = self.x, self.y+self.height * 0.5
            self.middleSand.size = sandWidth * 0.05, sandHeight * 2
            self.middleSand.pos = self.x + sandWidth/2.0 - sandWidth*0.02, self.y+0
            self.bottomSand.size = sandWidth, 0
            self.bottomSand.pos = self.x, self.y+0 + self.height * 0.041
            self.init = True

    def start_hourglass(self):
        print('start hourglass')
        pass

    def stop_hourglass(self, *args):
        self.middleSand.height = 0
        print("time is up")

    def update_hourglass (self, percent):
        # Rinat: change to percentage
        current_time = float(percent[0][0])
        total_time = float(percent[0][1])
        current_percent = current_time / total_time
        self.topSand.height =  self.sandHeight * current_percent
        self.bottomSand.height = self.sandHeight* (1 - current_percent)
        if (current_percent < 0.02):
            self.middleSand.height = 0




    # def animate_sand (self,*args):
    #     animTop = Animation(height=0,
    #                      duration=60,
    #                      transition='in_quad')
    #     #animTop.start(self.topSand)
    #     animBottom = Animation(height=100,
    #                      duration=4,
    #                      transition='in_quad')
    #     animBottom.start(self.bottomSand)

# runTouchApp(SolveTangramRoom())


