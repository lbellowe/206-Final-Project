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
    #Lindsey
    create_risk_table(cur, conn)
    add_data_from_json('risk_covid_data.json', cur, conn)
    #Kiran
    create_covid_table(cur, conn)
    add_from_json('covidstates.json', cur, conn)

    create_month_table(cur, conn)
    add_from_json('covidstates.json', cur, conn)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
 
