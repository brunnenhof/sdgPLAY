import anvil.server
import pymysql
import pandas as pd
import pickle
import random
import time
import ftplib
from ftplib import FTP, all_errors

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
def get_play_pkl():
  start_time = time.time()
  # Connect and login at once
  with FTP(host='w014f358.kasserver.com', user='w014f358', passwd='GUTEt9AVZQoR') as ftp:
    ftp.pwd()  # Usually default is /
    ftp.cwd('filesforgame')  # Change to `other_dir/`
    # For binary use `retrbinary()`
#    with open('fcol_in_mdf2.json', 'wb') as local_file:
#        ftp.retrbinary('RETR fcol_in_mdf.json', local_file.write)
    # For binary use `retrbinary()`
    with open('play.pkl', 'wb') as local_mdfpd:
      ftp.retrbinary('RETR play.pkl', local_mdfpd.write)
    unpickled_df = pd.read_pickle("play.pkl")
    print("--- %s seconds ---" % (time.time() - start_time))
    return unpickled_df

def get_reg_x_name_colx(acro):
  conn = connect()
  with conn.cursor() as cur:
    sql = ("select * from `regions` WHERE `abbreviation` = %s")
    cur.execute(sql, (acro))
    row = cur.fetchone()
    print (row)
    # return index, name, colorhex
    return cur.fetchone()

def create_single_plot():
  pass
  
def load_plots(region, single_ta):
  # region as 'nn' single ta as 'poverty', etc
  my_time = time.localtime()
  my_time_formatted = time.strftime("%a %d %b %G, %H:%M", my_time)
  cap = foot1 + ' on ' + my_time_formatted
  mdf = get_play_pkl()
  num_rows, num_cols = mdf.shape
# drop first 10 years from 1980 to 1990 to get the spin-up wrinkles out
  mdf = mdf[321:num_rows, :]
  regidx, long, farbe = get_reg_x_name_colx(region)
  print(region + '  ' + long)
  print('    ' + single_ta)
# get the names of all vars in the current TA / Ministry
  vars_info_l = vars_df[vars_df['ta'] == single_ta]
  for i in range(len(vars_info_l)):
    # name of the vensim variable
    var_l = vars_info_l.iloc[i,3]
    time.sleep(1)
    sdg_name = vars_info_l.iloc[i,1]
    sdg_idx = vars_info_l.iloc[i,0]
    varx_list = vars_df.index[vars_df['modelvariable'] == var_l].tolist()
    varx = varx_list[0] # make an integer
    print('        ', var_l, ' ', str(varx))
    if varx in[18, 20, 34]: # global variable
        var_l = var_l.replace(" ", "_")
        idx = fcol_in_mdf[var_l]
        dfv = mdf[:, idx]
        dfv = dfv[0:end_rowi-1]
    # Define a dictionary containing Students data
        dfvpd = pd.DataFrame(dfv, columns=['glob'])
        dfvpd = dfvpd * vars_df.iloc[varx, 12]
        yr = np.arange(1990, end_yr, 0.03125)
        dfvpd.insert(loc=0, column='yr', value=yr)
        yr_py_int = np.int_(yr_py)
        pvt = np.full((lx, 1), np.nan)  # placeholder for year points
        for i in range(lx):
            idx = max(1, yr_py_int.item(i))
            pvt[i] = dfvpd.iloc[idx-1, 1]
            fn = folder + region + '-' + str(varx) + '-' + single_ta + '.png'
            plot_glob_ta_pol(dfvpd, pvt, varx, fn)
    else: # regional variable
    # vensim uses underscores not whitespace in variable name
        var_l = var_l.replace(" ", "_")
        # find location of variable in mdf
        idx = fcol_in_mdf[var_l]
        # get the slice with all regional data for the variable
        dfv = mdf[:, idx:idx + 10]
        # get the slice of rows
        dfv = dfv[0:end_rowi - 1, :]
        # make a pd dataframe
        dfvpd = pd.DataFrame(dfv, columns=my_lab)
        # scale
        dfvpd = dfvpd * vars_df.iloc[varx, 12]
        # slice out the correct region column
        dfvpd = pd.DataFrame(dfvpd.iloc[:, regidx])
        # make a colum with correct time data
        yr = np.arange(1990, end_yr, 0.03125)
        # put the time in slot 0
        dfvpd.insert(loc=0, column='yr', value=yr)
        # fig = px.line(d3,x='yr',y='cn')
        # fig.show()
        # prepare the data for the years with thick dots
        yr_py_int = np.int_(yr_py)
        pvt = np.full((lx, 1), np.nan)  # placeholder for year points
        for i in range(lx):
            idx = max(1, yr_py_int.item(i))
            pvt[i] = dfvpd.iloc[idx-1, 1]
        # prepare the correct filename
        lfn = region + '-' + str(varx) + '-' + single_ta + '.png'
        fn = os.path.join(cwd, folder, lfn)
        # send for plotting
#        plot_each_reg_ta_pol(dfvpd, pvt, varx, fn)
        plot_each_reg_ta_pol2(dfvpd, pvt, varx, fn)

  pass
  
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
def get_reg_long_names(which_region):
  conn = connect()
  with conn.cursor() as cur:
    sql = ("select id, name from `regions` WHERE abbreviation = %s")
    cur.execute(sql, which_region)
    row = cur.fetchone()
    reg_long = row['name']
    reg_idx = row['id']
  return reg_idx, reg_long

@anvil.server.callable
def get_ministry_long(which_ministry):
  conn = connect()
  with conn.cursor() as cur:
    sql = ("select id, longname from `ministries` WHERE ministry = %s")
    cur.execute(sql, which_ministry)
    row = cur.fetchone()
    m_long = row['longname']
    m_idx = row['id']
  return m_idx, m_long


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
  print ('in save_player_choice: ' + region)
  print ('in save_player_choice: ' + ministry)
  # qick check if that role is still available  
  if ministry == 'energy':
    sql = ("SELECT energy FROM fill_roles WHERE game_id = %s AND region = %s")
    sqls = ("UPDATE fill_roles SET energy = 1 WHERE game_id = %s AND region = %s") # prepare for save
  elif ministry == 'poverty':
    sql = ("SELECT poverty FROM fill_roles WHERE game_id = %s AND region = %s")
    sqls = ("UPDATE fill_roles SET poverty = 1 WHERE game_id = %s AND region = %s")  
  elif ministry == 'inequality':
    sql = ("SELECT inequality FROM fill_roles WHERE game_id = %s AND region = %s")
    sqls = ("UPDATE fill_roles SET inequality = 1 WHERE game_id = %s AND region = %s")  
  elif ministry == 'food':
    sql = ("SELECT food FROM fill_roles WHERE game_id = %s AND region = %s")
    sqls = ("UPDATE fill_roles SET food = 1 WHERE game_id = %s AND region = %s")  
  elif ministry == 'future':
    sql = ("SELECT future FROM fill_roles WHERE game_id = %s AND region = %s")
    sqls = ("UPDATE fill_roles SET future = 1 WHERE game_id = %s AND region = %s")  
  elif ministry == 'empowerment':
    sql = ("SELECT empowerment FROM fill_roles WHERE game_id = %s AND region = %s")
    sqls = ("UPDATE fill_roles SET empowerment = 1 WHERE game_id = %s AND region = %s")  
  conn = connect()
  with conn.cursor() as cur:
    cur.execute(sql, [game_id, region])
    row = cur.fetchone()
    print (row)
    if row[ministry] == 1:
      return False
# handle False, ie role no longer available in client code
# we now know that the role is still available, so save it  
  conn = connect()
  with conn.cursor() as cur:
    cur.execute(sqls, (game_id, region))
    conn.commit()
    # now check if setting this role as taken alse means that ALL roles are taken
    # and the region needs to be set as taken / no longer available
    sql = ("SELECT * FROM `fill_roles` WHERE `game_id` = %s AND `region`= %s")
    cur.execute(sql, (game_id, region))
    all_regs = cur.fetchone()
    if all_ministries_taken(all_regs):  # set region to not available
      sql = ("UPDATE fill_roles SET reg_avail = 0 WHERE game_id = %s AND region = %s")
      cur.execute(sql, (game_id, region))
      conn.commit()
  return True
