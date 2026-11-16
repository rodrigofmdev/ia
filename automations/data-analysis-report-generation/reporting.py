import pandas as pd


def format_brazilian_number(value: float) -> str:
    integer_part, decimal_part = f"{value:.2f}".split(".")
    grouped_integer = f"{int(integer_part):,}".replace(",", ".")
    return f"{grouped_integer},{decimal_part}"


def format_brazilian_percentage(value: float) -> str:
    return f"{value:.1f}%".replace(".", ",")


def format_brazilian_list(values: list[str]) -> str:
    if len(values) == 1:
        return values[0]
    if len(values) == 2:
        return " e ".join(values)
    return f"{', '.join(values[:-1])} e {values[-1]}"


def generate_general_interpretation(
    category_summary: pd.DataFrame,
    metrics: dict,
) -> str:
    """Summarize the analyzed data in Brazilian Portuguese."""

    total_orders = metrics["orders_analyzed"]
    if not total_orders:
        return "Não foram encontrados pedidos válidos para análise."

    delivery_rate = format_brazilian_percentage(
        metrics["delivery_rate_pct"]
    )
    cancellation_rate = format_brazilian_percentage(
        metrics["cancellation_rate_pct"]
    )

    sentences = [
        f"Foram analisados {total_orders} pedidos, totalizando "
        f"R$ {format_brazilian_number(metrics['total_order_value'])}, "
        f"com ticket médio de "
        f"R$ {format_brazilian_number(metrics['average_order_value'])}."
    ]

    if not category_summary.empty:
        highest_order_count = int(category_summary["orders"].max())
        top_order_categories = metrics["categories_with_most_orders"]

        if len(top_order_categories) == 1:
            sentences.append(
                f"A categoria {top_order_categories[0]} teve o maior "
                f"número de pedidos ({highest_order_count})."
            )
        else:
            sentences.append(
                f"As categorias {format_brazilian_list(top_order_categories)} "
                f"empataram com {highest_order_count} pedidos cada."
            )

        highest_value_category = category_summary.iloc[0]
        sentences.append(
            f"A categoria {highest_value_category['category']} concentrou "
            f"o maior valor total, de "
            f"R$ {format_brazilian_number(highest_value_category['total_order_value'])}."
        )

    other_status_rate = max(
        0,
        round(
            100
            - metrics["delivery_rate_pct"]
            - metrics["cancellation_rate_pct"],
            1,
        ),
    )
    sentences.append(
        f"Quanto aos status, {delivery_rate} dos pedidos foram entregues, "
        f"{cancellation_rate} foram cancelados e "
        f"{format_brazilian_percentage(other_status_rate)} tiveram outros status."
    )

    return " ".join(sentences)


def generate_ai_summary(metrics: dict) -> str:
    """Generate a written interpretation of the metrics."""

    from openai import OpenAI

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um analista de operações. Escreva em português "
                    "do Brasil, com linguagem clara. Separe fatos observados "
                    "de hipóteses e não invente causas."
                ),
            },
            {
                "role": "user",
                "content": f"Analise estes indicadores: {metrics}",
            },
        ],
        temperature=0.2,
    )

    return (
        response.choices[0].message.content
        or "Não foi possível gerar o resumo pela IA."
    )


def build_report(
    category_summary: pd.DataFrame,
    metrics: dict,
    ai_summary: str | None = None,
) -> str:
    report_lines = [
        "# Relatório de análise de pedidos",
        "",
        "## Indicadores",
        "",
    ]

    metric_labels = {
        "orders_analyzed": "Pedidos analisados",
        "total_order_value": "Valor total dos pedidos",
        "average_order_value": "Ticket médio",
        "delivery_rate_pct": "Taxa de entrega",
        "cancellation_rate_pct": "Taxa de cancelamento",
        "categories_with_most_orders": "Categorias com mais pedidos",
    }

    for key, value in metrics.items():
        if key in ("total_order_value", "average_order_value"):
            formatted_value = f"R$ {format_brazilian_number(value)}"
        elif key in ("delivery_rate_pct", "cancellation_rate_pct"):
            formatted_value = format_brazilian_percentage(value)
        elif key == "categories_with_most_orders":
            formatted_value = (
                format_brazilian_list(value) if value else "N/A"
            )
        else:
            formatted_value = str(value)

        report_lines.append(
            f"- **{metric_labels[key]}:** {formatted_value}"
        )

    report_lines.extend(
        [
            "",
            "## Valor total por categoria",
            "",
            "| Categoria | Pedidos | Valor total (R$) |",
            "| --- | ---: | ---: |",
        ]
    )

    report_lines.extend(
        f"| {row.category} | {int(row.orders)} | "
        f"{format_brazilian_number(row.total_order_value)} |"
        for row in category_summary.itertuples(index=False)
    )

    report_lines.extend(
        [
            "",
            "## Gráfico",
            "",
            "![Valor total por categoria](order_value_by_category.png)",
            "",
            "## Interpretação",
            "",
            generate_general_interpretation(category_summary, metrics),
            "",
        ]
    )

    if ai_summary is not None:
        report_lines.extend(
            [
                "### Análise complementar gerada por IA",
                "",
                ai_summary,
                "",
            ]
        )

    report_lines.extend(
        [
            "## Limitações",
            "",
            "Esta base de dados é pequena e fictícia. Os indicadores "
            "descrevem somente os registros fornecidos; não permitem "
            "concluir causas nem representar o desempenho de uma operação real.",
            "",
        ]
    )

    return "\n".join(report_lines)
