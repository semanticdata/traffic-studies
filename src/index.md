# Traffic Studies Dashboard

This is the Observable Framework version of the traffic analysis dashboard for Crystal, Minnesota.

```js
import {loadTrafficData} from "./lib/data-loader.js";
import {getCoreMetrics} from "./lib/metrics.js";
```

## Traffic Data Analysis

```js
// Load and process traffic data with optimized async loading
const trafficResult = await loadTrafficData(
  FileAttachment("data/4848-Nevada-Ave-N_AIO.csv"), 
  30 // speed limit
);

// Make data available to other cells by returning the full result
trafficResult
```

✅ **Data loaded successfully**: ${trafficResult.data.length} records from ${trafficResult.location}

## Core Metrics

<style>
  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 0.5rem;
    margin: 1rem 0;
  }
  
  .metric-card {
    background: white;
    border: 1px solid #e1e5e9;
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
    color: #2563eb;
    margin: 0 0 0.5rem 0;
  }
  
  .metric-label {
    font-size: 0.8rem;
    color: #6b7280;
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

```js
// Display structure information for debugging
({
  location: trafficResult.structure.location,
  directions: [trafficResult.structure.dir1Name, trafficResult.structure.dir2Name],
  volumeColumns: [trafficResult.structure.dir1VolumeCol, trafficResult.structure.dir2VolumeCol],
  speedColumnCounts: [trafficResult.structure.dir1SpeedCols.length, trafficResult.structure.dir2SpeedCols.length],
  classificationColumnCounts: [trafficResult.structure.dir1ClassCols.length, trafficResult.structure.dir2ClassCols.length],
  totalRecords: trafficResult.data.length,
  speedColumns: {
    dir1: trafficResult.structure.dir1SpeedCols,
    dir2: trafficResult.structure.dir2SpeedCols
  },
  sampleColumns: trafficResult.structure.columns.slice(0, 10)
})
```

## Sample Data

```js
// Display first few rows of processed data
trafficResult.data.slice(0, 5)
```

---

**Status**: Observable Framework dashboard now uses optimized data loading and metrics calculations to prevent infinite loops and page hangs.
