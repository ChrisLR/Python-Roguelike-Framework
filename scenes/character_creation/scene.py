from bearlibterminal import terminal
from clubsandwich.ui import (
    UIScene,
    SingleLineTextInputView,
    LabelView,
    CyclingButtonView,
    ButtonView,
    LayoutOptions,
    WindowView,
)

from components.needs import Needs
from components.stats import make_character_stats
from data.python_templates.classes import character_class_templates
from data.python_templates.needs import hunger, thirst
from data.python_templates.outfits import starter_warrior, starter_thief, starter_ranger
from data.python_templates.races import race_templates
from scenes.game.scene import GameScene
from ui.controls.validatedintstepperview import ValidatedIntStepperView


class CharacterCreationScene(UIScene):
    ID = "CharacterCreation"
    # TODO Remake this properly using the new style controls interface.
    
    def __init__(self, game_context):
        self.covers_screen = True
        self.game_context = game_context
        self.sorted_classes = sorted(character_class_templates.values(), key=lambda c_class: c_class.name)
        sorted_classes_names = [character_class.name for character_class in self.sorted_classes]
        self.sorted_races = sorted(race_templates.values(), key=lambda race: race.name)
        sorted_races_names = [race.name for race in self.sorted_races]

        views = [
            WindowView(title='Character Creation', subviews=[
                LabelView("Name:", layout_options=LayoutOptions(**get_left_layout(2))),
                SingleLineTextInputView(
                    callback=self.set_name,
                    layout_options=LayoutOptions(**get_right_layout(3, width=0.2, right=0.4))
                ),
                LabelView("Class:", layout_options=LayoutOptions(**get_left_layout(3))),
                CyclingButtonView(
                    options=sorted_classes_names,
                    initial_value=sorted_classes_names[0],
                    callback=self.set_character_class,
                    layout_options=LayoutOptions(**get_right_layout(3))
                ),
                LabelView("Race:", layout_options=LayoutOptions(**get_left_layout(4))),
                CyclingButtonView(
                    options=sorted_races_names,
                    initial_value=sorted_races_names[0],
                    callback=self.set_race,
                    layout_options=LayoutOptions(**get_right_layout(4))
                ),
                LabelView("Strength:", layout_options=LayoutOptions(**get_left_layout(6))),
                ValidatedIntStepperView(
                    validation_callback=self.validate_points,
                    value=8, callback=lambda value: self.set_stat("Strength", value),
                    min_value=8, max_value=15,
                    layout_options=LayoutOptions(**get_right_layout(7, width=5)),
                ),
                LabelView("Dexterity:", layout_options=LayoutOptions(**get_left_layout(7))),
                ValidatedIntStepperView(
                    validation_callback=self.validate_points,
                    value=8, callback=lambda value: self.set_stat("Dexterity", value),
                    min_value=8, max_value=15,
                    layout_options=LayoutOptions(**get_right_layout(8, width=5)),
                ),
                LabelView("Constitution:", layout_options=LayoutOptions(**get_left_layout(8))),
                ValidatedIntStepperView(
                    validation_callback=self.validate_points,
                    value=8, callback=lambda value: self.set_stat("Constitution", value),
                    min_value=8, max_value=15,
                    layout_options=LayoutOptions(**get_right_layout(9, width=5)),
                ),
                LabelView("Intelligence:", layout_options=LayoutOptions(**get_left_layout(9))),
                ValidatedIntStepperView(
                    validation_callback=self.validate_points,
                    value=8, callback=lambda value: self.set_stat("Intelligence", value),
                    min_value=8, max_value=15,
                    layout_options=LayoutOptions(**get_right_layout(10, width=5)),
                ),
                LabelView("Charisma:", layout_options=LayoutOptions(**get_left_layout(10))),
                ValidatedIntStepperView(
                    validation_callback=self.validate_points,
                    value=8, callback=lambda value: self.set_stat("Charisma", value),
                    min_value=8, max_value=15,
                    layout_options=LayoutOptions(**get_right_layout(11, width=5)),
                ),
                LabelView("Wisdom:", layout_options=LayoutOptions(**get_left_layout(11))),
                ValidatedIntStepperView(
                    validation_callback=self.validate_points,
                    value=8, callback=lambda value: self.set_stat("Wisdom", value),
                    min_value=8, max_value=15,
                    layout_options=LayoutOptions(**get_right_layout(12, width=5))
                ),
                ButtonView('Finish', self.finish,
                           layout_options=LayoutOptions(**get_left_layout(13, left=0.45)))
            ])
        ]
        super().__init__(views)
        self.character_factory = self.game_context.character_factory
        self.body_factory = self.game_context.body_factory

        self.name = ""
        self.character_class = self.sorted_classes[0]
        self.race = self.sorted_races[0]
        self.stats = {
            "Strength": 8,
            "Dexterity": 8,
            "Constitution": 8,
            "Intelligence": 8,
            "Charisma": 8,
            "Wisdom": 8
        }
        self.points_left = 27

    def set_name(self, value):
        self.name = value

    def set_character_class(self, value):
        self.character_class = next((character_class for character_class in self.sorted_classes
                                     if character_class.name == value), None)

    def set_race(self, value):
        self.race = next((race for race in self.sorted_races
                          if race.name == value), None)

    def set_stat(self, name, value):
        self.stats[name] = value

    def validate_points(self, old_value, new_value):
        if new_value > old_value:
            point_cost = 1 if old_value < 13 else 2
            if self.points_left >= point_cost:
                self.points_left -= point_cost
                return True
        if new_value < old_value:
            point_cost = 1 if new_value < 13 else 2
            if new_value >= 8:
                self.points_left += point_cost
                return True
        return False

    def finish(self):
        self.game_context.player = self.character_factory.create(
            uid="player",
            name=self.name,
            class_uid=self.character_class.uid,
            race_uid=self.race.uid,
            stats=make_character_stats(
                **{uid.lower(): value for uid, value in self.stats.items()}),
            body_uid=self.race.body_template_uid
        )
        player = self.game_context.player
        player.register_component(Needs.create_standard(1, 100, hunger, thirst))
        # TODO We will need a much better way to assign outfits.
        if self.character_class.uid.lower() == "thief":
            starter_thief.apply(player)
        elif self.character_class.uid.lower() == "warrior":
            starter_warrior.apply(player)
        elif self.character_class.uid.lower() == "ranger":
            starter_ranger.apply(player)
        player.is_player = True
        self.director.replace_scene(GameScene(self.game_context))

    def terminal_read(self, val):
        super().terminal_read(val)
        if val == terminal.TK_UP:
            self.view.find_prev_responder()
        elif val == terminal.TK_DOWN:
            self.view.find_next_responder()


def get_left_layout(top, **kwargs):
    layout_options = dict(width=0.1, left=0.3, top=top, height=0.1, bottom=None, right=None)
    if kwargs:
        layout_options.update(kwargs)

    return layout_options


def get_right_layout(top, **kwargs):
    layout_options = dict(width=0.1, left=None, top=top, height=0.1, bottom=None, right=0.5)
    if kwargs:
        layout_options.update(kwargs)

    return layout_options

