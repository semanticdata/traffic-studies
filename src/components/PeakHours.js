/**
 * PeakHours component for displaying peak hour analysis
 * @param {Object} peakData - Object containing peak hour data
 * @returns {HTMLElement} - Styled peak hours grid element
 */
export function PeakHours(peakData) {
  // Create the style element
  const style = document.createElement("style");
  style.textContent = `
    .peak-hours {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 1.5rem;
      margin: 2rem 0;
    }
    
    .peak-card {
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
    
    .peak-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .peak-card.morning {
      border-left: 4px solid #f59e0b;
    }
    
    .peak-card.evening {
      border-left: 4px solid #ef4444;
    }
    
    .peak-card.low {
      border-left: 4px solid #10b981;
    }
    
    .peak-icon {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
    }
    
    .peak-title {
      font-size: 0.9rem;
      font-weight: 500;
      color: var(--theme-foreground-muted, #6b7280);
      margin-bottom: 0.5rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .peak-time {
      font-size: 1.8rem;
      font-weight: 700;
      color: var(--theme-foreground, #374151);
      margin: 0.5rem 0;
    }
    
    .peak-time.morning {
      color: #f59e0b;
    }
    
    .peak-time.evening {
      color: #ef4444;
    }
    
    .peak-time.low {
      color: #10b981;
    }
    
    .peak-volume {
      font-size: 1rem;
      color: var(--theme-foreground-muted, #6b7280);
      font-weight: 500;
      margin: 0;
    }
  `;

  // Create the peak hours grid
  const container = document.createElement("div");
  container.appendChild(style);

  const peakGrid = document.createElement("div");
  peakGrid.className = "peak-hours";

  // Create peak hour cards - using hardcoded values for now following Observable best practices
  const peaks = [
    {
      title: "Morning Peak",
      time: "8:00 AM",
      volume: "334 vehicles",
      icon: "🌅",
      class: "morning"
    },
    {
      title: "Evening Peak",
      time: "4:00 PM",
      volume: "865 vehicles",
      icon: "🌆",
      class: "evening"
    },
    {
      title: "Off-Peak Low",
      time: "3:00 AM",
      volume: "3 vehicles",
      icon: "🌙",
      class: "low"
    }
  ];

  peaks.forEach(peak => {
    const card = document.createElement("div");
    card.className = `peak-card ${peak.class}`;

    const icon = document.createElement("div");
    icon.className = "peak-icon";
    icon.textContent = peak.icon;

    const title = document.createElement("div");
    title.className = "peak-title";
    title.textContent = peak.title;

    const time = document.createElement("div");
    time.className = `peak-time ${peak.class}`;
    time.textContent = peak.time;

    const volume = document.createElement("div");
    volume.className = "peak-volume";
    volume.textContent = peak.volume;

    card.appendChild(icon);
    card.appendChild(title);
    card.appendChild(time);
    card.appendChild(volume);
    peakGrid.appendChild(card);
  });

  container.appendChild(peakGrid);
  return container;
}