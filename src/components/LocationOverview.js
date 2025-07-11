/**
 * LocationOverview component for displaying location information
 * @param {Object} trafficResult - The traffic result object from data loader
 * @param {number} speedLimit - Speed limit for the location
 * @returns {HTMLElement} - Styled location overview element
 */
export function LocationOverview(trafficResult, speedLimit = 30) {
  const container = document.createElement("div");
  container.style.cssText = `
    background: var(--theme-background-alt, #f8fafc);
    border: 1px solid var(--theme-foreground-muted, #e1e5e9);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
  `;

  const gridContainer = document.createElement("div");
  gridContainer.style.cssText = `
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
  `;

  const leftColumn = document.createElement("div");
  leftColumn.innerHTML = `
    <strong>Address:</strong> ${trafficResult.location}<br>
    <strong>City:</strong> Crystal, Minnesota<br>
    <strong>Speed Limit:</strong> ${speedLimit} mph
  `;

  const rightColumn = document.createElement("div");
  rightColumn.innerHTML = `
    <strong>Data Source:</strong> PicoCount 2500<br>
    <strong>Directions:</strong> ${trafficResult.structure.dir1Name}, ${trafficResult.structure.dir2Name}<br>
    <strong>Total Records:</strong> ${trafficResult.data.length}
  `;

  gridContainer.appendChild(leftColumn);
  gridContainer.appendChild(rightColumn);
  container.appendChild(gridContainer);

  return container;
}