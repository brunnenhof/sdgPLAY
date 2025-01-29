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
    cur.execute("SELECT * FROM games_info")
    return cur.fetchall()

  