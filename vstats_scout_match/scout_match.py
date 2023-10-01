from copy import deepcopy
from os import listdir
from os.path import join
import re

from .create_report import create_report

FILENAME_REGEX = r'([1-5]).txt'
CODE_REGEX = r'([*|a])([0-9]{2})([S|R|A|B|D|E|F])([H|M|Q|T|U|F|O]?)([#|+|!|/|\-|=])'
ACTIONS_DICT = {
  's': [],
  'r': [],
  'a': [],
  'b': [],
  'd': [],
  'e': [],
  'f': []
}

def scout_code(code, set_array):
  match = re.search(CODE_REGEX, code, flags=re.I)
  if(not match):
     print(f'Found invalid code: {code}')
  team = 'home' if match.group(1) == '*' else 'away'
  player = int(match.group(2))
  action = match.group(3)
  quality = match.group(5)
  if player not in set_array[team]:
    set_array[team][player] = deepcopy(ACTIONS_DICT)
  set_array[team][player][action.lower()].append(quality)

def scout_set(filepath):
  set = {
    'home': {},
    'away': {}
  }
  codes = []
  with open(filepath) as set_file:
    for rally in set_file:
      codes += rally.split()
  for code in codes:
    scout_code(code, set)
  return set

def scout(match_directory):
  sets_array = []
  for file in listdir(match_directory):
    match = re.search(FILENAME_REGEX, file)
    if match:
      sets_array.append(scout_set(join(match_directory, file)))
  create_report(match_directory, sets_array)
