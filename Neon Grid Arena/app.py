import math
import random
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'neongrid_secret_2026'
socketio = SocketIO(app, cors_allowed_origins='*')

players = {}
current_level = 1


def generate_walls(level):
  """Generates neon barrier walls based on current level hardness."""
  walls = []
  num_walls = min(3 + level * 2, 12)  # Increases walls per level

  for _ in range(num_walls):
    is_horizontal = random.choice([True, False])
    if is_horizontal:
      w = random.randint(100, 200)
      h = 16
    else:
      w = 16
      h = random.randint(100, 200)

    x = random.randint(100, 700 - w)
    y = random.randint(100, 500 - h)

    walls.append({
        'x': x,
        'y': y,
        'w': w,
        'h': h,
        'color': random.choice(['#ff007f', '#b026ff', '#ff5e00']),
    })

  return walls


walls = generate_walls(current_level)
coin = {
    'x': random.randint(50, 750),
    'y': random.randint(50, 550),
    'id': random.randint(1000, 9999),
}


@app.route('/')
def index():
  return render_template('index.html')


@socketio.on('join_game')
def handle_join(data):
  global current_level, walls
  player_id = request.sid
  color_choices = ['#00f0ff', '#ff007f', '#39ff14', '#ffb700', '#b026ff']

  players[player_id] = {
      'id': player_id[:5],
      'name': data.get('username', f'Pilot_{player_id[:3]}'),
      'x': 50,
      'y': 50,
      'color': random.choice(color_choices),
      'score': 0,
      'alive': True,
      'base_speed': 8,
  }

  emit(
      'init_state',
      {
          'my_id': player_id,
          'players': players,
          'coin': coin,
          'walls': walls,
          'level': current_level,
      },
      room=player_id,
  )


@socketio.on('respawn_player')
def handle_respawn():
  player_id = request.sid
  if player_id in players:
    players[player_id]['x'] = 50
    players[player_id]['y'] = 50
    players[player_id]['alive'] = True
    emit(
        'player_respawned',
        {'id': player_id, 'x': 50, 'y': 50},
        broadcast=True,
    )


@socketio.on('move_player')
def handle_move(data):
  global current_level, walls, coin
  player_id = request.sid

  if player_id not in players or not players[player_id]['alive']:
    return

  player = players[player_id]

  # Speed increases with level
  speed = player['base_speed'] + (current_level * 1.5)

  direction = data.get('direction')
  new_x, new_y = player['x'], player['y']

  if direction == 'up':
    new_y = max(16, player['y'] - speed)
  elif direction == 'down':
    new_y = min(584, player['y'] + speed)
  elif direction == 'left':
    new_x = max(16, player['x'] - speed)
  elif direction == 'right':
    new_x = min(784, player['x'] + speed)

  # Check Wall Collision (Game Over Condition)
  for w in walls:
    if (
        new_x + 12 > w['x']
        and new_x - 12 < w['x'] + w['w']
        and new_y + 12 > w['y']
        and new_y - 12 < w['y'] + w['h']
    ):

      player['alive'] = False
      socketio.emit(
          'game_over',
          {'id': player_id, 'name': player['name']},
          room=player_id,
      )
      return

  player['x'] = new_x
  player['y'] = new_y

  # Coin Collection & Level Up Logic
  dist_coin = math.hypot(player['x'] - coin['x'], player['y'] - coin['y'])
  if dist_coin < 28:
    player['score'] += 100

    # Level Up condition every 300 points
    if player['score'] >= current_level * 300:
      current_level += 1
      walls = generate_walls(current_level)
      socketio.emit(
          'level_up',
          {'level': current_level, 'walls': walls, 'player': player['name']},
      )

    coin = {
        'x': random.randint(50, 750),
        'y': random.randint(50, 550),
        'id': random.randint(1000, 9999),
    }
    socketio.emit(
        'coin_spawned',
        {
            'coin': coin,
            'collector_id': player_id,
            'score': player['score'],
            'name': player['name'],
        },
    )

  socketio.emit(
      'state_update', {'id': player_id, 'x': player['x'], 'y': player['y']}
  )


@socketio.on('disconnect')
def handle_disconnect():
  player_id = request.sid
  if player_id in players:
    del players[player_id]
    socketio.emit('player_left', {'id': player_id})


if __name__ == '__main__':
  socketio.run(app, debug=True, port=5000)