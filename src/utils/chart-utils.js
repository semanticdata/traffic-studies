import * as Plot from "npm:@observablehq/plot";

/**
 * Chart utilities for consistent Observable Plot styling
 */

/**
 * Default chart configuration for consistency
 */
export const DEFAULT_CHART_CONFIG = {
  width: 800,
  height: 400,
  marginLeft: 80,
  marginBottom: 60,
  style: {
    background: "transparent",
    fontFamily: "system-ui, sans-serif"
  },
  y: {
    grid: true,
    tickFormat: "~s"
  }
};

/**
 * Create a standardized bar chart
 * @param {Array} data - Chart data
 * @param {Object} options - Chart options
 * @returns {HTMLElement} - Observable Plot chart
 */
export function createBarChart(data, options = {}) {
  const config = {
    ...DEFAULT_CHART_CONFIG,
    ...options,
    marks: [
      Plot.barY(data, {
        x: options.x,
        y: options.y,
        fill: options.fill || "#3b82f6",
        tip: true,
        rx: 3,
        ...options.barOptions
      }),
      Plot.ruleY([0]),
      ...(options.additionalMarks || [])
    ]
  };

  return Plot.plot(config);
}

/**
 * Create a standardized line chart
 * @param {Array} data - Chart data
 * @param {Object} options - Chart options
 * @returns {HTMLElement} - Observable Plot chart
 */
export function createLineChart(data, options = {}) {
  const config = {
    ...DEFAULT_CHART_CONFIG,
    ...options,
    marks: [
      Plot.line(data, {
        x: options.x,
        y: options.y,
        stroke: options.stroke || "#3b82f6",
        strokeWidth: options.strokeWidth || 2,
        marker: options.marker || "circle",
        markerSize: options.markerSize || 4,
        tip: true,
        ...options.lineOptions
      }),
      Plot.ruleY([0]),
      ...(options.additionalMarks || [])
    ]
  };

  return Plot.plot(config);
}

/**
 * Create a standardized grouped bar chart
 * @param {Array} data - Chart data
 * @param {Object} options - Chart options
 * @returns {HTMLElement} - Observable Plot chart
 */
export function createGroupedBarChart(data, options = {}) {
  const config = {
    ...DEFAULT_CHART_CONFIG,
    ...options,
    color: {
      legend: true,
      domain: options.colorDomain || ["Category A", "Category B"],
      range: options.colorRange || ["#3b82f6", "#ef4444"]
    },
    marks: [
      Plot.barY(data, {
        x: options.x,
        y: options.y,
        fill: options.fill,
        tip: true,
        rx: 3,
        ...options.barOptions
      }),
      Plot.ruleY([0]),
      ...(options.additionalMarks || [])
    ]
  };

  return Plot.plot(config);
}

/**
 * Create a chart container with consistent styling
 * @param {HTMLElement} chart - Observable Plot chart
 * @param {string} className - Additional CSS class
 * @returns {HTMLElement} - Styled chart container
 */
export function createChartContainer(chart, className = "") {
  const container = document.createElement("div");
  container.className = `chart-container ${className}`;
  container.style.cssText = `
    margin: 1.5rem 0;
    padding: 1rem;
    background: var(--theme-background-alt, #f8fafc);
    border-radius: 8px;
    border: 1px solid var(--theme-foreground-muted, #e1e5e9);
    overflow-x: auto;
  `;

  container.appendChild(chart);
  return container;
}

/**
 * Common color palettes for charts
 */
export const CHART_COLORS = {
  primary: ["#3b82f6", "#ef4444"],
  traffic: ["#3b82f6", "#ef4444"], // Northbound, Southbound
  compliance: ["#10b981", "#ef4444"], // Good, Bad
  severity: ["#fbbf24", "#f97316", "#ef4444", "#dc2626"], // Minor to Severe
  temporal: ["#8b5cf6", "#06b6d4"], // Purple, Cyan
  classification: ["#6366f1", "#8b5cf6", "#3b82f6", "#06b6d4", "#10b981", "#f59e0b"]
};

/**
 * Hour formatter for time-based charts
 * @param {number} hour - Hour value (0-23)
 * @returns {string} - Formatted time string
 */
export function formatHour(hour) {
  if (hour === 0) return "12 AM";
  if (hour === 12) return "12 PM";
  if (hour > 12) return `${hour - 12} PM`;
  return `${hour} AM`;
}

/**
 * Create time-based x-axis configuration
 * @param {string} label - Axis label
 * @returns {Object} - X-axis configuration
 */
export function createTimeAxis(label = "Hour of Day") {
  return {
    label,
    domain: [0, 23],
    tickFormat: formatHour
  };
}