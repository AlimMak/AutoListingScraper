from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time

driver = webdriver.Chrome()
all_listings = []

url = "https://www.cargurus.com/Cars/l-Used-BMW-M3-d390"
driver.get(url)
time.sleep(5)

for page_num in range(1, 3):
    print(f"Scraping page {page_num}...")
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    listings = soup.find_all('div', attrs={'data-testid': 'srp-listing-tile'})
    print(f"  Found {len(listings)} listings")
    
    for listing in listings:
        title_tag = listing.find(attrs={'data-cg-ft': 'srp-listing-blade-title'})
        price_tag = listing.find(attrs={'data-cg-ft': 'srp-listing-blade-price'})
        

        location_span = listing.find('span', string=lambda text: text and ',' in text)
        
        if title_tag and price_tag:
            title = title_tag.text.strip()
            price = price_tag.text.strip()
            location = location_span.text.strip() if location_span else 'N/A'
            
            all_listings.append({
                'title': title,
                'price': price,
                'location': location
            })
            print(f"  [+] {title} - {price} - {location}")
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        next_button = None
        for btn in all_buttons:
            if "next page" in btn.text.lower():
                next_button = btn
                break
        
        if next_button:
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", next_button)
            print("  Clicked next page!")
            time.sleep(5)
        else:
            print("  No next button found!")
            break
    except Exception as e:
        print(f"Error: {e}")
        break

driver.quit()

with open('listings.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Year and Model', 'Price', 'Location'])
    
    for listing in all_listings:
        writer.writerow([listing['title'], listing['price'], listing['location']])

print(f"\nDone! Got {len(all_listings)} listings!")