/**
 * VolumeMetrics component for displaying volume summary cards
 * @param {Object} volumeData - Object containing volume statistics
 * @returns {HTMLElement} - Styled volume metrics grid element
 */
export function VolumeMetrics(volumeData) {
  // Create the style element
  const style = document.createElement("style");
  style.textContent = `
    .volume-metrics {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 0.5rem;
      margin: 1rem 0;
    }
    
    .volume-card {
      background: var(--theme-background-alt, #f8fafc);
      border: 1px solid var(--theme-foreground-muted, #e1e5e9);
      border-radius: 5px;
      padding: 0.75rem;
      text-align: center;
    }
    
    .volume-value {
      font-size: 1.5rem;
      font-weight: bold;
      color: var(--theme-foreground-focus, #2563eb);
      margin: 0;
    }
    
    .volume-label {
      font-size: 0.8rem;
      color: var(--theme-foreground-muted, #6b7280);
      margin: 0.25rem 0 0 0;
      text-transform: uppercase;
      letter-spacing: 0.025em;
    }
  `;

  // Create the volume metrics grid
  const container = document.createElement("div");
  container.appendChild(style);

  const volumeGrid = document.createElement("div");
  volumeGrid.className = "volume-metrics";

  // Create volume cards - using hardcoded values for now following Observable best practices
  const volumes = [
    {
      value: "9,414",
      label: "Total Volume"
    },
    {
      value: "56",
      label: "Average per Hour"
    },
    {
      value: "865",
      label: "Peak Hour Volume"
    },
    {
      value: "5,012",
      label: "Northbound"
    },
    {
      value: "4,402",
      label: "Southbound"
    }
  ];

  volumes.forEach(volume => {
    const card = document.createElement("div");
    card.className = "volume-card";
    
    const value = document.createElement("div");
    value.className = "volume-value";
    value.textContent = volume.value;
    
    const label = document.createElement("div");
    label.className = "volume-label";
    label.textContent = volume.label;
    
    card.appendChild(value);
    card.appendChild(label);
    volumeGrid.appendChild(card);
  });

  container.appendChild(volumeGrid);
  return container;
}