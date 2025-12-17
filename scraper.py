import requests
import csv
from bs4 import BeautifulSoup

# def scrape():

#     url =  'https://www.cargurus.com/Cars/l-Used-BMW-M3-d390'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     print(soup)

#     title = soup.select_one('h1').text
#     text = soup.select_one('p').text
#     link = soup.select_one('a').get('href')

#     print(title)
#     print(text)
#     print(link)


# if __name__ == '__main__':
#     scrape()






# - Year/Model tag: `h4`
# - Year/Model class: `_1p-k0 _-3wke _title_omo0s_1 _truncate_omo0s_12`
# - Price tag: `h4`
# - Price class: `_1p-k0 tPVlJ _priceText_15az9_97`

# firstCar = soup.find('h4')
# print(firstCar.text)

url = "https://www.cargurus.com/Cars/l-Used-BMW-M3-d390"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

allCars = soup.find_all('h4')


with open('listings.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(['Year and Model'])

    for car in allCars:
        text = car.text.strip()  
        if text[0:4].isdigit():  
            writer.writerow([text])


    writer.writerow(['Price'])

    for car in allCars:
        text = car.text.strip()
        if "$" in text and text[1].isdigit():
            writer.writerow([text])
    
print("Grabbed Listings!")


