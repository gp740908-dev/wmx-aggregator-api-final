#!/bin/bash
echo "🔧 Installing KlikFilm Aggregator API — FULL BYPASS MODE"

apt update && apt upgrade -y

# Install Python & tools
apt install -y python3 python3-pip python3-venv git curl unzip

# Setup project
mkdir -p /opt/klikfilm-api
cd /opt/klikfilm-api

# Copy your files here (you already pasted them)
# Or use wget if hosting zip

# Virtual env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Chrome for headless
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt update
apt install -y google-chrome-stable

# Install Chromedriver
CHROME_VERSION=$(google-chrome --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION")
curl -o /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$DRIVER_VERSION/chromedriver_linux64.zip"
unzip /tmp/chromedriver.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

# Create data/logs
mkdir -p data logs
touch data/cache.json
echo "{}" > data/cache.json

# Systemd service
cp deploy/klikfilm-api.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable klikfilm-api
systemctl start klikfilm-api

# Nginx
apt install -y nginx
cp deploy/nginx.conf /etc/nginx/sites-available/klikfilm
ln -sf /etc/nginx/sites-available/klikfilm /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl restart nginx

echo "🎉 DONE. Your API is LIVE at http://$(hostname -I | awk '{print $1}')"
echo "🎯 Test it: http://your-ip/movie/sample-action-123"
