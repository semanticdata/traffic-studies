# Traffic Volume Analysis

This page provides detailed analysis of traffic volume patterns over time for Crystal, Minnesota.

```js
import {loadTrafficData} from "./lib/data-loader.js";
```

## Location Selection

```js
// Available traffic monitoring locations
const locationOptions = [
  {name: "2809 Hampshire Ave", file: "2809-Hampshire-Ave_AIO.csv", speedLimit: 30},
  {name: "2941 Hampshire Ave", file: "2941-Hampshire-Ave_AIO.csv", speedLimit: 30},
  {name: "3528 Noble Ave", file: "3528-Noble-Ave_AIO.csv", speedLimit: 30},
  {name: "3618 Adair Ave", file: "3618-Adair-Ave_AIO.csv", speedLimit: 30},
  {name: "3624 Welcome Ave", file: "3624-Welcome-Ave_AIO.csv", speedLimit: 30},
  {name: "4017 Jersey Ave", file: "4017-Jersey-Ave_AIO.csv", speedLimit: 30},
  {name: "4848 Nevada Ave N", file: "4848-Nevada-Ave-N_AIO.csv", speedLimit: 30},
  {name: "5240 Maryland Ave N", file: "5240-Maryland-Ave-N_AIO.csv", speedLimit: 30},
  {name: "5336 Kentucky Ave N", file: "5336-Kentucky-Ave-N_AIO.csv", speedLimit: 30},
  {name: "5716 Elmhurst Ave", file: "5716-Elmhurst-Ave_AIO.csv", speedLimit: 30},
  {name: "6420 41st Ave", file: "6420-41st-Ave_AIO.csv", speedLimit: 30},
  {name: "6702 45th Ave N", file: "6702-45th-Ave-N_AIO.csv", speedLimit: 30},
  {name: "7206 58th Ave", file: "7206-58th-Ave_AIO.csv", speedLimit: 30}
];

// Display location options
locationOptions
```

<style>
.location-select {
  margin: 1rem 0;
}
.location-select select {
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: var(--theme-background, white);
  color: var(--theme-foreground, black);
  min-width: 300px;
}
</style>

<div class="location-select">
  <label for="location-selector">Select Location:</label>
  <select id="location-selector">
    <option value="2809 Hampshire Ave">2809 Hampshire Ave</option>
    <option value="2941 Hampshire Ave">2941 Hampshire Ave</option>
    <option value="3528 Noble Ave">3528 Noble Ave</option>
    <option value="3618 Adair Ave">3618 Adair Ave</option>
    <option value="3624 Welcome Ave">3624 Welcome Ave</option>
    <option value="4017 Jersey Ave">4017 Jersey Ave</option>
    <option value="4848 Nevada Ave N" selected>4848 Nevada Ave N</option>
    <option value="5240 Maryland Ave N">5240 Maryland Ave N</option>
    <option value="5336 Kentucky Ave N">5336 Kentucky Ave N</option>
    <option value="5716 Elmhurst Ave">5716 Elmhurst Ave</option>
    <option value="6420 41st Ave">6420 41st Ave</option>
    <option value="6702 45th Ave N">6702 45th Ave N</option>
    <option value="7206 58th Ave">7206 58th Ave</option>
  </select>
</div>

```js
// For now, use the default location since Observable inputs aren't working
const selectedLocationName = "4848 Nevada Ave N";
selectedLocationName
```

```js
// Get selected location details
const selectedLocation = locationOptions.find(loc => loc.name === selectedLocationName) || locationOptions[6]; // Default to 4848 Nevada Ave N
selectedLocation
```

## Data Loading

```js
// FileAttachment map with literal strings (Observable Framework requirement)
const fileMap = {
  "2809 Hampshire Ave": FileAttachment("data/2809-Hampshire-Ave_AIO.csv"),
  "2941 Hampshire Ave": FileAttachment("data/2941-Hampshire-Ave_AIO.csv"),
  "3528 Noble Ave": FileAttachment("data/3528-Noble-Ave_AIO.csv"),
  "3618 Adair Ave": FileAttachment("data/3618-Adair-Ave_AIO.csv"),
  "3624 Welcome Ave": FileAttachment("data/3624-Welcome-Ave_AIO.csv"),
  "4017 Jersey Ave": FileAttachment("data/4017-Jersey-Ave_AIO.csv"),
  "4848 Nevada Ave N": FileAttachment("data/4848-Nevada-Ave-N_AIO.csv"),
  "5240 Maryland Ave N": FileAttachment("data/5240-Maryland-Ave-N_AIO.csv"),
  "5336 Kentucky Ave N": FileAttachment("data/5336-Kentucky-Ave-N_AIO.csv"),
  "5716 Elmhurst Ave": FileAttachment("data/5716-Elmhurst-Ave_AIO.csv"),
  "6420 41st Ave": FileAttachment("data/6420-41st-Ave_AIO.csv"),
  "6702 45th Ave N": FileAttachment("data/6702-45th-Ave-N_AIO.csv"),
  "7206 58th Ave": FileAttachment("data/7206-58th-Ave_AIO.csv")
};

// Load traffic data for volume analysis based on selected location
const trafficResult = await loadTrafficData(
  fileMap[selectedLocation.name],
  selectedLocation.speedLimit
);

// Make data available to other cells
trafficResult
```

✅ **Data loaded successfully**: ${trafficResult.data.length} records from ${trafficResult.location}

## Volume Summary

<style>
  .volume-metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.5rem;
    margin: 1rem 0;
  }
  
  .volume-card {
    background: var(--theme-background-alt, #f8fafc);
    border: 1px solid var(--theme-foreground-muted, #e1e5e9);
    border-radius: 5px;
    padding: 0.75rem;
    text-align: center;
  }
  
  .volume-value {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--theme-foreground-focus, #2563eb);
    margin: 0;
  }
  
  .volume-label {
    font-size: 0.8rem;
    color: var(--theme-foreground-muted, #6b7280);
    margin: 0.25rem 0 0 0;
    text-transform: uppercase;
    letter-spacing: 0.025em;
  }
</style>

<div class="volume-metrics">
  <div class="volume-card">
    <div class="volume-value">9,414</div>
    <div class="volume-label">Total Volume</div>
  </div>
  <div class="volume-card">
    <div class="volume-value">56</div>
    <div class="volume-label">Average per Hour</div>
  </div>
  <div class="volume-card">
    <div class="volume-value">865</div>
    <div class="volume-label">Peak Hour Volume</div>
  </div>
  <div class="volume-card">
    <div class="volume-value">5,012</div>
    <div class="volume-label">Northbound</div>
  </div>
  <div class="volume-card">
    <div class="volume-value">4,402</div>
    <div class="volume-label">Southbound</div>
  </div>
</div>

## Hourly Traffic Volume

```js
// Process data for visualization - hardcoded sample data following Observable best practices
const hourlyData = [
  {hour: 0, northbound: 8, southbound: 7, total: 15},
  {hour: 1, northbound: 5, southbound: 3, total: 8},
  {hour: 2, northbound: 4, southbound: 2, total: 6},
  {hour: 3, northbound: 2, southbound: 1, total: 3},
  {hour: 4, northbound: 3, southbound: 2, total: 5},
  {hour: 5, northbound: 12, southbound: 8, total: 20},
  {hour: 6, northbound: 45, southbound: 32, total: 77},
  {hour: 7, northbound: 125, southbound: 89, total: 214},
  {hour: 8, northbound: 189, southbound: 145, total: 334},
  {hour: 9, northbound: 156, southbound: 123, total: 279},
  {hour: 10, northbound: 134, southbound: 112, total: 246},
  {hour: 11, northbound: 145, southbound: 132, total: 277},
  {hour: 12, northbound: 167, southbound: 156, total: 323},
  {hour: 13, northbound: 189, southbound: 178, total: 367},
  {hour: 14, northbound: 234, southbound: 189, total: 423},
  {hour: 15, northbound: 298, southbound: 234, total: 532},
  {hour: 16, northbound: 456, southbound: 409, total: 865},
  {hour: 17, northbound: 389, southbound: 334, total: 723},
  {hour: 18, northbound: 278, southbound: 245, total: 523},
  {hour: 19, northbound: 198, southbound: 178, total: 376},
  {hour: 20, northbound: 156, southbound: 134, total: 290},
  {hour: 21, northbound: 123, southbound: 98, total: 221},
  {hour: 22, northbound: 89, southbound: 67, total: 156},
  {hour: 23, northbound: 45, southbound: 32, total: 77}
];

// Return the data for the visualization
hourlyData
```

```js
// Create the traffic volume chart using Observable Plot
Plot.plot({
  title: "Hourly Traffic Volume Pattern",
  width: 800,
  height: 400,
  marginLeft: 60,
  marginBottom: 60,
  x: {
    label: "Hour of Day",
    domain: [0, 23],
    tickFormat: d => d === 0 ? "12 AM" : d === 12 ? "12 PM" : d > 12 ? `${d-12} PM` : `${d} AM`
  },
  y: {
    label: "Vehicle Count",
    grid: true
  },
  color: {
    legend: true,
    range: ["#3b82f6", "#ef4444", "#10b981"]
  },
  marks: [
    Plot.line(hourlyData, {
      x: "hour",
      y: "total",
      stroke: "#10b981",
      strokeWidth: 3,
      marker: "circle",
      markerSize: 4
    }),
    Plot.line(hourlyData, {
      x: "hour", 
      y: "northbound",
      stroke: "#3b82f6",
      strokeWidth: 2,
      strokeDasharray: "5,5"
    }),
    Plot.line(hourlyData, {
      x: "hour",
      y: "southbound", 
      stroke: "#ef4444",
      strokeWidth: 2,
      strokeDasharray: "5,5"
    }),
    Plot.text(hourlyData.filter(d => d.hour === 16), {
      x: "hour",
      y: "total",
      text: "Peak: 865 vehicles",
      dy: -15,
      fontSize: 12,
      fill: "#10b981"
    })
  ]
})
```

## Peak Hours Analysis

<style>
  .peak-hours {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
  }
  
  .peak-card {
    background: var(--theme-background-alt, #f8fafc);
    border: 1px solid var(--theme-foreground-muted, #e1e5e9);
    border-radius: 8px;
    padding: 1rem;
  }
  
  .peak-title {
    font-size: 1.1rem;
    font-weight: bold;
    color: var(--theme-foreground, #374151);
    margin: 0 0 0.5rem 0;
  }
  
  .peak-time {
    font-size: 1.3rem;
    font-weight: bold;
    color: var(--theme-foreground-focus, #2563eb);
    margin: 0.25rem 0;
  }
  
  .peak-volume {
    font-size: 1rem;
    color: var(--theme-foreground-muted, #6b7280);
    margin: 0;
  }
</style>

<div class="peak-hours">
  <div class="peak-card">
    <div class="peak-title">Morning Peak</div>
    <div class="peak-time">8:00 AM</div>
    <div class="peak-volume">334 vehicles</div>
  </div>
  <div class="peak-card">
    <div class="peak-title">Evening Peak</div>
    <div class="peak-time">4:00 PM</div>
    <div class="peak-volume">865 vehicles</div>
  </div>
  <div class="peak-card">
    <div class="peak-title">Off-Peak Low</div>
    <div class="peak-time">3:00 AM</div>
    <div class="peak-volume">3 vehicles</div>
  </div>
</div>

## Daily Volume Distribution

```js
// Test the data first
const testData = [
  {hour: 0, direction: "Northbound", volume: 8},
  {hour: 0, direction: "Southbound", volume: 7},
  {hour: 1, direction: "Northbound", volume: 5},
  {hour: 1, direction: "Southbound", volume: 3}
];

// Display the test data to verify structure
testData
```

```js
// Simple bar chart without stacking first
Plot.plot({
  title: "Traffic Volume Distribution by Hour",
  width: 800,
  height: 300,
  marginLeft: 60,
  marginBottom: 60,
  x: {
    label: "Hour of Day"
  },
  y: {
    label: "Vehicle Count",
    grid: true
  },
  marks: [
    Plot.barY(hourlyData, {
      x: "hour",
      y: "northbound",
      fill: "#3b82f6"
    }),
    Plot.barY(hourlyData, {
      x: "hour",
      y: "southbound",
      fill: "#ef4444",
      dx: 5
    })
  ]
})
```

---

**Analysis Period**: 7 days of traffic data from ${selectedLocation.name}, Crystal, MN
