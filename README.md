# Traffic Studies

Dashboard for analyzing traffic studies data for Crystal, Minnesota.

## 🚀 Usage

1. Clone the repository:

```bash
git clone https://github.com/semanticdata/traffic-studies.git
cd traffic-studies
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Run the dashboard:

```bash
streamlit run dashboard.py
```

## 📦 Data

Key Metrics:

- Total Vehicles
- Average Speed (Northbound/Eastbound)
- Average Speed (Southbound/Westbound)
- Speed Compliance (%)
- Daily Traffic - Average and Max
- Peak Hour (Number of Vehicles)
- Dominant Direction
- Busiest Day
- 85th Percentile Speed
- Peak Hour Factor (PHF)
- High Speed Violations
- Weekday/Weekend Ratio

Traffic Volume:

- Hourly Traffic Volume Distribution (per direction of travel)
- Daily Traffic Volume Patterns

Speed Analysis:

- Speed Violation Severity Analysis (+5, +10, +15 mph over)
- Speed Distribution (per direction of travel)
- Speed Compliance Analysis by Direction

Vehicle Classifications:

- 🏍️ Class 1: Motorcycles
- 🚗 Class 2: Passenger Cars
- 🚐 Class 3: Pickups, Vans
- 🚌 Class 4: Buses
- 🚛 Class 5: 2 Axles, 6 Tires
- 🚛 Class 6: 3 Axles

## 📜 License

The code in this repository is available under the [MIT License](LICENSE).
