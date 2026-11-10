"""Order service used for DocifyCode unit test generation tests."""


class OrderService:
    def calculate_total(self, prices, tax_rate):
        if not prices:
            return 0
        if tax_rate < 0:
            raise ValueError("tax_rate must not be negative")
        subtotal = sum(prices)
        return round(subtotal * (1 + tax_rate), 2)

    def apply_discount(self, total, discount_rate):
        if discount_rate < 0 or discount_rate > 1:
            raise ValueError("discount_rate must be between 0 and 1")
        return round(total * (1 - discount_rate), 2)

    def is_free_shipping(self, total):
        return total >= 100


def format_currency(amount):
    if amount < 0:
        return f"-${abs(amount):.2f}"
    return f"${amount:.2f}"
