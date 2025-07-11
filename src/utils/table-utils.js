/**
 * Table utilities for consistent data table styling
 */

/**
 * Load shared table styles
 * @returns {HTMLElement} - Style element with table CSS
 */
export function loadSharedTableStyles() {
  const style = document.createElement("style");
  style.textContent = `
    .data-table {
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0;
      font-size: 0.9rem;
      background: var(--theme-background-alt, #f8fafc);
      border: 1px solid var(--theme-foreground-muted, #e1e5e9);
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .data-table th {
      background: linear-gradient(135deg, var(--theme-background-alt, #f1f5f9) 0%, var(--theme-background, #ffffff) 100%);
      padding: 0.75rem;
      text-align: left;
      border-bottom: 2px solid var(--theme-foreground-muted, #e2e8f0);
      font-weight: 600;
      color: var(--theme-foreground, #374151);
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .data-table td {
      padding: 0.5rem 0.75rem;
      border-bottom: 1px solid var(--theme-foreground-muted, #e2e8f0);
      color: var(--theme-foreground-muted, #6b7280);
      font-size: 0.9rem;
    }
    
    .data-table tr:hover {
      background: var(--theme-background-alt, #f8fafc);
    }
    
    .data-table tbody tr:last-child td {
      border-bottom: none;
    }
    
    /* Striped rows */
    .data-table--striped tbody tr:nth-child(even) {
      background: rgba(0, 0, 0, 0.02);
    }
    
    /* Compact table */
    .data-table--compact th,
    .data-table--compact td {
      padding: 0.375rem 0.5rem;
    }
    
    /* Bordered table */
    .data-table--bordered th,
    .data-table--bordered td {
      border: 1px solid var(--theme-foreground-muted, #e2e8f0);
    }
    
    /* Responsive table wrapper */
    .table-wrapper {
      overflow-x: auto;
      margin: 1rem 0;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .table-wrapper .data-table {
      margin: 0;
      border-radius: 0;
      box-shadow: none;
    }
  `;

  return style;
}

/**
 * Create a data table with consistent styling
 * @param {Array} headers - Table headers
 * @param {Array} rows - Table rows (array of arrays)
 * @param {Object} options - Table options
 * @returns {HTMLElement} - Styled table element
 */
export function createDataTable(headers, rows, options = {}) {
  const {
    className = "",
    striped = false,
    compact = false,
    bordered = false,
    responsive = true
  } = options;

  const container = document.createElement("div");
  container.appendChild(loadSharedTableStyles());

  // Create table wrapper if responsive
  const wrapper = responsive ? document.createElement("div") : container;
  if (responsive) {
    wrapper.className = "table-wrapper";
    container.appendChild(wrapper);
  }

  const table = document.createElement("table");
  let tableClasses = "data-table";
  if (striped) tableClasses += " data-table--striped";
  if (compact) tableClasses += " data-table--compact";
  if (bordered) tableClasses += " data-table--bordered";
  if (className) tableClasses += ` ${className}`;
  table.className = tableClasses;

  // Create table header
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");

  headers.forEach(headerText => {
    const th = document.createElement("th");
    th.textContent = headerText;
    headerRow.appendChild(th);
  });

  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Create table body
  const tbody = document.createElement("tbody");

  rows.forEach(rowData => {
    const tr = document.createElement("tr");
    rowData.forEach(cellData => {
      const td = document.createElement("td");
      td.textContent = cellData;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });

  table.appendChild(tbody);
  wrapper.appendChild(table);

  return container;
}

/**
 * Create a summary table for key metrics
 * @param {Array} data - Array of {label, value} objects
 * @param {Object} options - Table options
 * @returns {HTMLElement} - Styled summary table
 */
export function createSummaryTable(data, options = {}) {
  const headers = ["Metric", "Value"];
  const rows = data.map(item => [item.label, item.value]);

  return createDataTable(headers, rows, {
    ...options,
    compact: true,
    striped: true
  });
}

/**
 * Create a comparison table
 * @param {Array} data - Array of objects with comparison data
 * @param {Array} columns - Column definitions
 * @param {Object} options - Table options
 * @returns {HTMLElement} - Styled comparison table
 */
export function createComparisonTable(data, columns, options = {}) {
  const headers = columns.map(col => col.header);
  const rows = data.map(item =>
    columns.map(col => {
      const value = item[col.key];
      return col.formatter ? col.formatter(value) : value;
    })
  );

  return createDataTable(headers, rows, {
    ...options,
    bordered: true
  });
}

/**
 * Common table data formatters
 */
export const TABLE_FORMATTERS = {
  number: (value) => value.toLocaleString(),
  percentage: (value) => `${value.toFixed(1)}%`,
  currency: (value) => `$${value.toFixed(2)}`,
  date: (value) => new Date(value).toLocaleDateString(),
  time: (value) => {
    const hour = parseInt(value);
    return hour === 0 ? "12 AM" : hour === 12 ? "12 PM" : hour > 12 ? `${hour - 12} PM` : `${hour} AM`;
  }
};

/**
 * Create a traffic data table with common columns
 * @param {Array} data - Traffic data array
 * @param {Object} options - Table options
 * @returns {HTMLElement} - Styled traffic table
 */
export function createTrafficDataTable(data, options = {}) {
  const columns = [
    { key: 'dateTime', header: 'Date/Time', formatter: TABLE_FORMATTERS.date },
    { key: 'northbound', header: 'Northbound', formatter: TABLE_FORMATTERS.number },
    { key: 'southbound', header: 'Southbound', formatter: TABLE_FORMATTERS.number },
    { key: 'total', header: 'Total', formatter: TABLE_FORMATTERS.number },
    { key: 'primaryDirection', header: 'Primary Direction' }
  ];

  return createComparisonTable(data, columns, {
    ...options,
    responsive: true
  });
}