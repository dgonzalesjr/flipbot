# card_evaluator.py
import re

# Example resale pricing table (can be expanded)
ESTIMATED_RESALE_VALUES = {
    "charizard gx": 45.00,
    "shining magikarp": 120.00,
    "blaines arcanine": 70.00,
    "lugia": 80.00
}

# Keywords for condition estimation
GOOD_CONDITION_TERMS = ["mint", "nm", "pack fresh", "excellent"]
BAD_CONDITION_TERMS = ["damaged", "creased", "played", "binder dent"]


def evaluate_card(title: str, price: float) -> dict:
    title_lower = title.lower()

    # Clean title
    cleaned = re.sub(r"[^a-z0-9\s]", "", title_lower)

    # Match estimated value from known cards
    resale_value = None
    for key, val in ESTIMATED_RESALE_VALUES.items():
        if key in cleaned:
            resale_value = val
            break

    # Estimate condition
    condition = "unknown"
    if any(term in cleaned for term in GOOD_CONDITION_TERMS):
        condition = "good"
    elif any(term in cleaned for term in BAD_CONDITION_TERMS):
        condition = "poor"

    # Try to detect grade
    grade_match = re.search(r"psa\s*(\d+)|bgs\s*(\d+)|cgc\s*(\d+)", cleaned)
    grade = int(grade_match.group(1) or grade_match.group(2) or grade_match.group(3)) if grade_match else None

    # Simple profit calc
    profit_estimate = resale_value - price if resale_value else None
    is_profitable = profit_estimate is not None and profit_estimate >= 10

    # Add reason
    if resale_value is None:
        reason = "No resale value match"
    elif profit_estimate is None:
        reason = "Could not estimate profit"
    elif profit_estimate < 10:
        reason = f"Profit too low (${profit_estimate:.2f})"
    else:
        reason = "Good margin"

    return {
        "title": title,
        "price": price,
        "resale_value": resale_value,
        "condition": condition,
        "grade": grade,
        "profit_estimate": profit_estimate,
        "should_buy": is_profitable,
        "reason": reason
    }
