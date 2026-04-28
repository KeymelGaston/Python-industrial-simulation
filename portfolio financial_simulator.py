"""
Investment Portfolio Simulator
===============================
HOW TO USE:
  1. Edit only the "USER CONFIGURATION" block below.
  2. Run the file: python portfolio_simulator.py
  3. Results will be printed, saved as Excel, and shown as a chart.

Do NOT edit anything below the "DO NOT EDIT BELOW THIS LINE" marker.
"""


# ╔══════════════════════════════════════════════════════════════════════╗
# ║              ⚙️  USER CONFIGURATION — EDIT HERE ONLY               ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  Modify the values below to change the simulation behavior.         ║
# ╚══════════════════════════════════════════════════════════════════════╝

# ── SIMULATION SETTINGS ───────────────────────────────────────────────
YEARS           = 1       # Number of years to simulate (e.g. 1, 5, 10)
INITIAL_CAPITAL = 10000   # Total amount to invest (in USD)
EXPORT_TO_EXCEL = True
OUTPUT_FILENAME = "portfolio_simulation.xlsx"

# ── ASSET DEFINITIONS ─────────────────────────────────────────────────
# weight       : % of total capital allocated to this asset (must add up to 1.0)
# annual_return: expected yearly return (0.10 = 10%)
# optimistic   : best case annual return
# pessimistic  : worst case annual return
# color        : chart color (hex code)

ASSETS = [
    {
        "name":        "Stocks",
        "weight":      0.50,       # 50% of portfolio
        "annual_return": 0.10,     # 10% average return
        "optimistic":  0.20,       # 20% best case
        "pessimistic": -0.10,      # -10% worst case
        "color":       "#3B82F6",
    },
    {
        "name":        "Bonds",
        "weight":      0.30,       # 30% of portfolio
        "annual_return": 0.05,     # 5% average return
        "optimistic":  0.08,       # 8% best case
        "pessimistic": 0.02,       # 2% worst case
        "color":       "#10B981",
    },
    {
        "name":        "Crypto",
        "weight":      0.20,       # 20% of portfolio
        "annual_return": 0.30,     # 30% average return
        "optimistic":  0.80,       # 80% best case
        "pessimistic": -0.50,      # -50% worst case
        "color":       "#F59E0B",
    },
]

# ╔══════════════════════════════════════════════════════════════════════╗
# ║           🚫  DO NOT EDIT BELOW THIS LINE                          ║
# ╚══════════════════════════════════════════════════════════════════════╝


import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass, field


# ── CONFIGURATION MODELS ──────────────────────────────────────────────

@dataclass
class AssetConfig:
    name: str
    weight: float
    annual_return: float
    optimistic: float
    pessimistic: float
    color: str = "#2563EB"

@dataclass
class PortfolioConfig:
    years: int           = 1
    initial_capital: float = 10000
    export_excel: bool   = True
    file_name: str       = "portfolio_simulation.xlsx"
    assets: list         = field(default_factory=list)

    def add_asset(self, asset: AssetConfig) -> "PortfolioConfig":
        self.assets.append(asset)
        return self


# ── ASSET MODEL ───────────────────────────────────────────────────────

class Asset:
    def __init__(self, config: AssetConfig, initial_capital: float):
        self.config          = config
        self.initial_capital = initial_capital * config.weight
        self.history_neutral    = []
        self.history_optimistic = []
        self.history_pessimistic= []

    def simulate(self, months: int):
        def run(rate):
            monthly = rate / 12
            value   = self.initial_capital
            history = [round(value, 2)]
            for _ in range(months):
                value *= (1 + monthly)
                history.append(round(value, 2))
            return history

        self.history_neutral     = run(self.config.annual_return)
        self.history_optimistic  = run(self.config.optimistic)
        self.history_pessimistic = run(self.config.pessimistic)

    @property
    def final_neutral(self):     return self.history_neutral[-1]
    @property
    def final_optimistic(self):  return self.history_optimistic[-1]
    @property
    def final_pessimistic(self): return self.history_pessimistic[-1]

    @property
    def total_change(self):
        if not self.history_neutral: return 0.0
        return ((self.final_neutral / self.initial_capital) - 1) * 100


# ── PORTFOLIO SIMULATOR ───────────────────────────────────────────────

class PortfolioSimulator:
    def __init__(self, config: PortfolioConfig):
        self.config  = config
        self.months  = config.years * 12
        self.assets  = [Asset(a, config.initial_capital) for a in config.assets]
        self.df      = None

    def run(self) -> "PortfolioSimulator":
        if not self.assets:
            raise ValueError("No assets configured.")
        for asset in self.assets:
            asset.simulate(self.months)

        months_col = list(range(self.months + 1))
        cols = {"Month": months_col}

        for a in self.assets:
            cols[f"{a.config.name} (Neutral)"]     = a.history_neutral
            cols[f"{a.config.name} (Optimistic)"]  = a.history_optimistic
            cols[f"{a.config.name} (Pessimistic)"] = a.history_pessimistic

        df = pd.DataFrame(cols)

        # Total portfolio per scenario
        df["TOTAL (Neutral)"]     = sum(df[f"{a.config.name} (Neutral)"]     for a in self.assets)
        df["TOTAL (Optimistic)"]  = sum(df[f"{a.config.name} (Optimistic)"]  for a in self.assets)
        df["TOTAL (Pessimistic)"] = sum(df[f"{a.config.name} (Pessimistic)"] for a in self.assets)

        self.df = df
        return self

    def print_summary(self) -> None:
        sep = "=" * 72
        total_neutral     = sum(a.final_neutral     for a in self.assets)
        total_optimistic  = sum(a.final_optimistic  for a in self.assets)
        total_pessimistic = sum(a.final_pessimistic for a in self.assets)

        print(f"\n{sep}")
        print(f"  PORTFOLIO SIMULATOR — {self.config.years} YEAR(S) | "
              f"Initial Capital: ${self.config.initial_capital:,.2f}")
        print(sep)
        print(f"  {'ASSET':<12} {'ALLOCATED':>10} {'NEUTRAL':>10} {'OPTIMISTIC':>12} {'PESSIMISTIC':>13} {'Δ%':>8}")
        print("-" * 72)
        for a in self.assets:
            print(f"  {a.config.name:<12} "
                  f"${a.initial_capital:>9,.2f} "
                  f"${a.final_neutral:>9,.2f} "
                  f"${a.final_optimistic:>11,.2f} "
                  f"${a.final_pessimistic:>12,.2f} "
                  f"{a.total_change:>+7.1f}%")
        print("-" * 72)
        change = ((total_neutral / self.config.initial_capital) - 1) * 100
        print(f"  {'TOTAL':<12} "
              f"${self.config.initial_capital:>9,.2f} "
              f"${total_neutral:>9,.2f} "
              f"${total_optimistic:>11,.2f} "
              f"${total_pessimistic:>12,.2f} "
              f"{change:>+7.1f}%")
        print(sep)
        if self.df is not None:
            print("\n" + self.df.to_string(index=False))

    def export_excel(self) -> None:
        with pd.ExcelWriter(self.config.file_name, engine="openpyxl") as writer:
            self.df.to_excel(writer, sheet_name="Simulation", index=False)
            ws = writer.sheets["Simulation"]
            for col in ws.columns:
                ws.column_dimensions[col[0].column_letter].width = (
                    max(len(str(c.value)) for c in col if c.value) + 4
                )
        print(f"\n  File saved: '{self.config.file_name}'")

    def plot(self) -> None:
        months_axis = self.df["Month"].tolist()

        fig = plt.figure(figsize=(16, 9), facecolor="#0F172A")
        fig.suptitle("INVESTMENT PORTFOLIO SIMULATOR — SCENARIO ANALYSIS",
                     fontsize=17, fontweight="bold", color="white", y=0.97)

        gs = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.3,
                              left=0.07, right=0.97, top=0.91, bottom=0.08)

        ax_main  = fig.add_subplot(gs[0, :])
        ax_bar   = fig.add_subplot(gs[1, 0])
        ax_scene = fig.add_subplot(gs[1, 1])

        for ax in (ax_main, ax_bar, ax_scene):
            ax.set_facecolor("#1E293B")
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")
            for spine in ax.spines.values():
                spine.set_color("#334155")

        # ── Main: neutral per asset ──────────────────────────────────
        for a in self.assets:
            ax_main.plot(months_axis, a.history_neutral,
                         marker="o", markersize=3, linewidth=2.5,
                         color=a.config.color, label=a.config.name)
            ax_main.annotate(f"${a.final_neutral:,.0f}",
                             (months_axis[-1], a.final_neutral),
                             xytext=(6, 0), textcoords="offset points",
                             color=a.config.color, fontsize=9,
                             fontweight="bold", va="center")

        ax_main.plot(months_axis, self.df["TOTAL (Neutral)"],
                     linewidth=3.5, linestyle="--", color="white",
                     label="TOTAL", zorder=5)
        ax_main.annotate(f"TOTAL: ${self.df['TOTAL (Neutral)'].iloc[-1]:,.0f}",
                         (months_axis[-1], self.df["TOTAL (Neutral)"].iloc[-1]),
                         xytext=(6, 0), textcoords="offset points",
                         color="white", fontsize=10, fontweight="bold", va="center")
        ax_main.set_title("Portfolio Growth by Month (Neutral Scenario)", fontsize=13)
        ax_main.set_xlabel("Month")
        ax_main.set_ylabel("Value (USD)")
        ax_main.legend(facecolor="#0F172A", labelcolor="white",
                       edgecolor="#334155", fontsize=9)
        ax_main.grid(True, alpha=0.15, color="white")
        ax_main.set_xticks(months_axis)

        # ── Bar: final value per asset ───────────────────────────────
        names  = [a.config.name for a in self.assets]
        finals = [a.final_neutral for a in self.assets]
        colors = [a.config.color for a in self.assets]
        bars = ax_bar.bar(names, finals, color=colors,
                          edgecolor="#0F172A", linewidth=1.5)
        for bar, val in zip(bars, finals):
            ax_bar.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 10,
                        f"${val:,.0f}", ha="center", va="bottom",
                        color="white", fontsize=9, fontweight="bold")
        ax_bar.set_title("Final Value per Asset (Neutral)", fontsize=11)
        ax_bar.set_ylabel("USD")
        ax_bar.grid(True, axis="y", alpha=0.15, color="white")

        # ── Grouped bar: 3 scenarios total ──────────────────────────
        scenario_vals = [
            self.df["TOTAL (Pessimistic)"].iloc[-1],
            self.df["TOTAL (Neutral)"].iloc[-1],
            self.df["TOTAL (Optimistic)"].iloc[-1],
        ]
        scenario_labels = ["Pessimistic", "Neutral", "Optimistic"]
        scenario_colors = ["#EF4444", "#94A3B8", "#22C55E"]
        bars2 = ax_scene.bar(scenario_labels, scenario_vals,
                             color=scenario_colors,
                             edgecolor="#0F172A", linewidth=1.5)
        for bar, val in zip(bars2, scenario_vals):
            ax_scene.text(bar.get_x() + bar.get_width() / 2,
                          bar.get_height() + 10,
                          f"${val:,.0f}", ha="center", va="bottom",
                          color="white", fontsize=9, fontweight="bold")
        ax_scene.axhline(self.config.initial_capital, color="white",
                         linewidth=1, linestyle="--", alpha=0.5)
        ax_scene.set_title("Total Portfolio — 3 Scenarios", fontsize=11)
        ax_scene.set_ylabel("USD")
        ax_scene.grid(True, axis="y", alpha=0.15, color="white")

        plt.savefig("portfolio_simulation.png", dpi=150,
                    bbox_inches="tight", facecolor="#0F172A")
        print("  Chart saved: 'portfolio_simulation.png'")
        plt.show()


# ── ENTRY POINT ───────────────────────────────────────────────────────

def main():
    config = PortfolioConfig(
        years=YEARS,
        initial_capital=INITIAL_CAPITAL,
        export_excel=EXPORT_TO_EXCEL,
        file_name=OUTPUT_FILENAME
    )
    for a in ASSETS:
        config.add_asset(AssetConfig(**a))

    sim = PortfolioSimulator(config)
    sim.run()
    sim.print_summary()
    if config.export_excel:
        sim.export_excel()
    sim.plot()

if __name__ == "__main__":
    main()
