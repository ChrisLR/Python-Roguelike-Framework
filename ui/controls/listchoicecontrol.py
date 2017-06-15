from settings import ControlColors
from ui.controls.base import BaseControl


class ListChoiceControl(BaseControl):
    def __init__(self, question, options, root_console):
        self.letter_index = ord('a')
        self.question = question
        self.options = [(self.__assign_letter(), option) for option in options]
        self.answer = None
        self.root_console = root_console
        self.finished = False
        self._formatted_options = ""

    def __assign_letter(self):
        self.letter_index += 1
        return chr(self.letter_index)

    @property
    def text(self):
        return self.question + "\n" + self._get_formatted_options()

    def _get_formatted_options(self):
        if self._formatted_options:
            return self._formatted_options

        text = ""
        width_char_count = 0
        for letter, option in self.options:
            new_text = "    ({}){}".format(letter, option.name)
            if width_char_count + len(new_text) > self.root_console.width:
                new_text += "\n"
                width_char_count = 0

            text += new_text
            width_char_count += len(new_text)
        self._formatted_options = text

        return self._formatted_options

    def handle_input(self, key_events, mouse_events):
        for key_event in key_events:
            if key_event.keychar:
                chosen_option = next((option for letter, option in self.options if letter == key_event.keychar), None)
                if chosen_option:
                    self.answer = chosen_option
                    self.finished = True

    def render(self, console, active):
        if active:
            color = ControlColors.ACTIVE_CONTROL_COLOR
        else:
            color = ControlColors.INACTIVE_CONTROL_COLOR

        width_char_count = 0
        console.setColors(fg=color, bg=ControlColors.BLACK_COLOR)
        console.printStr(self.question + "\n")
        console.setColors(fg=ControlColors.INACTIVE_CONTROL_COLOR, bg=ControlColors.BLACK_COLOR)
        for letter, option in self.options:
            new_text = "    ({}){}".format(letter, option.name)
            if width_char_count + len(new_text) > self.root_console.width:
                new_text += "\n"
                width_char_count = 0
            width_char_count += len(new_text)

            if self.answer and self.answer == option:
                console.setColors(fg=ControlColors.CHOSEN_CONTROL_COLOR, bg=ControlColors.BLACK_COLOR)
            else:
                console.setColors(fg=ControlColors.INACTIVE_CONTROL_COLOR, bg=ControlColors.BLACK_COLOR)
            console.printStr(new_text)
        console.printStr("\n")
