import sqlite3
import pandas as pd
import requests

DB_FILE = 'weather_audit.db'
EXCEL_FILE = 'weather_report.xlsx'

CITIES = {
    'Hasilpur': {'lat': 29.69, 'lon': 72.55},
    'Multan': {'lat': 30.15, 'lon': 71.52},
    'London': {'lat': 51.50, 'lon': -0.12},
    'Tokyo': {'lat': 35.67, 'lon': 139.65},
    'New York': {'lat': 40.71, 'lon': -74.00},
}


def init_db():
  """Initializes SQLite database for weather auditing."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature_c REAL,
            wind_speed_kmh REAL,
            weather_code INTEGER,
            status_code INTEGER,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
  conn.commit()
  conn.close()


def fetch_weather(city_name: str, coords: dict):
  """Fetches live weather metrics from Open-Meteo REST API."""
  url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current_weather=true"

  print(f'📡 Fetching REST API: {city_name}...')
  try:
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
      data = response.json().get('current_weather', {})
      temp = data.get('temperature', 0.0)
      wind = data.get('windspeed', 0.0)
      code = data.get('weathercode', 0)

      print(f'  ✅ 200 OK | Temp: {temp}°C | Wind: {wind} km/h')
      return {
          'city': city_name,
          'temperature_c': temp,
          'wind_speed_kmh': wind,
          'weather_code': code,
          'status_code': 200,
      }
    else:
      print(f'  ❌ HTTP Error {response.status_code}')
      return None

  except Exception as e:
    print(f'  ⚠️ Request Failed: {e}')
    return None


def save_reports(records: list):
  """Logs fetched data into SQLite and exports an Excel report."""
  if not records:
    print('No records to save.')
    return

  # 1. Save to SQLite
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  for r in records:
    cursor.execute(
        """
            INSERT INTO weather_logs (city, temperature_c, wind_speed_kmh, weather_code, status_code)
            VALUES (?, ?, ?, ?, ?)
        """,
        (
            r['city'],
            r['temperature_c'],
            r['wind_speed_kmh'],
            r['weather_code'],
            r['status_code'],
        ),
    )
  conn.commit()
  conn.close()

  df = pd.DataFrame(records)
  df.to_excel(EXCEL_FILE, index=False)
  print(f'\n📊 Excel Audit Report exported to: {EXCEL_FILE}')


def main():
  init_db()
  print('==================================================')
  print('🚀 WeatherPulse Lite API Pipeline')
  print('==================================================\n')

  audit_data = []
  for city, coords in CITIES.items():
    metrics = fetch_weather(city, coords)
    if metrics:
      audit_data.append(metrics)

  save_reports(audit_data)

  print('\n==================================================')
  print('🎉 Execution Complete! Check weather_audit.db & weather_report.xlsx')
  print('==================================================')


if __name__ == '__main__':
  main()