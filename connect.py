import random
import sqlite3
import datetime
import time


def db_connect():
    sqlite_file = './ObjectDB.db'
    db = sqlite3.connect(sqlite_file)
    sql = db.cursor()
    sql.execute(f"SELECT Name, Size, Tol, Ind FROM current WHERE status = {int(25)}")
    data = sql.fetchone()
    db.close()
    current_name = data[0]
    current_size = data[1]
    current_tol = data[2]
    current_index = data[3]
    return current_name, current_size, current_tol, current_index

def target_color():
    index = db_connect()[3]
    if index is 0:
        yellow_color = 53, 255, 236
        return yellow_color
    if index is 1:
        green_color = 107,255,53
        return green_color
    else:
        error_color = 0, 0, 255
        return error_color


def target_name():
    index = db_connect()[3]
    if index is 0:
        status_name_not_found = "TNF"
        return status_name_not_found
    if index is 1:
        status_name_found = "TCF"
        return status_name_found
    else:
        return "Error"

def zero_init():
    sqlite_file = './ObjectDB.db'
    db = sqlite3.connect(sqlite_file)
    sql = db.cursor()
    sql.execute(f'UPDATE current SET Ind = "0" WHERE status = {int(25)}')
    db.commit()
    db.close()


def tolerance_measurement(measure_size):
    index = db_connect()[3]
    if index is 1:
        origin_name = db_connect()[0]
        origin_size = db_connect()[1]
        origin_tol = db_connect()[2]
        if float(measure_size) > float(origin_size) + float(origin_tol) or float(measure_size) < float(origin_size) - float(origin_tol):
            status_time = datetime.datetime.now()
            status_color_red = 75, 63, 255
            text_status = "STATUS"
            log_text = f"{origin_name} A DEFECT AT {status_time}"
            #print(f"{float(measure_size) > float(origin_size) + float(origin_tol)}, {float(measure_size) < float(origin_size) - float(origin_tol)}")
            return text_status, status_color_red, log_text, 0
        elif float(measure_size) < float(measure_size) + float(origin_tol) or float(measure_size) > float(measure_size) - float(origin_tol):
            status_time = datetime.datetime.now()
            status_color_green = 107,255,53
            text_status = "STATUS"
            #print(measure_size)
            return text_status, status_color_green, status_time, 1
    if index is 0:
        status_time = datetime.datetime.now()
        status_yellow_color = 53, 255, 236
        text_status = "RULLER MODE"
        return text_status, status_yellow_color, status_time, 2
    else:
        return "error"

def percent(x):
    if x != 0:
        origin_size = db_connect()[1]
        origin_size = float(origin_size)
        mistake = (x - origin_size)
        tolerance_percent = (mistake / origin_size) * 100
        tolerance_percent = round(tolerance_percent, 3)
        tolerance_percent = str(tolerance_percent)
        return tolerance_percent, 1
    else:
        return " "



l = [1.65, 2.01]

def nearest(lst, target):
  return min(lst, key=lambda x: abs(x-target))

















