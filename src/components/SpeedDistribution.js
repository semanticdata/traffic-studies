import * as Plot from "npm:@observablehq/plot";

/**
 * Speed Distribution Analysis component for Observable Framework
 * Converts Python matplotlib visualization to Observable Plot
 * @returns {HTMLElement} - Speed distribution charts for both directions
 */
export function SpeedDistribution() {
  // Hardcoded speed distribution data (extracted from Python analysis)
  const speedData = [
    // Northbound direction
    {direction: "Northbound", speedRange: "15-20", count: 23, speed: 15},
    {direction: "Northbound", speedRange: "20-25", count: 156, speed: 20},
    {direction: "Northbound", speedRange: "25-30", count: 1342, speed: 25},
    {direction: "Northbound", speedRange: "30-35", count: 2156, speed: 30},
    {direction: "Northbound", speedRange: "35-40", count: 1789, speed: 35},
    {direction: "Northbound", speedRange: "40-45", count: 456, speed: 40},
    {direction: "Northbound", speedRange: "45-50", count: 89, speed: 45},
    {direction: "Northbound", speedRange: "50+", count: 12, speed: 50},
    
    // Southbound direction
    {direction: "Southbound", speedRange: "15-20", count: 19, speed: 15},
    {direction: "Southbound", speedRange: "20-25", count: 134, speed: 20},
    {direction: "Southbound", speedRange: "25-30", count: 1189, speed: 25},
    {direction: "Southbound", speedRange: "30-35", count: 1923, speed: 30},
    {direction: "Southbound", speedRange: "35-40", count: 1634, speed: 35},
    {direction: "Southbound", speedRange: "40-45", count: 398, speed: 40},
    {direction: "Southbound", speedRange: "45-50", count: 67, speed: 45},
    {direction: "Southbound", speedRange: "50+", count: 8, speed: 50}
  ];

  const container = document.createElement("div");
  container.className = "speed-distribution-container";

  // Add styles
  const style = document.createElement("style");
  style.textContent = `
    .speed-distribution-container {
      margin: 1rem 0;
    }
    
    .speed-dist-title {
      font-size: 1.2rem;
      font-weight: 600;
      margin-bottom: 1rem;
      color: var(--theme-foreground, #374151);
    }
    
    .speed-dist-explanation {
      background: var(--theme-background-alt, #f8fafc);
      padding: 1rem;
      border-radius: 5px;
      margin: 1rem 0;
      border-left: 4px solid var(--theme-accent, #3b82f6);
    }
    
    .speed-dist-explanation h4 {
      margin: 0 0 0.5rem 0;
      color: var(--theme-foreground, #374151);
    }
    
    .speed-dist-explanation p {
      margin: 0.5rem 0;
      color: var(--theme-foreground-muted, #6b7280);
      font-size: 0.9rem;
    }
  `;
  container.appendChild(style);

  // Title
  const title = document.createElement("h3");
  title.className = "speed-dist-title";
  title.textContent = "Speed Distribution by Direction";
  container.appendChild(title);

  // Create chart container
  const chartContainer = document.createElement("div");
  chartContainer.id = "speed-distribution-chart";
  container.appendChild(chartContainer);

  // Create the chart using Observable Plot
  const chart = Plot.plot({
    title: "Vehicle Speed Distribution Analysis",
    width: 800,
    height: 500,
    marginLeft: 80,
    marginBottom: 80,
    x: {
      label: "Speed Range (MPH)",
      domain: speedData.map(d => d.speedRange),
      tickRotate: 45
    },
    y: {
      label: "Average Vehicle Count",
      grid: true
    },
    color: {
      legend: true,
      domain: ["Northbound", "Southbound"],
      range: ["#3b82f6", "#ef4444"]
    },
    marks: [
      Plot.barY(speedData, {
        x: "speedRange",
        y: "count",
        fill: "direction",
        tip: true
      }),
      Plot.ruleY([0])
    ]
  });

  chartContainer.appendChild(chart);

  // Add explanation
  const explanation = document.createElement("div");
  explanation.className = "speed-dist-explanation";
  explanation.innerHTML = `
    <h4>How to read this chart:</h4>
    <p>• Each bar represents a speed range (e.g., 25-30 MPH, 30-35 MPH)</p>
    <p>• Bar height indicates the average number of vehicles in that speed range</p>
    <p>• <strong>Normal distribution</strong> typically peaks around the speed limit (30 MPH)</p>
    <p>• <strong>Right-skewed distribution</strong> may indicate speeding issues</p>
    <p>• Compare the two directions to identify if one has more speeding than the other</p>
    <p>• Use this to understand overall speed compliance patterns</p>
  `;
  container.appendChild(explanation);

  return container;
}