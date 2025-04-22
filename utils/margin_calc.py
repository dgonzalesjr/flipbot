def calculate_margin(
    ebay_price: float,
    stripe_sale_price: float,
    shipping_cost: float = 4.95,
    stripe_fee_percent: float = 0.029,
    stripe_fixed_fee: float = 0.30,
    min_margin_dollars: float = 5.00,
    min_margin_percent: float = 15.0
) -> dict:
    """
    Calculate profit margin on a FlipBot transaction.
    Returns dict with margin data and a flag indicating if it's worth buying.
    """

    # Calculate Stripe fee
    stripe_fee = stripe_sale_price * stripe_fee_percent + stripe_fixed_fee

    # Calculate net profit
    net_profit = stripe_sale_price - stripe_fee - ebay_price - shipping_cost

    # Calculate margin percent
    margin_percent = (net_profit / ebay_price) * 100 if ebay_price > 0 else 0

    # Decision flag
    should_buy = net_profit >= min_margin_dollars and margin_percent >= min_margin_percent

    return {
        "net_profit": round(net_profit, 2),
        "margin_percent": round(margin_percent, 2),
        "should_buy": should_buy
    }
