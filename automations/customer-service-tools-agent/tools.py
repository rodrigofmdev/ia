import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).parent
ORDERS_FILE = BASE_DIR / "data" / "orders_demo.json"

ORDERS = json.loads(ORDERS_FILE.read_text(encoding="utf-8"))

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "consultar_pedido",
            "description": "Consulta os dados de um pedido fictício pelo número.",
            "parameters": {
                "type": "object",
                "properties": {
                    "numero": {
                        "type": "string",
                        "description": "Número do pedido, por exemplo 1002.",
                    }
                },
                "required": ["numero"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_politica_troca",
            "description": "Consulta a política fictícia de troca da loja.",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
]


def consultar_pedido(numero: str) -> dict[str, Any]:
    """Look up an order in the local fictional dataset."""

    for order in ORDERS:
        if order["id"] == str(numero):
            return order.copy()

    return {"erro": "Pedido não encontrado na base de demonstração."}


def consultar_politica_troca() -> dict[str, str]:
    """Return the fictional exchange policy."""

    return {
        "prazo": "7 dias corridos após o recebimento",
        "condicao": "sem sinais de uso e com itens e embalagem preservados",
        "observacao": (
            "Consulte os termos oficiais da loja em uma aplicação real."
        ),
    }


def executar_ferramenta(
    nome: str,
    argumentos: dict[str, Any],
) -> dict[str, Any]:
    """Execute only the explicitly allowed, read-only tools."""

    if nome == "consultar_pedido":
        numero = argumentos.get("numero")
        if not isinstance(numero, str) or not numero.isdigit():
            return {"erro": "O número do pedido deve conter apenas dígitos."}
        return consultar_pedido(numero)

    if nome == "consultar_politica_troca":
        if argumentos:
            return {"erro": "Esta ferramenta não aceita argumentos."}
        return consultar_politica_troca()

    return {"erro": f"Ferramenta não permitida: {nome}."}
