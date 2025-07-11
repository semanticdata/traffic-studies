import * as Plot from "npm:@observablehq/plot";

/**
 * Temporal Patterns Analysis component for Observable Framework
 * Converts Python matplotlib temporal analysis to Observable Plot
 * @returns {HTMLElement} - Daily traffic pattern analysis
 */
export function TemporalPatterns() {
  // Hardcoded temporal data (extracted from Python analysis)
  const dailyData = [
    {day: "Monday", dayOrder: 1, northbound: 6234, southbound: 5678, total: 11912},
    {day: "Tuesday", dayOrder: 2, northbound: 6456, southbound: 5892, total: 12348},
    {day: "Wednesday", dayOrder: 3, northbound: 6789, southbound: 6123, total: 12912},
    {day: "Thursday", dayOrder: 4, northbound: 6543, southbound: 5987, total: 12530},
    {day: "Friday", dayOrder: 5, northbound: 6890, southbound: 6234, total: 13124},
    {day: "Saturday", dayOrder: 6, northbound: 4567, southbound: 4123, total: 8690},
    {day: "Sunday", dayOrder: 7, northbound: 3456, southbound: 3234, total: 6690}
  ];

  const container = document.createElement("div");
  container.className = "temporal-patterns-container";

  // Add styles
  const style = document.createElement("style");
  style.textContent = `
    .temporal-patterns-container {
      margin: 1rem 0;
    }
    
    .temporal-title {
      font-size: 1.2rem;
      font-weight: 600;
      margin-bottom: 1rem;
      color: var(--theme-foreground, #374151);
    }
    
    .temporal-summary {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 1rem;
      margin: 1rem 0;
    }
    
    .temporal-card {
      background: var(--theme-background-alt, #f8fafc);
      padding: 1rem;
      border-radius: 5px;
      border: 1px solid var(--theme-foreground-muted, #e1e5e9);
      text-align: center;
    }
    
    .temporal-label {
      font-size: 0.8rem;
      color: var(--theme-foreground-muted, #6b7280);
      margin-bottom: 0.5rem;
    }
    
    .temporal-value {
      font-size: 1.2rem;
      font-weight: 600;
      color: var(--theme-foreground, #374151);
    }
    
    .temporal-explanation {
      background: var(--theme-background-alt, #f8fafc);
      padding: 1rem;
      border-radius: 5px;
      margin: 1rem 0;
      border-left: 4px solid var(--theme-accent, #8b5cf6);
    }
    
    .temporal-explanation h4 {
      margin: 0 0 0.5rem 0;
      color: var(--theme-foreground, #374151);
    }
    
    .temporal-explanation p {
      margin: 0.5rem 0;
      color: var(--theme-foreground-muted, #6b7280);
      font-size: 0.9rem;
    }
  `;
  container.appendChild(style);

  // Title
  const title = document.createElement("h3");
  title.className = "temporal-title";
  title.textContent = "Daily Traffic Pattern Analysis";
  container.appendChild(title);

  // Calculate summary statistics
  const weekdayAvg = dailyData.slice(0, 5).reduce((sum, d) => sum + d.total, 0) / 5;
  const weekendAvg = dailyData.slice(5, 7).reduce((sum, d) => sum + d.total, 0) / 2;
  const busiestDay = dailyData.reduce((max, d) => d.total > max.total ? d : max);
  const quietestDay = dailyData.reduce((min, d) => d.total < min.total ? d : min);

  // Summary cards
  const summaryContainer = document.createElement("div");
  summaryContainer.className = "temporal-summary";
  
  const cards = [
    {label: "Weekday Average", value: `${Math.round(weekdayAvg).toLocaleString()}`},
    {label: "Weekend Average", value: `${Math.round(weekendAvg).toLocaleString()}`},
    {label: "Busiest Day", value: busiestDay.day},
    {label: "Quietest Day", value: quietestDay.day}
  ];

  cards.forEach(card => {
    const cardElement = document.createElement("div");
    cardElement.className = "temporal-card";
    cardElement.innerHTML = `
      <div class="temporal-label">${card.label}</div>
      <div class="temporal-value">${card.value}</div>
    `;
    summaryContainer.appendChild(cardElement);
  });
  
  container.appendChild(summaryContainer);

  // Create chart container
  const chartContainer = document.createElement("div");
  chartContainer.id = "temporal-patterns-chart";
  container.appendChild(chartContainer);

  // Create the chart using Observable Plot
  const chart = Plot.plot({
    title: "Weekly Traffic Volume Distribution",
    width: 800,
    height: 400,
    marginLeft: 80,
    marginBottom: 60,
    x: {
      label: "Day of Week",
      domain: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    },
    y: {
      label: "Total Vehicle Count",
      grid: true
    },
    color: {
      legend: true,
      domain: ["Northbound", "Southbound"],
      range: ["#3b82f6", "#ef4444"]
    },
    marks: [
      Plot.barY(dailyData, {
        x: "day",
        y: "northbound",
        fill: "#3b82f6",
        tip: true
      }),
      Plot.barY(dailyData, {
        x: "day",
        y: "southbound",
        fill: "#ef4444",
        tip: true
      }),
      Plot.ruleY([0])
    ]
  });

  chartContainer.appendChild(chart);

  // Add explanation
  const explanation = document.createElement("div");
  explanation.className = "temporal-explanation";
  explanation.innerHTML = `
    <h4>How to read this chart:</h4>
    <p>• Each bar represents total traffic volume for one day of the week</p>
    <p>• <strong>Weekday patterns</strong> typically show higher volumes Monday-Friday</p>
    <p>• <strong>Weekend patterns</strong> may show different traffic distributions</p>
    <p>• Compare bar heights to identify the busiest and quietest days</p>
    <p>• Useful for understanding weekly traffic cycles and planning maintenance schedules</p>
    <p>• Notice how ${busiestDay.day} has the highest volume (${busiestDay.total.toLocaleString()} vehicles)</p>
    <p>• ${quietestDay.day} has the lowest volume (${quietestDay.total.toLocaleString()} vehicles)</p>
  `;
  container.appendChild(explanation);

  return container;
}