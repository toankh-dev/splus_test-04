import functools

import pytest

from order_service import OrderService


@pytest.mark.parametrize(
    ("prices", "tax_rate", "expected", "expected_int"),
    [
        # TC1: 通常の価格合計に10%の税率を加算する。
        pytest.param([1200.0, 850.5], 0.1, 2255.55, False, id="TC1"),
        # TC2: 空リストでは整数の0を返す。
        pytest.param([], 0.1, 0, True, id="TC2"),
        # TC3: 空リストでは負の税率を検証しない。
        pytest.param([], -0.1, 0, True, id="TC3"),
        # TC4: 空リストでは税率の型を検証しない。
        pytest.param([], "invalid", 0, True, id="TC4"),
        # TC5: 税率0では税抜合計を返す。
        pytest.param([100], 0.0, 100.0, False, id="TC5"),
        # TC6: 整数価格に正の税率を適用する。
        pytest.param([100], 0.1, 110.0, False, id="TC6"),
        # TC7: 税率1.0を適用する。
        pytest.param([100], 1.0, 200.0, False, id="TC7"),
        # TC8: 1を超える税率も適用できる。
        pytest.param([100], 1.5, 250.0, False, id="TC8"),
        # TC10: 合計が0の場合も正常に計算する。
        pytest.param([0, 0.0], 0.1, 0.0, False, id="TC10"),
        # TC11: 負の価格を含む合計も計算する。
        pytest.param([-10.0, 20.0], 0.1, 11.0, False, id="TC11"),
        # TC12: Pythonのroundによる浮動小数点数の丸めを確認する。
        pytest.param([2.675], 0.0, 2.67, False, id="TC12"),
        # TC18: boolのTrueを数値の1として計算する。
        pytest.param([100], True, 200.0, False, id="TC18"),
        # TC20: 数値を含むtupleも反復可能な入力として計算する。
        pytest.param((100,), 0.1, 110.0, False, id="TC20"),
        # TC21: 空リストではNoneの税率を検証しない。
        pytest.param([], None, 0, True, id="TC21"),
        # TC22: 中間値を偶数側に丸めるPythonのroundの挙動を確認する。
        pytest.param([1.125], 0.0, 1.12, False, id="TC22"),
        # TC23: 負のゼロは有効な税率0として扱う。
        pytest.param([100], -0.0, 100.0, False, id="TC23"),
    ],
)
def test_calculate_total_valid_inputs(prices, tax_rate, expected, expected_int):
    result = OrderService.calculate_total(prices, tax_rate)

    assert result == expected
    if expected_int:
        assert type(result) is int


@pytest.mark.parametrize(
    ("prices", "tax_rate"),
    [
        # TC9: 空でない価格リストに負の税率を指定する。
        pytest.param([100], -0.01, id="TC9"),
    ],
)
def test_calculate_total_rejects_negative_tax_rate(prices, tax_rate):
    with pytest.raises(ValueError):
        OrderService.calculate_total(prices, tax_rate)


@pytest.mark.parametrize(
    ("prices", "tax_rate"),
    [
        # TC13: pricesがNoneで反復不能な場合。
        pytest.param(None, 0.1, id="TC13"),
        # TC14: pricesが数値で反復不能な場合。
        pytest.param(100, 0.1, id="TC14"),
        # TC15: 価格リストの要素が数値でない場合。
        pytest.param(["100"], 0.1, id="TC15"),
        # TC16: 空でない価格リストに文字列の税率を指定する場合。
        pytest.param([100], "0.1", id="TC16"),
        # TC17: 空でない価格リストにNoneの税率を指定する場合。
        pytest.param([100], None, id="TC17"),
    ],
)
def test_calculate_total_rejects_invalid_inputs(prices, tax_rate):
    with pytest.raises(TypeError):
        OrderService.calculate_total(prices, tax_rate)


def test_calculate_total_supports_partial_with_positional_prices_and_keyword_tax():
    # TC19: pricesを位置引数、tax_rateをキーワード引数として部分適用する。
    calculate = functools.partial(
        OrderService.calculate_total,
        [100],
        tax_rate=0.1,
    )

    assert calculate() == 110.0


def test_calculate_total_partial_preserves_rounding_behavior():
    # TC24: 中間値の丸めを部分適用した関数で確認する。
    calculate = functools.partial(
        OrderService.calculate_total,
        [1.125],
        tax_rate=0.0,
    )

    assert calculate() == 1.12