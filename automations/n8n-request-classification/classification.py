import json


CATEGORIES = (
    "Pagamento",
    "Entrega",
    "Produto",
    "Problema técnico",
    "Documentação",
    "Outro",
)
PRIORITIES = ("Alta", "Média", "Baixa")


def classify_by_rules(request: str) -> dict[str, str]:
    """Classify a request locally using simple keyword rules."""

    text = request.casefold()
    rules = [
        (
            ("cobrado duas vezes", "cobrança", "pagamento", "cartão"),
            "Pagamento",
            "Alta",
            "Financeiro",
        ),
        (
            ("não chegou", "atras", "prazo terminou", "endereço", "envio"),
            "Entrega",
            "Alta",
            "Logística",
        ),
        (
            ("trocar", "troca", "tamanho", "quebrado", "defeito"),
            "Produto",
            "Média",
            "Pós-venda",
        ),
        (
            ("aplicativo", "fecha sozinho", "erro", "não funciona"),
            "Problema técnico",
            "Média",
            "Tecnologia",
        ),
        (
            ("nota fiscal", "segunda via"),
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
                "responsible_team": team,
                "rationale": "Classificação local baseada em palavras-chave.",
            }

    return {
        "category": "Outro",
        "priority": "Média",
        "responsible_team": "Atendimento",
        "rationale": "Solicitação não identificada pelas regras locais.",
    }


def classify_with_ai(request: str) -> dict[str, str]:
    """Classify a request using the OpenAI API and validate its response."""

    from openai import OpenAI

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "Classifique solicitações de atendimento em português do "
                    "Brasil. Retorne somente um objeto JSON com as chaves "
                    "category, priority, responsible_team e rationale. "
                    f"category deve ser uma destas opções: {', '.join(CATEGORIES)}. "
                    f"priority deve ser uma destas opções: {', '.join(PRIORITIES)}. "
                    "Não invente informações."
                ),
            },
            {"role": "user", "content": request},
        ],
        temperature=0.1,
    )

    content = response.choices[0].message.content
    try:
        result = json.loads(content or "")
    except json.JSONDecodeError as error:
        raise ValueError("A IA retornou uma resposta que não é JSON válido.") from error

    required_fields = (
        "category",
        "priority",
        "responsible_team",
        "rationale",
    )
    if not isinstance(result, dict) or not all(
        isinstance(result.get(field), str) and result[field].strip()
        for field in required_fields
    ):
        raise ValueError("A resposta da IA não contém todos os campos válidos.")

    if result["category"] not in CATEGORIES:
        raise ValueError("A IA retornou uma categoria não permitida.")
    if result["priority"] not in PRIORITIES:
        raise ValueError("A IA retornou uma prioridade não permitida.")

    return {field: result[field].strip() for field in required_fields}
