import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import requests

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# LINK TO API THAT I AM USING: https://api.covidactnow.org/v2/counties.json?apiKey=68bed0b82fde4839aebeb691441fa7ef


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
def add_data_from_json(cur, conn):
    init_count = count_item_in_data_base(cur,conn)
    API_KEY = "68bed0b82fde4839aebeb691441fa7ef"
    JSON_link = "https://api.covidactnow.org/v2/counties.json?apiKey=68bed0b82fde4839aebeb691441fa7ef"
    base_url = "https://api.covidactnow.org/v2/counties.json?apiKey={}"
    request_url = base_url.format(API_KEY)
    param_dict = {'format': 'json'}
    r = requests.get(request_url, params = param_dict)
    data = r.text
    json_data = json.loads(data)

    # f = open(filename)
    # file_data = f.read()
    # f.close()
    # json_data = json.loads(file_data)
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
    # started CALCULATIONS HERE!
    conn.commit()
def visualize_state_risk_data(risk_num, cur, conn):
    cur.execute("SELECT risk_data.state, risk_data.riskLevels, risk_data.population FROM risk_data WHERE riskLevels > ?", (risk_num,))
    data= cur.fetchall()
    
    # print(data)
    state_lst = []
    risk_lst = []
    pop_lst = []
    og_risk = []
    state_risk_dict = {}

    for lst in data:
        pop_lst.append(lst[2])
        og_risk.append(lst[1])
        # print(lst)
        if lst[0] not in state_risk_dict:
            state_risk_dict[lst[0]] = lst[1]
        else: 
            state_risk_dict[lst[0]] += lst[1]
            # state_lst.append(lst[0])
    # print(len(og_risk))
    # print(len(pop_lst))
    for keys,values in state_risk_dict.items():
        # print(keys)
        avg_risk = values / 3
        state_lst.append(keys)
        risk_lst.append(avg_risk)
        state_risk_dict[keys] = avg_risk
        # will write this out 
    print(state_risk_dict)
    

    # print(state_lst)
    # print(risk_lst)

    # need to figure out how to get rid of MP
    # graph for avg risk and states
    plt.figure()
    plt.bar(state_lst, risk_lst, color = "pink")
    plt.xticks(rotation = 45)
    plt.xlabel("States")
    plt.ylabel("Average Risk")
    plt.title("Average Covid-19 Risk Level by State")
    plt.show()

    #  graph 2: scatter plot riskLevels versus popualtion 
    # plt.figure()
    # plt.scatter(risk_lst, og_risk)
    # plt.show()
        
    conn.commit()
    return state_risk_dict
def csv_out(data, file):
    fout = open(file, 'w')
    fout.write("Second API calculations: Finding average risk level per state" + "\n")
    fout.write(str(data))

# def main():
#     # SETUP DATABASE AND TABLE
#     cur, conn = setUpDatabase('weather.db')
#     create_risk_table(cur, conn)
#     add_data_from_json(cur, conn)
#     #visualize_state_risk_data(0, cur, conn)
#     data = visualize_state_risk_data(0, cur, conn)
#     csv_out(data, "second_api.txt") 
    
# if __name__ == "__main__":
#     main()