from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import sqlite3

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
        print(month_dict)
        for i in month_dict:
            mnth = i 
            state = month_dict[i][0]
            high = month_dict[i][1]
            low = month_dict[i][2]
    
            
            cur.execute("INSERT OR IGNORE INTO Weather (month, state, high_temp, low_temp) VALUES (?,?,?,?)", (mnth, state, high, low))
            
        
                
            
            conn.commit()


            



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

        # monthly_informations = [get_monthly_information(month, cur, conn) for month in html_list]
        



def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('weather.db')
    create_weather_table(cur, conn)

 
    

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
    





