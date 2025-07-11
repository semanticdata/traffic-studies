import * as Plot from "npm:@observablehq/plot";

/**
 * Temporal Patterns Analysis component for Observable Framework
 * Converts Python matplotlib temporal analysis to Observable Plot
 * @returns {HTMLElement} - Daily traffic pattern analysis
 */
export function TemporalPatterns() {
  // Hardcoded temporal data (extracted from Python analysis)
  const dailyData = [
    { day: "Monday", dayOrder: 1, northbound: 6234, southbound: 5678, total: 11912 },
    { day: "Tuesday", dayOrder: 2, northbound: 6456, southbound: 5892, total: 12348 },
    { day: "Wednesday", dayOrder: 3, northbound: 6789, southbound: 6123, total: 12912 },
    { day: "Thursday", dayOrder: 4, northbound: 6543, southbound: 5987, total: 12530 },
    { day: "Friday", dayOrder: 5, northbound: 6890, southbound: 6234, total: 13124 },
    { day: "Saturday", dayOrder: 6, northbound: 4567, southbound: 4123, total: 8690 },
    { day: "Sunday", dayOrder: 7, northbound: 3456, southbound: 3234, total: 6690 }
  ];

  const container = document.createElement("div");
  container.className = "temporal-patterns-container";

  // Add styles
  const style = document.createElement("style");
  style.textContent = `
    .temporal-patterns-container {
      margin: 2rem 0;
    }
    
    .temporal-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 1.5rem;
      color: var(--theme-foreground, #374151);
      background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-align: center;
    }
    
    .temporal-summary {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1.5rem;
      margin: 2rem 0;
    }
    
    .temporal-card {
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
    
    .temporal-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .temporal-card.weekday {
      border-left: 4px solid #3b82f6;
    }
    
    .temporal-card.weekend {
      border-left: 4px solid #06b6d4;
    }
    
    .temporal-card.peak {
      border-left: 4px solid #10b981;
    }
    
    .temporal-card.quiet {
      border-left: 4px solid #f59e0b;
    }
    
    .temporal-label {
      font-size: 0.9rem;
      font-weight: 500;
      color: var(--theme-foreground-muted, #6b7280);
      margin-bottom: 0.5rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .temporal-value {
      font-size: 1.6rem;
      font-weight: 700;
      color: var(--theme-foreground, #374151);
      margin: 0.5rem 0;
    }
    
    .temporal-value.weekday {
      color: #3b82f6;
    }
    
    .temporal-value.weekend {
      color: #06b6d4;
    }
    
    .temporal-value.peak {
      color: #10b981;
    }
    
    .temporal-value.quiet {
      color: #f59e0b;
    }
    
    .temporal-explanation {
      background: linear-gradient(135deg, var(--theme-background-alt, #f8fafc) 0%, var(--theme-background, #ffffff) 100%);
      padding: 1.5rem;
      border-radius: 12px;
      margin: 2rem 0;
      border-left: 4px solid;
      border-image: linear-gradient(135deg, #8b5cf6, #06b6d4) 1;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .temporal-explanation h4 {
      margin: 0 0 1rem 0;
      color: var(--theme-foreground, #374151);
      font-size: 1.1rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .temporal-explanation h4::before {
      content: '📅';
      font-size: 1.2rem;
    }
    
    .temporal-explanation p {
      margin: 0.75rem 0;
      color: var(--theme-foreground-muted, #6b7280);
      font-size: 0.95rem;
      line-height: 1.6;
      padding-left: 1rem;
      position: relative;
    }
    
    .temporal-explanation p::before {
      content: '•';
      position: absolute;
      left: 0;
      color: #8b5cf6;
      font-weight: bold;
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
    { label: "Weekday Average", value: `${Math.round(weekdayAvg).toLocaleString()}`, class: "weekday" },
    { label: "Weekend Average", value: `${Math.round(weekendAvg).toLocaleString()}`, class: "weekend" },
    { label: "Busiest Day", value: busiestDay.day, class: "peak" },
    { label: "Quietest Day", value: quietestDay.day, class: "quiet" }
  ];

  cards.forEach(card => {
    const cardElement = document.createElement("div");
    cardElement.className = `temporal-card ${card.class}`;
    cardElement.innerHTML = `
      <div class="temporal-label">${card.label}</div>
      <div class="temporal-value ${card.class}">${card.value}</div>
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
    style: {
      background: "transparent",
      fontFamily: "system-ui, sans-serif"
    },
    x: {
      label: "Day of Week",
      domain: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    },
    y: {
      label: "Total Vehicle Count",
      grid: true,
      tickFormat: "~s"
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
        tip: true,
        rx: 3
      }),
      Plot.barY(dailyData, {
        x: "day",
        y: "southbound",
        fill: "#ef4444",
        tip: true,
        rx: 3
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