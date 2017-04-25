import requests
try: import simplejson as json
except ImportError: import json
from bs4 import BeautifulSoup
import sqlite3
#import matplotlib.pyplot as plt

import time

site = ['https://www.bankbazaar.com/gold-rate-kolkata.html']
MetalPrice = {}

conn = sqlite3.connect('MetalPrices.db')
c = conn.cursor()

def removePunctuations(name):
	punctuations = [",",".","(",")",":","-","_","\n","\r","₹"]
	for punctuation in punctuations:
		name = name.replace(punctuation,"")
    #name = name.replace( "\u2013"," - " )
	name = name.replace("  ","")
	return name

moneycontrol = ['gold','zinc','silver','copper','aluminium','nickel']

'''def connectDB():
    conn = sqlite3.connect('flamelite.db')
    return conn'''

def createDB():
    query = "CREATE TABLE IF NOT EXISTS MetalPrice(Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , "
    query+= "Date TIMESTAMP DEFAULT CURRENT_DATE NOT NULL, "
    query+="Gold INT NOT NULL, "
    query+= "Zinc INT NOT NULL,"
    query+="Silver INT NOT NULL,"
    query+="Copper INT NOT NULL,"
    query+="Aluminium INT NOT NULL,"
    query+="Nickel INT NOT NULL)"
    c.execute(query)

def dataEntry(*a):
    #date = c.execute("SELECT CURRENT_DATE")
    #print(date)
    #print(c.execute("DATE('now')"))
    date=c.execute("SELECT * FROM MetalPrice WHERE Date=DATE('now')")
    if date:
        return
    c.execute("INSERT INTO MetalPrice (Date,Gold,Zinc,Silver,Copper,Aluminium,Nickel) VALUES(DATE('now'),?,?,?,?,?,?)",(a[0][0],a[0][1],a[0][2],a[0][3],a[0][4],a[0][5]))
    conn.commit()
    #print(arr[0][0])


def dataquery():
    query = "SELECT * Gold FROM Price"
    query = c.execute(query).fetchall()
    print(query)
#def plotgraph():


def getthePrice():

    '''Metal prices from money control'''
    arr = []
    for metal in moneycontrol:
        time.sleep(0.5)
        response = requests.get('http://www.moneycontrol.com/commodity/'+metal+'-price.html')
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.findAll("div", {"class": "FL brdr PR20 gr_13"})

        if data:
            price = data[0].find('span').string
            if metal=='gold':
                arr.append(price)
                MetalPrice['gold'] = 'Gold = '+price+' Rs/10 gram'
            else:
                arr.append(price)
                MetalPrice[metal]=metal+' = ' + price + ' Rs/kg'
        else:
            data = soup.findAll("div", {"class": "FL brdr PR20 rd_13"})
            price = data[0].find('span').string

            if metal=='gold':
                arr.append(price)
                MetalPrice['gold'] = 'Gold = '+price+' Rs/10 gram'
            else:
                arr.append(price)
                MetalPrice[metal]=metal+' = ' + price + ' Rs/kg'
        print(MetalPrice[metal])
    createDB()
    dataEntry(arr)
    print("Database updated!")
    #plotGraph()
    c.close()
    conn.close()


getthePrice()
