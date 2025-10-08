from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# === CONFIGURATION ===
groups = ["Goooo", "Material", "V3"]  # Replace with your group names
message = ("Giftque_Studio Amidst the festive aura resonating with positivity, extend your heartfelt wishes to loved ones with the perfect blend of your love and our thoughtful return gifts."
"\n\n #GiftiqueReturnGifts #ReturnGifts #BirthdayFavours #WeddingFavours #CorporateFavours #FestiveHampers #Hampers #CustomisedGifts #CustomisedHampers #Gifts #GiftShop #GiftsIdeas #Thambulam #ThambulamPlates") # Replace with your message
image_path = "Product1.jpg"     # Replace with your image path
chromedriver_path = "chromedriver.exe"  # Replace with your chromedriver path

def remove_non_bmp_chars(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

message = remove_non_bmp_chars(message)

# === SETUP SELENIUM ===
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

# === OPEN WHATSAPP WEB ===
driver.get("https://web.whatsapp.com")
print("📷 Scan the QR code if not already logged in.")
time.sleep(20)

wait = WebDriverWait(driver, 10)

# === FUNCTION TO SEND TO GROUP ===
def send_message_to_group(group_name):
    try:
        print(f"📤 Sending to: {group_name}")

        # Wait until popups (dialogs) are gone
        while True:
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))
                print("⏳ Waiting for popup to close...")
                time.sleep(2)
            except:
                break  # No popup found

        # Wait until the chat list becomes visible
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Chat list']")))

        # Search for the group
        search_box = wait.until(
           EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-tab='3']"))
        )
        ActionChains(driver).move_to_element(search_box).click().perform()
        search_box.clear()
        search_box.send_keys(group_name)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)

        # === Attach and send image with caption ===
        attach_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='plus-rounded']"))
        )
        attach_btn.click()
        time.sleep(1)

        # Upload the image
        image_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"))
        )
        image_input.send_keys(os.path.abspath(image_path))
        time.sleep(3)  # Allow image preview to appear

        # Type caption (cursor auto-focuses on the caption box)
        for i, line in enumerate(message.split('\n')):
            ActionChains(driver).send_keys(line).perform()
            if i != len(message.split('\n')) - 1:
                ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()

        time.sleep(1)

        # Click send
        send_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='wds-ic-send-filled']"))
        )
        send_btn.click()
        print(f"⏳ Waiting for message to be sent in: {group_name}")
        
        # Wait for image preview to disappear (indicates message sent)
        WebDriverWait(driver, 20).until_not(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@style, 'translateY') and @role='dialog']"))
        )
        
        print(f"✅ Image sent successfully to: {group_name}")
        time.sleep(2)

    except Exception as e:
        print(f"❌ Failed to send to {group_name}. Error: {e}")

# === LOOP OVER GROUPS ===
for group in groups:
    send_message_to_group(group)

print("✅ All messages sent.")
driver.quit()
