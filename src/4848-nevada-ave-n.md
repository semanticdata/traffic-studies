```js
import {loadTrafficData} from "./lib/data-loader.js";
import {getCoreMetrics} from "./lib/metrics.js";
import {LocationOverview} from "./components/LocationOverview.js";
import {CoreMetrics} from "./components/CoreMetrics.js";
import {VolumeMetrics} from "./components/VolumeMetrics.js";
import {PeakHours} from "./components/PeakHours.js";
import {DataTable} from "./components/DataTable.js";
import {getHourlyData} from "./components/HourlyData.js";
```

```js
// Load traffic data for this specific location
const trafficResult = await loadTrafficData(
  FileAttachment("data/4848-Nevada-Ave-N_AIO.csv"),
  30
);

trafficResult
```

# 4848 Nevada Ave N - Traffic Report

Comprehensive traffic analysis for ${trafficResult.location}, Crystal, Minnesota.

## Location Overview

```js
// Use the LocationOverview component
LocationOverview(trafficResult, 30)
```

## Core Metrics

```js
// Calculate core metrics for this location
const coreMetrics = getCoreMetrics(trafficResult.data, trafficResult.structure, 30);
coreMetrics
```

```js
// Use the CoreMetrics component
CoreMetrics(coreMetrics)
```

## Traffic Volume Analysis

### Volume Summary

```js
// Use the VolumeMetrics component
VolumeMetrics()
```

### Hourly Traffic Volume

```js
// Get hourly data from component
const hourlyData = getHourlyData();
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

### Peak Hours Analysis

```js
// Use the PeakHours component
PeakHours()
```

### Daily Volume Distribution

```js
// Simple bar chart showing directional volume distribution
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

## Data Analysis Summary

```js
// Display sample data for verification
const sampleData = trafficResult.data.slice(0, 5);
console.log("Sample data:", sampleData);
sampleData
```

```js
// Use the DataTable component
DataTable(sampleData)
```

### Data Summary

**Analysis Period**: 7 days of continuous traffic monitoring  
**Equipment**: PicoCount 2500 Traffic Counter  
**Data Quality**: ${trafficResult.data.length} validated records  
**Primary Direction**: Northbound (53.2% of total traffic)  

---

[← Back to Location Directory](./)
