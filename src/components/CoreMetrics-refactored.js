import { loadSharedCardStyles, createCard, createGradientTitle } from "../utils/style-utils.js";

/**
 * CoreMetrics component using shared styles - Example refactored version
 * @param {Object} coreMetrics - The core metrics object from getCoreMetrics
 * @returns {HTMLElement} - Styled metrics grid element
 */
export function CoreMetrics(coreMetrics) {
  const container = document.createElement("div");
  container.className = "card-container";

  // Load shared styles
  container.appendChild(loadSharedCardStyles());

  // Create gradient title
  const title = createGradientTitle("Core Traffic Metrics", "blue");
  container.appendChild(title);

  // Create metrics grid
  const metricsGrid = document.createElement("div");
  metricsGrid.className = "card-grid card-grid--large";

  // Create metric cards using shared utility
  const metrics = [
    {
      icon: "📊",
      label: "Total Vehicles",
      value: coreMetrics.totalVehicles.toLocaleString(),
      theme: "green"
    },
    {
      icon: "🏎️",
      label: "Average Speed",
      value: `${coreMetrics.combinedAvgSpeed.toFixed(1)} mph`,
      theme: "blue"
    },
    {
      icon: "🚦",
      label: "Speed Compliance",
      value: `${coreMetrics.complianceRate.toFixed(1)}%`,
      theme: "green"
    },
    {
      icon: "🎯",
      label: "85th Percentile Speed",
      value: `${coreMetrics.percentile85th.toFixed(0)} mph`,
      theme: "amber"
    },
    {
      icon: "⏰",
      label: "Peak Hour",
      value: `${coreMetrics.peakHour}:00`,
      theme: "red"
    },
    {
      icon: "🔄",
      label: "Dominant Direction",
      value: coreMetrics.dominantDirection,
      theme: "purple"
    }
  ];

  metrics.forEach(metric => {
    const card = createCard(metric);
    metricsGrid.appendChild(card);
  });

  container.appendChild(metricsGrid);
  return container;
}