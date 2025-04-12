from flask import Flask, jsonify, request
from models import Session, Location, Forecast
from sqlalchemy import func, desc

app = Flask(__name__)

@app.route('/locations')
def list_locations():
    session = Session()
    locations = session.query(Location).all()
    result = [{"id": loc.id, "name": loc.name, "latitude": loc.latitude, "longitude": loc.longitude} for loc in locations]
    return jsonify(result)

@app.route('/forecasts/latest')
def latest_forecasts():
    session = Session()
    latest_per_day = session.query(
        Forecast.location_id,
        Forecast.forecast_date,
        Forecast.the_temp,
        Forecast.wind_speed,
        Forecast.precipitation
    ).order_by(Forecast.forecast_date.desc()).all()

    result = [
        {
            "location_id": f.location_id,
            "date": f.forecast_date.isoformat(),
            "temperature": f.the_temp,
            "wind_speed": f.wind_speed,
            "precipitation": f.precipitation
        }
        for f in latest_per_day
    ]
    return jsonify(result)

@app.route('/forecasts/averages')
def average_forecasts():
    session = Session()
    subquery = session.query(
        Forecast.location_id,
        Forecast.forecast_date,
        Forecast.the_temp
    ).order_by(Forecast.forecast_date.desc()).limit(3).subquery()

    results = session.query(
        subquery.c.location_id,
        func.avg(subquery.c.the_temp).label("avg_temp")
    ).group_by(subquery.c.location_id).all()

    return jsonify([
        {"location_id": r[0], "average_temp": round(r[1], 2)} for r in results
    ])

@app.route('/metrics/top')
def top_locations():
    metric = request.args.get("metric", "the_temp")
    n = int(request.args.get("n", 3))
    session = Session()

    if metric not in ["the_temp", "wind_speed", "precipitation"]:
        return jsonify({"error": "Invalid metric"}), 400

    avg_query = session.query(
        Forecast.location_id,
        func.avg(getattr(Forecast, metric)).label("avg_metric")
    ).group_by(Forecast.location_id).order_by(desc("avg_metric")).limit(n)

    return jsonify([
        {"location_id": row[0], "avg_" + metric: round(row[1], 2)} for row in avg_query
    ])

if __name__ == '__main__':
    app.run(debug=True)
