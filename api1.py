import unittest
import sqlite3
import json
import os

#Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# CREATE TABLE FOR COVID DATA IN DATABASE
#we created a table with columns in SQLite 
def create_covid_table(cur, conn):
    #cur.execute("DROP TABLE IF EXISTS COVID19")
    cur.execute("CREATE TABLE IF NOT EXISTS \"COVID19\" (id INTEGER PRIMARY KEY, state TEXT, month TEXT, confirmed INT, deaths INT)")
    conn.commit()

def count_item(cur, conn):
    cur.execute("SELECT * FROM COVID19")
    items = cur.fetchall()
    return len(items)

def add_from_json(filename, cur, conn):
    init_count = count_item(cur, conn)
    # READ IN DATA
    f = open(filename)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    dict = {}
    for state in json_data:
        confirmed_dict = {"2020-04": 0, "2020-05" : 0, "2020-06": 0, "2020-07": 0, "2020-08": 0, "2020-09": 0
        , "2020-10": 0, "2020-11": 0, "2020-12": 0, "2021-01": 0, "2021-02": 0, "2021-03": 0}
        death_dict = {"2020-04" : 0, "2020-05" : 0, "2020-06": 0, "2020-07": 0, "2020-08": 0, "2020-09": 0
        , "2020-10": 0, "2020-11": 0, "2020-12": 0, "2021-01": 0, "2021-02": 0, "2021-03": 0}
        dict[state]={}
        for every_day_data in json_data[state]:
            month = every_day_data['date'][0:7]
            if month in confirmed_dict:
                confirmed_dict[month] += int(every_day_data["confirmed"])  
                death_dict[month] += int(every_day_data["deaths"])
                dict[state][month] = {"confirmed": confirmed_dict[month], "deaths": death_dict[month]}
    
    id = 0
    for item in dict:
        st = item
        for i in dict[item]:
            mnth = i
            confirmed = dict[item][i]['confirmed']
            deaths = dict[item][i]['deaths']
            cur.execute('INSERT OR IGNORE INTO COVID19(id, state, month, confirmed, deaths) VALUES(?,?,?,?,?)',
            (id, st, mnth, confirmed, deaths))
            id += 1
            count = count_item(cur, conn)
            if count - init_count >= 25:
                conn.commit()
                return
           
    conn.commit()

def create_month_table(cur,conn):
    months = ["April",
                     "May",
                     "June",
                     "July",
                     "August",
                     "September",
                     "October",
                     "November",
                     "December",
                     "January",
                     "February",
                     "March",]
    id = ["2020-04",
    "2020-05",
    "2020-06",
    "2020-07",
    "2020-08",
    "2020-09",
    "2020-10",
    "2020-11",
    "2020-12",
    "2021-01",
    "2021-02",
    "2021-03"]
    
    cur.execute("DROP TABLE IF EXISTS Month")
    cur.execute("CREATE TABLE Month (month_id TEXT PRIMARY KEY, title TEXT)")
  
    for i in range(len(months)):
        print(id[1])
        cur.execute("INSERT OR IGNORE INTO Month (month_id,title) VALUES (?,?)",(id[i],months[i]))
  
    conn.commit()
    

                




# def main():

#     cur, conn = setUpDatabase('weather.db')
#     create_covid_table(cur, conn)


#     add_from_json('covidstates.json', cur, conn)
    
    
# if __name__ == "__main__":
#     main()