"""Тесты корзины. Запуск: pytest -q"""
from decimal import Decimal

import pytest

from cart import cart_total, parse_price, with_tax


# --- parse_price -----------------------------------------------------------

@pytest.mark.parametrize(
    "raw, expected",
    [
        ("$29.99", Decimal("29.99")),
        ("$0.01", Decimal("0.01")),
        ("$1,299.50", Decimal("1299.50")),
        ("  $7.10  ", Decimal("7.10")),
    ],
)
def test_parse_price_valid(raw, expected):
    assert parse_price(raw) == expected


@pytest.mark.parametrize("raw", ["", "$", "abc", "$1.2.3", "1 299"])
def test_parse_price_invalid(raw):
    with pytest.raises(ValueError):
        parse_price(raw)


def test_parse_price_negative_rejected():
    with pytest.raises(ValueError):
        parse_price("-$5.00")


def test_parse_price_requires_string():
    with pytest.raises(TypeError):
        parse_price(29.99)


# --- cart_total ------------------------------------------------------------

def test_cart_total_empty():
    assert cart_total([]) == Decimal("0")


def test_cart_total_single():
    assert cart_total(["$29.99"]) == Decimal("29.99")


def test_cart_total_many():
    assert cart_total(["$10.00", "$5.50", "$0.50"]) == Decimal("16.00")


def test_cart_total_rounds_half_up():
    # 0.005 округляется вверх до 0.01
    assert cart_total(["$0.005"]) == Decimal("0.01")


# --- with_tax --------------------------------------------------------------

def test_with_tax_zero_rate():
    assert with_tax(Decimal("100.00"), Decimal("0")) == Decimal("100.00")


def test_with_tax_thousand():
    assert with_tax(Decimal("1000.00"), Decimal("0.0725")) == Decimal("1072.50")


def test_with_tax_rounds_half_up():
    # 10.005 -> 10.01
    assert with_tax(Decimal("10.00"), Decimal("0.0005")) == Decimal("10.01")


def test_with_tax_negative_rate_rejected():
    with pytest.raises(ValueError):
        with_tax(Decimal("10.00"), Decimal("-0.1"))


# --- сквозной сценарий -----------------------------------------------------

def test_checkout_scenario():
    prices = ["$29.99", "$9.99", "$15.99", "$49.99"]
    total = cart_total(prices)
    assert total == Decimal("105.96")
    assert with_tax(total, Decimal("0.0725")) == Decimal("113.64")
