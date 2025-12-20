from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import csv
import time
import random

def human_scroll_down(driver, distance=None):
    """Scroll like a human - smooth with variable speed"""
    if distance is None:
        distance = random.randint(300, 700)
    
    current_pos = driver.execute_script("return window.pageYOffset;")
    target_pos = current_pos + distance
    
    scroll_steps = random.randint(40, 60)
    
    for i in range(scroll_steps):
        if i < 10 or i > scroll_steps - 10:
            step = distance / scroll_steps * 0.5  
        else:
            step = distance / scroll_steps * 1.2  
            
        driver.execute_script(f"window.scrollBy(0, {step});")
        time.sleep(random.uniform(0.05, 0.1))  # SLOWER: was 0.01-0.03
    
    time.sleep(random.uniform(0.5, 1.0))  # LONGER PAUSE: was 0.3-0.7

def random_mouse_movement(driver):
    """Move mouse randomly like a human browsing"""
    try:
        elements = driver.find_elements(By.TAG_NAME, "div")[:20]
        if elements:
            random_elem = random.choice(elements)
            ActionChains(driver).move_to_element(random_elem).perform()
            time.sleep(random.uniform(0.3, 0.6))  # LONGER: was 0.1-0.3
    except:
        pass

driver = webdriver.Chrome()
all_listings = []

url = "https://www.cargurus.com/Cars/l-Used-BMW-M3-d390"
print("Opening CarGurus...")
driver.get(url)
time.sleep(random.uniform(5, 8))  # LONGER: was 3-5

# Act like reading the page
random_mouse_movement(driver)
time.sleep(random.uniform(2, 3))  # LONGER: was 1

try:
    print("\nLooking for distance dropdown...")
    
    human_scroll_down(driver, 200)
    time.sleep(random.uniform(2, 3))  # LONGER: was 1-2
    
    dropdown_element = None
    try:
        dropdown_element = driver.find_element(By.CSS_SELECTOR, "select[aria-label='Distance from me']")
        print("Found dropdown!")
    except:
        try:
            dropdown_element = driver.find_element(By.CSS_SELECTOR, "select.uHLXM")
        except:
            print("Couldn't find dropdown")
    
    if dropdown_element:
        # Hover before clicking
        ActionChains(driver).move_to_element(dropdown_element).perform()
        time.sleep(random.uniform(1, 2))  # LONGER: was 0.5-1
        
        distance_dropdown = Select(dropdown_element)
        print("Selecting Nationwide...")
        distance_dropdown.select_by_value("50000")
        
        print("[OK] Distance set to Nationwide!")
        print("Waiting for page to reload...")
        time.sleep(random.uniform(6, 10))  # MUCH LONGER: was 4-6
        
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='srp-listing-tile']"))
        )
        print("Page reloaded!\n")
        time.sleep(random.uniform(3, 5))  # LONGER: was 2-3
        
except Exception as e:
    print(f"Error changing distance: {e}")

# Only scrape 2 pages to be extra safe
for page_num in range(1, 3):  # REDUCED: was 1-4
    print(f"\n{'='*50}")
    print(f"Scraping page {page_num}...")
    print(f"{'='*50}")
    
    # Scroll to top slowly
    print("Scrolling to top...")
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(random.uniform(2, 3))  # LONGER: was 1-2
    
    # Wait for listings
    print("Waiting for listings to appear...")
    listings_found = False
    for attempt in range(3):
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='srp-listing-tile']"))
            )
            listings_found = True
            print(f"Listings appeared! (attempt {attempt + 1})")
            break
        except:
            print(f"Attempt {attempt + 1} failed, trying refresh...")
            if attempt < 2:
                driver.refresh()
                time.sleep(random.uniform(5, 8))
    
    if not listings_found:
        print("[X] Could not find listings after 3 attempts - stopping")
        break
    
    time.sleep(random.uniform(2, 4))  # LONGER: was 2
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    listings = soup.find_all('div', attrs={'data-testid': 'srp-listing-tile'})
    print(f"Found {len(listings)} total listings on page")
    
    if len(listings) == 0:
        print("[X] No listings in HTML - stopping")
        break
    
    # Browse more like a real person
    print("Browsing through listings...")
    for _ in range(random.randint(3, 5)):  # MORE SCROLLS: was 2-4
        human_scroll_down(driver)
        if random.random() < 0.4:  # HIGHER CHANCE: was 0.3
            random_mouse_movement(driver)
        time.sleep(random.uniform(0.5, 1.5))  # Random pauses while "reading"
    
    time.sleep(random.uniform(2, 3))  # LONGER: was 1-2
    
    scraped_count = 0
    for listing in listings:
        title_tag = listing.find(attrs={'data-cg-ft': 'srp-listing-blade-title'})
        price_tag = listing.find(attrs={'data-cg-ft': 'srp-listing-blade-price'})
        location_span = listing.find('span', string=lambda text: text and ',' in text)

        img_tag = listing.find('img', attrs={'data-cg-ft': 'srp-listing-blade-image'})
        color = 'N/A'
        if img_tag and img_tag.get('alt'):
            alt_text = img_tag.get('alt')
            color = alt_text.split()[0] if alt_text else 'N/A'
        
        if title_tag and price_tag:
            title = title_tag.text.strip()
            price = price_tag.text.strip()
            location = location_span.text.strip() if location_span else 'N/A'
            
            if "Home delivery from" in location or "/mo est." in location:
                continue
            
            all_listings.append({
                'title': title,
                'price': price,
                'color': color,
                'location': location
            })
            scraped_count += 1
            print(f"  [+] {title} - {price} - {color} - {location}")
    
    print(f"\nScraped {scraped_count} valid listings from this page")
    print(f"Total so far: {len(all_listings)}")
    
    # Don't navigate after last page
    if page_num >= 2:  # CHANGED: was 3
        print("\nReached target of 2 pages - stopping")
        break
    
    try:
        print("\nScrolling to bottom...")
        
        viewport_height = driver.execute_script("return window.innerHeight")
        total_height = driver.execute_script("return document.body.scrollHeight")
        current = driver.execute_script("return window.pageYOffset;")
        
        # Scroll down more gradually
        while current < total_height - viewport_height:
            human_scroll_down(driver)
            current = driver.execute_script("return window.pageYOffset;")
            
            # More frequent scroll-ups
            if random.random() < 0.3:  # HIGHER: was 0.2
                driver.execute_script(f"window.scrollBy(0, -{random.randint(50, 150)});")
                time.sleep(random.uniform(0.5, 1.0))  # LONGER: was 0.3-0.6
        
        time.sleep(random.uniform(2, 3))  # LONGER: was 1-2
        
        print("Looking for next button...")
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Found {len(all_buttons)} buttons total")
        
        next_button = None
        for btn in all_buttons:
            try:
                if "next page" in btn.text.lower():
                    next_button = btn
                    print("Found next page button!")
                    break
            except:
                continue
        
        if next_button:
            is_disabled = next_button.get_attribute("disabled")
            if is_disabled:
                print("Next button is disabled - stopping")
                break
            
            # Hover over button longer
            ActionChains(driver).move_to_element(next_button).perform()
            time.sleep(random.uniform(1, 2))  # LONGER: was 0.5-1
            
            print("Clicking next page...")
            driver.execute_script("arguments[0].click();", next_button)
            
            # MUCH LONGER wait between pages
            wait_time = random.uniform(10, 15)  # MUCH LONGER: was 5-8
            print(f"Waiting {wait_time:.1f}s for next page to load...")
            time.sleep(wait_time)
        else:
            print("No next button found - stopping")
            break
            
    except Exception as e:
        print(f"Error navigating to next page: {e}")
        break

print(f"\n{'='*50}")
print("Scraping complete!")
print(f"{'='*50}")
driver.quit()

with open('listings.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Year and Model', 'Price', 'Color', 'Location'])
    
    for listing in all_listings:
        writer.writerow([listing['title'], listing['price'], listing['color'], listing['location']])

print(f"\n[OK] Done! Got {len(all_listings)} listings saved to listings.csv!")