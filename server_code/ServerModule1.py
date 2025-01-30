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
  conn = connect()
  with conn.cursor() as cur:
    sql = ("select * from `fill_roles` WHERE `game_id` = %s AND `reg_avail` = %s")
    cur.execute(sql, (gi, 1))
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

