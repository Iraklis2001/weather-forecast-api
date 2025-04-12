import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from models import Session, Location, Forecast

USERNAME = "idh_irakleous_iraklis"
PASSWORD = "ePbLvk442J"

def fetch_forecast(lat, lon):
    today = datetime.utcnow().date()
    end_date = today + timedelta(days=7)
    interval = "PT24H"  
    date_range = f"{today}T00:00:00Z--{end_date}T00:00:00Z:{interval}"
    parameters = "t_2m:C,wind_speed_10m:ms,precip_1h:mm"
    url = f"https://api.meteomatics.com/{date_range}/{parameters}/{lat},{lon}/json"

    print(f"Fetching forecast for {lat},{lon}...")
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

def save_to_db(city_name, lat, lon, data):
    session = Session()

    location = Location(name=city_name, latitude=lat, longitude=lon)
    session.add(location)
    session.commit()

    dates = data["data"][0]["coordinates"][0]["dates"]
    temps = data["data"][0]["coordinates"][0]["dates"]
    winds = data["data"][1]["coordinates"][0]["dates"]
    precs = data["data"][2]["coordinates"][0]["dates"]

    for i in range(len(dates)):
        forecast = Forecast(
            location_id=location.id,
            forecast_date=datetime.fromisoformat(dates[i]["date"][:10]).date(),
            the_temp=temps[i]["value"],
            wind_speed=winds[i]["value"],
            precipitation=precs[i]["value"]
        )
        session.add(forecast)

    session.commit()
    session.close()

cities = [
    ("New York", 40.7128, -74.0060),
    ("London", 51.5074, -0.1278),
    ("Tokyo", 35.6895, 139.6917)
]

for name, lat, lon in cities:
    data = fetch_forecast(lat, lon)
    if data:
        save_to_db(name, lat, lon, data)
