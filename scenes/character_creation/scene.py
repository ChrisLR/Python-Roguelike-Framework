import tdl
from base.scene import BaseScene
from components.stats import make_character_stats
from components.needs import Needs
from data.python_templates.classes import character_class_templates
from data.python_templates.outfits import starter_warrior, starter_thief
from data.python_templates.races import race_templates
from data.python_templates.needs import hunger, thirst
from scenes.game.scene import GameScene
from ui import controls
from ui.controls.interface import ControlsInterface
from clubsandwich.ui import (
    UIScene,
    SingleLineTextInputView,
    LabelView,
    CyclingButtonView,
    IntStepperView,
    ButtonView,
    LayoutOptions,
    WindowView
)


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
                LabelView("Name:", layout_options=LayoutOptions(width=0.1, left=0.3, top=0.1, height=0.1, bottom=None, right=None)),
                SingleLineTextInputView(callback=self.set_name, layout_options=LayoutOptions(width=0.2, left=None, top=0.1, height=0.1, bottom=None, right=0.4)),

            ])
            # LabelView("Class:", layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=2, left=None, width=0.2, right=40)),
            # CyclingButtonView(
            #     options=sorted_classes_names,
            #     initial_value=sorted_classes_names[0],
            #     callback=self.set_character_class,
            #     layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=2),
            # ),
            # LabelView("Race:", layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=5),),
            # CyclingButtonView(
            #     options=sorted_races_names,
            #     initial_value=sorted_races_names[0],
            #     callback=self.set_race,
            #     layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=6),
            # ),
            # LabelView("Strength:", layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=7),),
            # IntStepperView(
            #     value=8, callback=lambda value: self.set_stat("Strength", value),
            #     min_value=8, max_value=15,
            #     layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=8),
            # ),
            # LabelView("Dexterity:", layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=9)),
            # IntStepperView(
            #     value=8, callback=lambda value: self.set_stat("Dexterity", value),
            #     min_value=8, max_value=15,
            #     layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=10),
            # ),
            # LabelView("Constitution:", layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=11)),
            # IntStepperView(
            #     value=8, callback=lambda value: self.set_stat("Constitution", value),
            #     min_value=8, max_value=15,
            #     layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=12),
            # ),
            # LabelView("Intelligence:", layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=13)),
            # IntStepperView(
            #     value=8, callback=lambda value: self.set_stat("Intelligence", value),
            #     min_value=8, max_value=15,
            #     layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=14),
            # ),
            # LabelView("Charisma:", layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=15)),
            # IntStepperView(
            #     value=8, callback=lambda value: self.set_stat("Charisma", value),
            #     min_value=8, max_value=15,
            #     layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=16),
            # ),
            # LabelView("Wisdom:", layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=17)),
            # IntStepperView(
            #     value=8, callback=lambda value: self.set_stat("Wisdom", value),
            #     min_value=8, max_value=15,
            #     layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=18),
            # ),
            # ButtonView('Finish', lambda: print("Yay"),
            #            layout_options=LayoutOptions.centered('intrinsic', 'intrinsic').with_updates(top=19))
            # ])
        ]
        super().__init__(views)
        self.character_factory = self.game_context.character_factory
        self.body_factory = self.game_context.body_factory
        self.options = ["Finish"]

        self.name = None
        self.character_class = None
        self.race = None
        self.stats = {}

        #cost_calculator=lambda current: 1 if current < 13 else 2

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

    def finish(self):
        self.game_context.player = self.character_factory.create(
            uid="player",
            name=self.name,
            class_uid=self.character_class.uid,
            race_uid=self.race.uid,
            stats=make_character_stats(
                **{uid.lower(): value for uid, value in self.stats.items()}),
            body_uid="humanoid"
        )
        player = self.game_context.player
        player.register_component(Needs.create_standard(1, 100, hunger, thirst))
        # TODO We will need a much better way to assign outfits.
        if self.character_class.uid.lower() == "thief":
            starter_thief.apply(player)
        else:
            starter_warrior.apply(player)
        self.director.transition_to(GameScene(self.game_context))
