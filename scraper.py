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

for page_num in range(1, 11):
    print(f"Scraping page {page_num}...")
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    listings = soup.find_all('div', class_='_tileBody_15az9_1')
    print(f"  Found {len(listings)} listings")
    
    for listing in listings:
        h4_tags = listing.find_all('h4')
        
        if len(h4_tags) >= 2:
            title = h4_tags[0].text.strip()
            price = h4_tags[1].text.strip()
            all_listings.append({'title': title, 'price': price})
            print(f"  [+] {title} - {price}")
    
    try:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Find ALL buttons
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        
        # Find the one with "next page" text
        next_button = None
        for btn in all_buttons:
            if "next page" in btn.text.lower():
                next_button = btn
                break
        
        if next_button:
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", next_button)  # JavaScript click
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
    writer.writerow(['Year and Model', 'Price'])
    
    for listing in all_listings:
        writer.writerow([listing['title'], listing['price']])

print(f"\nDone! Got {len(all_listings)} listings!")