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
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 1.5rem;
      margin: 2rem 0;
    }
    
    .volume-card {
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
    
    .volume-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .volume-card.total {
      border-left: 4px solid #10b981;
    }
    
    .volume-card.average {
      border-left: 4px solid #3b82f6;
    }
    
    .volume-card.peak {
      border-left: 4px solid #ef4444;
    }
    
    .volume-card.northbound {
      border-left: 4px solid #06b6d4;
    }
    
    .volume-card.southbound {
      border-left: 4px solid #f59e0b;
    }
    
    .volume-icon {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
    }
    
    .volume-label {
      font-size: 0.9rem;
      font-weight: 500;
      color: var(--theme-foreground-muted, #6b7280);
      margin-bottom: 0.5rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .volume-value {
      font-size: 1.8rem;
      font-weight: 700;
      color: var(--theme-foreground, #374151);
      margin: 0.5rem 0;
    }
    
    .volume-value.total {
      color: #10b981;
    }
    
    .volume-value.average {
      color: #3b82f6;
    }
    
    .volume-value.peak {
      color: #ef4444;
    }
    
    .volume-value.northbound {
      color: #06b6d4;
    }
    
    .volume-value.southbound {
      color: #f59e0b;
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
      label: "Total Volume",
      icon: "📈",
      class: "total"
    },
    {
      value: "56",
      label: "Average per Hour",
      icon: "⏱️",
      class: "average"
    },
    {
      value: "865",
      label: "Peak Hour Volume",
      icon: "🔥",
      class: "peak"
    },
    {
      value: "5,012",
      label: "Northbound",
      icon: "⬆️",
      class: "northbound"
    },
    {
      value: "4,402",
      label: "Southbound",
      icon: "⬇️",
      class: "southbound"
    }
  ];

  volumes.forEach(volume => {
    const card = document.createElement("div");
    card.className = `volume-card ${volume.class}`;
    
    const icon = document.createElement("div");
    icon.className = "volume-icon";
    icon.textContent = volume.icon;
    
    const label = document.createElement("div");
    label.className = "volume-label";
    label.textContent = volume.label;
    
    const value = document.createElement("div");
    value.className = `volume-value ${volume.class}`;
    value.textContent = volume.value;
    
    card.appendChild(icon);
    card.appendChild(label);
    card.appendChild(value);
    volumeGrid.appendChild(card);
  });

  container.appendChild(volumeGrid);
  return container;
}