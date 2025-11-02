---
title: "Weather Service Project (Part 2): Building the Interactive Frontend with GitHub Pages & JavaScript"
date: 2025-10-31
draft: False
categories: ["Projects", "Tools"]
tags: ["javascript", "frontend", "github pages", "html", "css", "papaparse", "chartjs", "serverless", "data-visualization"]
image: weather_frontend_dashboard.png
description: "Second installment of the Weather Service project. We dive into the frontend: serving a dynamic dashboard with GitHub Pages, reading CSV data with PapaParse.js, and creating interactive charts with Chart.js."
summary: "After building the data collector, it's time to visualize it! This post guides you through creating an interactive weather dashboard using GitHub Pages, vanilla JavaScript, PapaParse.js, and Chart.js. See your data come to life!"
---

In the [first part of this series](/blog/weather-service-part-1-backend), we laid the groundwork for our global weather service. We built a Python script to fetch weather data from OpenWeatherMap, stored it efficiently in separate CSV files for each city, and automated the entire collection process using GitHub Actions. Our "robot" is diligently gathering data 24/7.

But what good is data if you can't see it? Today, we shift our focus to the **frontend**: building an interactive, user-friendly dashboard that allows anyone to explore our collected weather data. We'll leverage the power of static site hosting with **GitHub Pages**, harness vanilla **JavaScript** to bring it to life, and use some excellent libraries for data handling and visualization. Let's make our data shine!

---

### Free Web Hosting: GitHub Pages

The first hurdle for any web project is hosting. Traditional servers can be costly and complex to manage. Following our "serverless and free" philosophy, **GitHub Pages** is the perfect solution. It allows you to host static websites directly from your GitHub repository.

**Activation is Trivial:**
1.  Go to `Settings > Pages` in your repository.
2.  Select your `main` branch (or whichever branch holds your web content) as the source.
3.  Choose the `/root` folder (or a `/docs` folder if you prefer) as the location for your web files.
4.  Click `Save`.

And just like that, your `index.html` file (and any linked assets) becomes publicly accessible at a URL like `https://your-username.github.io/your-repository-name/`. Simple, effective, and free! 🚀

---

### The Frontend Tech Stack: HTML, CSS, and Vanilla JS (with a little help)

For this dashboard, I opted for a lightweight approach: plain HTML for structure, a touch of CSS for styling, and **vanilla JavaScript** for interactivity. To handle specific tasks, I brought in two fantastic libraries:

1.  [**PapaParse.js**](https://www.papaparse.com/): The ultimate client-side CSV parser for the browser. It's the bridge between our raw CSV files and the JavaScript data structures we need for visualization.
2.  [**Chart.js**](https://www.chartjs.org/): A powerful and flexible JavaScript charting library that makes creating beautiful, responsive, and interactive graphs incredibly easy.

---

### The Dashboard Logic: Bringing Data to Life in `index.html`

Our `index.html` acts as the main canvas, orchestrating the fetching, parsing, and rendering of the weather data.

#### 1. Dynamic City Loading

Instead of hardcoding a list of cities, we want our dashboard to automatically update if we add new cities to our backend. We achieve this by fetching a simple `cities.txt` file (which contains one city name per line) and dynamically populating a `<select>` dropdown element using JavaScript's `fetch` API.

```javascript
const citySelector = document.getElementById('citySelector');
let myChart = null; // Global variable to store the Chart.js instance

async function loadCityList() {
    try {
        const response = await fetch('cities.txt');
        const text = await response.text();
        // Filter out empty lines from the text file
        const cities = text.split('\n').filter(line => line.trim() !== '');

        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelector.appendChild(option);
        });

        // Load the first city by default when the page loads
        if (cities.length > 0) {
            loadAndDrawData(cities[0]);
        }
    } catch (error) {
        console.error('Error loading city list:', error);
        // Display a user-friendly error message
    }
}

// Trigger loading cities when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', loadCityList);
```

#### 2. Reacting to User Selection

When a user selects a city from the dropdown, we need to respond immediately. An `addEventListener` on the `<select>` element detects the `change` event and calls our primary function to fetch and draw the data for the newly selected city.

```javascript
citySelector.addEventListener('change', (event) => {
    const selectedCity = event.target.value;
    loadAndDrawData(selectedCity);
});
```

#### 3. Fetching, Parsing, and Drawing the Data

This is the core function where everything comes together. It's responsible for:

  * Constructing the URL for the specific city's CSV file (e.g., `data/Leon.csv`).
  * Using `Papa.parse` to download and process the CSV content directly in the browser. PapaParse handles the asynchronous fetching and parsing, making it incredibly easy.
  * Extracting the relevant `labels` (dates) and `data` (temperatures) from the parsed CSV for Chart.js.
  * **Crucially**: Before drawing a new chart, we must **destroy the previous Chart.js instance** (`if (myChart) { myChart.destroy(); }`). Forgetting this step leads to overlapping charts and performance issues! 💥
  * Creating a new `Chart()` instance with the updated data.
  * Additionally, it calls a function to load and display the AI prediction for that city, seamlessly integrating it into the dashboard.

```javascript
function loadAndDrawData(city) {
    const csvUrl = `data/${city}.csv`; // Note the 'data/' folder from Part 1
    const ctx = document.getElementById('weatherChart').getContext('2d');

    Papa.parse(csvUrl, {
        download: true, // Tell PapaParse to fetch the file
        header: true,   // Treat the first row as headers
        skipEmptyLines: true,
        complete: function(results) {
            const weatherData = results.data;

            // Extract labels (dates) and data (temperatures)
            const labels = weatherData.map(row => row.date_time.split(' ')[0]); // Extract date only
            const maxTemps = weatherData.map(row => parseFloat(row.temp_max_c));
            const minTemps = weatherData.map(row => parseFloat(row.temp_min_c));

            // Destroy previous chart instance if it exists to avoid overlaps
            if (myChart) {
                myChart.destroy();
            }

            // Create new Chart.js instance
            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: `Max Temp (°C) - ${city}`,
                        data: maxTemps,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1
                    }, {
                        label: `Min Temp (°C) - ${city}`,
                        data: minTemps,
                        borderColor: 'rgb(54, 162, 235)',
                        tension: 0.1
                    }]
                },
                options: { // Chart options for responsiveness, title, etc.
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: false } },
                    plugins: { legend: { position: 'top' }, title: { display: true, text: `Historical Weather Data for ${city}` } }
                }
            });

            // Load and display AI prediction
            loadPrediction(city);
        },
        error: function(err, file) {
            console.error("Error parsing CSV:", err, file);
            // Optional: display user-friendly error message on the dashboard
            if (myChart) { myChart.destroy(); } // Clear chart on failure
        }
    });
}
```

#### 4. Displaying AI Predictions

Integrating the AI predictions (which we'll delve into in Part 3) is also handled by the frontend. The backend generates a `predictions.json` file, and our JavaScript simply fetches this JSON, finds the prediction for the selected city, and displays it.

```javascript
async function loadPrediction(city) {
    const predictionElement = document.getElementById('prediction');
    try {
        const response = await fetch('predictions.json');
        const predictions = await response.json();
        if (predictions && predictions[city]) {
             predictionElement.textContent = `Tomorrow's Max Temp. Prediction: ${predictions[city].toFixed(1)}°C`;
        } else {
             predictionElement.textContent = 'Prediction not available.';
        }
    } catch (error) {
         console.error('Error loading predictions:', error);
         predictionElement.textContent = 'Error loading prediction.';
    }
}
```

---

### Conclusion (Part 2)

We've now transformed raw data into an engaging and interactive experience! By combining GitHub Pages for hosting, vanilla JavaScript for logic, PapaParse.js for CSV handling, and Chart.js for beautiful visualizations, we've built a powerful frontend that is both free and highly effective.

The dashboard now provides immediate insights into historical weather patterns for any selected city. But what about the future? In the **third and final part of this series**, we'll dive deep into the exciting world of **Machine Learning** to add a predictive layer to our service. We'll explore how to use historical data to forecast tomorrow's weather, turning our service into a true weather "oracle." Stay tuned!

---

### References and Links of Interest:

* **Complete Web Service**: See the live project in action here: [https://datalaria.com/apps/weather/](https://datalaria.com/apps/weather/)
* **Project GitHub Repository**: Explore the source code and project structure: [https://github.com/Dalaez/app_weather](https://github.com/Dalaez/app_weather)
* **PapaParse.js**: Fast in-browser CSV parser for JavaScript: [https://www.papaparse.com/](https://www.papaparse.com/)
* **Chart.js**: Simple, yet flexible JavaScript charting for designers & developers: [https://www.chartjs.org/](https://www.chartjs.org/)
* **GitHub Pages**: Official documentation on how to host your sites: [https://docs.github.com/en/pages](https://docs.github.com/en/pages)