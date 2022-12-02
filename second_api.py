import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# LINK TO API THAT I AM USING: https://api.covidactnow.org/v2/county/AK.json?apiKey=68bed0b82fde4839aebeb691441fa7ef
# three extra states: DC, PR = puerto rico, 

# CREATE TABLE FOR risk_data IN DATABASE
def create_risk_table(cur, conn):
    # to restart and get the first 25 in db uncomment line 20 
    # cur.execute("DROP TABLE IF EXISTS risk_data")
    cur.execute("CREATE TABLE IF NOT EXISTS risk_data (state_county TEXT PRIMARY KEY, state TEXT, county TEXT, population INTEGER, riskLevels INTEGER)")
    conn.commit()

def count_item_in_data_base(cur, conn):
    cur.execute("SELECT * FROM risk_data")
    items = cur.fetchall()
    return len(items)


# CODE TO ADD JSON TO THE TABLE
def add_data_from_json(filename, cur, conn):
    init_count = count_item_in_data_base(cur,conn)

    f = open(filename)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    tup_list = []
    state_dict = {}
    for data in json_data: 
        state = data['state']
        # state_list.append(state)
        county = data['county']
        risk = data['riskLevels']['overall']
        population = data['population']
        tup_list.append((state, county, population))
        if state not in state_dict:
            state_dict[state] = []
        else:
            state_dict[state].append((county,population,risk))
    
    for state in state_dict:
        state_dict[state].sort(key=lambda x:x[1], reverse=True)
        top_3_pop = state_dict[state][0:3]
        # print(state, top_3_pop)

        for i in top_3_pop:
            county = i[0]
            population = i[1]
            risk = i[2]
           
    # print(state_dict['MI'])
            cur.execute("INSERT OR IGNORE INTO risk_data (state_county, state, county, population, riskLevels) VALUES (?, ?, ?, ?, ?)", (state+' '+county, state, county, population, risk))
            count = count_item_in_data_base(cur,conn)
            if count - init_count >= 25:
                conn.commit()
                return
            
        
    conn.commit()


# def visualize_risk_vs_state(cur, conn):
#     cur.execute("SELECT state, riskLevels FROM risk_data")
#     data = cur.fetchall()
#     conn.commit()
#     # print(data)
#     state_list = []
#     risk_list = []
#     for item in data:
#         state_list.append(item[0])
#         risk_list.append(item[1])    

#     plt.figure()
#     plt.bar(state_list, risk_list)
#     plt.xticks(rotation = 45)
#     plt.show()


    


# def main():
    # SETUP DATABASE AND TABLE
    # cur, conn = setUpDatabase('weather.db')
    # create_risk_table(cur, conn)
    # add_data_from_json('risk_covid_data.json', cur, conn)
    # visualize_risk_vs_state(cur, conn)
    
    
# if __name__ == "__main__":
#     main()

