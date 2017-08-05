import cocos

from scenes.character_creation.layer import CharacterCreationUILayer
from base.scene import BaseScene
from components.stats import make_character_stats
from components.needs import Needs
from data.python_templates.classes import character_class_templates
from data.python_templates.outfits import starter_warrior, starter_thief
from data.python_templates.races import race_templates
from data.python_templates.needs import hunger, thirst
from managers.console_manager import Menu
from ui import controls
from ui.controls.interface import ControlsInterface


class CharacterCreationScene(cocos.scene.Scene):
    ID = "CharacterCreation"
    # TODO Remake this properly using the new style controls interface.
    
    def __init__(self, game_context):
        self.character_factory = game_context.character_factory
        self.body_factory = game_context.body_factory
        sorted_class_templates = sorted(character_class_templates.values(), key=lambda c_class: c_class.name)
        sorted_race_templates = sorted(race_templates.values(), key=lambda race: race.name)
        self.layer = CharacterCreationUILayer(sorted_class_templates, sorted_race_templates)
        super().__init__(self.layer)
    #
    #     self.options = ["Finish"]
    #
    #     self.control_name = controls.InputControl("Name:")
    #     self.control_class = controls.ListChoiceControl(
    #         "Class:", root_console=self.main_console,
    #         options=
    #     )
    #     self.control_race = controls.ListChoiceControl(
    #         question="Race:", root_console=self.main_console,
    #         options=
    #     )
    #     self.control_stats = controls.PointDistributionControl(
    #         question="Stats:",
    #         options=["Strength", "Dexterity", "Constitution", "Intelligence", "Charisma", "Wisdom"],
    #         root_console=self.main_console,
    #         total_points=27,
    #         initial_value=8,
    #         max_value=15,
    #         cost_calculator=lambda current: 1 if current < 13 else 2
    #     )
    #     self.menu = Menu('Character Creation',
    #                      """
    #                      Create your adventure!
    #                      """,
    #                      self.options,
    #                      self.main_console.width,
    #                      self.main_console.height)
    #     self.controls = ControlsInterface(self.menu)
    #     self.menu.position = (0, 0)
    #     self.controls.add_control(self.control_name, 0, 0)
    #     self.controls.add_control(self.control_class, 0, 1)
    #     self.controls.add_control(self.control_race, 0, 4)
    #     self.controls.add_control(self.control_stats, 0, 8)
    #
    #     self.active_control = self.control_name
    #
    #     # TODO THIS should be in the menu itself.
    #     self.menu_draws = []
    #     self.create_menu()
    #
    # def create_menu(self):
    #     for option_text in self.options:
    #         text = '(' + chr(self.menu.letter_index) + ') ' + option_text + '   '
    #         self.menu.letter_index += 1
    #         self.menu_draws.append(text)
    #
    # def render_menu(self):
    #     for text in self.menu_draws:
    #         self.menu.printStr(text)
    #
    # def render(self):
    #     self.menu.clear()
    #     self.menu.move(0, 0)
    #     for control in self.controls.controls:
    #         if self.active_control is None \
    #                 or self.controls.controls.index(self.active_control) >= self.controls.controls.index(control):
    #             if control == self.active_control:
    #                 control.render(self.menu, True)
    #             else:
    #                 control.render(self.menu, False)
    #         self.menu.printStr("\n")
    #
    #     if not self.active_control:
    #         self.render_menu()
    #     self.main_console.blit(self.menu, 0, 0)
    #     tdl.flush()
    #
    # def handle_input(self, key_events, mouse_events):
    #     if self.active_control:
    #         self.active_control.handle_input(key_events, mouse_events)
    #         if self.active_control.finished:
    #             new_index = self.controls.controls.index(self.active_control) + 1
    #             if new_index < len(self.controls.controls):
    #                 self.active_control = self.controls.controls[new_index]
    #             else:
    #                 self.active_control = None
    #     else:
    #         for key_event in key_events:
    #             if key_event.keychar.upper() == 'A':
    #                 self.game_context.player = self.character_factory.create(
    #                     uid="player",
    #                     name=self.control_name.answer,
    #                     class_uid=self.control_class.answer.uid,
    #                     race_uid=self.control_race.answer.uid,
    #                     stats=make_character_stats(
    #                         **{uid.lower(): value for uid, value in self.control_stats.answer.items()}),
    #                     body_uid="humanoid"
    #                 )
    #                 player = self.game_context.player
    #                 player.register_component(Needs.create_standard(1, 100, hunger, thirst))
    #                 # TODO We will need a much better way to assign outfits.
    #                 if self.control_class.answer.uid.lower() == "thief":
    #                     starter_thief.apply(player)
    #                 else:
    #                     starter_warrior.apply(player)
    #                 self.transition_to("GameScene")
