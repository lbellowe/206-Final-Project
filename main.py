from xml.sax import parseString
from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import sqlite3
import json
import api1
import second_api 
import weather_beautiful_soup
import main 
import matplotlib.pyplot as plt
import numpy as np


from api1 import * 
from second_api import *
from weather_beautiful_soup import *

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

def main():
    cur, conn = setUpDatabase('weather.db')
    #Leah
    create_weather_table(cur, conn)
    get_all_monthly_information(cur,conn)
    write_csv(cur,conn)
    visualization_weather_data(cur, conn)
    #Lindsey
    create_risk_table(cur, conn)
    add_data_from_json('risk_covid_data.json', cur, conn)
    data = visualize_state_risk_data(0, cur, conn)
    csv_out(data, "second_api.csv") 
    #Kiran
    create_month_table(cur, conn)
    create_covid_table(cur, conn)

    add_from_json('covidstates.json', cur, conn)
    
    write_out("first_api.csv", cur, conn)

    covid_visualization(cur, conn)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
 
