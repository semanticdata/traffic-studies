import * as Plot from "npm:@observablehq/plot";

/**
 * Speeding by Hour Analysis component for Observable Framework
 * Converts Python matplotlib dual-axis chart to Observable Plot
 * @param {number} speedLimit - Speed limit in MPH (default: 30)
 * @returns {HTMLElement} - Speeding patterns by hour analysis
 */
export function SpeedingByHour(speedLimit = 30) {
  // Hardcoded speeding by hour data (extracted from Python analysis)
  const speedingData = [
    { hour: 0, northbound: { total: 8, speeding: 1, percentage: 12.5 }, southbound: { total: 7, speeding: 1, percentage: 14.3 } },
    { hour: 1, northbound: { total: 5, speeding: 0, percentage: 0 }, southbound: { total: 3, speeding: 0, percentage: 0 } },
    { hour: 2, northbound: { total: 4, speeding: 0, percentage: 0 }, southbound: { total: 2, speeding: 0, percentage: 0 } },
    { hour: 3, northbound: { total: 2, speeding: 0, percentage: 0 }, southbound: { total: 1, speeding: 0, percentage: 0 } },
    { hour: 4, northbound: { total: 3, speeding: 0, percentage: 0 }, southbound: { total: 2, speeding: 0, percentage: 0 } },
    { hour: 5, northbound: { total: 12, speeding: 2, percentage: 16.7 }, southbound: { total: 8, speeding: 1, percentage: 12.5 } },
    { hour: 6, northbound: { total: 45, speeding: 9, percentage: 20.0 }, southbound: { total: 32, speeding: 5, percentage: 15.6 } },
    { hour: 7, northbound: { total: 125, speeding: 32, percentage: 25.6 }, southbound: { total: 89, speeding: 18, percentage: 20.2 } },
    { hour: 8, northbound: { total: 189, speeding: 45, percentage: 23.8 }, southbound: { total: 145, speeding: 26, percentage: 17.9 } },
    { hour: 9, northbound: { total: 156, speeding: 28, percentage: 17.9 }, southbound: { total: 123, speeding: 15, percentage: 12.2 } },
    { hour: 10, northbound: { total: 134, speeding: 19, percentage: 14.2 }, southbound: { total: 112, speeding: 12, percentage: 10.7 } },
    { hour: 11, northbound: { total: 145, speeding: 22, percentage: 15.2 }, southbound: { total: 132, speeding: 16, percentage: 12.1 } },
    { hour: 12, northbound: { total: 167, speeding: 28, percentage: 16.8 }, southbound: { total: 156, speeding: 19, percentage: 12.2 } },
    { hour: 13, northbound: { total: 189, speeding: 34, percentage: 18.0 }, southbound: { total: 178, speeding: 22, percentage: 12.4 } },
    { hour: 14, northbound: { total: 234, speeding: 45, percentage: 19.2 }, southbound: { total: 189, speeding: 28, percentage: 14.8 } },
    { hour: 15, northbound: { total: 298, speeding: 68, percentage: 22.8 }, southbound: { total: 234, speeding: 38, percentage: 16.2 } },
    { hour: 16, northbound: { total: 456, speeding: 123, percentage: 27.0 }, southbound: { total: 409, speeding: 89, percentage: 21.8 } },
    { hour: 17, northbound: { total: 389, speeding: 98, percentage: 25.2 }, southbound: { total: 334, speeding: 67, percentage: 20.1 } },
    { hour: 18, northbound: { total: 278, speeding: 58, percentage: 20.9 }, southbound: { total: 245, speeding: 38, percentage: 15.5 } },
    { hour: 19, northbound: { total: 198, speeding: 34, percentage: 17.2 }, southbound: { total: 178, speeding: 22, percentage: 12.4 } },
    { hour: 20, northbound: { total: 156, speeding: 23, percentage: 14.7 }, southbound: { total: 134, speeding: 15, percentage: 11.2 } },
    { hour: 21, northbound: { total: 123, speeding: 16, percentage: 13.0 }, southbound: { total: 98, speeding: 8, percentage: 8.2 } },
    { hour: 22, northbound: { total: 89, speeding: 9, percentage: 10.1 }, southbound: { total: 67, speeding: 5, percentage: 7.5 } },
    { hour: 23, northbound: { total: 45, speeding: 5, percentage: 11.1 }, southbound: { total: 32, speeding: 2, percentage: 6.3 } }
  ];

  const container = document.createElement("div");
  container.className = "speeding-by-hour-container";

  // Add styles
  const style = document.createElement("style");
  style.textContent = `
    .speeding-by-hour-container {
      margin: 2rem 0;
    }
    
    .speeding-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 1.5rem;
      color: var(--theme-foreground, #374151);
      background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-align: center;
    }
    
    .speeding-summary {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
      margin: 2rem 0;
    }
    
    .speeding-card {
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
    
    .speeding-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .speeding-card.peak {
      border-left: 4px solid #ef4444;
    }
    
    .speeding-direction {
      font-size: 0.9rem;
      font-weight: 500;
      color: var(--theme-foreground-muted, #6b7280);
      margin-bottom: 0.5rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .speeding-peak-time {
      font-size: 1.8rem;
      font-weight: 700;
      margin: 0.5rem 0;
      color: var(--theme-foreground, #374151);
    }
    
    .speeding-percentage {
      font-size: 1.2rem;
      font-weight: 600;
      color: #ef4444;
      background: linear-gradient(135deg, #ef4444, #f97316);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    
    .chart-container {
      margin: 1.5rem 0;
      padding: 1rem;
      background: var(--theme-background-alt, #f8fafc);
      border-radius: 8px;
      border: 1px solid var(--theme-foreground-muted, #e1e5e9);
    }
    
    .chart-section {
      margin: 2rem 0;
    }
    
    .chart-section h4 {
      margin: 0 0 1rem 0;
      color: var(--theme-foreground, #374151);
      font-size: 1.2rem;
      font-weight: 600;
      text-align: center;
    }
    
    .speeding-explanation {
      background: linear-gradient(135deg, var(--theme-background-alt, #f8fafc) 0%, var(--theme-background, #ffffff) 100%);
      padding: 1.5rem;
      border-radius: 12px;
      margin: 2rem 0;
      border-left: 4px solid;
      border-image: linear-gradient(135deg, #ef4444, #f97316) 1;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .speeding-explanation h4 {
      margin: 0 0 1rem 0;
      color: var(--theme-foreground, #374151);
      font-size: 1.1rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .speeding-explanation h4::before {
      content: '⚡';
      font-size: 1.2rem;
    }
    
    .speeding-explanation p {
      margin: 0.75rem 0;
      color: var(--theme-foreground-muted, #6b7280);
      font-size: 0.95rem;
      line-height: 1.6;
      padding-left: 1rem;
      position: relative;
    }
    
    .speeding-explanation p::before {
      content: '•';
      position: absolute;
      left: 0;
      color: #ef4444;
      font-weight: bold;
    }
  `;
  container.appendChild(style);

  // Title
  const title = document.createElement("h3");
  title.className = "speeding-title";
  title.textContent = `Speeding Patterns by Hour (${speedLimit} MPH limit)`;
  container.appendChild(title);

  // Calculate peak speeding hours
  const northboundPeak = speedingData.reduce((max, d) =>
    d.northbound.percentage > max.northbound.percentage ? d : max
  );
  const southboundPeak = speedingData.reduce((max, d) =>
    d.southbound.percentage > max.southbound.percentage ? d : max
  );

  // Summary cards
  const summaryContainer = document.createElement("div");
  summaryContainer.className = "speeding-summary";

  const northCard = document.createElement("div");
  northCard.className = "speeding-card peak";
  northCard.innerHTML = `
    <div class="speeding-direction">Northbound Peak</div>
    <div class="speeding-peak-time">${northboundPeak.hour}:00</div>
    <div class="speeding-percentage">${northboundPeak.northbound.percentage}% speeding</div>
  `;
  summaryContainer.appendChild(northCard);

  const southCard = document.createElement("div");
  southCard.className = "speeding-card peak";
  southCard.innerHTML = `
    <div class="speeding-direction">Southbound Peak</div>
    <div class="speeding-peak-time">${southboundPeak.hour}:00</div>
    <div class="speeding-percentage">${southboundPeak.southbound.percentage}% speeding</div>
  `;
  summaryContainer.appendChild(southCard);

  container.appendChild(summaryContainer);

  // Prepare data for charts
  const northboundData = speedingData.map(d => ({
    hour: d.hour,
    total: d.northbound.total,
    speeding: d.northbound.speeding,
    percentage: d.northbound.percentage,
    direction: "Northbound"
  }));

  const southboundData = speedingData.map(d => ({
    hour: d.hour,
    total: d.southbound.total,
    speeding: d.southbound.speeding,
    percentage: d.southbound.percentage,
    direction: "Southbound"
  }));

  // Create chart containers
  const northChartContainer = document.createElement("div");
  northChartContainer.className = "chart-section";

  const northTitle = document.createElement("h4");
  northTitle.textContent = "Northbound - Speeding by Hour";
  northChartContainer.appendChild(northTitle);

  const northChart = document.createElement("div");
  northChart.className = "chart-container";
  northChartContainer.appendChild(northChart);

  // Northbound chart
  const northPlot = Plot.plot({
    width: 800,
    height: 300,
    marginLeft: 80,
    marginBottom: 60,
    x: {
      label: "Hour of Day",
      domain: [0, 23],
      tickFormat: d => d === 0 ? "12 AM" : d === 12 ? "12 PM" : d > 12 ? `${d - 12} PM` : `${d} AM`
    },
    y: {
      label: "Total Vehicles",
      grid: true
    },
    marks: [
      Plot.barY(northboundData, {
        x: "hour",
        y: "total",
        fill: "#e5e7eb",
        tip: true
      }),
      Plot.line(northboundData, {
        x: "hour",
        y: d => d.percentage * 10, // Scale for visibility
        stroke: "#ef4444",
        strokeWidth: 3,
        marker: "circle",
        markerSize: 4,
        tip: true
      }),
      Plot.ruleY([0])
    ]
  });

  northChart.appendChild(northPlot);
  container.appendChild(northChartContainer);

  // Southbound chart
  const southChartContainer = document.createElement("div");
  southChartContainer.className = "chart-section";

  const southTitle = document.createElement("h4");
  southTitle.textContent = "Southbound - Speeding by Hour";
  southChartContainer.appendChild(southTitle);

  const southChart = document.createElement("div");
  southChart.className = "chart-container";
  southChartContainer.appendChild(southChart);

  const southPlot = Plot.plot({
    width: 800,
    height: 300,
    marginLeft: 80,
    marginBottom: 60,
    x: {
      label: "Hour of Day",
      domain: [0, 23],
      tickFormat: d => d === 0 ? "12 AM" : d === 12 ? "12 PM" : d > 12 ? `${d - 12} PM` : `${d} AM`
    },
    y: {
      label: "Total Vehicles",
      grid: true
    },
    marks: [
      Plot.barY(southboundData, {
        x: "hour",
        y: "total",
        fill: "#e5e7eb",
        tip: true
      }),
      Plot.line(southboundData, {
        x: "hour",
        y: d => d.percentage * 10, // Scale for visibility
        stroke: "#ef4444",
        strokeWidth: 3,
        marker: "circle",
        markerSize: 4,
        tip: true
      }),
      Plot.ruleY([0])
    ]
  });

  southChart.appendChild(southPlot);
  container.appendChild(southChartContainer);

  // Add explanation
  const explanation = document.createElement("div");
  explanation.className = "speeding-explanation";
  explanation.innerHTML = `
    <h4>How to read these charts:</h4>
    <p>• <strong>Gray bars</strong> show total vehicle count by hour</p>
    <p>• <strong>Red line with dots</strong> shows percentage of vehicles speeding (scaled 10x for visibility)</p>
    <p>• <strong>High percentage + high volume</strong> indicates peak enforcement opportunities</p>
    <p>• <strong>High percentage + low volume</strong> may indicate off-peak speeding patterns</p>
    <p>• Peak speeding typically occurs during rush hours (7-9 AM, 4-6 PM)</p>
    <p>• Use this to optimize enforcement timing and identify when speeding is most problematic</p>
  `;
  container.appendChild(explanation);

  return container;
}