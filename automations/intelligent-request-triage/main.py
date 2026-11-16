import argparse
import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from classification import classify_by_rules, classify_with_ai

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
        description="Classify customer service requests."
    )

    parser.add_argument(
        "--mode",
        choices=["rules", "ia"],
        default="rules",
        help="Classification method: keyword rules or AI.",
    )

    parser.add_argument(
        "--entry",
        default=str(DATA_FILE),
        help="Path to the input CSV file.",
    )

    parser.add_argument(
        "--output",
        help="Optional path for the output CSV. Defaults to a timestamped folder.",
    )

    args = parser.parse_args()

    if args.mode == "ia" and not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "Set OPENAI_API_KEY to use --mode ia."
        )

    requests = pd.read_csv(args.entry)
    results = []

    for _, row in requests.iterrows():
        message = str(row["mensagem"])

        if args.mode == "ia":
            try:
                classification = classify_with_ai(message)
            except Exception as error:
                classification = classify_by_rules(message)
                classification["justificativa"] += (
                    f" Fallback local após erro na IA: "
                    f"{type(error).__name__}."
                )
        else:
            classification = classify_by_rules(message)

        results.append(
            {
                "id": row["id"],
                **classification,
                "metodo_solicitado": args.mode,
            }
        )

    output = pd.DataFrame(results)

    if args.output:
        output_path = Path(args.output)
        output_dir = output_path.parent
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = create_run_output_dir()
        output_path = output_dir / "results.csv"

    output.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig",
    )

    try:
        display_path = output_dir.relative_to(BASE_DIR)
    except ValueError:
        display_path = output_dir

    print(
        f"Classification complete. Generated files in: "
        f"{display_path}{os.sep}"
    )


if __name__ == "__main__":
    main()
