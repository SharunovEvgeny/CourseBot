import liquipediapy.exceptions as ex
from liquipediapy.liquipediapy import liquipediapy
import re
from liquipediapy.dota_modules.player import dota_player
from liquipediapy.dota_modules.team import dota_team
from liquipediapy.dota_modules.pro_circuit import dota_pro_circuit
import unicodedata
from liquipediapy import *
dota_p = dota("f")
player = dota_p.get_players()

print(player)