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
      margin: 2rem 0;
    }
    
    .speed-dist-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 1.5rem;
      color: var(--theme-foreground, #374151);
      background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-align: center;
    }
    
    .speed-dist-summary {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1.5rem;
      margin: 2rem 0;
    }
    
    .speed-dist-card {
      background: linear-gradient(135deg, var(--theme-background-alt, #f8fafc) 0%, var(--theme-background, #ffffff) 100%);
      padding: 1.5rem;
      border-radius: 12px;
      border: 1px solid var(--theme-foreground-muted, #e1e5e9);
      text-align: center;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
      transition: all 0.3s ease;
      position: relative;
      overflow: hidden;
    }
    
    .speed-dist-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .speed-dist-label {
      font-size: 0.9rem;
      font-weight: 500;
      color: var(--theme-foreground-muted, #6b7280);
      margin-bottom: 0.5rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .speed-dist-value {
      font-size: 1.8rem;
      font-weight: 700;
      color: var(--theme-foreground, #374151);
      margin: 0.5rem 0;
    }
    
    .speed-dist-peak {
      color: #10b981;
    }
    
    .speed-dist-average {
      color: #3b82f6;
    }
    
    .speed-dist-explanation {
      background: linear-gradient(135deg, var(--theme-background-alt, #f8fafc) 0%, var(--theme-background, #ffffff) 100%);
      padding: 1.5rem;
      border-radius: 12px;
      margin: 2rem 0;
      border-left: 4px solid;
      border-image: linear-gradient(135deg, #3b82f6, #6366f1) 1;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .speed-dist-explanation h4 {
      margin: 0 0 1rem 0;
      color: var(--theme-foreground, #374151);
      font-size: 1.1rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .speed-dist-explanation h4::before {
      content: '📊';
      font-size: 1.2rem;
    }
    
    .speed-dist-explanation p {
      margin: 0.75rem 0;
      color: var(--theme-foreground-muted, #6b7280);
      font-size: 0.95rem;
      line-height: 1.6;
      padding-left: 1rem;
      position: relative;
    }
    
    .speed-dist-explanation p::before {
      content: '•';
      position: absolute;
      left: 0;
      color: #3b82f6;
      font-weight: bold;
    }
  `;
  container.appendChild(style);

  // Title
  const title = document.createElement("h3");
  title.className = "speed-dist-title";
  title.textContent = "Speed Distribution by Direction";
  container.appendChild(title);

  // Calculate summary statistics
  const peakSpeedRange = speedData.reduce((max, d) => d.count > max.count ? d : max);
  const averageCount = speedData.reduce((sum, d) => sum + d.count, 0) / speedData.length;
  const totalVehicles = speedData.reduce((sum, d) => sum + d.count, 0);

  // Summary cards
  const summaryContainer = document.createElement("div");
  summaryContainer.className = "speed-dist-summary";
  
  const cards = [
    {label: "Peak Speed Range", value: peakSpeedRange.speedRange, class: "speed-dist-peak"},
    {label: "Average per Range", value: Math.round(averageCount).toLocaleString(), class: "speed-dist-average"},
    {label: "Total Vehicles", value: totalVehicles.toLocaleString(), class: "speed-dist-value"}
  ];

  cards.forEach(card => {
    const cardElement = document.createElement("div");
    cardElement.className = "speed-dist-card";
    cardElement.innerHTML = `
      <div class="speed-dist-label">${card.label}</div>
      <div class="speed-dist-value ${card.class}">${card.value}</div>
    `;
    summaryContainer.appendChild(cardElement);
  });
  
  container.appendChild(summaryContainer);

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
    style: {
      background: "transparent",
      fontFamily: "system-ui, sans-serif"
    },
    x: {
      label: "Speed Range (MPH)",
      domain: speedData.map(d => d.speedRange),
      tickRotate: 45
    },
    y: {
      label: "Average Vehicle Count",
      grid: true,
      tickFormat: "~s"
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
        tip: true,
        rx: 3
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