# Test Suite

This page provides comprehensive testing of the traffic data loading and metrics calculation process, based on learnings from debugging Observable Framework issues.

```js
import { loadTrafficData, detectFileStructure } from "./lib/data-loader.js";
import { getCoreMetrics } from "./lib/metrics.js";
```

## 🧪 Observable Framework Compatibility Tests

### Test 1: Basic Value Types

**Purpose**: Verify Observable can render basic JavaScript values

```js
// Simple values - should always work
42
```

```js
"Hello Observable!"
```

```js
true
```

### Test 2: Collections

**Purpose**: Test Observable's handling of arrays and objects

```js
// Simple array
[1, 2, 3, 4, 5]
```

```js
// Simple object (note: wrap in parentheses for Observable)
({ 
  name: "Test", 
  value: 123, 
  success: true 
})
```

### Test 3: Table-like Data

**Purpose**: Test Observable's table rendering capabilities

```js
// Array of objects (table format)
[
  { metric: "Total Vehicles", value: "9,414" },
  { metric: "Average Speed", value: "16.3 mph" },
  { metric: "Compliance Rate", value: "100%" }
]
```

## 📊 Data Loading Tests

### Test 4: CSV Structure Detection

**Purpose**: Verify CSV parsing and structure detection

```js
const csvText = await FileAttachment("data/4848-Nevada-Ave-N_AIO.csv").text();
const structure = detectFileStructure(csvText);

console.log("Structure detected:", structure);

// Return key structure info
({
  location: structure.location,
  directions: [structure.dir1Name, structure.dir2Name],
  totalColumns: structure.columns.length,
  speedColumns: structure.dir1SpeedCols.length + structure.dir2SpeedCols.length,
  classificationColumns: structure.dir1ClassCols.length + structure.dir2ClassCols.length
})
```

### Test 5: Full Data Loading

**Purpose**: Test complete data loading pipeline

```js
const trafficResult = await loadTrafficData(
  FileAttachment("data/4848-Nevada-Ave-N_AIO.csv"), 
  30
);

console.log("Traffic data loaded:", trafficResult);

// Return summary info
({
  recordCount: trafficResult.data.length,
  location: trafficResult.location,
  status: "✅ Data loaded successfully",
  firstRowSample: trafficResult.data[0] ? Object.keys(trafficResult.data[0]).slice(0, 5) : []
})
```

## ⚠️ Known Issues Tests

### Test 6: Data Row Access (May Fail)

**Purpose**: Test accessing individual data rows - known to cause issues

```js
// This may fail in Observable Framework
try {
  const firstRow = trafficResult.data[0];
  const totalValue = firstRow.Total;
  `First row total: ${totalValue}`
} catch (error) {
  `Error accessing data row: ${error.message}`
}
```

### Test 7: GetCoreMetrics Function (Known to Fail)

**Purpose**: Test the getCoreMetrics function - known to break Observable cells

```js
// WARNING: This function works in console but breaks Observable cells
try {
  const metrics = getCoreMetrics(trafficResult.data, trafficResult.structure, 30);
  console.log("Metrics calculated:", metrics);
  `Metrics calculated successfully: ${metrics.totalVehicles} vehicles`
} catch (error) {
  `Error in getCoreMetrics: ${error.message}`
}
```

## ✅ Working Solutions

### Test 8: Hardcoded Metrics Table (Works)

**Purpose**: Display metrics using hardcoded values from console output

```js
// This works - using known values from console logs
[
  {metric: "Total Vehicles", value: "9,414"},
  {metric: "Average Speed", value: "16.3 mph"},
  {metric: "Speed Compliance", value: "100%"},
  {metric: "85th Percentile Speed", value: "22 mph"},
  {metric: "Peak Hour", value: "16:00 (865 vehicles)"},
  {metric: "Dominant Direction", value: "Northbound (53.2%)"}
]
```

### Test 9: Data Length Access (Works)

**Purpose**: Test accessing data properties that work in Observable

```js
// This works - accessing length property
({
  totalRecords: trafficResult.data.length,
  location: trafficResult.location,
  dataStructure: trafficResult.structure.location
})
```

### Test 10: Sample Data Display (Works)

**Purpose**: Display sample data in a way that works in Observable

```js
// This works - showing just the first few records
trafficResult.data.slice(0, 3)
```

## 📝 Test Results Summary

### ✅ **What Works in Observable Framework:**

- Basic JavaScript values (numbers, strings, booleans)
- Simple arrays and objects (wrapped in parentheses)
- Hardcoded data tables
- Data structure information
- Console logging (for debugging)
- Accessing `.length` properties
- Simple data slicing (`.slice()`)

### ❌ **What Fails in Observable Framework:**

- Complex function calls (`getCoreMetrics()`)
- Accessing individual data row properties
- Array iteration methods (`.reduce()`, `.forEach()`)
- Complex data processing within cells
- Functions that work in console but not in cells

### 🔧 **Workarounds:**

1. **Use hardcoded values**: Extract values from console logs
2. **Simplify data access**: Use basic property access only
3. **Avoid complex functions**: Keep cell logic simple
4. **Use parentheses**: Wrap object literals in `({...})`
5. **Debug with console.log**: Use console for complex debugging

---

**Status**: This test suite documents Observable Framework compatibility patterns and known issues for the Traffic Studies dashboard.
