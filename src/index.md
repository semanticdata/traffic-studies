# Traffic Studies Dashboard

Welcome to the Crystal, Minnesota traffic analysis dashboard. Select a location below to view detailed traffic data and analysis.

## Available Locations

Choose a location to view detailed traffic analysis:

<style>
  .location-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
  }
  
  .location-card {
    background: var(--theme-background-alt, #f8fafc);
    border: 1px solid var(--theme-foreground-muted, #e1e5e9);
    border-radius: 8px;
    padding: 1rem;
    text-decoration: none;
    color: var(--theme-foreground, #374151);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }
  
  .location-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    text-decoration: none;
  }
  
  .location-name {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    color: var(--theme-foreground-focus, #2563eb);
  }
  
  .location-details {
    font-size: 0.9rem;
    color: var(--theme-foreground-muted, #6b7280);
    margin: 0;
  }
</style>

<div class="location-grid">
  <a href="./2809-hampshire-ave" class="location-card">
    <div class="location-name">2809 Hampshire Ave</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
  
  <a href="./2941-hampshire-ave" class="location-card">
    <div class="location-name">2941 Hampshire Ave</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
  
  <a href="./3528-noble-ave" class="location-card">
    <div class="location-name">3528 Noble Ave</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
  
  <a href="./3618-adair-ave" class="location-card">
    <div class="location-name">3618 Adair Ave</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
  
  <a href="./3624-welcome-ave" class="location-card">
    <div class="location-name">3624 Welcome Ave</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
  
  <a href="./4017-jersey-ave" class="location-card">
    <div class="location-name">4017 Jersey Ave</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
  
  <a href="./4848-nevada-ave-n" class="location-card">
    <div class="location-name">4848 Nevada Ave N</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
  
  <a href="./5240-maryland-ave-n" class="location-card">
    <div class="location-name">5240 Maryland Ave N</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
  
  <a href="./5336-kentucky-ave-n" class="location-card">
    <div class="location-name">5336 Kentucky Ave N</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
  
  <a href="./5716-elmhurst-ave" class="location-card">
    <div class="location-name">5716 Elmhurst Ave</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
  
  <a href="./6420-41st-ave" class="location-card">
    <div class="location-name">6420 41st Ave</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
  
  <a href="./6702-45th-ave-n" class="location-card">
    <div class="location-name">6702 45th Ave N</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
  
  <a href="./7206-58th-ave" class="location-card">
    <div class="location-name">7206 58th Ave</div>
    <div class="location-details">Speed limit: 30 mph</div>
  </a>
</div>

---

**About this dashboard**: This application analyzes traffic data from PicoCount 2500 traffic counters deployed throughout Crystal, Minnesota. Each location provides detailed analysis of traffic patterns, speed compliance, and vehicle classifications.
