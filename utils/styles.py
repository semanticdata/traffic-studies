# Custom CSS and styling configurations

CUSTOM_CSS = """
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: rgba(128, 128, 128, 0.1);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stMetric:hover {
        transform: translateY(-2px);
        transition: all 0.2s ease;
    }
    .stMetric > div[data-testid="stMetricLabel"] {
        color: var(--text-color);
    }
    .stMetric > div[data-testid="stMetricValue"] {
        color: var(--text-color);
        font-size: 1.6rem;
    }
    h1, h2, h3 {
        color: var(--text-color);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
    }
    </style>
"""
