import argparse
import os
import time
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

from analysis import generate_analysis
from reporting import build_report, generate_ai_summary

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data.csv"
OUTPUT_DIR = BASE_DIR / "output"


def create_run_output_dir() -> Path:
    """Create a unique output folder named with the current timestamp."""

    OUTPUT_DIR.mkdir(exist_ok=True)

    while True:
        run_output_dir = OUTPUT_DIR / datetime.now().strftime(
            "%Y-%m-%d-%H-%M-%S"
        )

        try:
            run_output_dir.mkdir()
        except FileExistsError:
            time.sleep(1)
        else:
            return run_output_dir


def main():
    parser = argparse.ArgumentParser(
        description="Generate an order analysis report."
    )

    parser.add_argument(
        "--input",
        default=str(DATA_FILE),
        help="Path to the input CSV file.",
    )

    parser.add_argument(
        "--ai-summary",
        action="store_true",
        help="Include an AI-generated interpretation in the report.",
    )

    args = parser.parse_args()

    category_summary, metrics = generate_analysis(args.input)

    ai_summary = None
    if args.ai_summary:
        if not os.getenv("OPENAI_API_KEY"):
            raise SystemExit(
                "Set OPENAI_API_KEY to use --ai-summary."
            )
        ai_summary = generate_ai_summary(metrics)

    run_output_dir = create_run_output_dir()

    category_summary.to_csv(
        run_output_dir / "orders_by_category.csv",
        index=False,
    )

    pd.Series(metrics).to_json(
        run_output_dir / "metrics.json",
        force_ascii=False,
        indent=2,
    )

    axis = category_summary.plot(
        kind="bar",
        x="category",
        y="total_order_value",
        legend=False,
        title="Valor total por categoria",
    )

    axis.set_xlabel("Categoria")
    axis.set_ylabel("Valor total (R$)")

    plt.tight_layout()

    plt.savefig(
        run_output_dir / "order_value_by_category.png",
        dpi=140,
    )

    plt.close()

    report_file = run_output_dir / "report.md"
    report_file.write_text(
        build_report(category_summary, metrics, ai_summary),
        encoding="utf-8",
    )

    relative_output_path = run_output_dir.relative_to(BASE_DIR)
    print(f"Analysis complete. Generated files in: {relative_output_path}")


if __name__ == "__main__":
    main()
