from copy import deepcopy
import json
from os import makedirs
from os.path import exists, join

SET_STATS = {
  'attack': {
    'sum': 0,
    'error': 0,
    'block': 0,
    'point': 0,
  },
  'receive': {
    'sum': 0,
    'error': 0,
    'pos': 0,
    'prf': 0
  },
  'serve': {
    'sum': 0,
    'error': 0,
    'point': 0
  },
  'block': {
    'point': 0,
    'touch': 0,
    'error': 0
  },
  'set': {
    'error': 0
  },
  'freeball': {
    'error': 0
  }
}

class Report:
  def init_paths(self, match_directory, sets_array):
    self.home_path = join(match_directory, 'home')
    self.away_path = join(match_directory, 'away')
    self.sets = sets_array
    self.total_sets = len(sets_array)
    if not exists(self.home_path):
      makedirs(self.home_path)
    if not exists(self.away_path):
      makedirs(self.away_path)

  def init_players(self, match_directory):
    self.home_players = {}
    with open(join(match_directory, 'home.json')) as f:
      home_team = json.load(f)
    for player in home_team.keys():
      self.home_players[int(player)] = []
      for _ in range(self.total_sets):
        self.home_players[int(player)].append(deepcopy(SET_STATS))

    self.away_players = {}
    with open(join(match_directory, 'away.json')) as f:
      away_team = json.load(f)
    for player in away_team.keys():
      self.away_players[int(player)] = []
      for _ in range(self.total_sets):
        self.away_players[int(player)].append(deepcopy(SET_STATS))

  def scout_player(self, player_array, player_code_array):
    player_array['attack']['sum'] = len(player_code_array['a'])
    player_array['attack']['error'] = player_code_array['a'].count('=')
    player_array['attack']['block'] = player_code_array['a'].count('/')
    player_array['attack']['point'] = player_code_array['a'].count('#')
    player_array['receive']['sum'] = len(player_code_array['r'])
    player_array['receive']['error'] = player_code_array['r'].count('=')
    player_array['receive']['pos'] = player_code_array['r'].count('+')
    player_array['receive']['prf'] = player_code_array['r'].count('#')
    player_array['serve']['sum'] = len(player_code_array['s'])
    player_array['serve']['error'] = player_code_array['s'].count('=')
    player_array['serve']['point'] = player_code_array['s'].count('#')
    player_array['block']['error'] = player_code_array['b'].count('=')
    player_array['block']['touch'] = player_code_array['b'].count('+') + player_code_array['b'].count('!') + player_code_array['b'].count('-')
    player_array['block']['point'] = player_code_array['b'].count('#')
    player_array['set']['error'] = player_code_array['e'].count('=')
    player_array['freeball']['error'] = player_code_array['f'].count('=')

  def scout_set(self, set, set_number):
    for player in set['home'].keys():
      self.scout_player(self.home_players[player][set_number], set['home'][player])
    for player in set['away'].keys():
      self.scout_player(self.away_players[player][set_number], set['away'][player])

  def scout_match(self, sets_array):
    set_number = 0
    for set in sets_array:
      self.scout_set(set, set_number)

  def create_player_set_stats(self, player, player_array, team_path, set):
    serve_total = 0
    serve_error = 0
    serve_point = 0
    receive_total = 0
    receive_error = 0
    receive_pos = 0
    receive_prf = 0
    attack_total = 0
    attack_error = 0
    attack_block = 0
    attack_point = 0
    block_point = 0
    block_touch = 0
    block_error = 0
    set_error = 0
    freeball_error = 0
    for set in range(len(player_array)):
      serve_total += player_array[set]['serve']['sum']
      serve_error += player_array[set]['serve']['error']
      serve_point += player_array[set]['serve']['point']
      receive_total += player_array[set]['receive']['sum']
      receive_error += player_array[set]['receive']['error']
      receive_pos += player_array[set]['receive']['pos']
      receive_prf += player_array[set]['receive']['prf']
      attack_total += player_array[set]['attack']['sum']
      attack_error += player_array[set]['attack']['error']
      attack_block += player_array[set]['attack']['block']
      attack_point += player_array[set]['attack']['point']
      block_error += player_array[set]['block']['error']
      block_error += player_array[set]['block']['touch']
      block_point += player_array[set]['block']['point']
      set_error += player_array[set]['set']['error']
      freeball_error += player_array[set]['freeball']['error']
    with open(join(team_path, f'{player}.txt'), 'a') as f:
      lines = [
        '',
        '',
        '',
        '-' * 50,
        f'set {set+1}',
        '-' * 50,
        '-' * 50,
        'points',
        '-' * 50,
        f'total: {serve_point + attack_point + block_point}',
        f'service winner: {serve_point}',
        f'attack: {attack_point}',
        f'block point {block_point}',
        '-' * 50,
        'serve',
        '-' * 50,
        f'total: {serve_total}',
        f'service_winner: {serve_point}',
        f'service error: {serve_error}',
        '-' * 50,
        'reception',
        '-' * 50,
        f'total: {receive_total}',
        f'receive error: {receive_error}',
        f'receive positive%: {format(receive_pos/receive_total, ".2%") if receive_total else "0%"}',
        f'receive perfect%: {format(receive_prf/receive_total, ".2%") if receive_total else "0%"}',
        '-' * 50,
        'attack',
        '-' * 50,
        f'total: {attack_total}',
        f'attack error: {attack_error}',
        f'attack blocked: {attack_block}',
        f'attack point: {attack_point}',
        f'attack point%: {format(attack_point/attack_total, ".2%") if attack_total else "0%"}',
        '-' * 50,
        'block',
        '-' * 50,
        f'block point: {block_point}',
        f'block touch: {block_touch}',
        f'block error: {block_error}'
      ]
      f.writelines(f'{line}\n' for line in lines)

  def create_player_stats(self, player, player_array, team_path):
    serve_total = 0
    serve_error = 0
    serve_point = 0
    receive_total = 0
    receive_error = 0
    receive_pos = 0
    receive_prf = 0
    attack_total = 0
    attack_error = 0
    attack_block = 0
    attack_point = 0
    block_point = 0
    block_touch = 0
    block_error = 0
    set_error = 0
    freeball_error = 0
    for set in range(len(player_array)):
      serve_total += player_array[set]['serve']['sum']
      serve_error += player_array[set]['serve']['error']
      serve_point += player_array[set]['serve']['point']
      receive_total += player_array[set]['receive']['sum']
      receive_error += player_array[set]['receive']['error']
      receive_pos += player_array[set]['receive']['pos']
      receive_prf += player_array[set]['receive']['prf']
      attack_total += player_array[set]['attack']['sum']
      attack_error += player_array[set]['attack']['error']
      attack_block += player_array[set]['attack']['block']
      attack_point += player_array[set]['attack']['point']
      block_error += player_array[set]['block']['error']
      block_touch += player_array[set]['block']['touch']
      block_point += player_array[set]['block']['point']
      set_error += player_array[set]['set']['error']
      freeball_error += player_array[set]['freeball']['error']
    with open(join(team_path, f'{player}.txt'), 'w') as f:
      lines = [
        '-' * 50,
        'points',
        '-' * 50,
        f'total: {serve_point + attack_point + block_point}',
        f'service winner: {serve_point}',
        f'attack: {attack_point}',
        f'block point {block_point}',
        '-' * 50,
        'serve',
        '-' * 50,
        f'total: {serve_total}',
        f'service_winner: {serve_point}',
        f'service error: {serve_error}',
        '-' * 50,
        'reception',
        '-' * 50,
        f'total: {receive_total}',
        f'receive error: {receive_error}',
        f'receive positive%: {format(receive_pos/receive_total, ".2%") if receive_total else "0%"}',
        f'receive perfect%: {format(receive_prf/receive_total, ".2%") if receive_total else "0%"}',
        '-' * 50,
        'attack',
        '-' * 50,
        f'total: {attack_total}',
        f'attack error: {attack_error}',
        f'attack blocked: {attack_block}',
        f'attack point: {attack_point}',
        f'attack point%: {format(attack_point/attack_total, ".2%") if attack_total else "0%"}',
        '-' * 50,
        'block',
        '-' * 50,
        f'block point: {block_point}',
        f'block touch: {block_touch}',
        f'block error: {block_error}'
      ]
      f.writelines(f'{line}\n' for line in lines)

  def create_team_stats(self, team_players, opponent_players, team_path):
    serve_total = 0
    serve_error = 0
    serve_point = 0
    receive_total = 0
    receive_error = 0
    receive_pos = 0
    receive_prf = 0
    attack_total = 0
    attack_error = 0
    attack_block = 0
    attack_point = 0
    block_point = 0
    block_error = 0
    set_error = 0
    freeball_error = 0
    opponent_error = 0
    for player in team_players.keys():
      for set in range(len(team_players[player])):
        serve_total += team_players[player][set]['serve']['sum']
        serve_error += team_players[player][set]['serve']['error']
        serve_point += team_players[player][set]['serve']['point']
        receive_total += team_players[player][set]['receive']['sum']
        receive_error += team_players[player][set]['receive']['error']
        receive_pos += team_players[player][set]['receive']['pos']
        receive_prf += team_players[player][set]['receive']['prf']
        attack_total += team_players[player][set]['attack']['sum']
        attack_error += team_players[player][set]['attack']['error']
        attack_block += team_players[player][set]['attack']['block']
        attack_point += team_players[player][set]['attack']['point']
        block_error += team_players[player][set]['block']['error']
        block_point += team_players[player][set]['block']['point']
        set_error += team_players[player][set]['set']['error']
        freeball_error += team_players[player][set]['freeball']['error']
    for player in opponent_players.keys():
      for set in range(len(opponent_players[player])):
        for key in ['attack', 'serve', 'block', 'set', 'freeball']:
          opponent_error += opponent_players[player][set][key]['error']
    with open(join(team_path, 'team.txt'), 'w') as f:
      lines = [
        '-' * 50,
        'points',
        '-' * 50,
        f'total: {serve_point + attack_point + block_point + opponent_error}',
        f'service winner: {serve_point}',
        f'attack: {attack_point}',
        f'block point {block_point}',
        f'opponent error: {opponent_error}',
        '-' * 50,
        'serve',
        '-' * 50,
        f'total: {serve_total}',
        f'service_winner: {serve_point}',
        f'service error: {serve_error}',
        '-' * 50,
        'reception',
        '-' * 50,
        f'total: {receive_total}',
        f'receive error: {receive_error}',
        f'receive positive%: {format(receive_pos/receive_total, ".2%")}',
        f'receive perfect%: {format(receive_prf/receive_total, ".2%")}',
        '-' * 50,
        'attack',
        '-' * 50,
        f'total: {attack_total}',
        f'attack error: {attack_error}',
        f'attack blocked: {attack_block}',
        f'attack point: {attack_point}',
        f'attack point%: {format(attack_point/attack_total, ".2%")}',
        '-' * 50,
        'block',
        '-' * 50,
        f'block point: {block_point}'
      ]
      f.writelines(f'{line}\n' for line in lines)

  def create_team_set_stats(self, team_players, opponent_players, team_path, set):
    serve_total = 0
    serve_error = 0
    serve_point = 0
    receive_total = 0
    receive_error = 0
    receive_pos = 0
    receive_prf = 0
    attack_total = 0
    attack_error = 0
    attack_block = 0
    attack_point = 0
    block_point = 0
    block_error = 0
    set_error = 0
    freeball_error = 0
    opponent_error = 0
    for player in team_players.keys():
      serve_total += team_players[player][set]['serve']['sum']
      serve_error += team_players[player][set]['serve']['error']
      serve_point += team_players[player][set]['serve']['point']
      receive_total += team_players[player][set]['receive']['sum']
      receive_error += team_players[player][set]['receive']['error']
      receive_pos += team_players[player][set]['receive']['pos']
      receive_prf += team_players[player][set]['receive']['prf']
      attack_total += team_players[player][set]['attack']['sum']
      attack_error += team_players[player][set]['attack']['error']
      attack_block += team_players[player][set]['attack']['block']
      attack_point += team_players[player][set]['attack']['point']
      block_error += team_players[player][set]['block']['error']
      block_point += team_players[player][set]['block']['point']
      set_error += team_players[player][set]['set']['error']
      freeball_error += team_players[player][set]['freeball']['error']
    for player in opponent_players.keys():
      for key in ['attack', 'serve', 'block', 'set', 'freeball']:
        opponent_error += opponent_players[player][set][key]['error']
    with open(join(team_path, f'set{set+1}.txt'), 'w') as f:
      lines = [
        '-' * 50,
        'points',
        '-' * 50,
        f'total: {serve_point + attack_point + block_point + opponent_error}',
        f'service winner: {serve_point}',
        f'attack: {attack_point}',
        f'block point {block_point}',
        f'opponent error: {opponent_error}',
        '-' * 50,
        'serve',
        '-' * 50,
        f'total: {serve_total}',
        f'service_winner: {serve_point}',
        f'service error: {serve_error}',
        '-' * 50,
        'reception',
        '-' * 50,
        f'total: {receive_total}',
        f'receive error: {receive_error}',
        f'receive positive%: {format(receive_pos/receive_total, ".2%")}',
        f'receive perfect%: {format(receive_prf/receive_total, ".2%")}',
        '-' * 50,
        'attack',
        '-' * 50,
        f'total: {attack_total}',
        f'attack error: {attack_error}',
        f'attack blocked: {attack_block}',
        f'attack point: {attack_point}',
        f'attack point%: {format(attack_point/attack_total, ".2%")}',
        '-' * 50,
        'block',
        '-' * 50,
        f'block point: {block_point}'
      ]
      f.writelines(f'{line}\n' for line in lines)

  def create_report(self):
    for set in range(self.total_sets):
      self.create_team_set_stats(self.home_players, self.away_players, self.home_path, set)
      self.create_team_set_stats(self.away_players, self.home_players, self.away_path, set)
    self.create_team_stats(self.home_players, self.away_players, self.home_path)
    self.create_team_stats(self.away_players, self.home_players, self.away_path)
    for player in self.home_players.keys():
      self.create_player_stats(player, self.home_players[player], self.home_path)
      for set in range(self.total_sets):
        self.create_player_set_stats(player, self.home_players[player], self.home_path, set)
    for player in self.away_players.keys():
      self.create_player_stats(player, self.away_players[player], self.away_path)
      for set in range(self.total_sets):
        self.create_player_set_stats(player, self.away_players[player], self.away_path, set)

  def __init__(self, match_directory, sets_array):
    self.init_paths(match_directory, sets_array)
    self.init_players(match_directory)
    self.scout_match(sets_array)
    self.create_report()

def create_report(match_directory, sets_array):
  Report(match_directory, sets_array)
