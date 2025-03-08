from calendar import c
import sys
from turtle import Screen
import psycopg2
import hashlib
from soupsieve import select
from urllib import response
import requests
from sympy import false
from mainscreen import Ui_MainWindow

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from decimal import Decimal, ROUND_HALF_UP


class Main_Class(QMainWindow):
    def __init__(self):
        super(Main_Class,self).__init__()
        self.mainscreen = Ui_MainWindow()
        self.mainscreen.setupUi(self) # login ekranı ui 
        self.CityInfo()
        self.mainscreen.btn_usa.clicked.connect(self.USACity)
        self.mainscreen.btn_nl.clicked.connect(self.NLCity)
        self.mainscreen.btn_tr.clicked.connect(self.TRCity)
        self.mainscreen.btn_weather.clicked.connect(self.Search)
        self.mainscreen.tableWidget.clicked.connect(self.Click_table)
        self.mainscreen.pushButton_2.clicked.connect(self.Quit)

    def CityInfo(self):
        
        conn = psycopg2.connect("dbname=weather_db user=postgres password=mertemir")
        cur = conn.cursor()

        cur.execute("select count(*) from city_table where country = 'nl'")
        len_db =cur.fetchone()
        
        cur.execute("select city,region,population from city_table where country = 'nl' order by population desc")
        c_list = cur.fetchall()
        
        
                
        self.mainscreen.tableWidget.setRowCount(len_db[0])
        self.mainscreen.tableWidget.setColumnCount(4)
        # self.mainscreen.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.mainscreen.tableWidget.setHorizontalHeaderLabels(("","City","Region","Population"))
        self.mainscreen.tableWidget.verticalHeader().setHidden(True)
        self.mainscreen.tableWidget.setColumnWidth(0,7)
        self.mainscreen.tableWidget.setColumnWidth(1,178)
        self.mainscreen.tableWidget.setColumnWidth(2,147)
        self.mainscreen.tableWidget.setColumnWidth(3,72)
        
        for i in range(len(c_list)):
            for j in range(4):   
                if j==0:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(i+1)))
                else:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(c_list[i][j-1])))

        self.mainscreen.txt_total.setText(str(len_db[0]))
        
        
    def NLCity(self):
        conn = psycopg2.connect("dbname=weather_db user=postgres password=mertemir")
        cur = conn.cursor()

        cur.execute("select count(*) from city_table where country = 'nl'")
        len_db =cur.fetchone()
        
        cur.execute("select city,region,population from city_table where country = 'nl' order by population desc")
        c_list = cur.fetchall()
        
        
                
        self.mainscreen.tableWidget.setRowCount(len_db[0])
        self.mainscreen.tableWidget.setColumnCount(4)
        # self.mainscreen.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.mainscreen.tableWidget.setHorizontalHeaderLabels(("","City","Region","Population"))
        self.mainscreen.tableWidget.verticalHeader().setHidden(True)
        self.mainscreen.tableWidget.setColumnWidth(0,7)
        self.mainscreen.tableWidget.setColumnWidth(1,178)
        self.mainscreen.tableWidget.setColumnWidth(2,147)
        self.mainscreen.tableWidget.setColumnWidth(3,72)
        
        for i in range(len(c_list)):
            for j in range(4):   
                if j==0:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(i+1)))
                else:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(c_list[i][j-1])))

        self.mainscreen.txt_total.setText(str(len_db[0]))
   
    
    def USACity(self):

        conn = psycopg2.connect("dbname=weather_db user=postgres password=mertemir")
        cur = conn.cursor()

        cur.execute("select count(*) from city_table where country = 'usa'")
        len_db =cur.fetchone()
        
        cur.execute("select city,region,population from city_table where country = 'usa' order by population desc")
        c_list = cur.fetchall()
        
        
                
        self.mainscreen.tableWidget.setRowCount(len_db[0])
        self.mainscreen.tableWidget.setColumnCount(4)
        # self.mainscreen.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.mainscreen.tableWidget.setHorizontalHeaderLabels(("","City","Region","Population"))
        self.mainscreen.tableWidget.verticalHeader().setHidden(True)
        self.mainscreen.tableWidget.setColumnWidth(0,7)
        self.mainscreen.tableWidget.setColumnWidth(1,178)
        self.mainscreen.tableWidget.setColumnWidth(2,147)
        self.mainscreen.tableWidget.setColumnWidth(3,72)
        
        for i in range(len(c_list)):
            for j in range(4):   
                if j==0:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(i+1)))
                else:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(c_list[i][j-1])))

        self.mainscreen.txt_total.setText(str(len_db[0]))
        
    
    def TRCity(self):
        conn = psycopg2.connect("dbname=weather_db user=postgres password=mertemir")
        cur = conn.cursor()

        cur.execute("select count(*) from city_table where country = 'tr'")
        len_db =cur.fetchone()
        
        cur.execute("select city,region,population from city_table where country = 'tr'")
        c_list = cur.fetchall()
                
        self.mainscreen.tableWidget.setRowCount(len_db[0])
        self.mainscreen.tableWidget.setColumnCount(4)
        # self.mainscreen.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.mainscreen.tableWidget.setHorizontalHeaderLabels(("","City","Region","Population"))
        self.mainscreen.tableWidget.verticalHeader().setHidden(True)
        self.mainscreen.tableWidget.setColumnWidth(0,7)
        self.mainscreen.tableWidget.setColumnWidth(1,125)
        self.mainscreen.tableWidget.setColumnWidth(2,200)
        self.mainscreen.tableWidget.setColumnWidth(3,72)
        
        for i in range(len(c_list)):
            for j in range(4):   
                if j==0:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(i+1)))
                else:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(c_list[i][j-1])))

        self.mainscreen.txt_total.setText(str(len_db[0]))
    def Click_table(self):
        for item in self.mainscreen.tableWidget.selectedItems():
            self.table_item = item.text()
        
        apiKEy = 'd0ad6e23d2c345f299b112647221405'
        url='http://api.weatherapi.com/v1/current.json'

        sehir = self.table_item # str değer dönüyor
        response = requests.get(url,params={
            'key': apiKEy,
            'q': sehir,
            'lang': 'tr'   
        })

        print(response)
        conn = psycopg2.connect("dbname=weather_db user=postgres password=mertemir")
        cur = conn.cursor()
        
        cur.execute(f"select country from city_table where city = '{sehir.title()}'")       
        c_list = cur.fetchone()
 
        if c_list == None:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.messagebox=QtWidgets.QMessageBox()
            self.messagebox.critical(self,'WARNING','Please Click City')
            self.messagebox.setWindowIcon(icon)
        else:   
            country = c_list[0]
            country_city = sehir.title()+"/"+country.upper()
            
            hava = response.json()
            print(hava)
            self.mainscreen.txt_city.setText(str(hava['location']['name']))
            self.mainscreen.txt_celcius.setText(str(hava['current']['temp_c']))
            self.mainscreen.txt_cloud.setText(str(hava['current']['cloud']))
            self.mainscreen.txt_country_city.setText(str(country_city))

            cur.execute(f"select region from city_table where city = '{sehir.title()}'")
            region = cur.fetchone()
            region_screen = region[0]
            self.mainscreen.txt_province.setText(str(region_screen))
            #self.mainscreen.txt_province.setText(str(hava['location']['region'])) her zaman doğru değer dönmüyor

            cur.execute(f"select population from city_table where city = '{sehir.title()}'")
            population = cur.fetchone() # tuple döner
            population_scr = population[0] # tuple ın sıfırıncı indeksi
            population_screen = "{pop_scr:,}".format(pop_scr=population_scr).replace(",", ".") # nüfusu nokta ile ayırma
            self.mainscreen.txt_population.setText(str(population_screen))
            
            cur.close()
            conn.commit()
            conn.close()

            fahr = (hava['current']['temp_c'] * 1.8) + 32
            fahr = round(fahr, 4)
            print(fahr)
            self.mainscreen.txt_fahr.setText(str(fahr))

        
    def Search(self):

        self.city_search = self.mainscreen.edt_search.text()
        
        apiKEy = 'd0ad6e23d2c345f299b112647221405'
        #apiKEy = '949f9ab1c7be6cef75d007c1da6c9b5c'
        url='http://api.weatherapi.com/v1/current.json'
        # url=f'https://api.openweathermap.org/data/2.5/weather?lat=35&lon=139&appid={apiKEy}'
        sehir = self.city_search

        response = requests.get(url,params={
            'key': apiKEy,
            'q': sehir,
            'lang': 'tr'
        })
        
        # response = requests.get(url)

        print(response)
        conn = psycopg2.connect("dbname=weather_db user=postgres password=mertemir")
        cur = conn.cursor()

        cur.execute(f"select country from city_table where city = '{sehir.title()}'")
        c_list = cur.fetchone()
                     
        if c_list == None:
            if sehir[0] == "i" or sehir[0] == "İ":
                sehir= "İ" +sehir[1:len(sehir)]
                print(sehir)
                cur.execute(f"select country from city_table where city = '{sehir.title()}'")
                c_list = cur.fetchone()
                if c_list == None:
                    city = sehir[0]
                    for x in sehir[1:len(sehir)]:
                        if x == "İ":
                            x = "i"
                        city += x
                    sehir = city
                    cur.execute(f"select country from city_table where city = '{sehir.title()}'")
                    c_list = cur.fetchone()

        country = c_list[0]

        country_city = sehir.title()+"/"+country.upper()
        
        hava = response.json()
        print(hava)
        self.mainscreen.txt_city.setText(sehir)
        try :
            self.mainscreen.txt_city.setText(str(hava['location']['name']))
            self.mainscreen.txt_celcius.setText(str(hava['current']['temp_c']))
            self.mainscreen.txt_cloud.setText(str(hava['current']['cloud']))
            fahr = (hava['current']['temp_c'] * 1.8) + 32
            fahr = round(fahr, 4)
            self.mainscreen.txt_fahr.setText(str(fahr))
        except:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.messagebox=QtWidgets.QMessageBox()
            self.messagebox.critical(self,'WARNING','Please Enter Available City!!!')
            self.messagebox.setWindowIcon(icon)
        self.mainscreen.txt_country_city.setText(str(country_city))

        cur.execute(f"select region from city_table where city = '{sehir.title()}'")
        region = cur.fetchone()
        region_screen = region[0]
        self.mainscreen.txt_province.setText(str(region_screen))
        #self.mainscreen.txt_province.setText(str(hava['location']['region'])) her zaman doğru değer dönmüyor

        cur.execute(f"select population from city_table where city = '{sehir.title()}'")
        population = cur.fetchone() # tuple döner
        population_scr = population[0] # tuple ın sıfırıncı indeksi
        population_screen = "{pop_scr:,}".format(pop_scr=population_scr).replace(",", ".") # nüfusu nokta ile ayırma
        self.mainscreen.txt_population.setText(str(population_screen))
        
        cur.close()
        conn.commit()
        conn.close()


        # print(hava)
        # print(hava['location']['name'])
        # print(hava['current']['temp_c'])
        # print(hava['current']['cloud'])
      
        if country == "nl":
            self.NLCity()
        elif country == "tr":
            self.TRCity()
        else:
            self.USACity()
    
    def Quit(self):
        sys.exit(app.exec())
        
app = QApplication(sys.argv)
mainwindow = Main_Class()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle("WEATHER")
icon = QtGui.QIcon()
# icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
widget.setWindowIcon(icon)
widget.setFixedHeight(850)
widget.setFixedWidth(900)
widget.show()
sys.exit(app.exec())