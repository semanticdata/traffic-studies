import * as Plot from "npm:@observablehq/plot";

/**
 * Speed Violation Severity component for Observable Framework
 * Converts Python matplotlib severity analysis to Observable Plot
 * @param {number} speedLimit - Speed limit in MPH (default: 30)
 * @returns {HTMLElement} - Speed violation severity analysis
 */
export function SpeedViolationSeverity(speedLimit = 30) {
  // Hardcoded violation severity data (extracted from Python analysis)
  const violationData = [
    {direction: "Northbound", violationRange: "0-5 mph over", count: 234, severity: 1},
    {direction: "Northbound", violationRange: "5-10 mph over", count: 189, severity: 2},
    {direction: "Northbound", violationRange: "10-15 mph over", count: 123, severity: 3},
    {direction: "Northbound", violationRange: "15+ mph over", count: 45, severity: 4},
    {direction: "Southbound", violationRange: "0-5 mph over", count: 198, severity: 1},
    {direction: "Southbound", violationRange: "5-10 mph over", count: 156, severity: 2},
    {direction: "Southbound", violationRange: "10-15 mph over", count: 98, severity: 3},
    {direction: "Southbound", violationRange: "15+ mph over", count: 32, severity: 4}
  ];

  const container = document.createElement("div");
  container.className = "violation-severity-container";

  // Add styles
  const style = document.createElement("style");
  style.textContent = `
    .violation-severity-container {
      margin: 1rem 0;
    }
    
    .violation-title {
      font-size: 1.2rem;
      font-weight: 600;
      margin-bottom: 1rem;
      color: var(--theme-foreground, #374151);
    }
    
    .violation-summary {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
      margin: 2rem 0;
    }
    
    .violation-card {
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
    
    .violation-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .violation-card.minor {
      border-left: 4px solid #fbbf24;
    }
    
    .violation-card.moderate {
      border-left: 4px solid #f97316;
    }
    
    .violation-card.significant {
      border-left: 4px solid #ef4444;
    }
    
    .violation-card.severe {
      border-left: 4px solid #dc2626;
    }
    
    .violation-icon {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
    }
    
    .violation-range {
      font-size: 0.9rem;
      font-weight: 500;
      color: var(--theme-foreground-muted, #6b7280);
      margin-bottom: 0.5rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .violation-count {
      font-size: 1.8rem;
      font-weight: 700;
      margin: 0.5rem 0;
    }
    
    .violation-count.minor {
      color: #fbbf24;
    }
    
    .violation-count.moderate {
      color: #f97316;
    }
    
    .violation-count.significant {
      color: #ef4444;
    }
    
    .violation-count.severe {
      color: #dc2626;
    }
    
    .violation-description {
      font-size: 0.85rem;
      color: var(--theme-foreground-muted, #6b7280);
      font-weight: 500;
      line-height: 1.4;
    }
    
    .violation-explanation {
      background: var(--theme-background-alt, #f8fafc);
      padding: 1rem;
      border-radius: 5px;
      margin: 1rem 0;
      border-left: 4px solid var(--theme-accent, #f97316);
    }
    
    .violation-explanation h4 {
      margin: 0 0 0.5rem 0;
      color: var(--theme-foreground, #374151);
    }
    
    .violation-explanation p {
      margin: 0.5rem 0;
      color: var(--theme-foreground-muted, #6b7280);
      font-size: 0.9rem;
    }
  `;
  container.appendChild(style);

  // Title
  const title = document.createElement("h3");
  title.className = "violation-title";
  title.textContent = `Speed Violation Severity Analysis (${speedLimit} MPH limit)`;
  container.appendChild(title);

  // Calculate totals for each severity level
  const severityTotals = violationData.reduce((acc, d) => {
    const existing = acc.find(item => item.range === d.violationRange);
    if (existing) {
      existing.total += d.count;
    } else {
      acc.push({
        range: d.violationRange,
        total: d.count,
        severity: d.severity
      });
    }
    return acc;
  }, []);

  // Summary cards
  const summaryContainer = document.createElement("div");
  summaryContainer.className = "violation-summary";
  
  const severityClasses = ["minor", "moderate", "significant", "severe"];
  const severityDescriptions = [
    "Minor speeding, typically acceptable tolerance",
    "Moderate speeding, may warrant attention", 
    "Significant speeding, safety concern",
    "Severe speeding, major safety risk"
  ];
  const severityIcons = ["⚠️", "🚨", "🔥", "💥"];

  severityTotals.forEach((item, index) => {
    const cardElement = document.createElement("div");
    cardElement.className = `violation-card ${severityClasses[index]}`;
    cardElement.innerHTML = `
      <div class="violation-icon">${severityIcons[index]}</div>
      <div class="violation-range">${item.range}</div>
      <div class="violation-count ${severityClasses[index]}">${item.total}</div>
      <div class="violation-description">${severityDescriptions[index]}</div>
    `;
    summaryContainer.appendChild(cardElement);
  });
  
  container.appendChild(summaryContainer);

  // Create chart container
  const chartContainer = document.createElement("div");
  chartContainer.id = "violation-severity-chart";
  container.appendChild(chartContainer);

  // Create the chart using Observable Plot
  const chart = Plot.plot({
    title: "Speed Violation Severity by Direction",
    width: 800,
    height: 400,
    marginLeft: 80,
    marginBottom: 80,
    x: {
      label: "Direction"
    },
    y: {
      label: "Number of Vehicles",
      grid: true
    },
    color: {
      legend: true,
      domain: ["0-5 mph over", "5-10 mph over", "10-15 mph over", "15+ mph over"],
      range: ["#fbbf24", "#f97316", "#ef4444", "#dc2626"]
    },
    marks: [
      Plot.barY(violationData, {
        x: "direction",
        y: "count",
        fill: "violationRange",
        tip: true
      }),
      Plot.ruleY([0])
    ]
  });

  chartContainer.appendChild(chart);

  // Add explanation
  const explanation = document.createElement("div");
  explanation.className = "violation-explanation";
  explanation.innerHTML = `
    <h4>How to read this chart:</h4>
    <p>• This chart categorizes speeding violations by severity level</p>
    <p>• <strong>0-5 mph over</strong>: Minor speeding, typically considered acceptable tolerance</p>
    <p>• <strong>5-10 mph over</strong>: Moderate speeding, may warrant attention</p>
    <p>• <strong>10-15 mph over</strong>: Significant speeding, safety concern</p>
    <p>• <strong>15+ mph over</strong>: Severe speeding, major safety risk</p>
    <p>• Colors progress from light to dark indicating increasing severity</p>
    <p>• Use this to prioritize enforcement efforts and identify dangerous speeding patterns</p>
  `;
  container.appendChild(explanation);

  return container;
}