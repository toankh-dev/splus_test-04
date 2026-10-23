import math
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext

import pytest

# 実際の配置に合わせてインポート先を指定する。
from order_service import OrderService


@pytest.fixture
def service():
    return OrderService()


@pytest.mark.parametrize(
    "total, discount_rate, expected, expected_type",
    [
        # TC1: 通常の20%割引。
        pytest.param(100, 0.2, 80.0, float, id="TC1"),
        # TC2: 整数の下限では整数を返す。
        pytest.param(100, 0, 100, int, id="TC2"),
        # TC3: 整数の上限では整数のゼロを返す。
        pytest.param(100, 1, 0, int, id="TC3"),
        # TC4: 浮動小数点数の下限。
        pytest.param(100.0, 0.0, 100.0, float, id="TC4"),
        # TC5: 浮動小数点数の上限。
        pytest.param(100.0, 1.0, 0.0, float, id="TC5"),
        # TC8: 下限の直内では丸めにより元の金額になる。
        pytest.param(100, 0.000001, 100.0, float, id="TC8"),
        # TC9: 上限の直内では丸めによりゼロになる。
        pytest.param(100, 0.999999, 0.0, float, id="TC9"),
        # TC10: 合計金額がゼロ。
        pytest.param(0, 0.5, 0.0, float, id="TC10"),
        # TC12: 負の合計金額も計算する。
        pytest.param(-100, 0.25, -75.0, float, id="TC12"),
        # TC13: 小数第3位を切り上げる。
        pytest.param(10.126, 0, 10.13, float, id="TC13"),
        # TC14: 小数第3位を切り捨てる。
        pytest.param(10.124, 0, 10.12, float, id="TC14"),
        # TC15: 中間値を下側の偶数へ丸める。
        pytest.param(1.125, 0, 1.12, float, id="TC15"),
        # TC16: 中間値を上側の偶数へ丸める。
        pytest.param(1.375, 0, 1.38, float, id="TC16"),
        # TC17: 二進浮動小数点の表現誤差を含む丸め。
        pytest.param(2.675, 0, 2.67, float, id="TC17"),
        # TC27: Falseは割引率0として扱う。
        pytest.param(100, False, 100, int, id="TC27"),
        # TC28: Trueは割引率1として扱う。
        pytest.param(100, True, 0, int, id="TC28"),
        # TC29: 合計金額のTrueは整数1として扱う。
        pytest.param(True, 0.5, 0.5, float, id="TC29"),
    ],
)
def test_apply_discount_returns_expected_value_and_type(
    service, total, discount_rate, expected, expected_type
):
    result = service.apply_discount(total, discount_rate)

    # 丸め後の厳密な値と型を確認し、整数と浮動小数点数を区別する。
    assert result == expected
    assert type(result) is expected_type


@pytest.mark.parametrize(
    "total, discount_rate",
    [
        # TC6: 下限の直外。
        pytest.param(100, -0.000001, id="TC6"),
        # TC7: 上限の直外。
        pytest.param(100, 1.000001, id="TC7"),
        # TC11: 合計金額がゼロでも割引率を検証する。
        pytest.param(0, -0.1, id="TC11"),
        # TC26: 合計金額の計算より先に割引率を検証する。
        pytest.param(None, 2, id="TC26"),
        # TC30: 割引率の正の無限大を拒否する。
        pytest.param(100, float("inf"), id="TC30"),
        # TC31: 割引率の負の無限大を拒否する。
        pytest.param(100, float("-inf"), id="TC31"),
    ],
)
def test_apply_discount_rejects_out_of_range_rate(service, total, discount_rate):
    with pytest.raises(ValueError) as exc_info:
        service.apply_discount(total, discount_rate)

    assert type(exc_info.value) is ValueError
    assert str(exc_info.value) == "discount_rate must be between 0 and 1"


@pytest.mark.parametrize(
    "total, discount_rate",
    [
        # TC18: 文字列と浮動小数点数の乗算で失敗する。
        pytest.param("100", 0.2, id="TC18"),
        # TC19: 文字列の整数倍は成功するが、roundで失敗する。
        pytest.param("100", 0, id="TC19"),
        # TC20: Noneの乗算で失敗する。
        pytest.param(None, 0.2, id="TC20"),
        # TC21: リストの整数倍は成功するが、roundで失敗する。
        pytest.param([100], 0, id="TC21"),
        # TC22: 文字列の割引率は最初の大小比較で失敗する。
        pytest.param(100, "0.2", id="TC22"),
        # TC23: Noneの割引率は最初の大小比較で失敗する。
        pytest.param(100, None, id="TC23"),
        # TC24: 複素数の割引率は大小比較で失敗する。
        pytest.param(100, 0.2 + 0j, id="TC24"),
        # TC25: 複素数の合計金額は乗算後のroundで失敗する。
        pytest.param(100 + 2j, 0.5, id="TC25"),
        # TC38: Decimalの合計金額とfloatの割引率は乗算できない。
        pytest.param(Decimal("100.00"), 0.25, id="TC38"),
        # TC39: floatの合計金額とDecimalの割引率は乗算できない。
        pytest.param(100.0, Decimal("0.25"), id="TC39"),
    ],
)
def test_apply_discount_rejects_incompatible_types(service, total, discount_rate):
    with pytest.raises(TypeError) as exc_info:
        service.apply_discount(total, discount_rate)

    # 型エラーの文言はPythonの実装に依存するため固定しない。
    assert type(exc_info.value) is TypeError


@pytest.mark.parametrize(
    "total, discount_rate",
    [
        # TC32: NaNの割引率は範囲検証を通過する。
        pytest.param(100, float("nan"), id="TC32"),
        # TC33: 合計金額のNaNが結果へ伝播する。
        pytest.param(float("nan"), 0.5, id="TC33"),
        # TC36: 無限大とゼロの乗算はNaNになる。
        pytest.param(float("inf"), 1, id="TC36"),
    ],
)
def test_apply_discount_returns_nan(service, total, discount_rate):
    result = service.apply_discount(total, discount_rate)

    assert type(result) is float
    # NaNは自身とも等しくないため、専用の判定を使用する。
    assert math.isnan(result)


@pytest.mark.parametrize(
    "total, discount_rate, expected",
    [
        # TC34: 正の無限大が結果へ伝播する。
        pytest.param(float("inf"), 0.5, float("inf"), id="TC34"),
        # TC35: 負の無限大が結果へ伝播する。
        pytest.param(float("-inf"), 0.5, float("-inf"), id="TC35"),
    ],
)
def test_apply_discount_returns_signed_infinity(
    service, total, discount_rate, expected
):
    result = service.apply_discount(total, discount_rate)

    assert type(result) is float
    assert math.isinf(result)
    assert result == expected


# TC37: 標準のDecimalコンテキストで値、型、小数桁を確認する。
def test_TC37_apply_discount_with_decimal(service):
    # 呼び出し元のコンテキストに依存せず、終了後は元に戻す。
    standard_context = Context(prec=28, rounding=ROUND_HALF_EVEN)
    with localcontext(standard_context):
        result = service.apply_discount(Decimal("100.00"), Decimal("0.25"))

    expected = Decimal("75.00")
    assert type(result) is Decimal
    assert result == expected
    # Decimalの等値比較だけでは末尾のゼロを区別できない。
    assert result.as_tuple() == expected.as_tuple()
    assert result.as_tuple().exponent == -2


# TC40: 負のゼロは値だけでなく符号も確認する。
def test_TC40_apply_discount_preserves_negative_zero(service):
    result = service.apply_discount(-0.0, 0.5)

    assert type(result) is float
    assert result == 0.0
    assert math.copysign(1.0, result) == -1.0