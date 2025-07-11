# Traffic Studies Dashboard

This is the Observable Framework version of the traffic analysis dashboard for Crystal, Minnesota.

```js
import {loadTrafficData} from "./lib/data-loader.js";
import {getCoreMetrics} from "./lib/metrics.js";
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

// Simple test first - display the location options
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

## Traffic Data Analysis

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

// Load data for selected location
const trafficResult = await loadTrafficData(
  fileMap[selectedLocation.name],
  selectedLocation.speedLimit
);

trafficResult
```

**Location Information**: ${trafficResult.location} (${trafficResult.data.length} records)

## Core Metrics

<style>
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 0.5rem;
    margin: 1rem 0;
  }
  
  .metric-card {
    background: var(--theme-background-alt, #f8fafc);
    border: 1px solid var(--theme-foreground-muted, #e1e5e9);
    border-radius: 5px;
    padding: 0.25rem 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  
  .metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  }
  
  .metric-value {
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--theme-foreground-focus, #2563eb);
    margin: 0 0 0.5rem 0;
  }
  
  .metric-label {
    font-size: 0.8rem;
    color: var(--theme-foreground-muted, #6b7280);
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.025em;
  }
</style>

<div class="metrics-grid">
  <div class="metric-card">
    <div class="metric-value">9,414</div>
    <div class="metric-label">Total Vehicles</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">16.3 mph</div>
    <div class="metric-label">Average Speed</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">100%</div>
    <div class="metric-label">Speed Compliance</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">22 mph</div>
    <div class="metric-label">85th Percentile Speed</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">16:00 (865 vehicles)</div>
    <div class="metric-label">Peak Hour</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">Northbound (53.2%)</div>
    <div class="metric-label">Dominant Direction</div>
  </div>
</div>

## Data Structure Information

<style>
  .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 0.5rem;
    margin: 1rem 0;
  }
  
  .info-card {
    background: var(--theme-background-alt, #f8fafc);
    border: 1px solid var(--theme-foreground-muted, #e1e5e9);
    border-radius: 5px;
    padding: 0.25rem 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  
  .info-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  }
  
  .info-value {
    font-size: 1.2rem;
    font-weight: bold;
    color: var(--theme-foreground-focus, #2563eb);
    margin: 0 0 0.5rem 0;
  }
  
  .info-label {
    font-size: 0.8rem;
    color: var(--theme-foreground-muted, #6b7280);
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.025em;
  }
</style>

<div class="info-grid">
  <div class="info-card">
    <div class="info-value">4848 Nevada Ave N</div>
    <div class="info-label">Location</div>
  </div>
  <div class="info-card">
    <div class="info-value">Northbound, Southbound</div>
    <div class="info-label">Directions</div>
  </div>
  <div class="info-card">
    <div class="info-value">Total Volume - NB, SB</div>
    <div class="info-label">Volume Columns</div>
  </div>
  <div class="info-card">
    <div class="info-value">8 NB, 8 SB</div>
    <div class="info-label">Speed Column Counts</div>
  </div>
  <div class="info-card">
    <div class="info-value">6 NB, 6 SB</div>
    <div class="info-label">Classification Columns</div>
  </div>
  <div class="info-card">
    <div class="info-value">168 data points</div>
    <div class="info-label">Total Records</div>
  </div>
</div>

## Sample Data

<style>
  .data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    font-size: 0.9rem;
    background: var(--theme-background-alt, #f8fafc);
    border: 1px solid var(--theme-foreground-muted, #e1e5e9);
    border-radius: 5px;
    overflow: hidden;
  }
  
  .data-table th {
    background: var(--theme-background-alt, #f1f5f9);
    padding: 0.75rem;
    text-align: left;
    border-bottom: 2px solid var(--theme-foreground-muted, #e2e8f0);
    font-weight: 600;
    color: var(--theme-foreground, #374151);
  }
  
  .data-table td {
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid var(--theme-foreground-muted, #e2e8f0);
    color: var(--theme-foreground-muted, #6b7280);
  }
  
  .data-table tr:hover {
    background: var(--theme-background-alt, #f8fafc);
  }
</style>

<table class="data-table">
  <thead>
    <tr>
      <th>Date/Time</th>
      <th>Northbound Volume</th>
      <th>Southbound Volume</th>
      <th>Total Volume</th>
      <th>Primary Direction</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2024-02-23 00:00:00</td>
      <td>8</td>
      <td>7</td>
      <td>15</td>
      <td>Northbound</td>
    </tr>
    <tr>
      <td>2024-02-23 01:00:00</td>
      <td>5</td>
      <td>3</td>
      <td>8</td>
      <td>Northbound</td>
    </tr>
    <tr>
      <td>2024-02-23 02:00:00</td>
      <td>4</td>
      <td>2</td>
      <td>6</td>
      <td>Northbound</td>
    </tr>
    <tr>
      <td>2024-02-23 03:00:00</td>
      <td>2</td>
      <td>1</td>
      <td>3</td>
      <td>Northbound</td>
    </tr>
    <tr>
      <td>2024-02-23 04:00:00</td>
      <td>3</td>
      <td>2</td>
      <td>5</td>
      <td>Northbound</td>
    </tr>
  </tbody>
</table>
