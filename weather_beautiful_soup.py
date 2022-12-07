from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import sqlite3
import math 
import matplotlib.pyplot as plt
import numpy as np

import json 
#https://www.extremeweatherwatch.com/us-state-averages
#before adding stuff to db chekc how much is in db 
#can import functions from other files
#  #add their files to my project folder and call their functions in here 
#three files and then one main file 
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_weather_table(cur,conn):
    # dont have primary key yet - idk what one would be bc all repeat prob
    # cur.execute("DROP TABLE IF EXISTS Weather")
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (state_month TEXT PRIMARY KEY, month TEXT, state TEXT, high_temp INTEGER, low_temp INTEGER)")
    conn.commit()
    pass


    

def get_yearly_weather(html_file):

    month_lst = []

    with open(html_file) as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    months = soup.find_all("option")
    for month in months[1:]:
        month_lst.append(month.text)
    return month_lst

    pass 


def get_monthly_information(month, cur, conn, item_size=50):
    state_lst = []
    high_temps = []
    low_temps = []
    month_lst = [] 
    month_dict = {}
 
   
    file_name = "html_files/" + month + ".html"
    with open(file_name) as f:
        soup = BeautifulSoup(f, 'html.parser')

    months = soup.find("title")
    months = months.text
    month_s = months.split(' ', 1)
    for m in month_s[0:]:
        if " " in m:
            continue
        else:
            month_lst.append(m)
  
    states_info = soup.find_all("tbody")
    for temp in states_info:
        state_name = temp.find_all("tr")
        for states in state_name:
            states_temp = states.find_all("td")
            state_lst.append(states_temp[0].text)
            high_temps.append(float(states_temp[1].text))
            low_temps.append(float(states_temp[2].text))
            

    for i in range(len(state_lst)):
        value = (state_lst[i], high_temps[i], low_temps[i])
        key = month_lst[0]
        month_dict[key] = value
   
      
        for i in month_dict:
            mnth = i 
            state = month_dict[i][0]
            high = month_dict[i][1]
            low = month_dict[i][2]
            
            cur.execute("INSERT OR IGNORE INTO Weather (state_month, month, state, high_temp, low_temp) VALUES (?,?,?,?,?)", (state+"_"+mnth, mnth, state, high, low))
            conn.commit()
            item_size -= 1
            if item_size==0:
                return

def calculations(month, cur, conn):
    max_high_temp_calc = []
    cur.execute("SELECT Weather.state, MAX(high_temp) AS maximum FROM Weather WHERE month = ?", (month,))
    data= cur.fetchone()
    max_high_temp_calc.append(data[0])
    max_high_temp_calc.append(data[1])

    min_high_temp_calc = []
    cur.execute("SELECT Weather.state, MIN(high_temp) AS minimum FROM Weather WHERE month = ?", (month,))
    data= cur.fetchone()
    min_high_temp_calc.append(data[0])
    min_high_temp_calc.append(data[1])

    max_low_temp_calc = []
    cur.execute("SELECT Weather.state, MAX(low_temp) AS maximum FROM Weather WHERE month = ?", (month,))
    data= cur.fetchone()
    max_low_temp_calc.append(data[0])
    max_low_temp_calc.append(data[1])

    min_low_temp_calc = []
    cur.execute("SELECT Weather.state, MIN(low_temp) AS minimum FROM Weather WHERE month = ?", (month,))
    data= cur.fetchone()
    data = list(data)
    min_low_temp_calc.append(data[0])
    min_low_temp_calc.append(data[1])

    new_lst = max_high_temp_calc + min_high_temp_calc + max_low_temp_calc + min_low_temp_calc

    return new_lst
    
def get_all_monthly_information(cur, conn):
    html_list = ["January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December"]

    for i in html_list:
        cur.execute("SELECT state From Weather where month = ?",(i,))
        state_list = cur.fetchall()
        if len(state_list)==50:
            continue
        elif len(state_list)==25:
            get_monthly_information(i, cur, conn)
            break
        else:
            get_monthly_information(i, cur, conn, item_size = 25)
            break

def write_csv(cur,conn):
    html_list = ["January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December"]

    with open("weather.csv", 'w') as f:
        header = ["Month"]+["Max High Temp State"]+["Max High Temp"] + ["Min High Temp State"] + ["Min High Temp"] + ["Max Low Temp State"] + ["Max Low Temp"] + ["Min Low Temp State"] + ["Min Low Temp"] 
        writer = csv.writer(f)
        writer.writerow(header)
        for i in html_list:
            data = [i]+calculations(i, cur, conn)
            writer.writerow(data)
        
def visualization_weather_data(cur, conn):
    html_list = ["January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December"]
    x_lst = []
    y_lst = []
    for i in html_list:
        data = calculations(i, cur, conn)
  
        x_lst = data[0:8:2]
        print(x_lst)
        y_lst = data[1:8:2]
        print(y_lst)
       
        plt.figure()
        plt.scatter(x_lst[0], y_lst[0], color ='purple', s = 70)
        plt.text(x_lst[0], y_lst[0], str(y_lst[0]) + "˚F", horizontalalignment ='center', verticalalignment='bottom', rotation=45)
        plt.scatter(x_lst[1], y_lst[1], color ='green', s = 70)
        plt.text(x_lst[1], y_lst[1], str(y_lst[1]) + "˚F", horizontalalignment ='center', verticalalignment='bottom', rotation=45)
        plt.scatter(x_lst[2], y_lst[2], color ='orange', s = 70)
        plt.text(x_lst[2], y_lst[2], str(y_lst[2]) + "˚F", horizontalalignment ='center', verticalalignment='bottom',rotation=45)
        plt.scatter(x_lst[3], y_lst[3], color ='blue', s = 70)
        plt.text(x_lst[3], y_lst[3], str(y_lst[3]) + "˚F", horizontalalignment ='center', verticalalignment='bottom', rotation=45)
        plt.legend(["Max High Temp" , "Min High Temp", "Max Low Temp", "Min Low Temp"], fontsize = 10)
        plt.tight_layout()
        plt.xlabel("State")
        plt.ylabel("Temperature(˚F)")
        plt.title(i + " Weather Data")
        plt.show()
  

# class TestCases(unittest.TestCase):

#     def setUp(self) -> None:
#             self.cur, self.conn = setUpDatabase('weather.db')

#     def test_create_weather_table(self):
#         self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='Weather'")

#     def test_get_yearly_weather(self):
#         yearly_stats = get_yearly_weather("html_files/Weather_for_All_Fifty_States.html")
      
    
#     def test_get_monthly_information(self):
#         cur, conn = setUpDatabase('weather.db')
#         html_list = ["January",
#                      "February",
#                      "March",
#                      "April",
#                      "May",
#                      "June",
#                      "July",
#                      "August",
#                      "September",
#                      "October",
#                      "November",
#                      "December"]
#         for i in html_list:
#             get_monthly_information(i, cur, conn)

# def main():
   
#     cur, conn = setUpDatabase('weather.db')
#     create_weather_table(cur, conn)
#     get_all_monthly_information(cur,conn)
#     visualization_weather_data(cur, conn)
   
# if __name__ == '__main__':
#     main()
#     unittest.main(verbosity=2)
    





