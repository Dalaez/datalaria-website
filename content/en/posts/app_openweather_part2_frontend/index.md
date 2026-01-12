---
title: "Weather Service Project (Part 2): Building the Interactive Frontend with GitHub Pages or Netlify and JavaScript"
date: 2025-11-08
draft: False
categories: ["Projects", "Tools"]
tags: ["javascript", "frontend", "github pages", "html", "css", "papaparse", "chartjs", "serverless", "data-visualization", "netlify"]
image: cover.png
description: "Second installment of the Weather Service project. We dive into the frontend: serving a dynamic dashboard with GitHub Pages or Netlify, reading CSV data with PapaParse.js, and creating interactive charts with Chart.js."
summary: "After building the data collector, it's time to visualize it! This post guides you through creating an interactive weather dashboard using GitHub Pages or Netlify, JavaScript, PapaParse.js, and Chart.js. Bring your data to life!"
---

In the [first part of this series](/blog/weather-service-part-1-backend), we laid the groundwork for our global weather service. We built a Python script to fetch weather data from OpenWeatherMap, efficiently stored it in city-specific CSV files, and automated the entire collection process using GitHub Actions. Our "robot" is diligently gathering data 24/7.

But what good is data if you can't see it? Today, we shift our focus to the **frontend**: building an interactive, user-friendly dashboard that allows anyone to explore the weather data we've collected. We'll leverage the power of static site hosting with **GitHub Pages or Netlify**, use "vanilla" **JavaScript** to bring it to life, and rely on some excellent libraries for data handling and visualization. Let's make our data shine!

![Conceptual image of Weather Service Frontend](AI_App_Weather_Image_Frontend.png)

---

### Free Web Hosting: GitHub Pages vs. Netlify

The first hurdle for any web project is hosting. Traditional servers can be costly and complex to manage. Following our "serverless and free" philosophy, both **GitHub Pages** and **Netlify** are perfect solutions for hosting static websites directly from your GitHub repository.

#### Option 1: GitHub Pages

GitHub Pages allows you to host static websites directly from your GitHub repository.

**Activation is trivial:**
1.  Go to `Settings > Pages` in your repository.
2.  Select your `main` branch (or the branch containing your web content) as the source.
3.  Choose the `/root` folder (or a `/docs` folder if you prefer) as the location of your web files.
4.  Click `Save`.

And just like that, your `index.html` file (and any linked assets) becomes publicly accessible at a URL like `https://your-username.github.io/your-repository-name/`. Simple, effective, and free! 🚀

#### Option 2: Netlify (the final choice for this project!)

For this project, I ultimately opted for **Netlify** due to its flexibility, ease of managing custom domains, and integrated continuous deployment. It also allows me to host the project directly under my Datalaria domain (`https://datalaria.com/apps/weather/`).

**Steps to deploy on Netlify:**

1.  **Connect Your Repository**: Log in to Netlify. Click "Add new site" then "Import an existing project". Connect your GitHub account and select your Weather Service project repository.
2.  **Deployment Configuration**:
    * **Owner**: Your GitHub account.
    * **Branch to deploy**: `main` (or the branch where your frontend code resides).
    * **Base directory**: Leave this empty if your `index.html` and assets are in the root of the repository, or specify a subfolder if applicable (e.g., `/frontend`).
    * **Build command**: Leave it empty, as our frontend is purely static with no build step required (no frameworks like React/Vue).
    * **Publish directory**: `.` (or the subfolder containing your static files, e.g., `/frontend`).
3.  **Deploy Site**: Click "Deploy site". Netlify will fetch your repository, deploy it, and provide you with a random URL.
4.  **Custom Domain (Optional but recommended)**: To use a domain like `datalaria.com/apps/weather/`:
    * Go to `Site settings > Domain management > Domains > Add a custom domain`.
    * Follow the steps to add your domain and configure it with your provider's DNS (by adding `CNAME` or `A` records).
    * For the specific path (`/apps/weather/`), you would typically configure a "subfolder" or "base URL" within your application if it's not directly at the root of the domain. In this case, our `index.html` is designed to be served from a subpath. Netlify handles this transparently once the site is deployed and your domain is configured.
    
It's that simple! Each `git push` to your configured branch will trigger a new deployment on Netlify, keeping your dashboard always up-to-date.

---

### The Frontend Tech Stack: HTML, CSS, and JavaScript (with a little help)

For this dashboard, I opted for a lightweight approach: plain HTML for structure, a bit of CSS for styling, and "vanilla" **JavaScript** (without complex frameworks) for interactivity. To handle specific tasks, I incorporated two fantastic libraries:

1.  [**PapaParse.js**](https://www.papaparse.com/): The fastest in-browser CSV parser for JavaScript. It's the bridge between our raw CSV files and the JavaScript data structures we need for visualization.
2.  [**Chart.js**](https://www.chartjs.org/): A powerful and flexible JavaScript charting library that makes creating beautiful, responsive, and interactive charts incredibly easy.

---

### The Dashboard Logic: Bringing Data to Life in `index.html`

Our `index.html` acts as the main canvas, orchestrating the fetching, parsing, and rendering of weather data.

#### 1. Dynamic City Loading

In stead of hardcoding a list of cities, we want our dashboard to automatically update if we add new cities in the backend. We achieve this by fetching a simple `ciudades.txt` file (containing one city name per line) and dynamically populating a `<select>` dropdown element using JavaScript's `fetch` API.

```javascript
const citySelector = document.getElementById('citySelector');
let myChart = null; // Global variable to store the Chart.js instance

async function loadCityList() {
    try {
        const response = await fetch('ciudades.txt');
        const text = await response.text();
        // Filter out empty lines from the text file
        const cities = text.split('\n').filter(line => line.trim() !== '');

        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelector.appendChild(option);
        });

        // Load the first city by default when the page initializes
        if (cities.length > 0) {
            loadAndDrawData(cities[0]);
        }
    } catch (error) {
        console.error('Error loading city list:', error);
        // Optional: Display a user-friendly error message
    }
}

// Trigger city loading when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', loadCityList);
```

#### 2. Reacting to User Selection

When a user selects a city from the dropdown, we need to respond immediately. An `addEventListener` on the `<select>` element detects the `change` event and calls our main function to fetch and draw the data for the newly selected city.

```javascript
citySelector.addEventListener('change', (event) => {
    const selectedCity = event.target.value;
    loadAndDrawData(selectedCity);
});
```

#### 3. Fetching, Parsing, and Drawing Data

This is the central function where everything comes to life. It is responsible for:

  * Constructing the URL for the specific city's CSV file (e.g., `data/Leon.csv`).
  * Using `Papa.parse` to download and process the CSV content directly in the browser. PapaParse handles asynchronous fetching and parsing, making it incredibly easy.
  * Extracting relevant `labels` (dates) and `data` (temperatures) from the parsed CSV for Chart.js.
  * **Crucial\!**: Before drawing a new chart, we must **destroy the previous Chart.js instance** (`if (myChart) { myChart.destroy(); }`). Forgetting this step leads to overlapping charts and performance issues! 💥
  * Creating a new `Chart()` instance with the updated data.
  * Additionally, it calls a function to load and display the AI prediction for that city, seamlessly integrating it into the dashboard.

```javascript
function loadAndDrawData(city) {
    const csvUrl = `datos/${city}.csv`; // Note the 'datos/' folder from Part 1
    const ctx = document.getElementById('weatherChart').getContext('2d');

    Papa.parse(csvUrl, {
        download: true, // Tells PapaParse to download the file
        header: true,   // Treats the first row as headers
        skipEmptyLines: true,
        complete: function(results) {
            const weatherData = results.data;

            // Extract labels (dates) and data (temperatures)
            const labels = weatherData.map(row => row.fecha_hora.split(' ')[0]); // Extract only the date
            const maxTemp = weatherData.map(row => parseFloat(row.temp_max_c));
            const minTemp = weatherData.map(row => parseFloat(row.temp_min_c));

            // Destroy the previous chart instance if it exists to prevent overlaps
            if (myChart) {
                myChart.destroy();
            }

            // Create a new Chart.js instance
            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: `Max Temp (°C) - ${city}`,
                        data: maxTemp,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1
                    }, {
                        label: `Min Temp (°C) - ${city}`,
                        data: minTemp,
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
            // Optional: display a user-friendly error message on the dashboard
            if (myChart) { myChart.destroy(); } // Clear chart if loading fails
        }
    });
}
```

#### 4. Displaying AI Predictions

The integration of AI predictions (which we'll delve into in Part 3) is also managed from the frontend. The backend generates a `predicciones.json` file, and our JavaScript simply fetches this JSON, finds the prediction for the selected city, and displays it.

```javascript
async function loadPrediction(city) {
    const predictionElement = document.getElementById('prediction');
    try {
        const response = await fetch('predicciones.json');
        const predictions = await response.json();
        if (predictions && predictions[city]) {
             predictionElement.textContent = `Max Temp. Prediction for tomorrow: ${predictions[city].toFixed(1)}°C`;
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

We've transformed raw data into an engaging and interactive experience! By combining static hosting from GitHub Pages or Netlify, "vanilla" JavaScript for logic, PapaParse.js for CSV handling, and Chart.js for beautiful visualizations, we've built a powerful frontend that is both free and highly effective.

The dashboard now provides immediate insight into the historical weather patterns of any selected city. But what about the future? In the **third and final part of this series**, we'll delve into the exciting world of **Machine Learning** to add a predictive layer to our service. We'll explore how to use historical data to forecast tomorrow's weather, turning our service into a true weather "oracle." Stay tuned!

---

### References and Links of Interest:

  * **Complete Web Service**: You can see the final project in action here: [https://datalaria.com/apps/weather/](https://datalaria.com/apps/weather/)
  * **Project GitHub Repository**: Explore the source code and project structure in my repository: [https://github.com/Dalaez/app_weather](https://github.com/Dalaez/app_weather)
  * **PapaParse.js**: Fast in-browser CSV parser for JavaScript: [https://www.papaparse.com/](https://www.papaparse.com/)
  * **Chart.js**: Simple, yet flexible JavaScript charting for designers & developers: [https://www.chartjs.org/](https://www.chartjs.org/)
  * **GitHub Pages**: Official documentation on how to host your sites: [https://docs.github.com/en/pages](https://docs.github.com/en/pages)
  * **Netlify**: Official Netlify website: [https://www.netlify.com/](https://www.netlify.com/)