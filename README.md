# weather.api
# Flask Weather Device Control API

This project is a simple Flask-based REST API that:
- Fetches live weather data from OpenWeatherMap
- Controls virtual devices like a fan, heater, and light
- Automatically turns devices on/off based on temperature

---

## Features

- Real-time weather info by city
- Virtual smart device simulation (fan, light, heater)
- Auto device control based on temperature (if >30°C, fan turns on; if <15°C, heater turns on)
- JSON-based API responses

---

##  Tech Stack

- Python 3
- Flask (for API)
- Requests (to call weather API)
- OpenWeatherMap (weather data provider)

---

##  Requirements

Install dependencies with:

```bash
pip install flask requests
