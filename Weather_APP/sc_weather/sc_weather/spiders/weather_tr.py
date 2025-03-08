import scrapy
import psycopg2
import requests



class WeatherSpiderSpider(scrapy.Spider):
    name = 'tr'
    allowed_domains = ['tr.wikipedia.org']
    start_urls = ['https://tr.wikipedia.org/wiki/T%C3%BCrkiye%27deki_illerin_n%C3%BCfuslar%C4%B1_(2020)']
    
    
    def parse(self, response):
        
        conn = psycopg2.connect("dbname=weather_db user=postgres password=1")
        cur = conn.cursor()
        print(50*"*")
        tr_list = []
        tr_all= []
        
        apiKEy = '949f9ab1c7be6cef75d007c1da6c9b5c'
        
        for i in range(2,83):
            city_tr       = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[{i}]/td[1]/a/text()').get()
            population_tr = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[{i}]/td[2]/text()').get()
            state_tr      = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[{i}]/td[3]/a/text()').get()
            
        
            # //*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[7]/td[1]/a
            # //*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[7]/td[2]
            # //*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[7]/td[3]
           
            
            if state_tr != None:
                state_tr      = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[{i}]/td[3]/a/text()').get()
            else:
                state_tr      = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[{i}]/td[3]/text()').get()
                
            tr_list.append(city_tr)
            tr_list.append(population_tr)
            tr_list.append(state_tr)
            tr_list.append("tr")
            ct = "tr"
            
            
            
            state_tr = state_tr.replace(" Bölgesi","")
            
            if city_tr == 'Gümüşane':
                city_tr = 'Gümüşhane'
            # cur.execute(f"insert into city_table (city,population,region,country) values ('{city_tr.title()}' ,'{int(population_tr)}','{state_tr}','tr')") 
            
            # conn.commit()
            
            # url1=f'https://api.openweathermap.org/data/2.5/weather?q={city_tr}&lang=en&appid={apiKEy}'
                
            # response1 = requests.get(url1)
            # hava=response1.json()
            # # print(hava['name'])
            # # print(hava['main']['temp'])
            # # print(hava['weather'][0]['description'])
            # # hava['weather'][0]['icon']
            
            # img_url = f"http://openweathermap.org/img/wn/{hava['weather'][0]['icon']}@2x.png"
            
            # cur.execute(f"select city_id from city_table where city = '{city_tr.title()}'")
            
            # c_id = cur.fetchone()
            
            # cur.execute(f"insert into weather_table (city_id,temp,cloud,img_url) values ('{c_id[0]}' ,'{hava['main']['temp']}','{hava['weather'][0]['description']}','{hava['weather'][0]['icon']}')") 
            
            # conn.commit()
            
            yield{
                "city" : city_tr,
                "population" : population_tr,
                "region": state_tr,
                "country" : ct
                
            }
            
            
            
            
            
            
            tr_all.append(tr_list)
            tr_list = []
        print(tr_all)
        print(len(tr_all))
        
        

        # for i in tr_all:
        #     i[2] = i[2].replace(" Bölgesi","")
            
        #     if i[0] == 'Gümüşane':
        #         i[0] = 'Gümüşhane'
        #     cur.execute(f"insert into city_table (city,population,region,country) values ('{i[0].title()}' ,'{int(i[1])}','{i[2]}','{i[3]}')") 
            
        #     conn.commit()
            
        #     url=f'https://api.openweathermap.org/data/2.5/weather?q={i[0]}&lang=en&appid={apiKEy}'
                
        #     response = requests.get(url)
        #     hava=response.json()
        #     # print(hava['name'])
        #     # print(hava['main']['temp'])
        #     # print(hava['weather'][0]['description'])
        #     # hava['weather'][0]['icon']
            
        #     img_url = f"http://openweathermap.org/img/wn/{hava['weather'][0]['icon']}@2x.png"
            
        #     cur.execute(f"select city_id from city_table where city = '{i[0].title()}'")
            
        #     c_id = cur.fetchone()
            
        #     cur.execute(f"insert into weather_table (city_id,temp,cloud,img_u.
        # rl) values ('{c_id[0]}' ,'{hava['main']['temp']}','{hava['weather'][0]['description']}','{hava['weather'][0]['icon']}')") 
            
        #     conn.commit()
            
            
        cur.close()
        conn.close()
        
