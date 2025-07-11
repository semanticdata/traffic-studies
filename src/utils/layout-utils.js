/**
 * Layout utilities for consistent section and container styling
 */

/**
 * Load shared layout styles
 * @returns {HTMLElement} - Style element with layout CSS
 */
export function loadSharedLayoutStyles() {
  const style = document.createElement("style");
  style.textContent = `
    /* Section containers */
    .section-container {
      margin: 2rem 0;
    }
    
    .section-container--compact {
      margin: 1rem 0;
    }
    
    .section-container--spacious {
      margin: 3rem 0;
    }
    
    /* Section headers */
    .section-header {
      margin-bottom: 1.5rem;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid var(--theme-foreground-muted, #e1e5e9);
    }
    
    .section-title {
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--theme-foreground, #374151);
      margin: 0;
    }
    
    .section-subtitle {
      font-size: 0.9rem;
      color: var(--theme-foreground-muted, #6b7280);
      margin: 0.5rem 0 0 0;
      font-weight: 500;
    }
    
    /* Content grids */
    .content-grid {
      display: grid;
      gap: 1.5rem;
      margin: 1.5rem 0;
    }
    
    .content-grid--2col {
      grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    }
    
    .content-grid--3col {
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    }
    
    .content-grid--4col {
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    }
    
    /* Flex layouts */
    .flex-container {
      display: flex;
      gap: 1.5rem;
      margin: 1.5rem 0;
    }
    
    .flex-container--column {
      flex-direction: column;
    }
    
    .flex-container--wrap {
      flex-wrap: wrap;
    }
    
    .flex-container--center {
      justify-content: center;
      align-items: center;
    }
    
    .flex-container--between {
      justify-content: space-between;
      align-items: center;
    }
    
    /* Content panels */
    .content-panel {
      background: var(--theme-background-alt, #f8fafc);
      border: 1px solid var(--theme-foreground-muted, #e1e5e9);
      border-radius: 8px;
      padding: 1.5rem;
      margin: 1rem 0;
    }
    
    .content-panel--elevated {
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .content-panel--bordered {
      border: 2px solid var(--theme-foreground-muted, #e1e5e9);
    }
    
    /* Dividers */
    .divider {
      border: none;
      height: 1px;
      background: var(--theme-foreground-muted, #e1e5e9);
      margin: 2rem 0;
    }
    
    .divider--thick {
      height: 2px;
      background: var(--theme-foreground-muted, #d1d5db);
    }
    
    .divider--dashed {
      background: none;
      border-top: 1px dashed var(--theme-foreground-muted, #e1e5e9);
    }
    
    /* Responsive utilities */
    @media (max-width: 768px) {
      .content-grid--2col,
      .content-grid--3col,
      .content-grid--4col {
        grid-template-columns: 1fr;
      }
      
      .flex-container {
        flex-direction: column;
      }
      
      .section-container {
        margin: 1rem 0;
      }
    }
    
    /* Spacing utilities */
    .spacing-sm { margin: 0.5rem 0; }
    .spacing-md { margin: 1rem 0; }
    .spacing-lg { margin: 1.5rem 0; }
    .spacing-xl { margin: 2rem 0; }
    
    .padding-sm { padding: 0.5rem; }
    .padding-md { padding: 1rem; }
    .padding-lg { padding: 1.5rem; }
    .padding-xl { padding: 2rem; }
    
    /* Background utilities */
    .bg-primary { background: var(--theme-background, #ffffff); }
    .bg-secondary { background: var(--theme-background-alt, #f8fafc); }
    .bg-muted { background: var(--theme-foreground-muted, #f1f5f9); }
    
    /* Border utilities */
    .border-light { border: 1px solid var(--theme-foreground-muted, #e1e5e9); }
    .border-medium { border: 2px solid var(--theme-foreground-muted, #d1d5db); }
    .border-rounded { border-radius: 8px; }
    .border-rounded-lg { border-radius: 12px; }
  `;

  return style;
}

/**
 * Create a section with consistent styling
 * @param {Object} options - Section options
 * @returns {HTMLElement} - Styled section element
 */
export function createSection(options = {}) {
  const {
    title,
    subtitle,
    className = "",
    spacing = "normal", // compact, normal, spacious
    withHeader = true
  } = options;

  const container = document.createElement("div");
  container.appendChild(loadSharedLayoutStyles());

  const section = document.createElement("section");
  let sectionClasses = "section-container";
  if (spacing === "compact") sectionClasses += " section-container--compact";
  if (spacing === "spacious") sectionClasses += " section-container--spacious";
  if (className) sectionClasses += ` ${className}`;
  section.className = sectionClasses;

  if (withHeader && title) {
    const header = document.createElement("div");
    header.className = "section-header";

    const titleElement = document.createElement("h2");
    titleElement.className = "section-title";
    titleElement.textContent = title;
    header.appendChild(titleElement);

    if (subtitle) {
      const subtitleElement = document.createElement("p");
      subtitleElement.className = "section-subtitle";
      subtitleElement.textContent = subtitle;
      header.appendChild(subtitleElement);
    }

    section.appendChild(header);
  }

  container.appendChild(section);
  return { container, section };
}

/**
 * Create a content grid with consistent styling
 * @param {Array} items - Array of HTML elements to add to grid
 * @param {Object} options - Grid options
 * @returns {HTMLElement} - Styled grid element
 */
export function createContentGrid(items, options = {}) {
  const {
    columns = 3, // 2, 3, or 4
    className = ""
  } = options;

  const grid = document.createElement("div");
  let gridClasses = "content-grid";
  if (columns === 2) gridClasses += " content-grid--2col";
  else if (columns === 3) gridClasses += " content-grid--3col";
  else if (columns === 4) gridClasses += " content-grid--4col";
  if (className) gridClasses += ` ${className}`;
  grid.className = gridClasses;

  items.forEach(item => {
    grid.appendChild(item);
  });

  return grid;
}

/**
 * Create a flex container with consistent styling
 * @param {Array} items - Array of HTML elements to add to container
 * @param {Object} options - Flex options
 * @returns {HTMLElement} - Styled flex container
 */
export function createFlexContainer(items, options = {}) {
  const {
    direction = "row", // row, column
    wrap = false,
    justify = "start", // start, center, between, around, evenly
    align = "stretch", // start, center, end, stretch
    className = ""
  } = options;

  const container = document.createElement("div");
  let containerClasses = "flex-container";
  if (direction === "column") containerClasses += " flex-container--column";
  if (wrap) containerClasses += " flex-container--wrap";
  if (justify === "center") containerClasses += " flex-container--center";
  if (justify === "between") containerClasses += " flex-container--between";
  if (className) containerClasses += ` ${className}`;
  container.className = containerClasses;

  items.forEach(item => {
    container.appendChild(item);
  });

  return container;
}

/**
 * Create a content panel with consistent styling
 * @param {HTMLElement} content - Content to wrap in panel
 * @param {Object} options - Panel options
 * @returns {HTMLElement} - Styled panel element
 */
export function createContentPanel(content, options = {}) {
  const {
    elevated = false,
    bordered = false,
    className = ""
  } = options;

  const panel = document.createElement("div");
  let panelClasses = "content-panel";
  if (elevated) panelClasses += " content-panel--elevated";
  if (bordered) panelClasses += " content-panel--bordered";
  if (className) panelClasses += ` ${className}`;
  panel.className = panelClasses;

  panel.appendChild(content);
  return panel;
}

/**
 * Create a divider element
 * @param {Object} options - Divider options
 * @returns {HTMLElement} - Styled divider element
 */
export function createDivider(options = {}) {
  const {
    thick = false,
    dashed = false,
    className = ""
  } = options;

  const divider = document.createElement("hr");
  let dividerClasses = "divider";
  if (thick) dividerClasses += " divider--thick";
  if (dashed) dividerClasses += " divider--dashed";
  if (className) dividerClasses += ` ${className}`;
  divider.className = dividerClasses;

  return divider;
}

/**
 * Create a responsive two-column layout
 * @param {HTMLElement} leftContent - Left column content
 * @param {HTMLElement} rightContent - Right column content
 * @param {Object} options - Layout options
 * @returns {HTMLElement} - Two-column layout
 */
export function createTwoColumnLayout(leftContent, rightContent, options = {}) {
  const container = createContentGrid([leftContent, rightContent], {
    columns: 2,
    ...options
  });

  return container;
}

/**
 * Create a dashboard layout with consistent sections
 * @param {Array} sections - Array of section objects
 * @returns {HTMLElement} - Complete dashboard layout
 */
export function createDashboardLayout(sections) {
  const container = document.createElement("div");
  container.appendChild(loadSharedLayoutStyles());

  const dashboard = document.createElement("div");
  dashboard.className = "dashboard-layout";

  sections.forEach((sectionData, index) => {
    const { container: sectionContainer, section } = createSection(sectionData);

    if (sectionData.content) {
      if (Array.isArray(sectionData.content)) {
        const grid = createContentGrid(sectionData.content, {
          columns: sectionData.columns || 3
        });
        section.appendChild(grid);
      } else {
        section.appendChild(sectionData.content);
      }
    }

    dashboard.appendChild(sectionContainer);

    // Add divider between sections (except last one)
    if (index < sections.length - 1) {
      const divider = createDivider();
      dashboard.appendChild(divider);
    }
  });

  container.appendChild(dashboard);
  return container;
}