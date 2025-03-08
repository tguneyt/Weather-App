import scrapy
import psycopg2
import requests

class WeatherSpiderSpider(scrapy.Spider):

# //*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[1]/th/table/tbody/tr/td[2]/a
# //*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[18]/th/table/tbody/tr/td[2]/a

    name = 'nl'
    allowed_domains = ['tr.wikipedia.org']
    start_urls = ['https://tr.wikipedia.org/wiki/Hollanda%27daki_%C5%9Fehirler_listesi']
    
    def parse(self, response):
        print(50*"*")
        nederland_list = []
        nederlands= []
        conn = psycopg2.connect("dbname=weather_db user=postgres password=1")
        cur = conn.cursor()
        apiKEy = '949f9ab1c7be6cef75d007c1da6c9b5c'
        
        for i in range(1,68):           
            city_nl = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table/tbody/tr[{i}]/td[2]/a/text()').get()
            population_nl = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table/tbody/tr[{i}]/td[6]/text()').get()
            state_nl = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table/tbody/tr[{i}]/td[7]/a/text()').get()
            if state_nl != None:
                state_nl = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table/tbody/tr[{i}]/td[7]/a/text()').get()
            else:
                state_nl = response.xpath(f'//*[@id="mw-content-text"]/div[1]/table/tbody/tr[{i}]/td[7]/text()').get()

            if city_nl != None:
                population_nl=population_nl.replace(".","")
                state_nl=state_nl.replace("\n","")
                if state_nl == "Kuzey Brabant":
                    state_nl =  "Noord Brabant"
                elif state_nl == "Kuzey Hollanda":
                    state_nl = "Noord Holland" 
                elif state_nl == "Güney Hollanda":
                    state_nl = "Zuid Holland" 
                if city_nl == "'s-Hertogenbosch":
                    city_nl="s-Hertogenbosch"    
                
                            
            nederland_list.append(city_nl)
            nederland_list.append(population_nl)
            nederland_list.append(state_nl)
            nederland_list.append("nl")
            ct = "nl"
            dic_ct={}
            
            yield{
                "city" : city_nl,
                "population" : population_nl,
                "region": state_nl,
                "country" : ct
                
            }
            
            
            
            
            if city_nl != None:
                population_nl=population_nl.replace(".","")
                state_nl=state_nl.replace("\n","")
                
                if state_nl == "Kuzey Brabant":
                    state_nl =  "Noord Brabant"
                elif state_nl == "Kuzey Hollanda":
                    state_nl = "Noord Holland" 
                elif state_nl == "Güney Hollanda":
                    state_nl = "Zuid Holland" 
                    
                if city_nl == "'s-Hertogenbosch":
                    city_nl="s-Hertogenbosch"
                    cur.execute(f"insert into city_table (city,population,region,country) values ('{city_nl.title()}' ,'{int(population_nl)}','{state_nl}','{ct}')") 
                else:    
                    cur.execute(f"insert into city_table (city,population,region,country) values ('{city_nl.title()}' ,'{int(population_nl)}','{state_nl}','{ct}')") 
                
                conn.commit()
                if city_nl == "s-Hertogenbosch":
                    sh = "Hertogenbosch"
                    url1=f'https://api.openweathermap.org/data/2.5/weather?q={sh}&lang=en&appid={apiKEy}'
                else:
                    url1=f'https://api.openweathermap.org/data/2.5/weather?q={city_nl}&lang=en&appid={apiKEy}'
                    
                response1 = requests.get(url1)
                hava=response1.json()
                # print(hava['name'])
                # print(hava['main']['temp'])
                # print(hava['weather'][0]['description'])
                # hava['weather'][0]['icon']
                img_url = f"http://openweathermap.org/img/wn/{hava['weather'][0]['icon']}@2x.png"
                
                cur.execute(f"select city_id from city_table where city = '{city_nl.title()}'")
                
                c_id = cur.fetchone()
                
                cur.execute(f"insert into weather_table (city_id,temp,cloud,img_url) values ('{c_id[0]}' ,'{hava['main']['temp']}','{hava['weather'][0]['description']}','{hava['weather'][0]['icon']}')") 
                
                conn.commit()
            
            
            
            
            
            
            nederlands.append(nederland_list)
            nederland_list = []
            
        nederlands.pop(0)
        print(nederlands)
        
        
        
        
        # # # for i in nederlands:
        # # #     i[1]=i[1].replace(".","")
        # # #     i[2]=i[2].replace("\n","")
        # # #     if i[2] == "Kuzey Brabant":
        # # #         i[2] =  "Noord Brabant"
        # # #     elif i[2] == "Kuzey Hollanda":
        # # #         i[2] = "Noord Holland" 
        # # #     elif i[2] == "Güney Hollanda":
        # # #         i[2] = "Zuid Holland" 
                
        # # #     if i[0] == "'s-Hertogenbosch":
        # # #         i[0]="s-Hertogenbosch"
        # # #         cur.execute(f"insert into city_table (city,population,region,country) values ('{i[0].title()}' ,'{i[1]}','{i[2]}','{i[3]}')") 
        # # #     else:    
        # # #         cur.execute(f"insert into city_table (city,population,region,country) values ('{i[0].title()}' ,'{i[1]}','{i[2]}','{i[3]}')") 
            
        # # #     conn.commit()
        # # #     if i[0] == "s-Hertogenbosch":
        # # #         sh = "Hertogenbosch"
        # # #         url=f'https://api.openweathermap.org/data/2.5/weather?q={sh}&lang=en&appid={apiKEy}'
        # # #     else:
        # # #         url=f'https://api.openweathermap.org/data/2.5/weather?q={i[0]}&lang=en&appid={apiKEy}'
                
        # # #     response = requests.get(url)
        # # #     hava=response.json()
        # # #     # print(hava['name'])
        # # #     # print(hava['main']['temp'])
        # # #     # print(hava['weather'][0]['description'])
        # # #     # hava['weather'][0]['icon']
        # # #     img_url = f"http://openweathermap.org/img/wn/{hava['weather'][0]['icon']}@2x.png"
            
        # # #     cur.execute(f"select city_id from city_table where city = '{i[0].title()}'")
            
        # # #     c_id = cur.fetchone()
            
        # # #     cur.execute(f"insert into weather_table (city_id,temp,cloud,img_url) values ('{c_id[0]}' ,'{hava['main']['temp']}','{hava['weather'][0]['description']}','{hava['weather'][0]['icon']}')") 
            
        # # #     conn.commit()
        
        # conn.commit()
        cur.close()
        conn.close()
        print(nederlands)
