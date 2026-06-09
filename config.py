import random

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 13; SM-G980F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
]

# Optional: Add rotating proxies (use residential or datacenter)
PROXIES = [
    # "http://user:pass@ip:port",
    # "socks5://1.2.3.4:1080"
]

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://klikfilm.com/",
    "Origin": "https://klikfilm.com",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}
