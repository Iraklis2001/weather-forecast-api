from models import Session, Location, Forecast

session = Session()

locations = session.query(Location).all()
for loc in locations:
    print(f"Location: {loc.name}")
    forecasts = session.query(Forecast).filter_by(location_id=loc.id).all()
    for f in forecasts:
        print(f"  {f.forecast_date} - Temp: {f.the_temp}°C, Wind: {f.wind_speed} m/s, Precip: {f.precipitation} mm")
