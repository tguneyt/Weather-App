import scrapy
from ..items import ScWeatherItem
import psycopg2
import requests
class WeatherSpiderSpider(scrapy.Spider):
    name = 'usa'
    allowed_domains = ['tr.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population']
    
    def parse(self, response):
        print(50*"*")
        usa_list = []
        usa_all= []   
        conn = psycopg2.connect("dbname=weather_db user=postgres password=4408")
        cur = conn.cursor()
        
        
        
        for i in range(1,327):
            
            city_usa = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[5]/tbody/tr[{i}]/td[1]/i/a/text()').get()
            
            if city_usa != None:
                city_usa = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[5]/tbody/tr[{i}]/td[1]/i/a/text()').get()
            
            else:
                city_usa = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[5]/tbody/tr[{i}]/td[1]/a/text()').get()
                
                if city_usa == None:
                    city_usa = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[5]/tbody/tr[{i}]/td[1]/b/a/text()').get()
                    
                    if city_usa == None:
                        city_usa = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[5]/tbody/tr[{i}]/td[1]/i/b/a/text()').get()
                        
                        if city_usa == None:
                            city_usa = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[5]/tbody/tr[{i}]/td[1]/b/a/i/text()').get()                        
                            
            ######################################################################
            state_usa = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[5]/tbody/tr[{i}]/td[2]/a/text()').get()
            #######################################################################
            population_usa = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[5]/tbody/tr[{i}]/td[3]/text()').get()
            
            usa_list.append(city_usa)
            usa_list.append(population_usa)
            usa_list.append(state_usa)
            usa_list.append("usa")
            ct = "usa"
            
            if city_usa != None:
                population_usa=str(population_usa).replace(",","")
                population_usa=str(population_usa).replace("\n","")
                # print(i[0], "   ",i[1])

                if city_usa=="Winston–Salem":
                    city_usa="Winston-Salem"
                if city_usa=="Lee's Summit":
                    city_usa="Summit"
            
                yield{
                    "city" : city_usa,
                    "population" : population_usa,
                    "region": state_usa,
                    "country" : ct
                    
                }
                # cur.execute(f"insert into city_table (city,population,region,country) values(%s,%s,%s,%s);", (city_usa.title() ,int(population_usa) ,state_usa.title(),ct))
                # #cur.execute(f"insert into city_table (city,population,region,country) values({i[0].title()} ,{int(i[1])} ,{i[2].title()},{i[3]})")
                
                # conn.commit()
                # apiKEy = '949f9ab1c7be6cef75d007c1da6c9b5c'
                # url1=f'https://api.openweathermap.org/data/2.5/weather?q={city_usa}&lang=en&appid={apiKEy}'
                    
                # response1 = requests.get(url1)
                # hava=response1.json()
                # # print(hava['name'])
                # # print(hava['main']['temp'])
                # # print(hava['weather'][0]['description'])
                # # hava['weather'][0]['icon']
                
                # img_url = f"http://openweathermap.org/img/wn/{hava['weather'][0]['icon']}@2x.png"
                
                # cur.execute(f"select city_id from city_table where city = '{city_usa.title()}'")
                
                # c_id = cur.fetchone()
                
                # cur.execute(f"insert into weather_table (city_id,temp,cloud,img_url) values ('{c_id[0]}' ,'{hava['main']['temp']}','{hava['weather'][0]['description']}','{hava['weather'][0]['icon']}')") 
                
                # conn.commit()

            
        #     usa_all.append(usa_list)
        #     usa_list = []
        # usa_all.pop(0)
       
        

        # # # for i in usa_all:
        # #     # i[1]=i[1].replace(",","")
        # #     # i[1]=i[1].replace("/n","")
        # #     # # print(i[0], "   ",i[1])
            
        # #     # if i[0]=="Winston–Salem":
        # #     #     i[0]="Winston-Salem"
        # #     # if i[0]=="Lee's Summit":
        # #     #     i[0]="Summit"
        # #     # cur.execute(f"insert into city_table (city,population,region,country) values(%s,%s,%s,%s);", (i[0].title() ,int(i[1]) ,i[2].title(),i[3]))
        # #     # #cur.execute(f"insert into city_table (city,population,region,country) values({i[0].title()} ,{int(i[1])} ,{i[2].title()},{i[3]})")
            
        # #     # conn.commit()
        # #     # apiKEy = '949f9ab1c7be6cef75d007c1da6c9b5c'
        # #     # url1=f'https://api.openweathermap.org/data/2.5/weather?q={i[0]}&lang=en&appid={apiKEy}'
                
        # #     # response1 = requests.get(url1)
        # #     # hava=response1.json()
        # #     # # print(hava['name'])
        # #     # # print(hava['main']['temp'])
        # #     # # print(hava['weather'][0]['description'])
        # #     # # hava['weather'][0]['icon']
            
        # #     # img_url = f"http://openweathermap.org/img/wn/{hava['weather'][0]['icon']}@2x.png"
            
        # #     # cur.execute(f"select city_id from city_table where city = '{i[0].title()}'")
            
        # #     # c_id = cur.fetchone()
            
        # #     # cur.execute(f"insert into weather_table (city_id,temp,cloud,img_url) values ('{c_id[0]}' ,'{hava['main']['temp']}','{hava['weather'][0]['description']}','{hava['weather'][0]['icon']}')") 
            
        # #     # conn.commit()
            
            
        cur.close()
        conn.close()
  


        
        print(usa_all)
        