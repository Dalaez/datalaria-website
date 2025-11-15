---
title: "Weather Service Project (Part 3): Predicting the Future with AI and OpenWeatherMap"
date: 2025-11-15
draft: False
categories: ["Projects", "AI", "Tools"]
tags: ["machine-learning", "regression", "openweathermpa", "python", "pandas", "scikit-learn", "javascript", "frontend", "data-prediction", "weather-forecast", "serverless"]
image: weather_forecast_dashboard.png
description: "The final installment of our Weather Service project. We dive into adding predictive capabilities, combining official OpenWeatherMap forecasts with our custom-built AI (Linear Regression) model to predict tomorrow's weather and visualize its accuracy."
summary: "From data collection to dynamic dashboards, now it's time to predict! This post explores integrating OpenWeatherMap's 5-day forecast and building our own 1-day AI prediction model using historical data, all visualized in our interactive frontend."
---

In the [first part of this series](/blog/weather-service-part-1-backend), we set up the backbone of our global weather service, collecting raw data using Python and GitHub Actions. Then, in [Part 2](/blog/weather-service-part-2-frontend), we transformed that raw data into a beautiful, interactive dashboard, leveraging GitHub Pages/Netlify, JavaScript, PapaParse.js, and Chart.js.

Now, it's time for the grand finale: adding predictive power to our Weather Service. We'll explore how to augment our historical data visualization with actual forecasts. This installment focuses on a dual approach: integrating an official, reliable forecast from a professional service (OpenWeatherMap) and, more excitingly, building and training our very own simple AI model (Linear Regression) to predict tomorrow's weather based on the historical data we've meticulously collected. Finally, we'll visualize both forecasts on our dashboard, allowing for a direct comparison and a real-world test of our AI's accuracy.

Let's turn our data into a crystal ball! 🔮

![Conceptual image of Weather Service Predictions](AI_App_Weather_Image_Predictions.png)

---

### The Predictive Core: OpenWeatherMap and Our Custom AI

The goal for this predictive functionality was twofold:

1.  **Official Forecast**: Obtain a reliable, multi-day forecast from a professional weather service (OpenWeatherMap - OWM).
2.  **Custom AI Prediction**: Create our own simple AI model (Linear Regression) trained on the historical data we've collected, to predict the next day's weather.
3.  **Visualization & Comparison**: Display and compare both forecasts to gauge the accuracy and performance of our custom AI model.

---

### 1. ⚙️ Backend Logic: `read_weather.py` Gets Smarter

Our `read_weather.py` script, previously responsible for data collection, now expands its role to gather data from both OWM and our historical archives, consolidating everything into a single `predicciones.json` file.

#### Step 1: Fetching OpenWeatherMap's 5-Day Forecast

We decided that in addition to our 1-day AI prediction, a 5-day forecast from OWM would provide valuable context.

* **API Endpoint**: We opted for the free `data/2.5/forecast` API (since OneCall 3.0 required a payment method).
* **Data Processing**: This API returns data in 3-hour blocks. We had to add Python logic to:
    * Iterate over the list of ~40 forecasts.
    * Group them by day (ignoring the current day).
    * For each of the next 5 days, calculate the maximum, minimum, and average temperature from all 3-hour blocks within that day.
* **Result**: A list of 5 objects (one per day) containing OWM's max, min, and average temperature predictions.

#### Step 2: Implementing Our AI Model (1-Day Prediction)

This is the core of our "homemade AI." For each city:

* **Data Loading**: We used `pandas` to read the city's historical CSV file (e.g., `datos/Madrid.csv`).
* **Feature Engineering**: Since we had multiple readings per day, the most crucial step was transforming this data:
    * **Resampling**: We used `df.resample('D')` from `pandas` to group data by day, calculating the actual daily aggregates (e.g., `temp_max`, `temp_min`, `avg_temp`, `avg_humidity`).
    * **Feature Creation (X)**: We created new "shifted" columns (`.shift(1)`) so that each row (representing a day) contained the previous day's data (e.g., `temp_max_lag1`, `avg_humidity_lag1`). We also added `day_of_year` to capture seasonality.
    * **Target Creation (y)**: We defined what we wanted to predict (e.g., the actual `temp_max` of the current day).
* **Training 3 Models**: Instead of one, we trained three independent Linear Regression models (`scikit-learn`):
    * `model_max`: Trained with `y = df_clean['temp_max']`.
    * `model_min`: Trained with `y = df_clean['temp_min']`.
    * `model_avg`: Trained with `y = df_clean['avg_temp']`.
* **Prediction**:
    * We took the last row of aggregated data (representing "today's" data).
    * Fed this data to the 3 models to predict "tomorrow's" values.
    * We included a safeguard (`MIN_RECORDS_FOR_IA = 10`) so the model only attempts to predict if it has sufficient historical data (e.g., 10 clean days).

#### Step 3: Consolidate and Save

The script combines the results from Steps 1 and 2 into a JSON structure and saves it to `predicciones.json`:

```json
{
  "Madrid": {
    "pred_owm_5day": [ 
      { "date": "...", "max": 15.0, "min": 10.0, "avg": 12.5 }, 
      ... (5 days) ...
    ],
    "pred_ia": {
      "max": 14.8,
      "min": 7.5,
      "avg": 11.2,
      "records": 120
    }
  },
  "A Coruña": {
     ...
     "pred_ia": { "max": null, "min": null, "avg": null, "records": 9 } // Example of insufficient data
  }
}
```

---

### 2. 🎨 Frontend Logic: `index.html` Visualizes the Future

The frontend is responsible for loading this `predicciones.json` file and presenting it in a visually appealing and informative way.

#### Step 1: Data Loading

  * `loadPredictions()`: We created a new `async` function that runs once during initialization (before `updateDashboard`).
  * `allPredictionsCache`: This function loads `predicciones.json` and saves it into this new global variable so that all visualization functions have access to it.

#### Step 2: Visualization in the "Super-Cards" (KPIs)

We wanted a direct and clear comparison.

  * **OWM 5-Day Forecast**:
      * We created a helper function `buildForecastHTML()`.
      * This function takes the `pred_owm_5day` list and generates an HTML block with a list of the 5 days and their max/min temperatures (e.g., "Sat, Nov 9: 15.1°C / 10.0°C").
  * **AI 1-Day Forecast (Comparison)**:
      * We created a second helper function `buildIAForecastHTML()`.
      * This function takes the `pred_ia` object and the first day of the OWM forecast (`pred_owm_5day[0]`).
      * **Comparison Logic**: For max, min, and average temperatures, it displays the AI's value and then, next to it, the difference from OWM.
      * **Visual Impact**: The difference is colored red (if our AI predicts warmer) or blue (if it predicts cooler), giving us an immediate visual cue of our model's deviation.
      * It also handles the "Insufficient Data" case (`${ia_preds.records}/${MIN_RECORDS_FOR_IA}`).
  * `updateKPIs()`: The card template was modified to call these two new functions, displaying both forecast blocks.

#### Step 3: Visualization in the Charts

We wanted the forecasts to be integrated directly into the existing charts.

  * **Evolution Chart (Dotted Line)**:
      * In `updateChart()`, we added a new dataset for each city.
      * This dataset uses the average of the OWM prediction (`pred_owm_5day`).
      * We applied the style `borderDash: [5, 5]` to draw it as a dotted line.
      * We "stitched" the beginning of this line to the last real data point to make it appear as a seamless continuation.
  * **Variation Chart (Striped Bars)**:
      * In `updateVariationChart()`, we added another dataset for each city.
      * The `y` data for this set is `day.max - day.min` (the variation) from the OWM forecast.
      * For styling, we created a helper function `createStripedPattern()` that draws a striped pattern on a canvas.
      * We used this pattern as the `backgroundColor` for the forecast bars, differentiating them from the solid bars of real data.

---

### Conclusion (Part 3)

With this final installment, our Weather Service project is complete! We've successfully integrated both professional 5-day forecasts from OpenWeatherMap and a custom 1-day AI prediction model, all powered by our collected historical data. The frontend now provides a rich, interactive experience that not only visualizes past weather but also offers a glimpse into the future, complete with a comparative analysis of our AI's performance.

This journey has covered everything from backend data collection, automation with GitHub Actions, static site hosting with Netlify, to dynamic frontend development with vanilla JavaScript, advanced data parsing with PapaParse.js, interactive charting with Chart.js, and finally, dipping our toes into Machine Learning for predictive analytics.

We've built a robust, serverless, and insightful application entirely on free services. The possibilities for expansion (e.g., more complex ML models, different data sources, user accounts) are endless, but for now, we have a fully functional weather oracle!

---

### References and Links of Interest:

  * **Complete Web Service**: You can see the final project in action here: [https://datalaria.com/apps/weather/](https://datalaria.com/apps/weather/)
  * **Project GitHub Repository**: Explore the source code and project structure in my repository: [https://github.com/Dalaez/app_weather](https://github.com/Dalaez/app_weather)
  * **OpenWeatherMap API**: [https://openweathermap.org/api](https://openweathermap.org/api)
  * **Pandas**: Python Data Analysis Library: [https://pandas.pydata.org/](https://pandas.pydata.org/)
  * **Scikit-learn**: Machine Learning in Python: [https://scikit-learn.org/](https://scikit-learn.org/)
  * **PapaParse.js**: Fast in-browser CSV parser for JavaScript: