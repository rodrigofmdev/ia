import json


def classify_by_rules(message: str) -> dict[str, str]:
    """Classify a customer request using keyword rules."""

    text = message.lower()

    rules = [
        (
            ["cobrado duas vezes", "cobrança", "pagamento", "cartão"],
            "Pagamento",
            "Alta",
            "Financeiro",
        ),
        (
            ["não chegou", "atras", "prazo terminou", "endereço", "envio"],
            "Entrega",
            "Alta",
            "Logística",
        ),
        (
            ["trocar", "troca", "tamanho", "quebrado", "defeito"],
            "Produto",
            "Média",
            "Pós-venda",
        ),
        (
            ["aplicativo", "fecha sozinho", "erro", "não funciona"],
            "Problema técnico",
            "Média",
            "Tecnologia",
        ),
        (
            ["nota fiscal", "segunda via"],
            "Documentação",
            "Baixa",
            "Atendimento",
        ),
    ]

    for keywords, category, priority, team in rules:
        if any(keyword in text for keyword in keywords):
            return {
                "category": category,
                "priority": priority,
                "teams": team,
                "justificativa": "Classificação por palavras-chave.",
            }

    return {
        "category": "Não identificado",
        "priority": "A avaliar",
        "teams": "Atendimento",
        "justificativa": "A solicitação precisa de revisão humana.",
    }


def classify_with_ai(message: str) -> dict[str, str]:
    """Classify a customer request using the OpenAI API."""

    from openai import OpenAI

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "Você classifica solicitações de atendimento. "
                    "Retorne JSON com as chaves category, priority, "
                    "teams e justificativa. "
                    "priority deve ser Alta, Média ou Baixa. "
                    "Seja conservador e não invente informações."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        temperature=0.1,
    )

    data = json.loads(
        response.choices[0].message.content or "{}"
    )

    fields = (
        "category",
        "priority",
        "teams",
        "justificativa",
    )

    if not isinstance(data, dict) or not all(field in data for field in fields):
        raise ValueError(
            "The AI response is missing one or more required fields."
        )

    return {
        field: str(data[field])
        for field in fields
    }
