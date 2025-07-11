import * as Plot from "npm:@observablehq/plot";

/**
 * Vehicle Classification Distribution component for Observable Framework
 * Converts Python matplotlib vehicle classification analysis to Observable Plot
 * @returns {HTMLElement} - Vehicle classification distribution analysis
 */
export function VehicleClassification() {
  // Hardcoded vehicle classification data (extracted from Python analysis)
  const classificationData = [
    {vehicleType: "Class 1 - Motorcycles", northbound: 23, southbound: 18, total: 41, percentage: 0.3},
    {vehicleType: "Class 2 - Passenger Cars", northbound: 4567, southbound: 3892, total: 8459, percentage: 89.2},
    {vehicleType: "Class 3 - Pickups, Vans", northbound: 456, southbound: 389, total: 845, percentage: 8.9},
    {vehicleType: "Class 4 - Buses", northbound: 12, southbound: 15, total: 27, percentage: 0.3},
    {vehicleType: "Class 5 - 2 Axles, 6 Tires", northbound: 89, southbound: 67, total: 156, percentage: 1.6},
    {vehicleType: "Class 6 - 3 Axles", northbound: 34, southbound: 23, total: 57, percentage: 0.6}
  ];

  const container = document.createElement("div");
  container.className = "vehicle-classification-container";

  // Add styles
  const style = document.createElement("style");
  style.textContent = `
    .vehicle-classification-container {
      margin: 2rem 0;
    }
    
    .classification-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 1.5rem;
      color: var(--theme-foreground, #374151);
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-align: center;
    }
    
    .classification-summary {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
      margin: 2rem 0;
    }
    
    .classification-card {
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
    
    .classification-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .classification-card.dominant {
      border-left: 4px solid #10b981;
    }
    
    .classification-card.secondary {
      border-left: 4px solid #3b82f6;
    }
    
    .classification-card.minor {
      border-left: 4px solid #6b7280;
    }
    
    .classification-type {
      font-size: 0.9rem;
      font-weight: 500;
      color: var(--theme-foreground-muted, #6b7280);
      margin-bottom: 0.5rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .classification-percentage {
      font-size: 2rem;
      font-weight: 700;
      margin: 0.5rem 0;
    }
    
    .classification-percentage.dominant {
      color: #10b981;
    }
    
    .classification-percentage.secondary {
      color: #3b82f6;
    }
    
    .classification-percentage.minor {
      color: #6b7280;
    }
    
    .classification-count {
      font-size: 1rem;
      color: var(--theme-foreground-muted, #6b7280);
      font-weight: 500;
    }
    
    .classification-legend {
      background: linear-gradient(135deg, var(--theme-background-alt, #f8fafc) 0%, var(--theme-background, #ffffff) 100%);
      padding: 1.5rem;
      border-radius: 12px;
      margin: 2rem 0;
      border-left: 4px solid;
      border-image: linear-gradient(135deg, #6366f1, #8b5cf6) 1;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .classification-legend h4 {
      margin: 0 0 1rem 0;
      color: var(--theme-foreground, #374151);
      font-size: 1.1rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .classification-legend h4::before {
      content: '🚗';
      font-size: 1.2rem;
    }
    
    .legend-item {
      display: flex;
      align-items: center;
      margin: 0.75rem 0;
      color: var(--theme-foreground-muted, #6b7280);
      font-size: 0.95rem;
      padding: 0.5rem;
      border-radius: 6px;
      transition: background-color 0.2s ease;
    }
    
    .legend-item:hover {
      background: var(--theme-background-alt, #f8fafc);
    }
    
    .legend-emoji {
      margin-right: 0.75rem;
      font-size: 1.4rem;
    }
    
    .classification-explanation {
      background: linear-gradient(135deg, var(--theme-background-alt, #f8fafc) 0%, var(--theme-background, #ffffff) 100%);
      padding: 1.5rem;
      border-radius: 12px;
      margin: 2rem 0;
      border-left: 4px solid;
      border-image: linear-gradient(135deg, #6366f1, #8b5cf6) 1;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .classification-explanation h4 {
      margin: 0 0 1rem 0;
      color: var(--theme-foreground, #374151);
      font-size: 1.1rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .classification-explanation h4::before {
      content: '📊';
      font-size: 1.2rem;
    }
    
    .classification-explanation p {
      margin: 0.75rem 0;
      color: var(--theme-foreground-muted, #6b7280);
      font-size: 0.95rem;
      line-height: 1.6;
      padding-left: 1rem;
      position: relative;
    }
    
    .classification-explanation p::before {
      content: '•';
      position: absolute;
      left: 0;
      color: #6366f1;
      font-weight: bold;
    }
  `;
  container.appendChild(style);

  // Title
  const title = document.createElement("h3");
  title.className = "classification-title";
  title.textContent = "Vehicle Classification Distribution";
  container.appendChild(title);

  // Summary cards for top 3 classes
  const topClasses = classificationData
    .sort((a, b) => b.percentage - a.percentage)
    .slice(0, 3);

  const summaryContainer = document.createElement("div");
  summaryContainer.className = "classification-summary";
  
  const cardClasses = ["dominant", "secondary", "minor"];
  
  topClasses.forEach((item, index) => {
    const cardElement = document.createElement("div");
    cardElement.className = `classification-card ${cardClasses[index]}`;
    cardElement.innerHTML = `
      <div class="classification-type">${item.vehicleType}</div>
      <div class="classification-percentage ${cardClasses[index]}">${item.percentage}%</div>
      <div class="classification-count">${item.total.toLocaleString()} vehicles</div>
    `;
    summaryContainer.appendChild(cardElement);
  });
  
  container.appendChild(summaryContainer);

  // Create chart container
  const chartContainer = document.createElement("div");
  chartContainer.id = "vehicle-classification-chart";
  container.appendChild(chartContainer);

  // Prepare data for chart
  const chartData = [];
  classificationData.forEach(item => {
    chartData.push({
      vehicleType: item.vehicleType.replace(" - ", "\n"),
      direction: "Northbound",
      count: item.northbound
    });
    chartData.push({
      vehicleType: item.vehicleType.replace(" - ", "\n"),
      direction: "Southbound", 
      count: item.southbound
    });
  });

  // Create the chart using Observable Plot
  const chart = Plot.plot({
    title: "Vehicle Classification by Direction",
    width: 800,
    height: 500,
    marginLeft: 80,
    marginBottom: 100,
    style: {
      background: "transparent",
      fontFamily: "system-ui, sans-serif"
    },
    x: {
      label: "Vehicle Type",
      tickRotate: 45
    },
    y: {
      label: "Vehicle Count",
      grid: true,
      tickFormat: "~s"
    },
    color: {
      legend: true,
      domain: ["Northbound", "Southbound"],
      range: ["#3b82f6", "#ef4444"]
    },
    marks: [
      Plot.barY(chartData, {
        x: "vehicleType",
        y: "count",
        fill: "direction",
        tip: true,
        rx: 3
      }),
      Plot.ruleY([0])
    ]
  });

  chartContainer.appendChild(chart);

  // Add vehicle class legend
  const legend = document.createElement("div");
  legend.className = "classification-legend";
  legend.innerHTML = `
    <h4>Vehicle Class Legend (FHWA Standards)</h4>
    <div class="legend-item">
      <span class="legend-emoji">🏍️</span>
      <strong>Class 1</strong>: Motorcycles
    </div>
    <div class="legend-item">
      <span class="legend-emoji">🚗</span>
      <strong>Class 2</strong>: Passenger Cars
    </div>
    <div class="legend-item">
      <span class="legend-emoji">🚐</span>
      <strong>Class 3</strong>: Pickups, Vans
    </div>
    <div class="legend-item">
      <span class="legend-emoji">🚌</span>
      <strong>Class 4</strong>: Buses
    </div>
    <div class="legend-item">
      <span class="legend-emoji">🚛</span>
      <strong>Class 5</strong>: 2 Axles, 6 Tires
    </div>
    <div class="legend-item">
      <span class="legend-emoji">🚛</span>
      <strong>Class 6</strong>: 3 Axles
    </div>
  `;
  container.appendChild(legend);

  // Add explanation
  const explanation = document.createElement("div");
  explanation.className = "classification-explanation";
  explanation.innerHTML = `
    <h4>How to read this chart:</h4>
    <p>• This chart shows the distribution of different vehicle types in each direction</p>
    <p>• Each bar represents a vehicle classification based on the Federal Highway Administration (FHWA) system</p>
    <p>• <strong>Class 2 (Passenger Cars)</strong> typically dominates traffic in residential areas (${classificationData[1].percentage}%)</p>
    <p>• <strong>Class 3 (Pickups, Vans)</strong> represents light commercial and personal vehicles (${classificationData[2].percentage}%)</p>
    <p>• <strong>Classes 4-6</strong> represent larger commercial vehicles (buses, trucks)</p>
    <p>• Compare the two directions to identify if one has more commercial traffic</p>
    <p>• Use this data for infrastructure planning and understanding traffic composition</p>
  `;
  container.appendChild(explanation);

  return container;
}