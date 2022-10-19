# -*- coding: utf-8 -*-


from datetime import datetime
from sys import exc_info
from traceback import format_tb
from colorama import init, Fore, Style
init()

class Color:
    red = Fore.RED
    yellow = Fore.YELLOW
    green = Fore.GREEN
    light_blue = Fore.CYAN
    blue = Fore.BLUE
    default = Style.RESET_ALL
    bold = Style.BRIGHT

class Shout:

    def __init__(self) -> None:
        self.muted_func = [
            "VK.getEvent",
            "VK.getBot",
            "VK.__init__"
            "DB.__init__",
            "Install"
        ]
        self.notice = False
    
    def announcement(self, func):

        def middle(*args, **kwargs):

            func_name = str(func.__qualname__)

            try:
                if self.notice and func_name not in self.muted_func and func_name.split(".")[0] not in self.muted_func:
                    start_time = datetime.now()
                    response = func(*args, **kwargs)
                    end_time = datetime.now()

                    string = f"{func_name} {Color.blue}"
                    
                    attributes = args
                    attributes = attributes[1:]
                    for i in attributes:
                        string += f"'{i}', "

                    print(Color.bold + string + Color.default, '{}'.format(end_time - start_time))

                else:
                    response = func(*args, **kwargs)

                return response
            except Exception as e:
                error = exc_info()[2]
                tb = format_tb(error)
                print(f"{Color.red}{func_name}: {Color.default}{e}\n\n{Color.red}", "\n".join(list(tb)), Color.default)
        
        return middle
