/**
 * LocationOverview component for displaying location information
 * @param {Object} trafficResult - The traffic result object from data loader
 * @param {number} speedLimit - Speed limit for the location
 * @returns {HTMLElement} - Styled location overview element
 */
export function LocationOverview(trafficResult, speedLimit = 30) {
  // Create the style element
  const style = document.createElement("style");
  style.textContent = `
    .location-overview {
      // background: linear-gradient(135deg, var(--theme-background-alt, #f8fafc) 0%, var(--theme-background, #ffffff) 100%);
      // padding: 1.5rem;
      // border-radius: 12px;
      // border: 1px solid var(--theme-foreground-muted, #e1e5e9);
      // box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
      // margin: 2rem 0;
      // border-left: 4px solid #6366f1;
    }
    
    .location-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 1.5rem;
    }
    
    .location-card {
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
    
    .location-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .location-card.address {
      border-left: 4px solid #10b981;
    }
    
    .location-card.technical {
      border-left: 4px solid #3b82f6;
    }
    
    .location-icon {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
    }
    
    .location-title {
      font-size: 0.9rem;
      font-weight: 500;
      color: var(--theme-foreground-muted, #6b7280);
      margin-bottom: 1rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .location-detail {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 0.75rem 0;
      padding: 0.5rem 0;
      border-bottom: 1px solid var(--theme-foreground-muted, #e1e5e9);
    }
    
    .location-detail:last-child {
      border-bottom: none;
    }
    
    .location-label {
      font-size: 0.9rem;
      color: var(--theme-foreground-muted, #6b7280);
      font-weight: 500;
    }
    
    .location-value {
      font-size: 0.9rem;
      color: var(--theme-foreground, #374151);
      font-weight: 600;
    }
    
    .location-value.address {
      color: #10b981;
    }
    
    .location-value.technical {
      color: #3b82f6;
    }
  `;

  const container = document.createElement("div");
  container.className = "location-overview";
  container.appendChild(style);

  const gridContainer = document.createElement("div");
  gridContainer.className = "location-grid";

  // Address card
  const addressCard = document.createElement("div");
  addressCard.className = "location-card address";
  addressCard.innerHTML = `
    <div class="location-icon">📍</div>
    <div class="location-title">Location Details</div>
    <div class="location-detail">
      <span class="location-label">Address:</span>
      <span class="location-value address">${trafficResult.location}</span>
    </div>
    <div class="location-detail">
      <span class="location-label">City:</span>
      <span class="location-value address">Crystal, Minnesota</span>
    </div>
    <div class="location-detail">
      <span class="location-label">Speed Limit:</span>
      <span class="location-value address">${speedLimit} mph</span>
    </div>
  `;

  // Technical card
  const technicalCard = document.createElement("div");
  technicalCard.className = "location-card technical";
  technicalCard.innerHTML = `
    <div class="location-icon">🔧</div>
    <div class="location-title">Technical Details</div>
    <div class="location-detail">
      <span class="location-label">Data Source:</span>
      <span class="location-value technical">PicoCount 2500</span>
    </div>
    <div class="location-detail">
      <span class="location-label">Directions:</span>
      <span class="location-value technical">${trafficResult.structure.dir1Name}, ${trafficResult.structure.dir2Name}</span>
    </div>
    <div class="location-detail">
      <span class="location-label">Total Records:</span>
      <span class="location-value technical">${trafficResult.data.length.toLocaleString()}</span>
    </div>
  `;

  gridContainer.appendChild(addressCard);
  gridContainer.appendChild(technicalCard);
  container.appendChild(gridContainer);

  return container;
}