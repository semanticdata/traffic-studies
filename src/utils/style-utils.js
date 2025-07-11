/**
 * Style utilities for loading shared CSS and creating common UI elements
 */

/**
 * Load shared card styles
 * @returns {HTMLElement} - Style element with shared card CSS
 */
export function loadSharedCardStyles() {
  const style = document.createElement("style");
  style.textContent = `
    /* Shared Card Styles */
    .card-container {
      margin: 2rem 0;
    }

    .card-grid {
      display: grid;
      gap: 1.5rem;
      margin: 2rem 0;
    }

    .card-grid--small {
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    }

    .card-grid--medium {
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    }

    .card-grid--large {
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    }

    .card {
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

    .card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    /* Card color themes */
    .card--green { border-left: 4px solid #10b981; }
    .card--blue { border-left: 4px solid #3b82f6; }
    .card--red { border-left: 4px solid #ef4444; }
    .card--amber { border-left: 4px solid #f59e0b; }
    .card--purple { border-left: 4px solid #8b5cf6; }
    .card--indigo { border-left: 4px solid #6366f1; }
    .card--cyan { border-left: 4px solid #06b6d4; }
    .card--orange { border-left: 4px solid #f97316; }
    .card--yellow { border-left: 4px solid #fbbf24; }
    .card--gray { border-left: 4px solid #6b7280; }

    /* Card content elements */
    .card__icon {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
    }

    .card__label {
      font-size: 0.9rem;
      font-weight: 500;
      color: var(--theme-foreground-muted, #6b7280);
      margin-bottom: 0.5rem;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .card__value {
      font-size: 1.8rem;
      font-weight: 700;
      color: var(--theme-foreground, #374151);
      margin: 0.5rem 0;
    }

    .card__description {
      font-size: 0.85rem;
      color: var(--theme-foreground-muted, #6b7280);
      font-weight: 500;
      line-height: 1.4;
    }

    /* Colored values */
    .card__value--green { color: #10b981; }
    .card__value--blue { color: #3b82f6; }
    .card__value--red { color: #ef4444; }
    .card__value--amber { color: #f59e0b; }
    .card__value--purple { color: #8b5cf6; }
    .card__value--indigo { color: #6366f1; }
    .card__value--cyan { color: #06b6d4; }
    .card__value--orange { color: #f97316; }
    .card__value--yellow { color: #fbbf24; }
    .card__value--gray { color: #6b7280; }

    /* Gradient titles */
    .gradient-title {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 1.5rem;
      color: var(--theme-foreground, #374151);
      text-align: center;
    }

    .gradient-title--blue {
      background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .gradient-title--green {
      background: linear-gradient(135deg, #10b981 0%, #059669 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .gradient-title--red {
      background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .gradient-title--purple {
      background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .gradient-title--indigo {
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    /* Explanation boxes */
    .explanation-box {
      background: linear-gradient(135deg, var(--theme-background-alt, #f8fafc) 0%, var(--theme-background, #ffffff) 100%);
      padding: 1.5rem;
      border-radius: 12px;
      margin: 2rem 0;
      border-left: 4px solid;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    .explanation-box--blue {
      border-image: linear-gradient(135deg, #3b82f6, #6366f1) 1;
    }

    .explanation-box--green {
      border-image: linear-gradient(135deg, #10b981, #059669) 1;
    }

    .explanation-box--red {
      border-image: linear-gradient(135deg, #ef4444, #f97316) 1;
    }

    .explanation-box--purple {
      border-image: linear-gradient(135deg, #8b5cf6, #06b6d4) 1;
    }

    .explanation-box--indigo {
      border-image: linear-gradient(135deg, #6366f1, #8b5cf6) 1;
    }

    .explanation-box__title {
      margin: 0 0 1rem 0;
      color: var(--theme-foreground, #374151);
      font-size: 1.1rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .explanation-box__text {
      margin: 0.75rem 0;
      color: var(--theme-foreground-muted, #6b7280);
      font-size: 0.95rem;
      line-height: 1.6;
      padding-left: 1rem;
      position: relative;
    }

    .explanation-box__text::before {
      content: '•';
      position: absolute;
      left: 0;
      font-weight: bold;
    }

    .explanation-box__text--blue::before { color: #3b82f6; }
    .explanation-box__text--green::before { color: #10b981; }
    .explanation-box__text--red::before { color: #ef4444; }
    .explanation-box__text--purple::before { color: #8b5cf6; }
    .explanation-box__text--indigo::before { color: #6366f1; }
  `;

  return style;
}

/**
 * Create a card element with shared styling
 * @param {Object} options - Card configuration options
 * @param {string} options.icon - Emoji icon
 * @param {string} options.label - Card label
 * @param {string} options.value - Card value
 * @param {string} options.description - Optional description
 * @param {string} options.theme - Color theme (green, blue, red, etc.)
 * @returns {HTMLElement} - Styled card element
 */
export function createCard(options) {
  const { icon, label, value, description, theme = 'blue' } = options;

  const card = document.createElement("div");
  card.className = \`card card--\${theme}\`;
  
  let cardHTML = \`
    <div class="card__icon">\${icon}</div>
    <div class="card__label">\${label}</div>
    <div class="card__value card__value--\${theme}">\${value}</div>
  \`;
  
  if (description) {
    cardHTML += \`<div class="card__description">\${description}</div>\`;
  }
  
  card.innerHTML = cardHTML;
  return card;
}

/**
 * Create a gradient title element
 * @param {string} text - Title text
 * @param {string} theme - Color theme
 * @returns {HTMLElement} - Styled title element
 */
export function createGradientTitle(text, theme = 'blue') {
  const title = document.createElement("h3");
  title.className = \`gradient-title gradient-title--\${theme}\`;
  title.textContent = text;
  return title;
}

/**
 * Create an explanation box element
 * @param {string} title - Box title
 * @param {Array} texts - Array of explanation texts
 * @param {string} theme - Color theme
 * @param {string} emoji - Title emoji
 * @returns {HTMLElement} - Styled explanation box
 */
export function createExplanationBox(title, texts, theme = 'blue', emoji = '📊') {
  const box = document.createElement("div");
  box.className = \`explanation-box explanation-box--\${theme}\`;
  
  let boxHTML = \`
    <h4 class="explanation-box__title">
      <span>\${emoji}</span>
      \${title}
    </h4>
  \`;
  
  texts.forEach(text => {
    boxHTML += \`<p class="explanation-box__text explanation-box__text--\${theme}">\${text}</p>\`;
  });
  
  box.innerHTML = boxHTML;
  return box;
}
`;

  return style;
}