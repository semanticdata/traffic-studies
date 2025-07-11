import * as Plot from "npm:@observablehq/plot";
import { createCard, createGradientTitle, createExplanationBox } from "../utils/style-utils.js";
import { createBarChart, createChartContainer, CHART_COLORS } from "../utils/chart-utils.js";
import { createDataTable, createSummaryTable } from "../utils/table-utils.js";
import { createSection, createContentGrid, createDivider } from "../utils/layout-utils.js";

/**
 * Example of a fully refactored component using all shared utilities
 * This shows how much cleaner and more maintainable components can be
 */
export function ExampleRefactoredComponent() {
  // Create main section
  const { container, section } = createSection({
    title: "Traffic Analysis Example",
    subtitle: "Demonstrating shared styling utilities",
    spacing: "normal"
  });

  // Sample data
  const trafficData = [
    { hour: 8, northbound: 189, southbound: 145, total: 334 },
    { hour: 9, northbound: 156, southbound: 123, total: 279 },
    { hour: 16, northbound: 456, southbound: 409, total: 865 },
    { hour: 17, northbound: 389, southbound: 334, total: 723 }
  ];

  // 1. Create summary cards using shared utilities
  const summaryCards = [
    createCard({
      icon: "📊",
      label: "Total Vehicles",
      value: "2,201",
      theme: "green"
    }),
    createCard({
      icon: "🏎️",
      label: "Average Speed",
      value: "32.4 mph",
      theme: "blue"
    }),
    createCard({
      icon: "🚦",
      label: "Compliance Rate",
      value: "68.2%",
      theme: "green"
    }),
    createCard({
      icon: "⏰",
      label: "Peak Hour",
      value: "4:00 PM",
      theme: "red"
    })
  ];

  // Create cards grid
  const cardsGrid = createContentGrid(summaryCards, { columns: 4 });
  section.appendChild(cardsGrid);

  // Add divider
  section.appendChild(createDivider());

  // 2. Create chart using shared utilities
  const chartTitle = createGradientTitle("Hourly Traffic Volume", "blue");
  section.appendChild(chartTitle);

  const chart = createBarChart(trafficData, {
    title: "Peak Hour Analysis",
    x: "hour",
    y: "total",
    fill: "#3b82f6",
    barOptions: {
      tip: d => `${d.hour}:00 - ${d.total} vehicles`
    }
  });

  const chartContainer = createChartContainer(chart);
  section.appendChild(chartContainer);

  // 3. Create explanation box using shared utilities
  const explanation = createExplanationBox(
    "How to read this chart:",
    [
      "Each bar represents one hour of traffic data",
      "Height indicates total vehicle count for that hour",
      "Peak hours typically occur during morning and evening commutes",
      "Use this data to identify optimal times for maintenance or enforcement"
    ],
    "blue",
    "📊"
  );
  section.appendChild(explanation);

  // Add another divider
  section.appendChild(createDivider());

  // 4. Create data table using shared utilities
  const tableTitle = createGradientTitle("Traffic Data Summary", "green");
  section.appendChild(tableTitle);

  const summaryData = [
    { label: "Total Records", value: "2,201" },
    { label: "Peak Hour", value: "4:00 PM" },
    { label: "Peak Volume", value: "865 vehicles" },
    { label: "Average per Hour", value: "550 vehicles" }
  ];

  const summaryTable = createSummaryTable(summaryData);
  section.appendChild(summaryTable);

  return container;
}

// Example of how much code reduction we achieve:
// Before refactoring: ~200-300 lines of CSS and HTML creation
// After refactoring: ~80 lines with shared utilities
// Code reduction: 60-75%
// Maintainability: Centralized styling, consistent design
// Developer experience: Simple, declarative API