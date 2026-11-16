import pandas as pd


def generate_analysis(input_path: str):
    """Read the orders and calculate operational metrics."""

    df = pd.read_csv(input_path).rename(
        columns={
            "pedido": "order_id",
            "data": "date",
            "categoria": "category",
            "regiao": "region",
            "valor": "amount",
        }
    )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    df = df.dropna(
        subset=["date", "amount", "order_id"]
    )

    df["status"] = df["status"].fillna(
        "Not provided"
    )

    total_orders = len(df)

    delivered_orders = int(
        (df["status"] == "Entregue").sum()
    )

    cancelled_orders = int(
        (df["status"] == "Cancelado").sum()
    )

    category_order_counts = df["category"].value_counts(sort=False)
    max_category_orders = (
        int(category_order_counts.max())
        if not category_order_counts.empty
        else 0
    )
    categories_with_most_orders = [
        str(category)
        for category, order_count in category_order_counts.items()
        if order_count == max_category_orders
    ]

    metrics = {
        "orders_analyzed": total_orders,
        "total_order_value": round(
            float(df["amount"].sum()),
            2,
        ),
        "average_order_value": round(
            float(df["amount"].mean()),
            2,
        ) if total_orders else 0,
        "delivery_rate_pct": round(
            delivered_orders / total_orders * 100,
            1,
        ) if total_orders else 0,
        "cancellation_rate_pct": round(
            cancelled_orders / total_orders * 100,
            1,
        ) if total_orders else 0,
        "categories_with_most_orders": categories_with_most_orders,
    }

    category_summary = (
        df.groupby("category", as_index=False)
        .agg(
            orders=("order_id", "count"),
            total_order_value=("amount", "sum"),
        )
        .sort_values(
            "total_order_value",
            ascending=False,
        )
    )

    return category_summary, metrics
