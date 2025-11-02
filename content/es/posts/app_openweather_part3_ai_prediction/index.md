---
title: "Weather Service Project (Part 1): Building the Data Collector with Python and GitHub Actions"
date: 2025-11-31
draft: False
categories: ["Projects", "Tools"]
tags: ["python", "api", "github actions", "automation", "serverless", "data", "backend"]
image: weather_backend_collector.png
description: "First installment in the series on building a weather service. We focus on the backend: connecting to the OpenWeatherMap API, storing data in CSV, and automating everything 24/7 for free with GitHub Actions."
summary: "We kick off our weather project by building the engine: a Python script that talks to an API, saves historical data, and runs daily thanks to GitHub Actions. I'll share the tricks and challenges!"
---

As I mentioned in a previous post, one of my goals with Datalaria is to get my hands dirty with projects that allow me to learn and connect different technologies in the data world. Today, we begin a series dedicated to one of those projects: the creation of a **complete global weather service**, from data collection to visualization and prediction, all serverless and using free tools.

In this first installment, we will focus on the **heart of the system: the backend data collector**. We'll see how to build a "robot" that works for us 24/7, connecting to an external API, saving structured information, and doing all this automatically and for free. Let's dive in!

![Conceptual image of Weather Service](AI_App_Weather_Image.png)

---

### The First Step: Talking to the OpenWeatherMap API

Every weather service needs a data source. I chose [OpenWeatherMap](https://openweathermap.org/) for its popularity and generous free plan. The initial process is straightforward:

1.  **Register**: Create an account on their website.
2.  **Get the API Key**: Generate a unique key that will identify us in each call. It's like our "key" to access their data.
3.  **Store the Key**: **Never** directly in the code! We'll discuss this further below.

With the key in hand (or almost!), I wrote a first `test_clima.py` script to test the connection using Python's fantastic `requests` library:

```python
import requests

API_KEY = "YOUR_API_KEY_HERE" # Temporarily! We'll use Secrets later
CITY = "Madrid"
URL = f"[https://api.openweathermap.org/data/2.5/weather?q=](https://api.openweathermap.org/data/2.5/weather?q=){CITY}&appid={API_KEY}&units=metric&lang=es"

try:
    response = requests.get(URL)
    response.raise_for_status() # Raises an exception for HTTP errors (4xx or 5xx)
    data = response.json()
    print(f"Temperature in {CITY}: {data['main']['temp']}°C")
except requests.exceptions.RequestException as e:
    print(f"Error connecting to the API: {e}")
except KeyError as e:
    print(f"Unexpected API response, key missing: {e}")
```

**First Obstacle Overcome (with Patience):** When I first ran it, I got a 401 Unauthorized error! 😱 It turns out that OpenWeatherMap API Keys can take a few hours to activate after being generated. The lesson: sometimes, the solution is simply to wait. ⏳

-----

### The "Database": Why CSV and Not SQL?

With data flowing, I needed to store it. I could have set up an SQL database (PostgreSQL, MySQL...), but that would involve complexity, a server (cost), and for this project, it was overkill.

I opted for radical simplicity: **CSV (Comma Separated Values) files**.

  * **Advantages**: Easy to read and write with Python, perfectly versionable with Git (we can track changes), and sufficient for the initial data volume we'd be handling.
  * **Key Logic**: I needed to append a new row to each city's file daily, but only write the header (`fecha_hora`, `ciudad`, `temperatura_c`, etc.) the first time. Python's native `csv` library and `os.path.exists` make this trivial:

```python
import csv
import os
from datetime import datetime

# ... (code to fetch API data for a city) ...

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
data_row = [now, city, temperature, ...] # List with the data
header = ['date_time', 'city', 'temperature_c', ...] # List with column names
file_name = f"data/{city}.csv" # We'll create a 'data' folder

# Ensure the 'data' folder exists
os.makedirs(os.path.dirname(file_name), exist_ok=True)

is_new_file = not os.path.exists(file_name)

try:
    with open(file_name, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if is_new_file:
            writer.writerow(header) # Write header ONLY if new file
        writer.writerow(data_row) # Append the new data row
    print(f"Data saved for {city}")
except IOError as e:
    print(f"Error writing to {file_name}: {e}")
```

-----

### The Automation Robot: GitHub Actions to the Rescue 🤖

Here comes the magic: how to make this script run daily without having a server constantly on? The answer is **GitHub Actions**, the automation engine integrated into GitHub. It's like having a small robot working for us for free.

**Security First: Never Upload Your API Key!**
The biggest mistake would be to upload `registrar_clima.py` with the `API_KEY` written directly in the code. Anyone could see it on GitHub.

  * **Solution**: Use GitHub's **Repository Secrets**.
    1.  Go to `Settings > Secrets and variables > Actions` in your GitHub repository.
    2.  Create a new secret named `OPENWEATHER_API_KEY` and paste your key there.
    3.  In your Python script, read the key securely using `os.environ.get("OPENWEATHER_API_KEY")`.

**The Robot's Brain: The `.github/workflows/update-weather.yml` File**
This YAML file tells GitHub Actions what to do and when:

```yaml
name: Daily Weather Data Update

on:
  workflow_dispatch: # Allows manual triggering from GitHub
  push:
    branches: [ main ] # Triggers if changes are pushed to the main branch
  schedule:
    - cron: '0 6 * * *' # The key: triggers daily at 06:00 UTC

jobs:
  update_data:
    runs-on: ubuntu-latest # Use a free Linux virtual machine
    steps:
      - name: Checkout repository code
        uses: actions/checkout@v4 # Downloads our code

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10' # Or your preferred version

      - name: Install necessary dependencies
        run: pip install -r requirements.txt # Reads requirements.txt and installs requests, etc.

      - name: Execute data collection script
        run: python registrar_clima.py # Our main script!
        env:
          OPENWEATHER_API_KEY: ${{ secrets.OPENWEATHER_API_KEY }} # Securely injects the secret

      - name: Save new data to repository (Commit & Push)
        run: |
          git config user.name 'github-actions[bot]' # Identifies the 'bot'
          git config user.email 'github-actions[bot]@users.noreply.github.com'
          git add data/*.csv # Adds ONLY the modified CSV files in the 'data' folder
          # Check if there are changes before committing to avoid empty commits
          git diff --staged --quiet || git commit -m "Automated weather data update 🤖"
          git push # Pushes changes to the repository
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # Automatic token to allow the push
```

**This last step is crucial!** The Action itself acts as a user, performing `git add`, `git commit`, and `git push` of the CSV files that the Python script has just modified. This way, the updated data is saved in our repository every day.

-----

### The Scaling Problem (and the Necessary Architectural Pivot)

My initial idea was to monitor about 1000 cities and store everything in a single `weather_data.csv` file. I did a quick calculation: 1000 cities \* \~200 bytes/day \* 365 days \* 3 years... over 200 MB! 😱

**Why is this a problem?** Because the frontend (our dashboard, which we'll see in the next post) runs in the user's browser. It would have to download that *entire* 200 MB just to display the graph for *one* city. Totally unacceptable in terms of performance. 🐢

**The Architectural Solution:** Switch to a **"one file per entity"** strategy.

  * We create a `data/` folder.
  * The `registrar_clima.py` script now generates (or appends data to) one CSV file per city: `data/Madrid.csv`, `data/Leon.csv`, `data/Tokyo.csv`, etc.

This way, when the user wants to see the weather for Leon, the frontend will only download the `data/Leon.csv` file, which will be just a few kilobytes. Instant loading! ✨

**Second Scaling Obstacle (API Limits):** OpenWeatherMap, in its free plan, allows about 60 calls per minute. My loop to get data for 155 cities (my current list) would make these calls too quickly.

  * **Vital Solution:** Add `import time` at the beginning of the Python script and `time.sleep(1.1)` at the end of the `for city in cities:` loop. This introduces a pause of slightly more than 1 second between each API call, ensuring we stay below the limit and avoid being blocked. 🚦

-----

### Conclusion (Part 1)

We've got the foundation! We've built a robust and automated system that:

  * Connects to an external API securely.
  * Processes and stores historical data for multiple entities (cities).
  * Runs daily, at no cost, thanks to GitHub Actions.
  * Is designed to scale efficiently.

In the next post, we'll put on our frontend developer hats and build the interactive dashboard that will allow any user to explore this data with dynamic graphs. Don't miss it!

---

### References and Links of Interest:

* **Complete Web Service**: You can see the final result of this project in action here: [https://dalaez.github.io/app_weather/](https://dalaez.github.io/app_weather/)
* **Project GitHub Repository**: Explore the source code and project structure in my repository: [https://github.com/Dalaez/app_weather](https://github.com/Dalaez/app_weather)
* **OpenWeatherMap**: Weather API documentation: [https://openweathermap.org/api](https://openweathermap.org/api)
* **Python Requests**: Documentation for the HTTP requests library: [https://requests.readthedocs.io/en/master/](https://requests.readthedocs.io/en/master/)
* **GitHub Actions**: Official GitHub Actions guide: [https://docs.github.com/en/actions](https://docs.github.com/en/actions)