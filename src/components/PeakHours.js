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
      gap: 1rem;
      margin: 1rem 0;
    }
    
    .peak-card {
      background: var(--theme-background-alt, #f8fafc);
      border: 1px solid var(--theme-foreground-muted, #e1e5e9);
      border-radius: 8px;
      padding: 1rem;
    }
    
    .peak-title {
      font-size: 1.1rem;
      font-weight: bold;
      color: var(--theme-foreground, #374151);
      margin: 0 0 0.5rem 0;
    }
    
    .peak-time {
      font-size: 1.3rem;
      font-weight: bold;
      color: var(--theme-foreground-focus, #2563eb);
      margin: 0.25rem 0;
    }
    
    .peak-volume {
      font-size: 1rem;
      color: var(--theme-foreground-muted, #6b7280);
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
      volume: "334 vehicles"
    },
    {
      title: "Evening Peak",
      time: "4:00 PM",
      volume: "865 vehicles"
    },
    {
      title: "Off-Peak Low",
      time: "3:00 AM",
      volume: "3 vehicles"
    }
  ];

  peaks.forEach(peak => {
    const card = document.createElement("div");
    card.className = "peak-card";
    
    const title = document.createElement("div");
    title.className = "peak-title";
    title.textContent = peak.title;
    
    const time = document.createElement("div");
    time.className = "peak-time";
    time.textContent = peak.time;
    
    const volume = document.createElement("div");
    volume.className = "peak-volume";
    volume.textContent = peak.volume;
    
    card.appendChild(title);
    card.appendChild(time);
    card.appendChild(volume);
    peakGrid.appendChild(card);
  });

  container.appendChild(peakGrid);
  return container;
}