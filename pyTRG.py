"""
TGR 3.0.0
Author : Merwin
A module for doing minimal graphic rendering in the terminal.
"""

import os
import cv2
import sys
import re
import time
from pynput import keyboard
from subprocess import call
import threading
from sty import fg, bg

if (sys.platform == "win32"):
    import ctypes
    from ctypes import wintypes
else:
    import termios


class pyTGR:
    def __init__(self):
        self.Key = keyboard.Key
        self.fixed = []
        self.fixed_x = []
        self.fixed_y = []
        self.bg = [0, 0, 0]
        self.term_history = ""

    def set_bg(self, bg):
        """
        For setting the bg color.
        :param bg: rgb color code
        :return: None
        """
        self.bg = bg
        self.update_from_history()

    def get_terminal_size(self):
        """
        Returns the terminal size ,[cols , lines]
        :return: Size [ cols , lines ]
        """
        return [os.get_terminal_size().columns, os.get_terminal_size().lines]

    def clear_history(self):
        """
        Clears the History of Terminal.
        :return: None
        """
        self.term_history = ""

    def update_from_history(self):
        """
        Refresh the terminal's bg. Uses the data stored in Terminal History.
        :return: None
        """
        current = self.term_history.replace("___+terminal_bg+___", bg(self.bg[0], self.bg[1], self.bg[2]))
        current_2 = current.split("\n")
        self.clear_terminal()
        for e in current_2:
            self.print(e, end="\n")

    def print(self, data, end="\n"):
        """
        Prints str
        :param data: str , the str to be printed.
        :param end: The end param for printing. By default '\n'
        :return: None
        """
        data = str(data)
        v = self.get_terminal_size()[0] - len(data)
        if v > 0:
            data += " " * v
        c = f"{bg(self.bg[0], self.bg[1], self.bg[2])}{data}{bg.rs}{end}"
        self.term_history += f"___+terminal_bg+___{data}{bg.rs}{end}"
        print(c, end="")

    def draw_vertical_pixel(self, color):
        """
        Print a pixel , vertically.
        :param color: Color of the pixel , rgb .
        :return: None
        """
        print(f"{fg(color[0], color[1], color[2])} {fg.rs}")

    def draw_horizontal_pixel(self, color):
        """
        Print a pixel , horizontally.
        :param color: Color: Color of the pixel , rgb .
        :return: None
        """
        print(f"{fg(color[0], color[1], color[2])} {fg.rs}", end="")

    def draw_pixel(self, x, y, color):
        """
        Print a pixel , at a given position.
        :param x: x - position.
        :param y: y - position.
        :param color: Color of the pixel.
        :return: None
        """
        pos = "\033[%d;%dH" % (y, x)
        print(pos, end="")
        print(f"{bg(color[0], color[1], color[2])} {bg.rs}", end="")

    def set_cursor(self, x, y):
        """
        Move the terminal cursor to a given position.
        :param x: x - position.
        :param y: y - position.
        :return: None
        """
        pos = "\033[%d;%dH" % (y, x)
        print(f"{pos}", end="")

    def spinning_animation_bars(self, revolutions, delay, side_text=" Loading...", color=[255, 255, 255]):
        """
        Animation : spinning - 1.
        :param revolutions: Times.
        :param delay: The delay between the change of each symbol.
        :param side_text: The text about the animation.
        :param color: The color of the bars in rgb.
        :return: None
        """
        rev = 0
        while rev != revolutions:
            print(f'\r{fg(color[0], color[1], color[2])}\\ {side_text}{fg.rs}', end="")
            time.sleep(delay)
            print(f'\r{fg(color[0], color[1], color[2])}| {side_text}{fg.rs}', end="")
            time.sleep(delay)
            print(f'\r{fg(color[0], color[1], color[2])}/ {side_text}{fg.rs}', end="")
            time.sleep(delay)
            print(f'\r{fg(color[0], color[1], color[2])}| {side_text}{fg.rs}', end="")
            time.sleep(delay)
            rev += 1

    def spinning_animation(self, delay, revolutions, side_text=" Loading...", color=[255, 255, 255]):
        """
        Animation : spinning - 2.
        :param delay: The delay between the change of each symbol.
        :param revolutions: Times.
        :param side_text: The text about the animation.
        :param color: The color of the symbols in rgb.
        :return: None
        """
        rev = 0
        while rev != revolutions:
            print(f'\r{fg(color[0], color[1], color[2])}^ {side_text}{fg.rs}', end="")
            time.sleep(delay)
            print(f'\r{fg(color[0], color[1], color[2])}< {side_text}{fg.rs}', end="")
            time.sleep(delay)
            print(f'\r{fg(color[0], color[1], color[2])}> {side_text}{fg.rs}', end="")
            time.sleep(delay)
            print(f'\r{fg(color[0], color[1], color[2])}_ {side_text}{fg.rs}', end="")
            time.sleep(delay)
            rev += 1

    def bar_animation(self, delay, len_, color_1=[47, 152, 237], color_2=[96, 96, 97],
                      finished_text="Finished Loading..."):
        """
        Animation : Bar
        :param delay: Delay between each bar.
        :param len_: Number of bars.
        :param color_1: Color in rgb.
        :param color_2: color in rgb.
        :param finished_text: The text on finishing.
        :return: None
        """
        c = 0
        print(f"{bg(color_2[0], color_2[1], color_2[2])} {bg.rs}", end="")
        while c != len_:
            if c % 2 == 0:
                print(f"{bg(color_1[0], color_1[1], color_1[2])}  {bg.rs}", end="")
            else:
                print(f"{bg(color_2[0], color_2[1], color_2[2])} {bg.rs}", end="")
            c += 1
            time.sleep(delay)
        if len_ % 2 != 0:
            print(f"{color_2} ", end="")
        print(f" {finished_text}", end="")

    def strip_animation(self, duration, strips, finished_text="Loaded...", color=[255, 255, 255]):
        """
        Animation - Strip.
        :param duration: delay between each strip.
        :param strips: number of strips.
        :param finished_text: The text on finishing.
        :param color: color of the strips.
        :return: None
        """
        c = 0
        while strips != c:
            print(f"{fg(color[0], color[1], color[2])}|{fg.rs}", end="")
            time.sleep(duration)
            c += 1
        print(f" {finished_text}", end="")

    def fixed_text(self, txt, bg_, fg_, x, y):
        """
        Text which can be fixed a position , and doesn't get removed by the clear func.
        :param txt: Test to be saved.
        :param bg_: background color rgb.
        :param fg_: foreground color rgb.
        :param x: x - position.
        :param y: y - position.
        :return: None
        """
        self.fixed.append(f'{bg(bg_[0], bg_[1], bg_[2])}{fg(fg_[0], fg_[1], fg_[2])}{txt}{fg.rs}{bg.rs}')
        self.fixed_x.append(x)
        self.fixed_y.append(y)
        self.set_cursor(x, y)
        print(f'{bg(bg_[0], bg_[1], bg_[2])}{fg(fg_[0], fg_[1], fg_[2])}{txt}{fg.rs}{bg.rs}', end="")

    def remove_fixed_text(self, txt):
        """
        To remove a text from fixed texts.
        :param txt: The text which is to be removed.
        :return: None
        """
        ind = self.fixed.index(txt)
        self.fixed.remove(txt)
        del self.fixed_y[ind]
        del self.fixed_x[ind]

    def new_row(self):
        """
        Move to a new row.
        :return: None
        """
        print("\n")
        self.term_history += "\n"

    def text(self, text, fg_, bg_):
        """
        Print Text , with fg and bg color.
        :param text:Text to be printed.
        :param fg_: Foreground color rgb.
        :param bg_: Background color rgb.
        :return: None
        """
        print(f"{bg(bg_[0], bg_[1], bg_[2])}{fg(fg_[0], fg_[1], fg_[2])}{text}{fg.rs}{bg.rs}")
        self.term_history += f"{bg(bg_[0], bg_[1], bg_[2])}{fg(fg_[0], fg_[1], fg_[2])}{text}{fg.rs}{bg.rs}\n"

    def updating_text(self, txt, color=[255, 255, 255], bg_=[0, 0, 0]):
        """
        A text which can be changed.
        :param txt: Primary text.
        :param color: Foreground color rgb.
        :param bg_: Background color rgb.
        :return: None
        """
        print(f"\r{bg(bg_[0], bg_[1], bg_[2])}{fg(color[0], color[1], color[2])} {txt}{fg.rs}{bg.rs}", end="")

    def print_image_ascii(self, path, size=None, print_=True):
        """
        Print an image as ascii.
        :param path: The path of the image.
        :param size: The size of the image to be printed in.(optional)
        :param print_: The printing of image , bool.(optional)
        :return: The ascii image.
        """
        value_dict = {8: '@', 7: '#', 6: 'B', 5: '%', 4: '/', 3: 'a', 2: '-', 1: '.'}
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Making it greyscale
        if size != None:
            img = cv2.resize(img, size)  # Resizing it
        s = ''
        for row in img:
            for p in row:
                n = 0
                if p < 30:
                    n = 1
                elif p < 50:
                    n = 2
                elif p < 90:
                    n = 3
                elif p < 110:
                    n = 4
                elif p < 150:
                    n = 5
                elif p < 180:
                    n = 6
                elif p < 220:
                    n = 7
                else:
                    n = 8
                s += value_dict[n]
            s += ' \n'
        if print_:
            print(s)
        self.term_history += s
        return s

    def play_video_ascii(self, path, frame_delay=0.09, size=None):
        """
        To play a video in ascii form.
        :param path: The path of the video.
        :param frame_delay: The delay between each frame, int. (optional)
        :param size: The size of the video played. (optional)
        :return: None
        """
        cam = cv2.VideoCapture(path)
        value_dict = {8: '@', 7: '#', 6: 'B', 5: '%', 4: '/', 3: 'a', 2: '-', 1: '.'}
        frame_list = []
        while True:
            res, img = cam.read()
            if res != True:
                break
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Making it greyscale
            if size != None:
                img = cv2.resize(img, size)  # Resizing it
            s = ''
            for row in img:
                for p in row:
                    if p < 30:
                        n = 1
                    elif p < 50:
                        n = 2
                    elif p < 90:
                        n = 3
                    elif p < 110:
                        n = 4
                    elif p < 150:
                        n = 5
                    elif p < 180:
                        n = 6
                    elif p < 220:
                        n = 7
                    else:
                        n = 8
                    s += value_dict[n]
                s += ' \n'
            frame_list.append(s)
        cam.release()

        for e in frame_list:
            print(e)
            time.sleep(frame_delay)
            self.clear_terminal()

    def play_video_color(self, path, frame_delay=0.09, size=None, reduce_by=None):
        """
        Play video.
        :param path: The path of the video.
        :param frame_delay: The delay between each frame, int. (optional)
        :param size: The of the video played. (optional)
        :param reduce_by: The ratio by which the video size should be reduced. (optional)
        :return: None
        """
        frames = self.load_video(path, size, reduce_by)
        for e in frames:
            print(e)
            time.sleep(frame_delay)
            self.clear_terminal()

    def load_video(self, file, size, reduce_by=None):
        """
        Func used in the module.
        """
        frames = []
        cam = cv2.VideoCapture(file)
        while True:
            res, frame = cam.read()
            if res != True:
                break
            if reduce_by != None:
                frame = cv2.resize(frame, (int(frame.shape[0] * reduce_by), int(frame.shape[1] * reduce_by)))
            frames.append(self.print_frame_color(frame, 1, resize_img=size, print_img=False))
        return frames

    def print_frame_color(self, img, print_size=2, resize_img=None, print_img=True):
        """
        Func used in the module.
        """
        txt = " " * print_size
        file = img
        if resize_img != None:
            file = cv2.resize(file, resize_img)
        final_text = ""
        for y in file:
            for x in y:
                if list(x) != [0, 0, 0]:
                    final_text += f"{bg(x[2], x[1], x[0])}{txt}{bg.rs}"
                else:
                    final_text += txt
            final_text += "\n"
        if print_img:
            print(final_text)
        return final_text

    def loading_percentage(self, delay, max_percent=100, color=[255, 255, 255]):
        """
        Animation - progressive.
        :param delay: The delay between each progress.
        :param max_percent: The max. (optional)
        :param color: The color of the loader. (optional)
        :return: None
        """
        c = 0
        while c != max_percent + 1:
            print(
                f"\r{fg(color[0], color[1], color[2])}[{c}]{self.find_number_of_repetition('0', str(max_percent)) * ' '}{fg.rs}",
                end="")
            time.sleep(delay)
            c += 1

    def find_number_of_repetition(self, chr, string):
        """
        Func used in the module.
        """
        c = 0
        for each in string:
            if each == chr:
                c += 1
        return c

    def draw_line(self, x, y, width, color):
        """
        To draw a line.
        :param x: x  - position
        :param y: y - position
        :param width: width of the line.
        :param color: Color of the line , rgb.
        :return: None
        """
        t = 0
        while t != width:
            self.draw_pixel(x, y, color)
            t += 1
            x += 1

    def draw_circle(self, diameter, color):
        """
        To draw a circle.
        :param diameter: The diameter of the circle.
        :param color: color of the circle , rgb.
        :return: None
        """
        radius = diameter / 2 - .5
        r = (radius + .25) ** 2 + 1

        result = ''

        for i in range(diameter):
            y = (i - radius) ** 2
            for j in range(diameter):
                x = (j - radius) ** 2
                if x + y <= r:
                    result = result + f'{bg(color[0], color[1], color[2])}   {bg.rs}'
                else:
                    result = result + '   '
            result = result + '\n'
        self.term_history += result
        print(result)

    def draw_rect(self, x, y, width, height, color, filled=True):
        """
        To draw rectangle.
        :param x: x - position.
        :param y: y - position.
        :param width: width of the rectangle.
        :param height: height of the rectangle.
        :param color: color of the rectangle , rgb.
        :param filled: If the rectangle should be filled. (optional)
        :return: None
        """
        if filled:
            t = 0
            while height != t:
                self.draw_line(x, y, width, color)
                y += 1
                t += 1
        else:
            t = 0
            while t != height:
                if t == 0:
                    self.draw_line(x, y, width, color)
                elif t == height - 1:
                    self.draw_line(x, y, width, color)
                else:
                    self.draw_pixel(x, y, color)
                    self.draw_pixel(x + width - 1, y, color)
                y += 1
                t += 1
        self.print("")

    def print_img_color(self, file, print_size=2, resize_img=None, print_img=True):
        """
        For printing a img.
        :param file: File name.
        :param print_size: The size of the print. (optional)
        :param resize_img: The size to which the image have to be resized. (optional)
        :param print_img: If you want to print the image. (optional)
        :return: Image_string
        """
        txt = " " * print_size
        file = cv2.imread(file)
        if resize_img != None:
            file = cv2.resize(file, resize_img)
        final_text = ""
        for y in file:
            for x in y:
                if list(x) != [0, 0, 0]:
                    final_text += f"{bg(x[2], x[1], x[0])}{txt}{bg.rs}"
                else:
                    final_text += txt
            final_text += "\n"
        if print_img:
            self.term_history += final_text
            print(final_text)
        return final_text

    def get_cursor_pos(self):
        """
        Returns the position of the cursor.
        :return: Position
        """
        if (sys.platform == "win32"):
            OldStdinMode = ctypes.wintypes.DWORD()
            OldStdoutMode = ctypes.wintypes.DWORD()
            kernel32 = ctypes.windll.kernel32
            kernel32.GetConsoleMode(kernel32.GetStdHandle(-10), ctypes.byref(OldStdinMode))
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
            kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), ctypes.byref(OldStdoutMode))
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        else:
            OldStdinMode = termios.tcgetattr(sys.stdin)
            _ = termios.tcgetattr(sys.stdin)
            _[3] = _[3] & ~(termios.ECHO | termios.ICANON)
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, _)
        try:
            _ = ""
            sys.stdout.write("\x1b[6n")
            sys.stdout.flush()
            while not (_ := _ + sys.stdin.read(1)).endswith('R'):
                True
            res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)
        finally:
            if (sys.platform == "win32"):
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), OldStdinMode)
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), OldStdoutMode)
            else:
                termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, OldStdinMode)
        if (res):
            return (res.group("x"), res.group("y"))
        return (-1, -1)

    def _terminal_event_scan(self, _, fun):
        """
        Func used by the module.
        """
        pre_1 = self.get_terminal_size()
        pre_2 = self.get_cursor_pos()
        while True:
            cur_1 = self.get_terminal_size()
            cur_2 = self.get_cursor_pos()
            if pre_1 != cur_1:
                pre_1 = cur_1
                fun("size")
            if pre_2 != cur_2:
                pre_2 = cur_2
                fun("cursor")

    def init_terminal_events(self, function):
        """
        To monitor Terminal events.
        Types of events:
            change in size: size
            change in cursor position : cursor
        :param function: A function which will be called on events ,event will be passed as an argument.
        :return: None
        """
        thr = threading.Thread(target=self._terminal_event_scan, args=("", function))
        thr.start()

    def init_keyboard(self, on_press):
        """
        To monitor Keyboard events.
        :param on_press: The function to be called if a key is pressed ,key will be passed as an argument.
        :return: None
        """
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

    def clear_terminal(self):
        """
        Used for clearing the terminal.
        :return: None
        """
        _ = call('clear' if os.name == 'posix' else 'cls')
        if len(self.fixed) != 0:
            for e in range(0, len(self.fixed)):
                self.set_cursor(self.fixed_x[e], self.fixed_y[e])
                self.print(self.fixed[e], end="")

    def close_terminal(self):
        """
        Used to close the terminal.
        :return: None
        """
        _ = call('exit')



class Examples:
    def __init__(self):
        pass
    def Video_Image(self):
        """
        A video and Image viewer made in pyTGR3.
        :return: None
        """
        term = pyTGR()
        term.print("Photo and Video on Terminal...")
        term.print("Stop to end the program...")
        cmd = ""
        while True:
            cmd = input("Command (stop,image,video) > ").lower()
            if cmd == "stop":
                break
            try:
                if cmd == "image":
                    f = input("File name : ")
                    t = input("color or ascii : ").lower()
                    if t == "color":
                        term.print_img_color(f, resize_img=(100, 100))
                    else:
                        term.print_image_ascii(f, size=(100, 100))
                else:
                    f = input("File name : ")
                    t = input("color or ascii : ").lower()
                    if t == "color":
                        term.play_video_color(f, size=(100, 100))
                    else:
                        term.play_video_ascii(f, size=(100, 100))
            except:
                term.print("Some Error Occurred..")
    def Square_movement(self):
        """
        Moving a square on terminal using keys...
        :return: None
        """
        self.term = pyTGR()

        self.x = 0
        self.y = 0


        self.term.clear_terminal()
        self.term.init_keyboard(on_press=self.on_event)
        self.term.draw_rect(x, y, 10, 5, [250, 250, 60])

        while True:
            pass

    def on_event(self,key):
        """
        Used as a part of Square movement example.
        :return: None
        """
        if key == self.term.Key.up:
            self.y -= 1
            self.term.clear_terminal()
            self.term.draw_rect(self.x, self.y, 10, 5, [250, 250, 60])
        elif key == self.term.Key.down:
            self.y += 1
            self.term.clear_terminal()
            self.term.draw_rect(self.x, self.y, 10, 5, [250, 250, 60])
        elif key == self.term.Key.right:
            self.x += 2
            self.term.clear_terminal()
            self.term.draw_rect(self.x, self.y, 10, 5, [250, 250, 60])
        elif key == self.term.Key.left:
            self.x -= 2
            self.term.clear_terminal()
            self.term.draw_rect(self.x, self.y, 10, 5, [250, 250, 60])

x = 2
y = 2

def pressed_2(key):
    global x, y
    if key == key.up:
        y -= 1
    elif key == key.down:
        y += 1
    elif key == key.right:
        x += 1
    elif key == key.left:
        x -= 1


def terminal_changes(event):
    print(event)


if __name__ == '__main__':
    renderer = pyTGR()
    # renderer.loading_animation(0.05,20)
    # renderer.spinning_animation_bars(10,0.09,"  Loading...")
    # renderer.spinning_animation(0.1,10)
    # renderer.strip_animation(0.01,100)
    # renderer.loading_percentage(0.1,max_percent=50)
    # renderer.clear_terminal()
    # renderer.set_cursor(50,5)
    # renderer.draw_pixel(10,10,color=[255,0,0])
    # renderer.draw_line(10,10,60,color=[0,244,11])
    # renderer.draw_rect(10,10,20,20,color=[0,244,11])

    # drawing a pattern
    # renderer.draw_rect(10,10,10,10,color=[0,244,11],filled=False)
    # time.sleep(3)
    # renderer.clear_terminal()
    # renderer.draw_rect(1,1,10,10,color=[0,244,11])
    # time.sleep(3)
    # renderer.set_cursor(30,30)
    # renderer.new_row()
    # renderer.loading_animation(0.05,20,)
    # renderer.clear_terminal()
    # renderer.draw_circle(10,[100,100,100])
    # time.sleep(5)
    # renderer.clear_terminal()

    # keyboard events
    # def on_event(key):
    # print(key)
    # renderer.init_keyboard(on_press=on_event)
    # renderer.loading_percentage(0.5)

    # print image ascii
    # renderer.print_image_ascii("python3.jpg")
    # time.sleep(5)
    # renderer.clear_terminal()

    # print image color
    # renderer.print_img_color("python3.jpg",print_size=1,resize_img=(100,100))
    # time.sleep(5)
    # renderer.clear_terminal()

    # play video ascii
    # renderer.play_video_ascii("test_video.mp4",size=(100,100))

    # play video color
    # renderer.play_video_color("test_video.mp4",frame_delay=0.09 ,size=(50,50), reduce_by=1/2)

    # terminal mem
    # renderer.print("Hello")
    # renderer.print("Hello")
    # renderer.set_bg([200,20,30])

    # Terminal events : terminal size change , terminal cursor position
    # renderer.init_terminal_events(terminal_changes)

    # close the terminal
    # renderer.close_terminal()

