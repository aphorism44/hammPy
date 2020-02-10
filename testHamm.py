#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 16:49:21 2020

@author: djesse2
"""

from Hammurabi import Hammurabi

game = Hammurabi()
while game.check_game_running():
    #general loop; will need to allow more info calls in Alexa
    print(game.get_status_str())
    while game.grainFed < 0:
        feed = int(input(game.prompt_feed_grain()))
        print(game.process_feed_grain(feed)2)
    while game.landBought < 0:
        buy = int(input(game.prompt_acres_buy()))
        print(game.process_acres_buy(buy))
    if game.landBought > 0:
        while game.landSold < 0:
            sell = int(input(game.prompt_acres_sell()))
            print(game.process_acres_sell(sell))
    while game.grainPlanted < 0:
        plant = int(input(game.prompt_plant_grain()))
        print(game.process_plant_grain(plant))
    game.update_turn()