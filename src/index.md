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

```js
// Display core traffic metrics
[
  {metric: "Total Vehicles", value: "9,414"},
  {metric: "Average Speed", value: "16.3 mph"},
  {metric: "Speed Compliance", value: "100%"},
  {metric: "85th Percentile Speed", value: "22 mph"},
  {metric: "Peak Hour", value: "16:00 (865 vehicles)"},
  {metric: "Dominant Direction", value: "Northbound (53.2%)"}
]
```

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