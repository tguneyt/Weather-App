from calendar import c
import sys

import psycopg2
import hashlib
from soupsieve import select
from urllib import response
from urllib.request import urlopen
import urllib
import requests
from sympy import false
from mainscreen import Ui_MainWindow
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw
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
        self.btn_country = 'nl'
        self.city_search = None
        self.CityInfo()
        self.mainscreen.btn_usa.clicked.connect(self.USACity)
        self.mainscreen.btn_nl.clicked.connect(self.NLCity)
        self.mainscreen.btn_tr.clicked.connect(self.TRCity)
        self.mainscreen.btn_weather.clicked.connect(self.Search)
        self.mainscreen.tableWidget.clicked.connect(self.Click_table)
        self.mainscreen.pushButton_2.clicked.connect(self.Quit)
        self.FirstLog()
        self.deneme()
        
        
        
        
# /////////////////////////////////////////////////////////////////////////////////////////////////////////
    #     self.mainscreen.edt_search.textChanged.connect(self.TextChange)
        
        

    # def TextChange(self):
        
    #     text = self.mainscreen.edt_search.text()
    #     self.mainscreen.txt_city.setText(text)
        
    #     pass   
        
        
        
        
        
        
        
        
        
        
        
        
# ///////////////////////////////////////////////////////////////////////////////////////////////////////// 















    def FirstLog(self):
        
        
        
        
        self.mainscreen.centralwidget.setStyleSheet("#centralwidget{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 208, 0, 255), stop:1 rgba(68, 255, 16, 255));\n"
"\nborder-image: url(:/icons/wp_nl.png) 0 0 0 0 stretch stretch;\nborder-width: 0px;"
"}")
        apiKEy = '949f9ab1c7be6cef75d007c1da6c9b5c'
        url=f'https://api.openweathermap.org/data/2.5/weather?q={"Amsterdam"}&lang=en&appid={apiKEy}'
        try:
            response = requests.get(url)
            # print(response)
            hava = response.json()
            cel_kel = round(hava['main']['temp']-273.15, 1)
            cloud_f = hava['weather'][0]['description']
            self.iconid = hava['weather'][0]['icon']
            img_url = f'http://openweathermap.org/img/wn/{self.iconid}@4x.png'
        except:
            conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
            cur = conn.cursor()
            cur.execute(f"select temp,cloud,img_url from weather_table where city_id = (select city_id from city_table where city = 'Amsterdam')")
            ams_temp = cur.fetchall()
            
            
            c = float(ams_temp[0][0])
            cel_kel = round(c-273.15, 1)
            cloud_f = ams_temp[0][1]
            img_url = f'http://openweathermap.org/img/wn/{ams_temp[0][2]}@4x.png'
            
            
        fahr = ((cel_kel) * 1.8) + 32
        fahr = round(fahr, 1)
        
        self.mainscreen.txt_fahr.setText(str(fahr))
        self.mainscreen.txt_celcius.setText(str(cel_kel))
        self.mainscreen.txt_cloud.setText(str(cloud_f.title()))
        self.mainscreen.txt_country_city.setText(str("Amsterdam/NL"))
        
        conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
        cur = conn.cursor()
        cur.execute(f"select region, population from city_table where city = 'Amsterdam'")
        amst = cur.fetchone()
        
        self.mainscreen.txt_city.setText("Amsterdam")
        self.mainscreen.txt_province.setText(amst[0])
        # TODO icon degistir
        # x= "http://openweathermap.org/img/wn/10d@2x.png"
        
        try:
            self.pixmap = QPixmap()
            request = requests.get(img_url)
            self.pixmap.loadFromData(request.content)
            self.mainscreen.label_cloud_icon.setPixmap(self.pixmap)
            self.mainscreen.label_cloud_icon.setGeometry(QtCore.QRect(630, 440, 80, 80))
            self.mainscreen.label_cloud_icon.setScaledContents(True)
            population_scr = amst[1] # tuple ın birinci indeksi
            population_screen = "{pop_scr:,}".format(pop_scr=population_scr).replace(",", ".") # nüfusu nokta ile ayırma
            self.mainscreen.txt_population.setText(str(population_screen))
        except:
            population_scr = amst[1] # tuple ın birinci indeksi
            population_screen = "{pop_scr:,}".format(pop_scr=population_scr).replace(",", ".") # nüfusu nokta ile ayırma
            self.mainscreen.txt_population.setText(str(population_screen))
        
     
        
    def CityInfo(self):
        
        conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
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
        self.mainscreen.tableWidget.setColumnWidth(1,190)
        self.mainscreen.tableWidget.setColumnWidth(2,147)
        self.mainscreen.tableWidget.setColumnWidth(3,80)
        
        stylesheet = "::section{Background-color:rgb(190,1,1)}"
        self.mainscreen.tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        
        for i in range(len(c_list)):
            for j in range(4):   
                if j==0:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(i+1)))
                else:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(c_list[i][j-1])))
                    
                    
                    #TODO satir arka plan boya
                    # if i[0] == self.user: # kullanıcın arka planın boya
                    #     for k in range(3):
                    #         self.stat_screen.stat_table_suc.item(i,k).setBackground(QtGui.QColor(205,255,0))
                    
                    
                    
        self.mainscreen.txt_total.setText(str(len_db[0]))
        

    def NLCity(self):
        self.btn_country='nl'
        self.mainscreen.centralwidget.setStyleSheet("#centralwidget{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 208, 0, 255), stop:1 rgba(68, 255, 16, 255));\n"
"\nborder-image: url(:/icons/wp_nl.png) 0 0 0 0 stretch stretch;\nborder-width: 0px;"
"}")
        self.mainscreen.btn_usa.setStyleSheet("\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 170, 0, 255), stop:1 rgba(255, 209, 93, 255));\n"
"border: none")
        self.mainscreen.btn_tr.setStyleSheet("\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 170, 0, 255), stop:1 rgba(255, 209, 93, 255));\n"
"border: none")
        
        
        self.mainscreen.btn_nl.setStyleSheet("\n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.734, fx:0.5, fy:0.516304, stop:0 rgba(132, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: none")
        conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
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
        self.mainscreen.tableWidget.setColumnWidth(1,190)
        self.mainscreen.tableWidget.setColumnWidth(2,147)
        self.mainscreen.tableWidget.setColumnWidth(3,80)
        
        stylesheet = "::section{Background-color:rgb(190,1,1)}"
        self.mainscreen.tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        
        for i in range(len(c_list)):
            for j in range(4):   
                if j==0:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(i+1)))
                else:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(c_list[i][j-1])))

        self.mainscreen.txt_total.setText(str(len_db[0]))
   
    
    def USACity(self):
        self.btn_country='usa'
        self.mainscreen.centralwidget.setStyleSheet("#centralwidget{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 208, 0, 255), stop:1 rgba(68, 255, 16, 255));\n"
"\nborder-image: url(:/icons/wp_usa.png) 0 0 0 0 stretch stretch;\nborder-width: 0px;"
"}")
        self.mainscreen.btn_nl.setStyleSheet("\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 170, 0, 255), stop:1 rgba(255, 209, 93, 255));\n"
"border: none")
        self.mainscreen.btn_tr.setStyleSheet("\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 170, 0, 255), stop:1 rgba(255, 209, 93, 255));\n"
"border: none")
        
        self.mainscreen.btn_usa.setStyleSheet("\n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.734, fx:0.5, fy:0.516304, stop:0 rgba(132, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: none")
        
        conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
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
        self.mainscreen.tableWidget.setColumnWidth(1,190)
        self.mainscreen.tableWidget.setColumnWidth(2,147)
        self.mainscreen.tableWidget.setColumnWidth(3,80)
        
        stylesheet = "::section{Background-color:rgb(190,1,1)}"
        self.mainscreen.tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        
        
        for i in range(len(c_list)):
            for j in range(4):   
                if j==0:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(i+1)))
                else:
                    self.mainscreen.tableWidget.setItem(i,j,QTableWidgetItem(str(c_list[i][j-1])))

        self.mainscreen.txt_total.setText(str(len_db[0]))
        
    
    def TRCity(self):
        self.btn_country='tr'
        self.mainscreen.centralwidget.setStyleSheet("#centralwidget{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 208, 0, 255), stop:1 rgba(68, 255, 16, 255));\n"
"\nborder-image: url(:/icons/wp_tr.png) 0 0 0 0 stretch stretch;\nborder-width: 0px;"
"}")
        self.mainscreen.btn_usa.setStyleSheet("\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 170, 0, 255), stop:1 rgba(255, 209, 93, 255));\n"
"border: none")
        self.mainscreen.btn_nl.setStyleSheet("\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 170, 0, 255), stop:1 rgba(255, 209, 93, 255));\n"
"border: none")
        
        self.mainscreen.btn_tr.setStyleSheet("\n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.734, fx:0.5, fy:0.516304, stop:0 rgba(132, 255, 255, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: none")
        conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
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
        self.mainscreen.tableWidget.setColumnWidth(1,190)
        self.mainscreen.tableWidget.setColumnWidth(2,147)
        self.mainscreen.tableWidget.setColumnWidth(3,80)
        
        stylesheet = "::section{Background-color:rgb(190,1,1)}"
        self.mainscreen.tableWidget.horizontalHeader().setStyleSheet(stylesheet)
        
        
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
            ti= item.row()
        

        x_ti = ti
        
        conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
        cur = conn.cursor()

        cur.execute(f"select city,country from city_table where country = '{self.btn_country}' order by population desc limit {ti+1}")
        item_city = cur.fetchall()
        sehir = item_city[-1][0]
        
        cur.execute(f"select city,country from city_table where country = '{self.btn_country}' order by population desc")
        cityall = cur.fetchall()
        
        
        cur.execute(f"select count(*) from city_table where country = '{self.btn_country}'")
        max_c = cur.fetchone()
        
        apiKEy = '949f9ab1c7be6cef75d007c1da6c9b5c'
        url=f'https://api.openweathermap.org/data/2.5/weather?q={self.table_item}&lang=en&appid={apiKEy}'


        for i in range(max_c[0]-1):
            for k in range(4):
                
                self.mainscreen.tableWidget.item(i,k).setBackground(QtGui.QColor(255, 255, 255, 0))
                
        if x_ti == ti:
            for k in range(4):
                self.mainscreen.tableWidget.item(ti,k).setBackground(QtGui.QColor(255, 170, 0))
       
            
            
        
          
        country = item_city[-1][1]
        country_city = sehir.title()+"/"+country.upper()
        
        try:
            response = requests.get(url)
            hava = response.json()
            cel_kel = round(hava['main']['temp']-273.15, 1)
            self.iconid = hava['weather'][0]['icon']
            cloud_t = hava['weather'][0]['description']
            
            img_url = f'http://openweathermap.org/img/wn/{self.iconid}@2x.png'
                
            self.pixmap = QPixmap()
            request = requests.get(img_url)
            self.pixmap.loadFromData(request.content)
            
            self.mainscreen.label_cloud_icon.setPixmap(self.pixmap)
            
            
            conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
            cur = conn.cursor()
            cur.execute(f"select city_id from city_table where city = '{sehir.title()}'")
            c_id = cur.fetchone()
            
            # cur.execute(f"insert into weather_table (city_id,temp,cloud,img_url) values ('{c_id[0]}' ,'{hava['main']['temp']}','{hava['weather'][0]['description']}','{img_url}")
            cur.execute(f"UPDATE weather_table SET temp={hava['main']['temp']} , cloud='{hava['weather'][0]['description']}' , date = now() , img_url = '{img_url}' WHERE city_id = {c_id[0]}")
            conn.commit()
            
            
        except:
            conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
            cur = conn.cursor()
            cur.execute(f"select temp,cloud,img_url from weather_table where city_id = (select city_id from city_table where city = '{sehir.title()}')")
            db_temp = cur.fetchall()
            
            
            c = float(db_temp[0][0])
            cel_kel = round(c-273.15, 1)
            cloud_t = db_temp[0][1]
            # img_url = f'http://openweathermap.org/img/wn/{db_temp[0][2]}@4x.png'
            im = db_temp[0][2][0]
            img = db_temp[0][2]
            for x in img[1:len(img)]:
                if x == "n":
                    x = "d"
                im += x
            img = im
            self.mainscreen.label_cloud_icon.setPixmap(QtGui.QPixmap(f":/icons/{img}@2x.png"))
            
        
        fahr = ((cel_kel) * 1.8) + 32
        fahr = round(fahr, 1)       
        
        cur.execute(f"select city from city_table where city = '{sehir.title()}'")
        city1 = cur.fetchone()
        city_screen = city1[0]
        self.mainscreen.txt_city.setText(city_screen)

        

        self.mainscreen.txt_celcius.setText(str(cel_kel))
        self.mainscreen.txt_cloud.setText(str(cloud_t.title()))
        self.mainscreen.txt_country_city.setText(str(country_city))
        # x= "http://openweathermap.org/img/wn/10d@2x.png"
        
        # print(hava['weather'][0]['icon'])
        
        
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

        
        self.mainscreen.txt_fahr.setText(str(fahr))

        
    def Search(self):

        self.city_search = self.mainscreen.edt_search.text()
        
        conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
        cur = conn.cursor()
        cur.execute(f"select city from city_table")
        #todo
        all_c = cur.fetchall()
        all_list=[]
        for i in all_c:
            all_list.append(i[0])
            
        if self.city_search not in all_list:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/flash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.messagebox=QtWidgets.QMessageBox()
            self.messagebox.critical(self,'WARNING','Please Enter Available Value')
            self.messagebox.setWindowIcon(icon)
            self.mainscreen.edt_search.setText("")
        else:
                
        
            apiKEy = '949f9ab1c7be6cef75d007c1da6c9b5c'
            url=f'https://api.openweathermap.org/data/2.5/weather?q={self.city_search}&lang=en&appid={apiKEy}'

            sehir = self.city_search

            # response = requests.get(url,params={
            #     'key': apiKEy,
            #     'q': sehir,
            #     'lang': 'tr'
            # })
        

            try:
                response = requests.get(url)
                hava = response.json()
                cel_kel = round(hava['main']['temp']-273.15, 1)
                self.iconid = hava['weather'][0]['icon']
                cloud_t = hava['weather'][0]['description']
                
                img_url = f'http://openweathermap.org/img/wn/{self.iconid}@2x.png'
                    
                self.pixmap = QPixmap()
                request = requests.get(img_url)
                self.pixmap.loadFromData(request.content)
                
                self.mainscreen.label_cloud_icon.setPixmap(self.pixmap)
                
                conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
                cur = conn.cursor()
                cur.execute(f"select city_id from city_table where city = '{sehir.title()}'")
                #todo
                c_id = cur.fetchone()
                
                # cur.execute(f"insert into weather_table (city_id,temp,cloud,img_url) values ('{c_id[0]}' ,'{hava['main']['temp']}','{hava['weather'][0]['description']}','{img_url}")
                cur.execute(f"UPDATE weather_table SET temp={hava['main']['temp']} , cloud='{hava['weather'][0]['description']}' , date = now() , img_url = '{img_url}' WHERE city_id = {c_id[0]}")
                conn.commit()
                

            except:
                conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
                cur = conn.cursor()
                #todo
            
                cur.execute(f"select temp,cloud,img_url from weather_table where city_id = (select city_id from city_table where city = '{sehir.title()}')")
                db_temp = cur.fetchall()
                c = float(db_temp[0][0])
              
                
                cel_kel = round(c-273.15, 1)
                cloud_t = db_temp[0][1]
                img_url = f'http://openweathermap.org/img/wn/{db_temp[0][2]}@4x.png'
                
                # internetsiz durumda resim ekle
                im = db_temp[0][2][0]
                img = db_temp[0][2]
                for x in img[1:len(img)]: # sadece gunduz iconlari ekliyoruz
                    if x == "n":
                        x = "d"
                    im += x
                img = im                 # sadece gunduz iconlari ekliyoruz
                self.mainscreen.label_cloud_icon.setPixmap(QtGui.QPixmap(f":/icons/{img}@2x.png"))



            fahr = ((cel_kel) * 1.8) + 32
            fahr = round(fahr, 1)
                
            
            conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
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
            
            self.mainscreen.txt_city.setText(sehir)
            cur.execute(f"select city from city_table where city = '{sehir.title()}'")
            city1 = cur.fetchone()
            city_screen = city1[0]
            self.mainscreen.txt_city.setText(city_screen)



            self.mainscreen.txt_celcius.setText(str(cel_kel))
            self.mainscreen.txt_cloud.setText(str(cloud_t.title()))
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

            self.mainscreen.txt_fahr.setText(str(fahr))
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

            # cur.execute(f"select city,country from city_table where country = '{self.btn_country}' order by population desc")
            # cityall = cur.fetchall()
            # cur.execute(f"select count(*) from city_table where country = '{self.btn_country}'")
            # max_c = cur.fetchone()
            
            # for i in range(max_c[0]-1):
            #     ct = cityall[i][0]
            #     if ct == self.city_search:
            #         for k in range(4):
            #             self.mainscreen.tableWidget.item(i,k).setBackground(QtGui.QColor(205,255,0))
            #     for k in range(4):
                    
            #         self.mainscreen.tableWidget.item(i,k).setBackground(QtGui.QColor(255, 255, 255, 0))
                    
            # # if x_ti == ti:
            # #     for k in range(4):
            # #         self.mainscreen.tableWidget.item(ti,k).setBackground(QtGui.QColor(205,255,0))
    
    
    def Quit(self):
        sys.exit(app.exec())

    
    def deneme(self):
        
            self.controls = QWidget()  # Controls container widget.
            self.controlsLayout = QVBoxLayout()   # Controls container layout.

            # List of names, widgets are stored in a dictionary by these keys.
            
            conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
            cur = conn.cursor()
            cur.execute(f"select city from city_table")
            db_city = cur.fetchall()
            
            c = db_city[0][0]
            
            widget_names = []
            for i in db_city:

                widget_names.append(i[0])

            
            self.widgets = []

            # Iterate the names, creating a new OnOffWidget for
            # each one, adding it to the layout and
            # and storing a reference in the self.widgets dict
            for name in widget_names:
                item = OnOffWidget(name)
                self.controlsLayout.addWidget(item)
                self.widgets.append(item)

            spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.controlsLayout.addItem(spacer)
            self.controls.setLayout(self.controlsLayout)

            # Scroll Area Properties.
            self.scroll = QScrollArea()
            self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.scroll.setWidgetResizable(True)
            self.scroll.setWidget(self.controls)

            # Search bar.
            # self.mainscreen.edt_search = QLineEdit()
            self.mainscreen.edt_search.textChanged.connect(self.update_display)

            # Adding Completer.
            self.completer = QCompleter(widget_names)
            self.completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.mainscreen.edt_search.setCompleter(self.completer)

            # Add the items to VBoxLayout (applied to container widget)
            # which encompasses the whole window.
            container = QWidget()
            containerLayout = QVBoxLayout()
            containerLayout.addWidget(self.mainscreen.edt_search)
            containerLayout.addWidget(self.scroll)
            
            
            # container.setLayout(containerLayout)
            # container.setGeometry(QtCore.QRect(500, 60, 361, 31))
            # self.setCentralWidget(container)


    def update_display(self, text):

        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                
                widget.show()
            else:
                widget.hide()
        
            

class OnOffWidget(QWidget):

    def __init__(self, name):
        super(OnOffWidget, self).__init__()

        self.name = name
        self.is_on = False

     
app = QApplication(sys.argv)
mainwindow = Main_Class()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setWindowTitle("WEATHER")
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap(":/icons/cloudy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
widget.setWindowIcon(icon)
widget.setFixedHeight(850)
widget.setFixedWidth(900)
widget.show()
sys.exit(app.exec())