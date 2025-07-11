import * as Plot from "npm:@observablehq/plot";

/**
 * Speed Compliance Visualization component for Observable Framework
 * Converts Python matplotlib compliance analysis to Observable Plot
 * @param {number} speedLimit - Speed limit in MPH (default: 30)
 * @returns {HTMLElement} - Speed compliance comparison chart
 */
export function SpeedCompliance(speedLimit = 30) {
  // Hardcoded compliance data (extracted from Python analysis)
  const complianceData = [
    {direction: "Northbound", compliance: "Compliant", count: 1521, percentage: 68.2},
    {direction: "Northbound", compliance: "Non-Compliant", count: 702, percentage: 31.8},
    {direction: "Southbound", compliance: "Compliant", count: 1342, percentage: 71.4},
    {direction: "Southbound", compliance: "Non-Compliant", count: 537, percentage: 28.6}
  ];

  const container = document.createElement("div");
  container.className = "speed-compliance-container";

  // Add styles
  const style = document.createElement("style");
  style.textContent = `
    .speed-compliance-container {
      margin: 1rem 0;
    }
    
    .compliance-title {
      font-size: 1.2rem;
      font-weight: 600;
      margin-bottom: 1rem;
      color: var(--theme-foreground, #374151);
    }
    
    .compliance-summary {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin: 1rem 0;
    }
    
    .compliance-card {
      background: var(--theme-background-alt, #f8fafc);
      padding: 1rem;
      border-radius: 5px;
      border: 1px solid var(--theme-foreground-muted, #e1e5e9);
      text-align: center;
    }
    
    .compliance-direction {
      font-weight: 600;
      color: var(--theme-foreground, #374151);
      margin-bottom: 0.5rem;
    }
    
    .compliance-rate {
      font-size: 1.5rem;
      font-weight: 700;
      margin: 0.5rem 0;
    }
    
    .compliance-rate.good {
      color: #10b981;
    }
    
    .compliance-rate.warning {
      color: #f59e0b;
    }
    
    .compliance-rate.poor {
      color: #ef4444;
    }
    
    .compliance-explanation {
      background: var(--theme-background-alt, #f8fafc);
      padding: 1rem;
      border-radius: 5px;
      margin: 1rem 0;
      border-left: 4px solid var(--theme-accent, #10b981);
    }
    
    .compliance-explanation h4 {
      margin: 0 0 0.5rem 0;
      color: var(--theme-foreground, #374151);
    }
    
    .compliance-explanation p {
      margin: 0.5rem 0;
      color: var(--theme-foreground-muted, #6b7280);
      font-size: 0.9rem;
    }
  `;
  container.appendChild(style);

  // Title
  const title = document.createElement("h3");
  title.className = "compliance-title";
  title.textContent = `Speed Compliance Analysis (${speedLimit} MPH limit)`;
  container.appendChild(title);

  // Summary cards
  const summaryContainer = document.createElement("div");
  summaryContainer.className = "compliance-summary";
  
  const northboundData = complianceData.filter(d => d.direction === "Northbound");
  const southboundData = complianceData.filter(d => d.direction === "Southbound");
  
  const northboundCompliance = northboundData.find(d => d.compliance === "Compliant").percentage;
  const southboundCompliance = southboundData.find(d => d.compliance === "Compliant").percentage;
  
  // Northbound card
  const northCard = document.createElement("div");
  northCard.className = "compliance-card";
  northCard.innerHTML = `
    <div class="compliance-direction">Northbound</div>
    <div class="compliance-rate ${northboundCompliance >= 70 ? 'good' : northboundCompliance >= 60 ? 'warning' : 'poor'}">
      ${northboundCompliance.toFixed(1)}%
    </div>
    <div>Speed Compliant</div>
  `;
  summaryContainer.appendChild(northCard);
  
  // Southbound card
  const southCard = document.createElement("div");
  southCard.className = "compliance-card";
  southCard.innerHTML = `
    <div class="compliance-direction">Southbound</div>
    <div class="compliance-rate ${southboundCompliance >= 70 ? 'good' : southboundCompliance >= 60 ? 'warning' : 'poor'}">
      ${southboundCompliance.toFixed(1)}%
    </div>
    <div>Speed Compliant</div>
  `;
  summaryContainer.appendChild(southCard);
  
  container.appendChild(summaryContainer);

  // Create chart container
  const chartContainer = document.createElement("div");
  chartContainer.id = "speed-compliance-chart";
  container.appendChild(chartContainer);

  // Create the chart using Observable Plot
  const chart = Plot.plot({
    title: "Speed Compliance Comparison by Direction",
    width: 800,
    height: 400,
    marginLeft: 80,
    marginBottom: 60,
    x: {
      label: "Direction"
    },
    y: {
      label: "Vehicle Count",
      grid: true
    },
    color: {
      legend: true,
      domain: ["Compliant", "Non-Compliant"],
      range: ["#10b981", "#ef4444"]
    },
    marks: [
      Plot.barY(complianceData, {
        x: "direction",
        y: "count",
        fill: "compliance",
        tip: true
      }),
      Plot.ruleY([0])
    ]
  });

  chartContainer.appendChild(chart);

  // Add explanation
  const explanation = document.createElement("div");
  explanation.className = "compliance-explanation";
  explanation.innerHTML = `
    <h4>How to read this chart:</h4>
    <p>• <strong>Green bars</strong> represent vehicles traveling at or below the speed limit</p>
    <p>• <strong>Red bars</strong> represent vehicles exceeding the speed limit</p>
    <p>• Compare bar heights to see the compliance rate for each direction</p>
    <p>• Higher green bars indicate better speed compliance</p>
    <p>• Overall compliance rates above 70% are considered good</p>
    <p>• Use this to quickly assess overall speed compliance and identify problem directions</p>
  `;
  container.appendChild(explanation);

  return container;
}