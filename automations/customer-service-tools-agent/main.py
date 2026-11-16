import argparse
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from tools import TOOL_DEFINITIONS, executar_ferramenta

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
MAX_TOOL_ROUNDS = 5

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


def execute_demo(question: str) -> tuple[str, list[dict[str, Any]]]:
    """Select and run a read-only tool using simple demo rules."""

    question_lower = question.lower()

    if any(word in question_lower for word in ("troca", "devolver", "devolução")):
        tool_name = "consultar_politica_troca"
        arguments: dict[str, Any] = {}
    else:
        order_numbers = re.findall(r"\b\d{4}\b", question)
        if not order_numbers:
            return (
                "Não identifiquei um número de pedido ou uma dúvida sobre "
                "trocas. Tente perguntar sobre um pedido, como o 1002, ou "
                "sobre a política de troca.",
                [],
            )
        tool_name = "consultar_pedido"
        arguments = {"numero": order_numbers[0]}

    result = executar_ferramenta(tool_name, arguments)
    tool_calls = [
        {
            "name": tool_name,
            "arguments": arguments,
            "result": result,
        }
    ]

    if "erro" in result:
        return result["erro"], tool_calls

    if tool_name == "consultar_politica_troca":
        answer = (
            f"A política fictícia permite solicitar a troca em até "
            f"{result['prazo']}, desde que o produto esteja "
            f"{result['condicao']}. {result['observacao']}"
        )
    else:
        formatted_amount = (
            f"{result['valor']:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
        answer = (
            f"O pedido {result['id']} está com status "
            f"'{result['status']}'. Previsão: {result['previsao']}. "
            f"Valor: R$ {formatted_amount}."
        )

    return answer, tool_calls


def execute_with_ai(question: str) -> tuple[str, list[dict[str, Any]]]:
    """Run the OpenAI tool-calling loop with an allowlist of tools."""

    from openai import OpenAI

    client = OpenAI()
    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "Você é um agente de atendimento. Responda em português "
                "brasileiro e use as ferramentas disponíveis quando "
                "necessário. As ferramentas são somente leitura e retornam "
                "dados fictícios. Nunca afirme que alterou pedidos, aprovou "
                "reembolsos ou realizou pagamentos. Se não houver ferramenta "
                "adequada, explique que não pode fazer essa operação."
            ),
        },
        {"role": "user", "content": question},
    ]
    tool_calls_made: list[dict[str, Any]] = []

    for round_number in range(MAX_TOOL_ROUNDS + 1):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
            temperature=0.2,
        )
        message = response.choices[0].message

        if not message.tool_calls:
            return message.content or "Não foi possível gerar uma resposta.", tool_calls_made

        if round_number == MAX_TOOL_ROUNDS:
            raise RuntimeError(
                f"The AI exceeded the limit of {MAX_TOOL_ROUNDS} tool rounds."
            )

        messages.append(message.model_dump(exclude_none=True))

        for tool_call in message.tool_calls:
            try:
                arguments = json.loads(tool_call.function.arguments)
                if not isinstance(arguments, dict):
                    raise ValueError("Tool arguments must be a JSON object.")
                result = executar_ferramenta(
                    tool_call.function.name,
                    arguments,
                )
            except (json.JSONDecodeError, ValueError) as error:
                arguments = {}
                result = {"erro": str(error)}

            tool_calls_made.append(
                {
                    "name": tool_call.function.name,
                    "arguments": arguments,
                    "result": result,
                }
            )
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )

    raise RuntimeError("The AI tool-calling loop ended unexpectedly.")


def main():
    parser = argparse.ArgumentParser(
        description="Demonstrate a customer service agent with read-only tools."
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--demo",
        dest="mode",
        action="store_const",
        const="demo",
        help="Select tools using simple local rules without an API.",
    )
    mode_group.add_argument(
        "--ai",
        dest="mode",
        action="store_const",
        const="ai",
        help="Use the OpenAI API to select and call tools.",
    )
    parser.set_defaults(mode="demo")

    parser.add_argument(
        "--pergunta",
        default="Onde está o pedido 1002?",
        help="Question to ask the customer service agent.",
    )
    args = parser.parse_args()

    if args.mode == "demo":
        answer, tool_calls = execute_demo(args.pergunta)
        mode = "demo"
    else:
        if not os.getenv("OPENAI_API_KEY"):
            raise SystemExit(
                "Set OPENAI_API_KEY to use --ai, or run with --demo."
            )
        answer, tool_calls = execute_with_ai(args.pergunta)
        mode = "ai"

    run_output_dir = create_run_output_dir()
    interaction_file = run_output_dir / "interaction.json"
    interaction_file.write_text(
        json.dumps(
            {
                "mode": mode,
                "question": args.pergunta,
                "tool_calls": tool_calls,
                "answer": answer,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    relative_output_path = run_output_dir.relative_to(BASE_DIR)
    print(f"Agent response: {answer}")
    print(f"Generated files in: {relative_output_path}{os.sep}")


if __name__ == "__main__":
    main()
