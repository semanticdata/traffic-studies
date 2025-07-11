/**
 * DataTable component for displaying sample traffic data
 * @param {Array} sampleData - Array of sample data objects
 * @returns {HTMLElement} - Styled data table element
 */
export function DataTable(sampleData) {
  // Create the style element
  const style = document.createElement("style");
  style.textContent = `
    .data-table {
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0;
      font-size: 0.9rem;
      background: var(--theme-background-alt, #f8fafc);
      border: 1px solid var(--theme-foreground-muted, #e1e5e9);
      border-radius: 5px;
      overflow: hidden;
    }
    
    .data-table th {
      background: var(--theme-background-alt, #f1f5f9);
      padding: 0.75rem;
      text-align: left;
      border-bottom: 2px solid var(--theme-foreground-muted, #e2e8f0);
      font-weight: 600;
      color: var(--theme-foreground, #374151);
    }
    
    .data-table td {
      padding: 0.5rem 0.75rem;
      border-bottom: 1px solid var(--theme-foreground-muted, #e2e8f0);
      color: var(--theme-foreground-muted, #6b7280);
    }
    
    .data-table tr:hover {
      background: var(--theme-background-alt, #f8fafc);
    }
  `;

  // Create the table container
  const container = document.createElement("div");
  container.appendChild(style);

  const table = document.createElement("table");
  table.className = "data-table";

  // Create table header
  const thead = document.createElement("thead");
  const headerRow = document.createElement("tr");

  const headers = ["Date/Time", "Northbound Volume", "Southbound Volume", "Total Volume", "Primary Direction"];
  headers.forEach(headerText => {
    const th = document.createElement("th");
    th.textContent = headerText;
    headerRow.appendChild(th);
  });

  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Create table body with hardcoded data (following Observable best practices)
  const tbody = document.createElement("tbody");

  const rows = [
    ["2024-02-23 00:00:00", "8", "7", "15", "Northbound"],
    ["2024-02-23 01:00:00", "5", "3", "8", "Northbound"],
    ["2024-02-23 02:00:00", "4", "2", "6", "Northbound"],
    ["2024-02-23 03:00:00", "2", "1", "3", "Northbound"],
    ["2024-02-23 04:00:00", "3", "2", "5", "Northbound"]
  ];

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
  container.appendChild(table);

  return container;
}