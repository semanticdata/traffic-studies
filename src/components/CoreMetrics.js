/**
 * CoreMetrics component for displaying traffic metrics in a card layout
 * @param {Object} coreMetrics - The core metrics object from getCoreMetrics
 * @returns {HTMLElement} - Styled metrics grid element
 */
export function CoreMetrics(coreMetrics) {
  // Create the style element
  const style = document.createElement("style");
  style.textContent = `
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 0.5rem;
      margin: 1rem 0;
    }
    
    .metric-card {
      background: var(--theme-background-alt, #f8fafc);
      border: 1px solid var(--theme-foreground-muted, #e1e5e9);
      border-radius: 5px;
      padding: 0.25rem 0.5rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .metric-value {
      font-size: 1.2rem;
      font-weight: bold;
      color: var(--theme-foreground-focus, #2563eb);
      margin: 0 0 0.5rem 0;
    }
    
    .metric-label {
      font-size: 0.8rem;
      color: var(--theme-foreground-muted, #6b7280);
      margin: 0;
      text-transform: uppercase;
      letter-spacing: 0.025em;
    }
  `;

  // Create the metrics grid
  const container = document.createElement("div");
  container.appendChild(style);

  const metricsGrid = document.createElement("div");
  metricsGrid.className = "metrics-grid";

  // Create metric cards
  const metrics = [
    {
      value: coreMetrics.totalVehicles.toLocaleString(),
      label: "Total Vehicles"
    },
    {
      value: `${coreMetrics.combinedAvgSpeed.toFixed(1)} mph`,
      label: "Average Speed"
    },
    {
      value: `${coreMetrics.complianceRate.toFixed(1)}%`,
      label: "Speed Compliance"
    },
    {
      value: `${coreMetrics.percentile85th.toFixed(0)} mph`,
      label: "85th Percentile Speed"
    },
    {
      value: `${coreMetrics.peakHour}:00 (${coreMetrics.peakVehicles} vehicles)`,
      label: "Peak Hour"
    },
    {
      value: `${coreMetrics.dominantDirection} (${coreMetrics.dominantPct.toFixed(1)}%)`,
      label: "Dominant Direction"
    }
  ];

  metrics.forEach(metric => {
    const card = document.createElement("div");
    card.className = "metric-card";
    
    const value = document.createElement("div");
    value.className = "metric-value";
    value.textContent = metric.value;
    
    const label = document.createElement("div");
    label.className = "metric-label";
    label.textContent = metric.label;
    
    card.appendChild(value);
    card.appendChild(label);
    metricsGrid.appendChild(card);
  });

  container.appendChild(metricsGrid);
  return container;
}