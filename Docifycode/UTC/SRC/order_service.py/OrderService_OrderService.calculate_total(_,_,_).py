import math
from decimal import Decimal

import pytest

# 対象クラスが定義されているモジュールから読み込む。
from order_service import OrderService


@pytest.fixture
def service():
    return OrderService()


@pytest.mark.parametrize(
    "prices,tax_rate,expected,expected_type",
    [
        # TC1: 複数商品の合計に税率を適用する。
        pytest.param([10, 20, 30], 0.1, 66.0, float, id="TC1"),
        # TC2: 整数の税率ゼロでは整数を返す。
        pytest.param([10, 20], 0, 30, int, id="TC2"),
        # TC3: 浮動小数点の税率ゼロでは浮動小数点を返す。
        pytest.param([10, 20], 0.0, 30.0, float, id="TC3"),
        # TC4: 空でないリストの小計がゼロになる。
        pytest.param([0, 0], 0.1, 0.0, float, id="TC4"),
        # TC5: 商品が一件で税率が百分の百になる。
        pytest.param([10], 1, 20, int, id="TC5"),
        # TC6: 百分の百を超える税率も受け付ける。
        pytest.param([10], 1.5, 25.0, float, id="TC6"),
        # TC9: 負のゼロは負の税率として拒否されない。
        pytest.param([10], -0.0, 10.0, float, id="TC9"),
        # TC10: 空リストは整数のゼロを返す。
        pytest.param([], 0.1, 0, int, id="TC10"),
        # TC11: 空リストでは負の税率の検証を省略する。
        pytest.param([], -0.1, 0, int, id="TC11"),
        # TC12: 空リストでは未設定の税率との比較を省略する。
        pytest.param([], None, 0, int, id="TC12"),
        # TC13: 未設定の価格は偽として短絡する。
        pytest.param(None, 0.1, 0, int, id="TC13"),
        # TC14: 整数ゼロは反復可能でなくても短絡する。
        pytest.param(0, 0.1, 0, int, id="TC14"),
        # TC15: 偽の真偽値も整数のゼロを返す。
        pytest.param(False, 0.1, 0, int, id="TC15"),
        # TC16: 空文字列は加算されず短絡する。
        pytest.param("", 0.1, 0, int, id="TC16"),
        # TC17: 正確に表現できる境界で偶数側へ切り下げる。
        pytest.param([10.125], 0.0, 10.12, float, id="TC17"),
        # TC18: 正確に表現できる境界で偶数側へ切り上げる。
        pytest.param([10.375], 0.0, 10.38, float, id="TC18"),
        # TC19: 二進浮動小数点の表現に従って丸める。
        pytest.param([2.675], 0.0, 2.67, float, id="TC19"),
        # TC20: 正の小額が丸めによってゼロになる。
        pytest.param([0.004], 0.0, 0.0, float, id="TC20"),
        # TC21: 負の価格による調整をそのまま合計する。
        pytest.param([10, -3], 0.1, 7.7, float, id="TC21"),
        # TC22: 負の小計にも税率を適用する。
        pytest.param([-10], 0.1, -11.0, float, id="TC22"),
        # TC24: 数値のタプルを合計できる。
        pytest.param((10, 20), 0.1, 33.0, float, id="TC24"),
        # TC36: 真偽値の価格と税率を整数として計算する。
        pytest.param([True, False], True, 2, int, id="TC36"),
    ],
)
def test_calculate_total_values_and_types(
    service, prices, tax_rate, expected, expected_type
):
    original_prices = prices.copy() if isinstance(prices, list) else None

    result = service.calculate_total(prices, tax_rate)

    # 丸め結果そのものと厳密な戻り値の型を確認する。
    assert result == expected
    assert type(result) is expected_type

    # 呼び出し元の価格リストを変更しないことも確認する。
    if isinstance(prices, list):
        assert prices == original_prices


@pytest.mark.parametrize(
    "prices,tax_rate",
    [
        # TC7: ゼロ直下の負の税率を拒否する。
        pytest.param([10], -0.000001, id="TC7"),
        # TC8: 整数の負の税率を拒否する。
        pytest.param([10], -1, id="TC8"),
        # TC23: 小計がゼロでも空リストでなければ税率を検証する。
        pytest.param([10, -10], -0.1, id="TC23"),
        # TC37: 不正な価格の加算より先に負の税率を拒否する。
        pytest.param([10, "invalid"], -0.1, id="TC37"),
        # TC40: 負の無限大を負の税率として拒否する。
        pytest.param([10], -math.inf, id="TC40"),
    ],
)
def test_calculate_total_rejects_negative_tax(service, prices, tax_rate):
    original_prices = prices.copy()

    with pytest.raises(ValueError) as exc_info:
        service.calculate_total(prices, tax_rate)

    assert type(exc_info.value) is ValueError
    assert str(exc_info.value) == "tax_rate must not be negative"
    assert prices == original_prices


@pytest.mark.parametrize(
    "prices,tax_rate",
    [
        # TC28: 真となる非反復可能な整数は合計できない。
        pytest.param(10, 0.1, id="TC28"),
        # TC29: 文字列を価格の反復可能オブジェクトとして加算できない。
        pytest.param("10", 0.1, id="TC29"),
        # TC30: 価格中の数値文字列は自動変換されない。
        pytest.param([10, "20"], 0.1, id="TC30"),
        # TC31: 価格中の欠損値は加算できない。
        pytest.param([10, None], 0.1, id="TC31"),
        # TC32: 文字列の税率と整数ゼロは比較できない。
        pytest.param([10], "0.1", id="TC32"),
        # TC33: 空でない価格では未設定の税率との比較が失敗する。
        pytest.param([10], None, id="TC33"),
        # TC34: 複素数の税率と整数ゼロは比較できない。
        pytest.param([10], 0.1 + 0j, id="TC34"),
        # TC35: 複素数価格の合計と乗算はできても丸めはできない。
        pytest.param([1 + 2j], 0.1, id="TC35"),
        # TC45: 浮動小数点の小計と十進数の税率は乗算できない。
        pytest.param([10.0], Decimal("0.1"), id="TC45"),
    ],
)
def test_calculate_total_rejects_incompatible_types(service, prices, tax_rate):
    # 処理系によって異なる例外文言には依存しない。
    with pytest.raises(TypeError) as exc_info:
        service.calculate_total(prices, tax_rate)

    assert type(exc_info.value) is TypeError


def test_tc25_generator_is_consumed(service):
    # TC25: 数値ジェネレーターを合計し、呼び出し後の消費状態を確認する。
    prices = (price for price in (10, 20))

    result = service.calculate_total(prices, 0.1)

    assert result == 33.0
    assert type(result) is float
    sentinel = object()
    assert next(prices, sentinel) is sentinel
    assert list(prices) == []


def test_tc26_empty_generator_returns_float_zero(service):
    # TC26: 空ジェネレーターは真なので税計算と丸めまで実行される。
    prices = (price for price in ())

    result = service.calculate_total(prices, 0.1)

    assert result == 0.0
    assert type(result) is float
    assert list(prices) == []


def test_tc27_empty_generator_rejects_negative_tax(service):
    # TC27: 空ジェネレーターでも負の税率を検証する。
    prices = (price for price in ())

    with pytest.raises(ValueError) as exc_info:
        service.calculate_total(prices, -0.1)

    assert type(exc_info.value) is ValueError
    assert str(exc_info.value) == "tax_rate must not be negative"


@pytest.mark.parametrize(
    "prices,tax_rate",
    [
        # TC38: 非数の税率は拒否されず結果に伝播する。
        pytest.param([10], math.nan, id="TC38"),
        # TC41: 非数の価格が合計と結果に伝播する。
        pytest.param([math.nan], 0.1, id="TC41"),
        # TC43: ゼロと正の無限大の乗算は非数になる。
        pytest.param([0], math.inf, id="TC43"),
    ],
)
def test_calculate_total_returns_nan(service, prices, tax_rate):
    result = service.calculate_total(prices, tax_rate)

    assert type(result) is float
    assert math.isnan(result)


@pytest.mark.parametrize(
    "prices,tax_rate",
    [
        # TC39: 正の無限大の税率は正の無限大を返す。
        pytest.param([10], math.inf, id="TC39"),
        # TC42: 正の無限大の価格は正の無限大を返す。
        pytest.param([math.inf], 0.1, id="TC42"),
        # TC44: 巨大な価格の合計は例外ではなく正の無限大になる。
        pytest.param([1e308, 1e308], 0.1, id="TC44"),
    ],
)
def test_calculate_total_returns_positive_infinity(service, prices, tax_rate):
    result = service.calculate_total(prices, tax_rate)

    assert type(result) is float
    assert math.isinf(result)
    assert result == math.inf