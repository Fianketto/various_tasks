import requests
from bs4 import BeautifulSoup as bs


url = 'https://yandex.ru/search/?text=пробки в москве'
resp = requests.get(url)



soup = bs(resp.text, 'lxml')
html_c = soup.find('html')

div = html_c.find('div', {'class': 'traffic-summary'})
traffic_level = div.find('a').text
traffic_description = div.find('div', {'class': 'traffic-summary__status'}).text


print(traffic_level)
print(traffic_description)






