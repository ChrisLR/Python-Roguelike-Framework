#!/usr/bin/env python
"""
The main entry point for the game
"""
from cocos.director import director
director.init()
from managers.game_manager import GameManager

if __name__ == '__main__':
    game_manager = GameManager()
    game_manager.start()
