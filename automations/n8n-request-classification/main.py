import argparse
import csv
import os
import time
from datetime import datetime
from pathlib import Path

from classification import classify_by_rules, classify_with_ai

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
DEFAULT_REQUEST = "Meu pedido ainda não chegou e o prazo de entrega terminou."
OUTPUT_FIELDS = (
    "created_at",
    "request",
    "category",
    "priority",
    "responsible_team",
    "rationale",
    "mode",
)


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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Classify a customer request and save the result."
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--demo",
        dest="mode",
        action="store_const",
        const="demo",
        help="Classify locally without an API key (default).",
    )
    mode_group.add_argument(
        "--ai",
        dest="mode",
        action="store_const",
        const="ai",
        help="Classify with the OpenAI API.",
    )
    parser.set_defaults(mode="demo")
    parser.add_argument(
        "--request",
        default=DEFAULT_REQUEST,
        help="Customer request text to classify.",
    )
    args = parser.parse_args()

    if args.mode == "ai":
        if not os.getenv("OPENAI_API_KEY"):
            raise SystemExit(
                "Set OPENAI_API_KEY to use --ai, or run with --demo."
            )
        classification = classify_with_ai(args.request)
    else:
        classification = classify_by_rules(args.request)

    run_output_dir = create_run_output_dir()
    result_path = run_output_dir / "classified_request.csv"
    result = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "request": args.request,
        **classification,
        "mode": args.mode,
    }

    with result_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerow(result)

    relative_output_path = run_output_dir.relative_to(BASE_DIR)
    print("Classification complete.")
    print(f"Generated files in: {relative_output_path}{os.sep}")
    print(f"Request: {args.request}")
    print(f"Category: {classification['category']}")
    print(f"Priority: {classification['priority']}")
    print(f"Responsible team: {classification['responsible_team']}")
    print(f"Rationale: {classification['rationale']}")


if __name__ == "__main__":
    main()
