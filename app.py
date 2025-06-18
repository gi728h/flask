from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

def fetch_announcements_with_retry(max_retries=10, delay=2):
    url = "https://www.nseindia.com/api/corporate-announcements?index=invitsreits"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/",
        "X-Requested-With": "XMLHttpRequest"
    }

    session = requests.Session()
    try:
        session.get("https://www.nseindia.com", headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        return {"error": f"Error hitting homepage: {e}"}, False

    retries = 0
    while retries < max_retries:
        try:
            response = session.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json(), True
            else:
                print(f"Attempt {retries + 1}: Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {retries + 1}: Request failed: {e}")

        retries += 1
        time.sleep(delay)

    return {"error": "Failed to fetch data after retries."}, False

@app.route("/", methods=["GET"])
def get_announcements():
    data, success = fetch_announcements_with_retry()
    status_code = 200 if success else 500
    return jsonify(data), status_code

