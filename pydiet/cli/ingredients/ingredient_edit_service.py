from typing import TYPE_CHECKING, Dict

from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.ingredients.ingredient_service import IngredientService
    from pyconsoleapp import ConsoleApp


class IngredientEditService():
    def __init__(self):
        self._ingredient_service: 'IngredientService' = \
            inject('pydiet.ingredient_service')
        self.__flag_number_name_map:Dict[int, str]
        self.__current_nutrient_number_name_map:Dict[int, str]        
        self.ingredient: 'Ingredient'
        self.app: 'ConsoleApp' = inject('pydiet.app')
        self.temp_cost_mass: float
        self.temp_cost_mass_units: str
        self.current_flag_number:int
        self.cycling_flags:bool
        self.current_nutrient_group:str
        self.current_nutrient_number:int

    @property
    def flag_number_name_map(self)->Dict[int, str]:
        if not self.__flag_number_name_map:
            self.__flag_number_name_map = \
                self._create_number_name_map(self.ingredient.flag_data)
        return self.__flag_number_name_map

    @property
    def current_nutrient_number_name_map(self)->Dict[int, str]:
        # Determine this dynamically because the current nutrient
        # group could change;
        return self._create_number_name_map(self.ingredient.\
            _data[self.current_nutrient_group])

    def _create_number_name_map(self, dict_to_map: Dict) -> Dict[int, str]:
        map: Dict[int, str] = {}
        for i, key in enumerate(dict_to_map.keys(), start=1):
            map[i] = key
        return map

    def flag_name_from_number(self, selection_number:int)->str:
        return self.flag_number_name_map[selection_number]

    def nutrient_name_from_number(self, selection_number: int) -> str:
        return self.current_nutrient_number_name_map[selection_number]

    def show_ingredient_summary(self) -> None:
        self.app.set_window_text(
            self._ingredient_service.summarise_ingredient(self.ingredient)
        )
        self.app.show_text_window()

