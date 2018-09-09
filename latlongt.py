import csv
import requests

list = []
    
with open("store.csv",encoding='cp949') as f:
    wf = open("storelocation.csv", "w")
    rows = csv.reader(f)
    for line in rows:
        list.append(line)
    for s in list:
        print(s[2])
        URL = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=ko&address={}'.format(s[2])
        response = requests.get(URL)
        
        data = response.json()
        
        # lat, longt 추출
        lat = data['results'][0]['geometry']['location']['lat']
        longt = data['results'][0]['geometry']['location']['lng']
        
        print("lat = ", lat , " longt = " , longt)
        wf.write(s[0] + "," + s[1] + "," + str(lat) + "," + str(longt) + "\n")
