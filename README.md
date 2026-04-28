# Industrial & Financial Simulation Suite

A collection of Python simulation tools designed for industrial and financial analysis.
Each tool is fully configurable by the user — no coding knowledge required to run and adjust parameters.

---

## Tools Included

### 1. Industrial Simulator
Simulates stock growth across multiple factories over a configurable number of months.
Models production rates, consumption rates, and their monthly evolution.

### 2. Portfolio financial Simulator
Simulates the growth of an investment portfolio across multiple asset classes.
Models three scenarios — neutral, optimistic, and pessimistic — over a configurable time period.

---

## Requirements

Install the required libraries before running either tool:

```
pip install pandas matplotlib openpyxl
```

---

## How to Run

```
python industrial_simulator.py
```
```
python portfolio_simulator.py
```

---

## How to Configure

Both tools follow the same structure.
Open the file and edit **only** the top section marked:

```
⚙️  USER CONFIGURATION — EDIT HERE ONLY
```

Do not touch anything below the `🚫 DO NOT EDIT BELOW THIS LINE` marker.

---

## Industrial Simulator — Parameters

### General settings

| Variable          | What it does                          | Example          |
|-------------------|---------------------------------------|------------------|
| `MONTHS`          | Number of months to simulate          | `12`             |
| `EXPORT_TO_EXCEL` | Save results to an Excel file         | `True / False`   |
| `OUTPUT_FILENAME` | Name of the output Excel file         | `"results.xlsx"` |

### Factory settings

| Parameter                | What it does                                       | Example       |
|--------------------------|----------------------------------------------------|---------------|
| `name`                   | Label shown in the table and chart                 | `"FACTORY 1"` |
| `initial_stock`          | Starting stock level                               | `60.0`        |
| `initial_production`     | Production rate at month 0 (0.20 = 20%)            | `0.20`        |
| `production_growth`      | Monthly increase in production rate (0.02 = +2%)   | `0.02`        |
| `initial_consumption`    | Consumption rate at month 0 (0.05 = 5%)            | `0.05`        |
| `consumption_reduction`  | Monthly decrease in consumption rate (0.03 = -3%)  | `0.03`        |
| `color`                  | Line/bar color in the chart (hex code)             | `"#3B82F6"`   |

---

## Portfolio Simulator — Parameters

### General settings

| Variable          | What it does                          | Example          |
|-------------------|---------------------------------------|------------------|
| `YEARS`           | Number of years to simulate           | `1`              |
| `INITIAL_CAPITAL` | Total amount to invest (USD)          | `10000`          |
| `EXPORT_TO_EXCEL` | Save results to an Excel file         | `True / False`   |
| `OUTPUT_FILENAME` | Name of the output Excel file         | `"results.xlsx"` |

### Asset settings

| Parameter        | What it does                                  | Example     |
|------------------|-----------------------------------------------|-------------|
| `name`           | Label shown in the table and chart            | `"Stocks"`  |
| `weight`         | % of capital allocated (must add up to 1.0)   | `0.50`      |
| `annual_return`  | Expected yearly return (0.10 = 10%)           | `0.10`      |
| `optimistic`     | Best case annual return                       | `0.20`      |
| `pessimistic`    | Worst case annual return                      | `-0.10`     |
| `color`          | Line/bar color in the chart (hex code)        | `"#3B82F6"` |

---

## Output

Both tools generate the same types of output:

| File          | Description                                  |
|---------------|----------------------------------------------|
| `.xlsx`       | Monthly breakdown table per asset or factory |
| `.png`        | Chart saved automatically                    |
| Console       | Summary table printed on every run           |

---

## Project Structure

```
├── industrial_simulator.py   # Factory stock growth simulator
├── portfolio financial_simulator.py    # Investment portfolio simulator
└── README.md                 # This file
```

