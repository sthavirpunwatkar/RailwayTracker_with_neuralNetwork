import os
from dotenv import load_dotenv
import requests
from datetime import datetime

API_KEY = os.getenv("RAPIDAPI_KEY")

URL = "https://indian-railway-irctc.p.rapidapi.com/api/trains/v1/train/status"

def calculate_delay(stations):
    for stn in stations:
        if "arrivalTime" in stn and "actual_arrival_time" in stn:

            scheduled = stn["arrivalTime"]
            actual = stn["actual_arrival_time"]

            if scheduled and actual:
                try:
                    fmt = "%H:%M"

                    t1 = datetime.strptime(scheduled, fmt)
                    t2 = datetime.strptime(actual, fmt)

                    delay = (t2 - t1).total_seconds() / 60

                    if delay > 0:
                        return delay

                except:
                    continue

    return 0

def get_train_status(train_number):
    today = datetime.now().strftime("%Y%m%d")

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "indian-railway-irctc.p.rapidapi.com",
        "x-rapid-api": "rapid-api-database"
    }

    params = {
        "departure_date": today,
        "isH5": "true",
        "client": "web",
        "train_number": train_number
    }

    try:
        response = requests.get(URL, headers=headers, params=params)
        data = response.json()

        stations = data.get("body",{}).get("stations",[])

        delay = calculate_delay(stations)


        return {
            "delay": delay,
            "raw": data,
        }

    except Exception as e:
        return {
            "delay": 0,
            "error": str(e)
        }
