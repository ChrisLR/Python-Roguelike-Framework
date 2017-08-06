import cocos
from cocos.director import director

from components.needs import Needs
from components.stats import StatsEnum
from components.stats import make_character_stats
from data.python_templates.classes import character_class_templates
from data.python_templates.needs import hunger, thirst
from data.python_templates.outfits import starter_thief, starter_warrior
from data.python_templates.races import race_templates
from scenes.game.scene import GameScene
from ui.controls.pointdistributioncontrol import PointDistributionMenuItem
from util.pointdistribution import PointDistribution


class CharacterCreationMenu(cocos.menu.Menu):
    def __init__(self, title, game_context):
        super().__init__(title)
        self.game_context = game_context
        self.character_factory = game_context.character_factory
        self.body_factory = game_context.body_factory
        sorted_class_templates = sorted(character_class_templates.values(), key=lambda c_class: c_class.name)
        sorted_race_templates = sorted(race_templates.values(), key=lambda race: race.name)

        width, height = director.get_window_size()
        self.font_title['font_size'] = 10
        self.font_title['width'] = width
        self.font_title['multiline'] = True
        self.font_title['align'] = 'center'
        self.font_item['font_size'] = 10
        self.font_item_selected['font_size'] = 10
        stats = [
            StatsEnum.Strength,
            StatsEnum.Dexterity,
            StatsEnum.Constitution,
            StatsEnum.Intelligence,
            StatsEnum.Wisdom,
            StatsEnum.Charisma
        ]
        point_distribution = PointDistribution(stats, 27, 8, 15, lambda current: 1 if current < 13 else 2)
        self.create_menu([
            cocos.menu.EntryMenuItem(
                'Name:', callback_func=self.set_name, value='', max_length=20),
            cocos.menu.MultipleMenuItem(
                'Race:', callback_func=self.set_race,
                items=[str(race) for race in sorted_race_templates]),
            cocos.menu.MultipleMenuItem(
                'Class:', callback_func=self.set_class_template,
                items=[str(class_template) for class_template in sorted_class_templates]),
            PointDistributionMenuItem(StatsEnum.Strength, self.set_stat, point_distribution),
            PointDistributionMenuItem(StatsEnum.Dexterity, self.set_stat, point_distribution),
            PointDistributionMenuItem(StatsEnum.Constitution, self.set_stat, point_distribution),
            PointDistributionMenuItem(StatsEnum.Intelligence, self.set_stat, point_distribution),
            PointDistributionMenuItem(StatsEnum.Wisdom, self.set_stat, point_distribution),
            PointDistributionMenuItem(StatsEnum.Charisma, self.set_stat, point_distribution),
            cocos.menu.MenuItem('Start', callback_func=self.finalize_character_and_start_game),
            cocos.menu.MenuItem('Back', callback_func=lambda: director.pop())
        ])
        self.name = None
        self.race = None
        self.class_template = None
        self.stats = {}

    def set_name(self, value):
        self.name = value

    def set_race(self, value):
        self.race = next([race_template for race_template
                          in race_templates.itervalues()
                          if race_templates.name == value])

    def set_class_template(self, value):
        self.class_template = next([class_template for class_template
                                    in character_class_templates.itervalues()
                                    if class_template.name == value])

    def set_stat(self, attribute, value):
        self.stats[attribute] = value

    def finalize_character_and_start_game(self):
        self.game_context.player = self.character_factory.create(
            uid="player",
            name=self.name,
            class_uid=self.class_template.uid,
            race_uid=self.race.uid,
            stats=make_character_stats(
                **{uid.lower(): value for uid, value in self.stats.items()}),
            body_uid="humanoid"
        )
        player = self.game_context.player
        player.register_component(Needs.create_standard(1, 100, hunger, thirst))
        # TODO We will need a much better way to assign outfits.
        if self.class_template.uid.lower() == "thief":
            starter_thief.apply(player)
        else:
            starter_warrior.apply(player)
        director.push(GameScene())
