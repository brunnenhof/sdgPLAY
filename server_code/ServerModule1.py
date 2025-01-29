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
    return cur.fetchall()

  