from typing import TYPE_CHECKING

from pyconsoleapp.components import ConsoleAppComponent
from pyconsoleapp import configs as cfg

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp

class DoubleHrComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.set_print_function(self.print)

    def print(self):
        output = '='*cfg.terminal_width_chars+'\n'
        return output
