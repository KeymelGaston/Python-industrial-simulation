# Python-industrial-simulation
Multi-factory industrial stock simulator built in Python. Configurable parameters, Excel export, and multi-panel data visualization. Clean OOP architecture.
# Industrial Simulator

Simulates stock growth across multiple factories over a configurable number of months.
Outputs a summary table, an Excel file, and a chart.

---

## Requirements

Install the required libraries before running:

```
pip install pandas matplotlib openpyxl
```

---

## How to Run

```
python industrial_simulator.py
```

---

## How to Configure

Open `industrial_simulator.py` and edit **only** the top section marked:

```
⚙️  USER CONFIGURATION — EDIT HERE ONLY
```

Do not touch anything below the `🚫 DO NOT EDIT BELOW THIS LINE` marker.

### General settings

| Variable         | What it does                          | Example        |
|------------------|---------------------------------------|----------------|
| `MONTHS`         | Number of months to simulate          | `12`           |
| `EXPORT_TO_EXCEL`| Save results to an Excel file         | `True / False` |
| `OUTPUT_FILENAME`| Name of the output Excel file         | `"results.xlsx"` |

### Factory settings

Each factory is a block inside the `FACTORIES` list:

| Parameter               | What it does                                      | Example  |
|-------------------------|---------------------------------------------------|----------|
| `name`                  | Label shown in the table and chart                | `"FACTORY 1"` |
| `initial_stock`         | Starting stock level                              | `60.0`   |
| `initial_production`    | Production rate at month 0 (0.20 = 20%)           | `0.20`   |
| `production_growth`     | Monthly increase in production rate (0.02 = +2%)  | `0.02`   |
| `initial_consumption`   | Consumption rate at month 0 (0.05 = 5%)           | `0.05`   |
| `consumption_reduction` | Monthly decrease in consumption rate (0.03 = -3%) | `0.03`   |
| `color`                 | Line/bar color in the chart (hex code)            | `"#3B82F6"` |

### Adding a third factory

Uncomment the example block already included at the bottom of the `FACTORIES` list and adjust the values.

---

## Output

| File                        | Description                        |
|-----------------------------|------------------------------------|
| `simulation_factories.xlsx` | Table with monthly stock per factory |
| `simulation_factories.png`  | Chart saved automatically           |
| Console                     | Summary printed on every run        |

---

## Quick Example

Change `MONTHS` to `24` and `initial_stock` of Factory 1 to `80.0`, then run.
The table, chart, and Excel will all update automatically.
