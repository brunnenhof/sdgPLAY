import anvil.server
import pymysql

def connect():
  connection = pymysql.connect(host='w014f358.kasserver.com',
                               port=3306,
                               user='d0429633',
                               password = '7Pzfz6zBCSdNLRtbvXDV',
                               database='d0429633',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
  return connection

@anvil.server.callable
def get_latest_game():
  conn = connect()
  with conn.cursor() as cur:
    sql = ("select * from `games_info` WHERE `closed` = %s AND `next_step_p` = %s ORDER BY `started_on` DESC LIMIT 1")
    cur.execute(sql, (0, 0))
    return cur.fetchone()

@anvil.server.callable
def get_entered_game(gi):
  conn = connect()
  with conn.cursor() as cur:
    sql = ("select * from `games_info` WHERE `closed` = %s AND `next_step_p` = %s ORDER BY `started_on` AND `game_id` = %s ")
    cur.execute(sql, (0, 0, gi))
    return cur.fetchone()

@anvil.server.callable
def get_roles(gi):
  conn = connect()
  with conn.cursor() as cur:
    sql = ("select * from `fill_roles` WHERE `game_id` = %s ")
    cur.execute(sql, (gi))
    return cur.fetchall()

@anvil.server.callable
def get_roles_for_a_region(gi, reg):
  conn = connect()
  with conn.cursor() as cur:
    sql = ("select * from `fill_roles` WHERE `game_id` = %s AND `region` = %s")
    cur.execute(sql, (gi, reg))
    return cur.fetchone()

@anvil.server.callable
def get_regions_for_players(gi):
  # return a list of dictionaries with regions NOT played by human players
  conn = connect()
  with conn.cursor() as cur:
    sql = ("select * from `fill_roles` WHERE `game_id` = %s AND `reg_avail` = %s")
    cur.execute(sql, (gi, 0))
    return cur.fetchall()

@anvil.server.callable
def get_reg_long_names():
  conn = connect()
  with conn.cursor() as cur:
        sql = ("select abbreviation, name from `regions`")
        cur.execute(sql)
        rr = cur.fetchall()
        reg_short = []
        reg_long = []
        for i in range(len(rr)):
            reg_short.append(rr[i]['abbreviation'])
            reg_long.append(rr[i]['name'])
  return reg_short, reg_long

def all_ministries_taken(m):
  if m['poverty'] == 0:
    return False
  if m['inequality'] == 0:
    return False
  if m['empowerment'] == 0:
    return False
  if m['food'] == 0:
    return False
  if m['energy'] == 0:
    return False
  if m['future'] == 0:
    return False
  return True

@anvil.server.callable
def save_player_choice(game_id, ministry, region):
  if ministry == 'poverty':
    sql = ("UPDATE fill_roles SET poverty = 1 WHERE game_id = %s AND region = %s")
  elif ministry == 'inequality':
    sql = ("UPDATE fill_roles SET inequality = 1 WHERE game_id = %s AND region = %s")
  elif ministry == 'empowerment':
    sql = ("UPDATE fill_roles SET empowerment = 1 WHERE game_id = %s AND region = %s")
  elif ministry == 'food':
    sql = ("UPDATE fill_roles SET food = 1 WHERE game_id = %s AND region = %s")
  elif ministry == 'energy':
    sql = ("UPDATE fill_roles SET energy = 1 WHERE game_id = %s AND region = %s")
  elif ministry == 'future':
    sql = ("UPDATE fill_roles SET future = 1 WHERE game_id = %s AND region = %s")
#  print (ministry)
#  print (region)
  conn = connect()
  with conn.cursor() as cur:
    cur.execute(sql, (game_id, region))
    conn.commit()
    sql = ("SELECT * FROM `fill_roles` WHERE `game_id` = %s AND `region`= %s")
    cur.execute(sql, (game_id, region))
    all_regs = cur.fetchone()
    if all_ministries_taken(all_regs):  # set region to not available
      sql = ("UPDATE fill_roles SET reg_avail = 1 WHERE game_id = %s AND region = %s")
      cur.execute(sql, (game_id, region))
      conn.commit()
