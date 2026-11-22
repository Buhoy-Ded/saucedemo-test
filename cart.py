"""Корзина saucedemo: разбор цен, итог, налог.

Учебный модуль для CI: маленький, но с краевыми случаями,
на которых тесты действительно что-то проверяют.
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

CENTS = Decimal("0.01")


def parse_price(raw: str) -> Decimal:
    """Разбирает цену вида "$29.99" или "$1,299.99" в Decimal.

    >>> parse_price("$29.99")
    Decimal('29.99')
    >>> parse_price("$1,299.50")
    Decimal('1299.50')
    """
    if not isinstance(raw, str):
        raise TypeError(f"цена должна быть строкой, получено {type(raw).__name__}")

    cleaned = raw.strip().replace("$", "").replace(",", "")
    if not cleaned:
        raise ValueError("пустая цена")

    try:
        value = Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError(f"не удалось разобрать цену: {raw!r}") from exc

    if value < 0:
        raise ValueError(f"цена не может быть отрицательной: {raw!r}")

    return value


def cart_total(prices: list[str]) -> Decimal:
    """Сумма цен корзины. Пустая корзина — ноль.

    >>> cart_total([])
    Decimal('0.00')
    >>> cart_total(["$10.00", "$5.50"])
    Decimal('15.50')
    """
    total = Decimal("0")
    for price in prices:
        total += parse_price(price)
    return total.quantize(CENTS, rounding=ROUND_HALF_UP)


def with_tax(total: Decimal, rate: Decimal) -> Decimal:
    """Добавляет налог и округляет до копеек (половина — вверх).

    >>> with_tax(Decimal("100.00"), Decimal("0.0725"))
    Decimal('107.25')
    """
    if rate < 0:
        raise ValueError("ставка налога не может быть отрицательной")

    result = total * (Decimal("1") + rate)
    return result.quantize(CENTS, rounding=ROUND_HALF_UP)
