import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
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
            cur.execute('INSERT OR IGNORE INTO covid19(id, state, month, confirmed, deaths) VALUES(?,?,?,?,?)',
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
    date = ["2020-04",
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
    id = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]
    
    cur.execute("DROP TABLE IF EXISTS Month")
    cur.execute("CREATE TABLE Month (month_id INTEGER PRIMARY KEY, title TEXT, month_num TEXT)")
  
    for i in range(len(months)):
        cur.execute("INSERT OR IGNORE INTO Month (month_id,title,month_num) VALUES (?,?,?)",(id[i],months[i], date[i]))
  
    conn.commit()
    
# def join_month_covid(cur, conn):
#     cur.execute("SELECT Month.title FROM Month JOIN COVID19 ON Month.month_id = COVID19.month")
#     dates = cur.fetchall()
#     print(dates)
#     conn.commit()

#CALCULATIONS
def max_cases_per_state(cur, conn):
   cur.execute("SELECT COVID19.state, month.title, MAX(COVID19.confirmed) FROM COVID19 JOIN Month ON Month.month_num = COVID19.month GROUP BY COVID19.state")
   max = cur.fetchall()
   conn.commit()
   return max
def min_cases_per_state(cur, conn):
    cur.execute("SELECT COVID19.state, month.title, MIN(COVID19.confirmed) FROM COVID19 JOIN Month ON Month.month_num = COVID19.month GROUP BY COVID19.state")
    min = cur.fetchall()
    conn.commit()
    return min
def max_deaths_per_state(cur, conn):
    cur.execute("SELECT COVID19.state, month.title, MAX(COVID19.deaths) FROM COVID19 JOIN Month ON Month.month_num = COVID19.month GROUP BY COVID19.state")
    max = cur.fetchall()
    conn.commit()
    return max
def min_deaths_per_state(cur, conn):
    cur.execute("SELECT COVID19.state, month.title, MIN(COVID19.deaths) FROM COVID19 JOIN Month ON Month.month_num = COVID19.month GROUP BY COVID19.state")
    min = cur.fetchall()
    conn.commit()
    return min

#WRITE TO CSV FILE
def write_out(file, cur, conn):
    fout = open(file, 'w')
    fout.write("First API Calculations:" + "\n")
    fout.write("Month with the most confirmed cases per state:" + "\n")
    fout.write(str(max_cases_per_state(cur, conn)) + "\n")
    fout.write("Month with the least confirmed cases per state:" + "\n")
    fout.write(str(min_cases_per_state(cur, conn)) + "\n")
    fout.write("Month with the most deaths per state:" + "\n")
    fout.write(str(max_deaths_per_state(cur, conn)) + "\n")
    fout.write("Month with the least deaths per state:" + "\n")
    fout.write(str(min_deaths_per_state(cur, conn)) + "\n")

#VISUALIZATIONS
def covid_visualization(cur, conn):
    max_cases = max_cases_per_state(cur, conn)
    min_cases = min_cases_per_state(cur, conn)
    max_deaths = max_deaths_per_state(cur, conn)
    min_deaths = min_deaths_per_state(cur, conn)
    state_lst = []
    maxc = []
    minc = []
    maxd = []
    mind = []
    for i in max_cases:
        state_lst.append(i[0])
        maxc.append(i[2])
    for i in min_cases:
        minc.append(i[2])
    for i in max_deaths:
        maxd.append(i[2])
    for i in min_deaths:
        mind.append(i[2])
    #FIRST GRAPH: Max Cases
    plt.figure()
    plt.bar(state_lst, maxc, color = "green")
    plt.xticks(rotation = 90)
    plt.xlabel = ("States")
    plt.ylabel = ("Confirmed Cases")
    plt.title("Confirmed Cases per State in March")
    plt.show()

    plt.figure()
    plt.bar(state_lst, minc, color = "green")
    plt.xticks(rotation = 90)
    plt.xlabel = ("States")
    plt.ylabel = ("Confirmed Cases")
    plt.title("Confirmed Cases per State in April")
    plt.show()

    plt.figure()
    plt.bar(state_lst, maxd, color = "green")
    plt.xticks(rotation = 90)
    plt.xlabel = ("States")
    plt.ylabel = ("Deaths")
    plt.title("Deaths per State in March")
    plt.show()

    plt.figure()
    plt.bar(state_lst, mind, color = "green")
    plt.xticks(rotation = 90)
    plt.xlabel = ("States")
    plt.ylabel = ("Deaths")
    plt.title("Deaths per State in April")
    plt.show()

# def main():

#     cur, conn = setUpDatabase('weather.db')
#     create_month_table(cur, conn)
#     create_covid_table(cur, conn)

#     add_from_json('covidstates.json', cur, conn)
    
#     write_out("first_api.csv", cur, conn)

#     covid_visualization(cur, conn)
    
# if __name__ == "__main__":
#     main()