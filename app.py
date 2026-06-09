— Flask API
from flask import Flask, jsonify
from flask_cors import CORS
import time
import json
import os
from scraper_engine import StealthScraper

app = Flask(__name__)
CORS(app)

CACHE_FILE = "data/cache.json"
CACHE_TTL = 3600 # 1 hour
scraper = None
cache = {}

def load_cache():
global cache
if os.path.exists(CACHE_FILE):
try:
with open(CACHE_FILE, 'r') as f:
cache = json.load(f)
except:
cache = {}

def save_cache():
try:
with open(CACHE_FILE, 'w') as f:
json.dump(cache, f)
except Exception as e:
print(f"[ERROR] Cache save failed: {e}")

load_cache()

def get_scraper():
global scraper
if scraper is None:
scraper = StealthScraper()
return scraper

@app.route('/movie/<movie_id>')
def get_movie(movie_id):
global scraper

# Check cache
if movie_id in cache:
cached = cache[movie_id]
if time.time() - cached.get("cached_at", 0) < CACHE_TTL:
return jsonify(cached["data"])

scraper = get_scraper()
data = scraper.get_movie_data(movie_id)

if not data.get("success"):
return jsonify(data), 500

stream_url = scraper.extract_stream(data["player_src"])

final_data = {
"title": data["title"],
"image": data["image"],
"sinopsis": data["sinopsis"],
"stream_url": stream_url,
"source_page": data["source_url"],
"fetched_at": int(time.time()),
"bypass": "full_sub_included_v3"
}

# Cache it
cache[movie_id] = {
"data": final_data,
"cached_at": time.time()
}
save_cache()

return jsonify(final_data)

@app.route('/health')
def health():
return jsonify({
"status": "alive",
"message": "stream theft engine online",
"bypass": "enabled"
})

if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)
