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
    cur.execute("DROP TABLE IF EXISTS Weather")
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (id INTEGER PRIMARY KEY autoincrement, month TEXT, state TEXT, high_temp INTEGER, low_temp INTEGER)")
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


def get_monthly_information(month, cur, conn):
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
        
        

            
            cur.execute("INSERT OR IGNORE INTO Weather (month, state, high_temp, low_temp) VALUES (?,?,?,?)", (mnth, state, high, low))
            
        
                
            
            conn.commit()


    max_high_temp_calc = []
    cur.execute("SELECT Weather.state, MAX(high_temp) AS maximum FROM Weather WHERE month = ?", (month,))
    data= cur.fetchone()
    max_high_temp_calc.append(data[0])
    max_high_temp_calc.append(data[1])
# print(max_high_temp_calc)
# conn.commit()


    min_high_temp_calc = []
    cur.execute("SELECT Weather.state, MIN(high_temp) AS minimum FROM Weather WHERE month = ?", (month,))
    data= cur.fetchone()
    min_high_temp_calc.append(data[0])
    min_high_temp_calc.append(data[1])
# print(min_high_temp_calc)
# conn.commit()


    max_low_temp_calc = []
    cur.execute("SELECT Weather.state, MAX(low_temp) AS maximum FROM Weather WHERE month = ?", (month,))
    data= cur.fetchone()
    max_low_temp_calc.append(data[0])
    max_low_temp_calc.append(data[1])
# print(max_low_temp_calc)
# conn.commit()


    min_low_temp_calc = []
    cur.execute("SELECT Weather.state, MIN(low_temp) AS minimum FROM Weather WHERE month = ?", (month,))
    data= cur.fetchone()
    data = list(data)
    min_low_temp_calc.append(data[0])
    min_low_temp_calc.append(data[1])
    # print(min_low_temp_calc)

    new_lst = max_high_temp_calc + min_high_temp_calc + max_low_temp_calc + min_low_temp_calc

    return new_lst
    

    #for each MONTH it prints:
    #max high_temp, min high_temp, max low-temp, min_low_temp 

        # with open("weather.csv", 'w') as f:
        #     header = ["Month"]+["Max High Temp"] + ["Min High Temp"] + ["Max Low Temp"] + ["Min Low Temp"]
        #     header = ','.join(header)
        #     f.write(header+'\n')
        #     for i in month_lst:
        #         f.write(month_lst+new_lst)
        # # for monthly_temps in min_low_temp_calc:
        # #     print(monthly_temps)
           
            
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

    with open("weather.csv", 'w') as f:
        header = ["Month"]+["Max High Temp State"]+["Max High Temp"] + ["Min High Temp State"] + ["Min High Temp"] + ["Max Low Temp State"] + ["Max Low Temp"] + ["Min Low Temp State"] + ["Min Low Temp"] 
        writer = csv.writer(f)
        writer.writerow(header)
        for i in html_list:
            data = [i]+get_monthly_information(i, cur, conn)
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
    for i in html_list:
        cur.execute('SELECT Weather.state, Weather.high_temp, Weather.low_temp FROM Weather WHERE month = ?',(i,))
        weather_data = cur.fetchall()
        conn.commit()
        state_lst = []
        high_lst = []
        low_lst = [] 
        for item in weather_data:
            state_lst.append(item[0])
            high_lst.append(item[1])
            low_lst.append(item[2])

        X_axis = np.arange(len(state_lst))
        plt.bar(X_axis - 0.2, high_lst, 0.4, label = 'High Temp')
        plt.bar(X_axis - 0.2, low_lst, 0.4, label = 'Low Temp')

  
        plt.xticks(X_axis, state_lst)
        plt.xlabel("State")
        plt.ylabel("Temperature(fahrenheit)")
        plt.title(i)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.legend()
        plt.show()

class TestCases(unittest.TestCase):

    def setUp(self) -> None:
            self.cur, self.conn = setUpDatabase('weather.db')

    def test_create_weather_table(self):
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='Weather'")

    def test_get_yearly_weather(self):
        yearly_stats = get_yearly_weather("html_files/Weather_for_All_Fifty_States.html")
      
    
    def test_get_monthly_information(self):
        cur, conn = setUpDatabase('weather.db')
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
            get_monthly_information(i, cur, conn)
    


        
        



# def main():
   
#     cur, conn = setUpDatabase('weather.db')
#     create_weather_table(cur, conn)
#     get_all_monthly_information(cur,conn)
#     visualization_weather_data(cur, conn)
   
# if __name__ == '__main__':
#     main()
#     unittest.main(verbosity=2)
    





