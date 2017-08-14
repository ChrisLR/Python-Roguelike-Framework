from bearlibterminal import terminal


DEVELOPMENT = True

DUNGEON_COLORS = {
    'dark_blue_wall': (0, 0, 100),
    'dark_gray_wall': (75, 75, 75),
    'light_wall': (130, 110, 50),
    'dark_ground': (75, 75, 75),
    'light_ground': (160, 144, 40),
}


# Create a dictionary that maps keys to vectors.
# Names of the available keys can be found in the online documentation:
# http://packages.python.org/tdl/tdl.event-module.html
KEY_MAPPINGS = {

    # standard arrow keys
    terminal.TK_UP: [0, -1],
    terminal.TK_DOWN: [0, 1],
    terminal.TK_LEFT: [-1, 0],
    terminal.TK_RIGHT: [1, 0],

    # number-pad keys
    # These keys will always show as KPx regardless if num-lock
    # is on or off.  Keep in mind that some keyboards and laptops
    # may be missing a keypad entirely.
    # 7 8 9
    # 4   6
    # 1 2 3
    terminal.TK_KP_1: [-1, 1],
    terminal.TK_KP_2: [0, 1],
    terminal.TK_KP_3: [1, 1],
    terminal.TK_KP_4: [-1, 0],
    terminal.TK_KP_6: [1, 0],
    terminal.TK_KP_7: [-1, -1],
    terminal.TK_KP_8: [0, -1],
    terminal.TK_KP_9: [1, -1],
}


class ControlColors(object):
    # TODO This should be moved into a sort of UI Color Theme
    ACTIVE_CONTROL_COLOR = (255, 255, 0)
    INACTIVE_CONTROL_COLOR = (255, 255, 255)
    CHOSEN_CONTROL_COLOR = (100, 255, 100)
    BLACK_COLOR = (0, 0, 0)
