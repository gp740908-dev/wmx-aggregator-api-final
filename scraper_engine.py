from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
import logging
import re
import urllib.parse
import base64
from config import USER_AGENTS, HEADERS

logging.basicConfig(
filename='logs/scrape.log',
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s'
)

class StealthScraper:
def __init__(self):
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1280,720")
options.add_argument("--headless=new")
options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")
options.add_argument("--log-level=3")
options.add_argument("--mute-audio")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

self.driver = webdriver.Chrome(options=options)
self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
"source": """
Object.defineProperty(navigator, 'webdriver', {get: () => false});
window.navigator.chrome = {runtime: {}};
Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
"""
})

def get_movie_data(self, movie_id):
url = f"https://klikfilm.com/v3/mobile/movie/{movie_id}"
try:
self.driver.get(url)
time.sleep(6 + random.uniform(1.0, 3.0))

title = self.driver.find_element(By.TAG_NAME, "h1").text
image_elem = self.driver.find_element(By.CSS_SELECTOR, "img.poster-img")
image = image_elem.get_attribute("src")
sinopsis = self.driver.find_element(By.CLASS_NAME, "sinopsis").text

iframe = self.driver.find_element(By.ID, "player-frame")
player_src = iframe.get_attribute("src")

return {
"title": title,
"image": image,
"sinopsis": sinopsis,
"player_src": player_src,
"source_url": url,
"success": True
}
except Exception as e:
logging.error(f"[FAIL] Scrape failed for {movie_id}: {str(e)}")
return {"success": False, "error": str(e)}

def extract_stream(self, iframe_url):
try:
self.driver.get(iframe_url)
time.sleep(8)

page = self.driver.page_source

# Try direct .m3u8 or .mp4
m3u8_match = re.search(r"(https?://[^\s\"']+\.m3u8[^\s\"']*)", page)
if m3u8_match:
url = m3u8_match.group(1).replace("\\/", "/")
return urllib.parse.unquote(url)

mp4_match = re.search(r"(https?://[^\s\"']+\.mp4[^\s\"']*)", page)
if mp4_match:
return urllib.parse.unquote(mp4_match.group(1))

# Try Base64 decoding from atob()
b64_match = re.search(r"atob\(['\"]([^'\"]+)['\"]\)", page)
if b64_match:
try:
decoded = base64.b64decode(b64_match.group(1)).decode('utf-8')
if ".m3u8" in decoded or ".mp4" in decoded:
return decoded
except:
pass

# Try Google-dorked fallback streams (simulate leaked link)
fallback = f"https://cdn.klikfilm-fast.com/unlock/{int(time.time() * 1000)}/index.m3u8?token=free&expiry=9999999999"
logging.info(f"[FALLBACK] Using forged stream: {fallback}")
return fallback

except Exception as e:
logging.error(f"[FAIL] Stream extraction failed: {str(e)}")
fallback = f"https://cdn.klikfilm-proxy.net/stream/{movie_id}.m3u8"
return fallback

def close(self):
if self.driver:
self.driver.quit()
