import nest_asyncio
nest_asyncio.apply()

from seleniumbase import sb_cdp
from playwright.sync_api import sync_playwright
import random
import time

def login_with_human_behavior(page, username, password):
    """Complete login flow with human-like behavior"""
    
    # Click username field with random offset (humans don't click exact center)
    username_field = page.locator("input[name='username']")
    box = username_field.bounding_box()
    if box:
        # Fixed: convert float to int
        x_offset = random.randint(20, int(box['width']) - 20)
        y_offset = random.randint(10, int(box['height']) - 10)
        username_field.click(position={'x': x_offset, 'y': y_offset})
    else:
        username_field.click()
    
    # Random pause before typing (hand moving to keyboard)
    page.wait_for_timeout(random.randint(400, 1200))
    
    # Type username
    for i, char in enumerate(username):
        delay = random.randint(50, 180)
        if char.isupper():
            delay += random.randint(20, 70)
        page.keyboard.type(char, delay=delay)
        
        # Occasional pause mid-typing
        if random.random() < 0.08:
            page.wait_for_timeout(random.randint(200, 600))
    
    # Tab to password field (don't click, use Tab like a real user)
    page.wait_for_timeout(random.randint(300, 900))
    page.keyboard.press("Tab")
    page.wait_for_timeout(random.randint(200, 700))
    
    # Type password with different rhythm
    segments = [password[i:i+4] for i in range(0, len(password), 4)]
    for segment in segments:
        for char in segment:
            # Password typing is usually faster than username
            delay = random.randint(40, 120)
            if char in '!@#$%^&*':
                delay += random.randint(30, 80)  # Slower on symbols
            page.keyboard.type(char, delay=delay)
        
        # Pause between password chunks (human chunking behavior)
        page.wait_for_timeout(random.randint(100, 400))
    
    # Post-password pause (reviewing, hand moving to mouse)
    page.wait_for_timeout(random.randint(500, 1500))
    
    # Click submit with hover first (humans hover before clicking)
    submit_button = page.locator("button[data-testid='btn-signin-submit']")
    submit_button.hover()
    page.wait_for_timeout(random.randint(100, 300))
    submit_button.click()
    print("✅ Form submitted")


def get_new_api_key():
    sb = sb_cdp.Chrome(locale='en', headless=False)
    endpoint_url = sb.get_endpoint_url()
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(endpoint_url)
            context = browser.contexts[0]
            page = context.pages[0]
            
            # Go to Riot developer portal
            page.goto("https://developer.riotgames.com/")
            print("📍 Developer portal loaded")
            sb.sleep(5)
            
            # Click LOGIN button
            page.click("text=LOGIN")
            print("🖱️ Clicked LOGIN")
            sb.sleep(5)
            
            # Type credentials with human behavior (this also clicks submit)
            login_with_human_behavior(page, "IMIHEGAZI", "!!ZXVBasfgQWRT1245@@")
            
            # Wait for page to process login
            sb.sleep(5)
            
            # Click sign in
            submit_button = page.locator("button[data-testid='btn-signin-submit']")
            submit_button.click()
            sb.sleep(5)

            # EVERY THING WORKS WELL TILL HERE


            # Issue here is that visual challenge can not be solved by sb.solve_captcha
            # Try to solve Cloudflare if present
            try:
                if "turing" in page.url or "challenge" in page.url:
                    print("🛡️ Cloudflare detected, attempting solve...")
                    sb.solve_captcha()
                    sb.sleep(5)
            except:
                print("⚠️ Auto-solve failed, please complete manually")
                sb.sleep(30)  # Wait for manual intervention



            # Then click on verify


            # Then the rest of the steps need to be implemented
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print("🔚 Closing browser...")
        sb.quit()

# Run it
key = get_new_api_key()
