import curses
from curses import wrapper
import boto3


class Service(object):
    def __init__(self):
        self.client = boto3.client(self.get_boto_service_name())

    def get_boto_service_name(self):
        return self.__class__.__name__.replace("Service", "").lower()


class LambdaService(Service):
    pass


class Screen(object):
    def __init__(self, scr):
        self.scr = scr
        self.initial_setup()

    def initial_setup(self):
        pass

class HomeScreen(Screen):

    def initial_setup(self):
        self.cursor_position = 0


    def draw(self, input_key):
        service_names = [
            "Lambda",
            "S3",
            "VPC",
            ]

        if input_key == "KEY_UP":
            if self.cursor_position == 0:
                self.cursor_position = len(service_names) - 1
            else:
                self.cursor_position -= 1
        elif input_key == "KEY_DOWN":
            if self.cursor_position == (len(service_names) - 1):
                self.cursor_position = 0
            else:
                self.cursor_position += 1

        for y, service_name in enumerate(service_names):
            if y == self.cursor_position:
                self.scr.addstr(y, 0, service_name, curses.A_REVERSE)
            else:
                self.scr.addstr(y, 0, service_name)

        return self


class FooterScreen(Screen):

    def draw(self, input_key):
        last_y = curses.LINES - 1
        self.scr.addstr(last_y, 0, f"Typed [{input_key or ''}]", curses.A_REVERSE)


def main(stdscr):
    curr_scr = HomeScreen(stdscr)
    footer_scr = FooterScreen(stdscr)
    input_key = None
    while True:
        try:
            # Clear screen
            stdscr.clear()
            curr_scr = curr_scr.draw(input_key)
            footer_scr.draw(input_key)
            input_key = stdscr.getkey()
            
            if input_key == "q":
                break

        except KeyboardInterrupt:
            break


wrapper(main)
