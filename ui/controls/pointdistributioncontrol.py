from settings import ControlColors
from ui.controls.base import BaseControl


class PointDistributionControl(BaseControl):
    # TODO This works well for a point system, but modifiers aren't shown
    def __init__(self, question, options, root_console, initial_value, max_value, total_points, cost_calculator):
        self.question = question
        self.options = options
        self.initial_value = initial_value
        self.max_value = max_value
        self.total_points = total_points
        self.used_points = 0
        self.assigned_points = {option: initial_value for option in self.options}
        self.active_option = options[0]
        self.root_console = root_console
        self.finished = False
        self._formatted_options = ""
        self.list_formatted_options = []
        self.cost_calculator = cost_calculator

    @property
    def text(self):
        return self.question + "\n" + self._get_formatted_options()

    @property
    def answer(self):
        return self.assigned_points

    def _get_formatted_options(self):
        text = ""
        self.list_formatted_options.clear()
        for option in self.options:
            new_text = "    {}: {} \n".format(option, self.assigned_points[option])
            self.list_formatted_options.append((option, new_text))
            text += new_text
        self._formatted_options = text

        return self._formatted_options

    def handle_input(self, key_events):
        for key_event in key_events:
            if key_event.keychar:
                if key_event.key == "F4":
                    # TODO I REALLY dislike the F4.. as if F4 always closed the game! Find the source and make it right
                    raise SystemExit("Window was closed.")

                if key_event.key == 'KP6' or key_event.key == "RIGHT":
                    self.__increase_value()

                if key_event.key == 'KP4' or key_event.key == "LEFT":
                    self.__decrease_value()

                if key_event.key == "KP8" or key_event.key == "UP":
                    self.__cycle_previous_option()

                if key_event.key == "KP2" or key_event.key == "DOWN":
                    self.__cycle_next_option()

                if key_event.key == "ENTER":
                    if self.options.index(self.active_option) == len(self.options) - 1:
                        self.finished = True
                        return
                    else:
                        self.__cycle_next_option()

    def render(self, console, active):
        console.printStr("Points Left {}\n".format(self.total_points - self.used_points))
        self._get_formatted_options()
        for option, text in self.list_formatted_options:
            if active and option == self.active_option:
                console.setColors(fg=ControlColors.ACTIVE_CONTROL_COLOR, bg=ControlColors.BLACK_COLOR)
            else:
                console.setColors(fg=ControlColors.INACTIVE_CONTROL_COLOR, bg=ControlColors.BLACK_COLOR)
            console.printStr(text)

    def __increase_value(self):
        point_cost = self.cost_calculator(self.assigned_points[self.active_option])

        if ((self.total_points - (self.used_points + point_cost) >= 0)
                and self.assigned_points[self.active_option] < self.max_value):
            self.used_points += point_cost
            self.assigned_points[self.active_option] += 1

    def __decrease_value(self):
        point_cost = self.cost_calculator(self.assigned_points[self.active_option])

        if self.assigned_points[self.active_option] > self.initial_value:
            self.used_points -= point_cost
            self.assigned_points[self.active_option] -= 1

    def __cycle_next_option(self):
        current_index = self.options.index(self.active_option)
        if current_index == len(self.options) - 1:
            self.active_option = self.options[0]
        else:
            self.active_option = self.options[current_index + 1]

    def __cycle_previous_option(self):
        current_index = self.options.index(self.active_option)
        if current_index == 0:
            self.active_option = self.options[-1]
        else:
            self.active_option = self.options[current_index - 1]
