import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(name: str) -> stripe.Product:
    """Создает продукт в Stripe."""
    return stripe.Product.create(name=name)


def create_stripe_price(amount: float, product_id: str) -> stripe.Price:
    """Создает цену в Stripe."""
    return stripe.Price.create(
        currency='rub',
        unit_amount=int(amount * 100),
        product=product_id,
    )


def create_stripe_session(price_id: str) -> stripe.checkout.Session:
    """Создает сессию оплаты в Stripe."""
    return stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/payment_success/",
        cancel_url="http://127.0.0.1:8000/payment_cancel/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
