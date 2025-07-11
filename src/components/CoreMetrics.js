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
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 1.5rem;
      margin: 2rem 0;
    }
    
    .metric-card {
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
    
    .metric-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .metric-card.total {
      border-left: 4px solid #10b981;
    }
    
    .metric-card.speed {
      border-left: 4px solid #3b82f6;
    }
    
    .metric-card.compliance {
      border-left: 4px solid #10b981;
    }
    
    .metric-card.percentile {
      border-left: 4px solid #f59e0b;
    }
    
    .metric-card.peak {
      border-left: 4px solid #ef4444;
    }
    
    .metric-card.direction {
      border-left: 4px solid #8b5cf6;
    }
    
    .metric-value {
      font-size: 1.8rem;
      font-weight: 700;
      color: var(--theme-foreground, #374151);
      margin: 0.5rem 0;
    }
    
    .metric-value.total {
      color: #10b981;
    }
    
    .metric-value.speed {
      color: #3b82f6;
    }
    
    .metric-value.compliance {
      color: #10b981;
    }
    
    .metric-value.percentile {
      color: #f59e0b;
    }
    
    .metric-value.peak {
      color: #ef4444;
    }
    
    .metric-value.direction {
      color: #8b5cf6;
    }
    
    .metric-label {
      font-size: 0.9rem;
      font-weight: 500;
      color: var(--theme-foreground-muted, #6b7280);
      margin-bottom: 0.5rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .metric-icon {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
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
      label: "Total Vehicles",
      icon: "📊",
      class: "total"
    },
    {
      value: `${coreMetrics.combinedAvgSpeed.toFixed(1)} mph`,
      label: "Average Speed",
      icon: "🏎️",
      class: "speed"
    },
    {
      value: `${coreMetrics.complianceRate.toFixed(1)}%`,
      label: "Speed Compliance",
      icon: "🚦",
      class: "compliance"
    },
    {
      value: `${coreMetrics.percentile85th.toFixed(0)} mph`,
      label: "85th Percentile Speed",
      icon: "🎯",
      class: "percentile"
    },
    {
      value: `${coreMetrics.peakHour}:00`,
      label: "Peak Hour",
      icon: "⏰",
      class: "peak"
    },
    {
      value: `${coreMetrics.dominantDirection}`,
      label: "Dominant Direction",
      icon: "🔄",
      class: "direction"
    }
  ];

  metrics.forEach(metric => {
    const card = document.createElement("div");
    card.className = `metric-card ${metric.class}`;
    
    const icon = document.createElement("div");
    icon.className = "metric-icon";
    icon.textContent = metric.icon;
    
    const label = document.createElement("div");
    label.className = "metric-label";
    label.textContent = metric.label;
    
    const value = document.createElement("div");
    value.className = `metric-value ${metric.class}`;
    value.textContent = metric.value;
    
    card.appendChild(icon);
    card.appendChild(label);
    card.appendChild(value);
    metricsGrid.appendChild(card);
  });

  container.appendChild(metricsGrid);
  return container;
}