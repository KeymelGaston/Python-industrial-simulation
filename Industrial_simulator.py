"""
Industrial Simulator - Multiple Factories
==========================================
HOW TO USE:
  1. Edit only the "USER CONFIGURATION" block below.
  2. Run the file: python industrial_simulator.py
  3. Results will be printed, saved as Excel, and shown as a chart.

Do NOT edit anything below the "DO NOT EDIT BELOW THIS LINE" marker.
"""


# ╔══════════════════════════════════════════════════════════════════════╗
# ║              ⚙️  USER CONFIGURATION — EDIT HERE ONLY               ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  Modify the values below to change the simulation behavior.         ║
# ║  Each factory can have completely different settings.               ║
# ╚══════════════════════════════════════════════════════════════════════╝

# ── SIMULATION SETTINGS ───────────────────────────────────────────────
MONTHS          = 12      # Number of months to simulate (e.g. 6, 12, 24)
EXPORT_TO_EXCEL = True    # Save results to Excel? True or False
OUTPUT_FILENAME = "simulation_factories.xlsx"

# ── FACTORY DEFINITIONS ───────────────────────────────────────────────
# Add or remove factories by copying/deleting a block.
# Each factory needs: name, initial_stock, initial_production,
#                     production_growth, initial_consumption,
#                     consumption_reduction, color

FACTORIES = [
    {
        "name":                 "FACTORY 1",
        "initial_stock":        60.0,   # Starting stock level
        "initial_production":   0.20,   # Production rate at month 0    (0.20 = 20%)
        "production_growth":    0.02,   # Monthly increase in production (0.02 = +2%)
        "initial_consumption":  0.05,   # Consumption rate at month 0   (0.05 =  5%)
        "consumption_reduction":0.03,   # Monthly decrease in consumption(0.03 = -3%)
        "color":                "#3B82F6",  # Chart color (hex code)
    },
    {
        "name":                 "FACTORY 2",
        "initial_stock":        60.0,
        "initial_production":   0.20,
        "production_growth":    0.02,
        "initial_consumption":  0.05,
        "consumption_reduction":0.03,
        "color":                "#10B981",
    },
    # ── To add a third factory, uncomment the block below: ────────────
    # {
    #     "name":                 "FACTORY 3",
    #     "initial_stock":        45.0,
    #     "initial_production":   0.18,
    #     "production_growth":    0.025,
    #     "initial_consumption":  0.06,
    #     "consumption_reduction":0.02,
    #     "color":                "#F59E0B",
    # },
]

# ╔══════════════════════════════════════════════════════════════════════╗
# ║           🚫  DO NOT EDIT BELOW THIS LINE                          ║
# ╚══════════════════════════════════════════════════════════════════════╝


import pandas as pd
import matplotlib.pyplot as plt
from dataclasses import dataclass, field


# ── CONFIGURATION MODELS ──────────────────────────────────────────────

@dataclass
class FactoryConfig:
    name: str
    initial_stock: float        = 60.0
    initial_production: float   = 0.20
    production_growth: float    = 0.02
    initial_consumption: float  = 0.05
    consumption_reduction: float= 0.03
    color: str                  = "#2563EB"

@dataclass
class SimulationConfig:
    months: int          = 12
    export_excel: bool   = True
    file_name: str       = "simulation_factories.xlsx"
    factories: list      = field(default_factory=list)

    def add_factory(self, factory: FactoryConfig) -> "SimulationConfig":
        self.factories.append(factory)
        return self


# ── FACTORY MODEL ─────────────────────────────────────────────────────

class Factory:
    def __init__(self, config: FactoryConfig):
        self.config  = config
        self.history = []

    def simulate(self, months: int) -> list:
        stock = self.config.initial_stock
        prod  = self.config.initial_production
        cons  = self.config.initial_consumption
        self.history = [round(stock, 4)]
        for _ in range(months):
            stock = stock * (1 + prod) * (1 - cons)
            self.history.append(round(stock, 4))
            prod *= (1 + self.config.production_growth)
            cons *= (1 - self.config.consumption_reduction)
        return self.history

    @property
    def final_stock(self) -> float:
        return self.history[-1] if self.history else 0.0

    @property
    def total_change(self) -> float:
        if not self.history:
            return 0.0
        return ((self.history[-1] / self.history[0]) - 1) * 100


# ── MAIN SIMULATOR ────────────────────────────────────────────────────

class IndustrialSimulator:
    def __init__(self, config: SimulationConfig):
        self.config    = config
        self.factories = [Factory(f) for f in config.factories]
        self.df        = None

    def run(self) -> "IndustrialSimulator":
        if not self.factories:
            raise ValueError("No factories configured for simulation.")
        for factory in self.factories:
            factory.simulate(self.config.months)
        cols = {"Month": list(range(self.config.months + 1))}
        for f in self.factories:
            cols[f.config.name] = f.history
        df = pd.DataFrame(cols)
        df["TOTAL"] = df[[f.config.name for f in self.factories]].sum(axis=1)
        self.df = df
        return self

    def print_summary(self) -> None:
        sep = "=" * 72
        print(f"\n{sep}")
        print(f"  INDUSTRIAL SIMULATOR — {len(self.factories)} FACTORY(IES) | {self.config.months} MONTHS")
        print(sep)
        for f in self.factories:
            sign = "▲" if f.total_change >= 0 else "▼"
            print(f"  {f.config.name:<20} "
                  f"{f.config.initial_stock:>8.2f} -> {f.final_stock:>8.2f}  "
                  f"{sign} {abs(f.total_change):.1f}%")
        ti = sum(f.config.initial_stock for f in self.factories)
        tf = sum(f.final_stock for f in self.factories)
        print(f"  {'TOTAL':<20} {ti:>8.2f} -> {tf:>8.2f}  "
              f"▲ {((tf / ti) - 1) * 100:.1f}%")
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
        fig.suptitle("INDUSTRIAL SIMULATOR — STOCK ANALYSIS",
                     fontsize=17, fontweight="bold", color="white", y=0.97)
        gs = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.3,
                              left=0.07, right=0.97, top=0.91, bottom=0.08)
        ax_main  = fig.add_subplot(gs[0, :])
        ax_bar   = fig.add_subplot(gs[1, 0])
        ax_delta = fig.add_subplot(gs[1, 1])

        for ax in (ax_main, ax_bar, ax_delta):
            ax.set_facecolor("#1E293B")
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")
            for spine in ax.spines.values():
                spine.set_color("#334155")

        for f in self.factories:
            ax_main.plot(months_axis, f.history, marker="o", markersize=4,
                         linewidth=2.5, color=f.config.color, label=f.config.name)
            ax_main.annotate(f"{f.final_stock:.1f}",
                             (months_axis[-1], f.final_stock),
                             xytext=(6, 0), textcoords="offset points",
                             color=f.config.color, fontsize=9, fontweight="bold", va="center")

        ax_main.plot(months_axis, self.df["TOTAL"], linewidth=3.5,
                     linestyle="--", color="white", label="TOTAL", zorder=5)
        ax_main.annotate(f"TOTAL: {self.df['TOTAL'].iloc[-1]:.1f}",
                         (months_axis[-1], self.df["TOTAL"].iloc[-1]),
                         xytext=(6, 0), textcoords="offset points",
                         color="white", fontsize=10, fontweight="bold", va="center")
        ax_main.set_title("Stock Evolution by Month", fontsize=13)
        ax_main.set_xlabel("Month")
        ax_main.set_ylabel("Stock (%)")
        ax_main.legend(facecolor="#0F172A", labelcolor="white",
                       edgecolor="#334155", fontsize=9)
        ax_main.grid(True, alpha=0.15, color="white")
        ax_main.set_xticks(months_axis)

        finals = [f.final_stock for f in self.factories]
        names  = [f.config.name for f in self.factories]
        colors = [f.config.color for f in self.factories]
        bars = ax_bar.bar(names, finals, color=colors, edgecolor="#0F172A", linewidth=1.5)
        for bar, val in zip(bars, finals):
            ax_bar.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                        f"{val:.1f}", ha="center", va="bottom",
                        color="white", fontsize=9, fontweight="bold")
        ax_bar.set_title("Final Stock per Factory", fontsize=11)
        ax_bar.set_ylabel("Stock (%)")
        ax_bar.grid(True, axis="y", alpha=0.15, color="white")

        changes = [f.total_change for f in self.factories]
        bc = ["#22C55E" if v >= 0 else "#EF4444" for v in changes]
        bars2 = ax_delta.bar(names, changes, color=bc, edgecolor="#0F172A", linewidth=1.5)
        for bar, val in zip(bars2, changes):
            ax_delta.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                          f"{val:+.1f}%", ha="center", va="bottom",
                          color="white", fontsize=9, fontweight="bold")
        ax_delta.set_title("Total Change (%)", fontsize=11)
        ax_delta.set_ylabel("Delta %")
        ax_delta.axhline(0, color="white", linewidth=0.8, alpha=0.5)
        ax_delta.grid(True, axis="y", alpha=0.15, color="white")

        plt.savefig("simulation_factories.png", dpi=150,
                    bbox_inches="tight", facecolor="#0F172A")
        print("  Chart saved: 'simulation_factories.png'")
        plt.show()


# ── ENTRY POINT ───────────────────────────────────────────────────────

def main():
    config = SimulationConfig(months=MONTHS,
                              export_excel=EXPORT_TO_EXCEL,
                              file_name=OUTPUT_FILENAME)
    for f in FACTORIES:
        config.add_factory(FactoryConfig(**f))

    sim = IndustrialSimulator(config)
    sim.run()
    sim.print_summary()
    if config.export_excel:
        sim.export_excel()
    sim.plot()

if __name__ == "__main__":
    main()
