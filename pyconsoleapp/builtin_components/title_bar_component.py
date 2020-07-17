from typing import TYPE_CHECKING

from pyconsoleapp import styles
from pyconsoleapp.components import ConsoleAppComponent

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp


class TitleBarComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self.set_print_function(self.print)

    def print(self):
        output = '{app_name} | {route}\n'.format(
            app_name=styles.weight(self.app.name, 'bright'),
            route=styles.fore(self.app.route.replace('.', '>'), 'blue')
        )
        return output
