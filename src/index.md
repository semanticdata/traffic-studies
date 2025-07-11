# Traffic Studies Dashboard

This is the Observable Framework version of the traffic analysis dashboard for Crystal, Minnesota.

```js
import {loadTrafficData} from "./lib/data-loader.js";
import {getCoreMetrics} from "./lib/metrics.js";
```

```js
// Load and process traffic data with optimized async loading
const trafficResult = await loadTrafficData(
  FileAttachment("data/4848-Nevada-Ave-N_AIO.csv"), 
  30 // speed limit
);

// Make data available to other cells by returning the full result
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
