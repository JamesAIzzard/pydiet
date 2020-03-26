from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

from pydiet.cli.ingredients import ingredient_edit_scope as ingredient_scope

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService
    from pydiet.cli.ingredients import ingredient_edit_scope

_MENU_TEMPLATE = '''Choose an option:
(1) - Manage ingredients.
(2) - Manage recipes.
(3) - Manage user goals.
(4) - Run optimiser.
'''


class MainMenu(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ingredient_service:'IngredientService' = inject('pydiet.ingredient_service')
        self._ingredient_edit_scope:'ingredient_edit_scope' = inject('pydiet.ingredient_edit_scope')
        self.set_option_response('1', self.on_manage_ingredients)
        self.set_option_response('2', self.on_manage_recipes)
        self.set_option_response('3', self.on_manage_goals)
        self.set_option_response('4', self.on_run_optimiser)

    def print(self):
        output = _MENU_TEMPLATE
        output = self.get_component('StandardPageComponent').print(output)
        return output

    def on_manage_ingredients(self):
        # Put a fresh ingredient on the scope;
        self._ingredient_edit_scope.ingredient = self._ingredient_service.get_new_ingredient()
        # Go!
        self.goto('.ingredients')

    def on_manage_recipes(self):
        raise NotImplementedError

    def on_manage_goals(self):
        raise NotImplementedError

    def on_run_optimiser(self):
        raise NotImplementedError
