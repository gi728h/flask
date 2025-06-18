from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)
os.environ["FLASK_APP"] = "app.py"

SCRAPER_API_KEY = "bddbe58454cae7fbcd8e59e536773212"

@app.route("/", methods=["GET"])
def get_announcements():
    payload = {
        'api_key': SCRAPER_API_KEY,
        'url': 'https://www.nseindia.com/api/corporate-announcements?index=equities',
        'output_format': 'text',
        'country_code': 'in',
        'device_type': 'desktop'
    }

    try:
        r = requests.get('https://api.scraperapi.com/', params=payload, timeout=10)
        r.raise_for_status()
        return r.text, 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
