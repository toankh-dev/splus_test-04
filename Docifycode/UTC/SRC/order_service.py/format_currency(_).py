from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, localcontext

import pytest

# 対象関数を定義しているモジュールから読み込む。
from target import format_currency


@pytest.fixture(autouse=True)
def isolated_decimal_context():
    # Decimalの設定を固定し、テスト終了後には元の設定を復元する。
    with localcontext() as context:
        context.prec = 28
        context.rounding = ROUND_HALF_EVEN
        context.traps[InvalidOperation] = True
        yield


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        # TC1: 正の整数にドル記号と小数点以下2桁を付ける。
        pytest.param(42, "$42.00", id="TC1"),
        # TC2: 負の整数では負号をドル記号の前に置く。
        pytest.param(-42, "-$42.00", id="TC2"),
        # TC3: 整数のゼロは非負数の分岐で表示する。
        pytest.param(0, "$0.00", id="TC3"),
        # TC4: 小数部が1桁の場合は末尾をゼロで補う。
        pytest.param(12.3, "$12.30", id="TC4"),
        # TC5: 負数の負号の位置と小数部2桁の保持を確認する。
        pytest.param(-12.34, "-$12.34", id="TC5"),
        # TC6: 小数点以下3桁以上の値を切り下げて表示する。
        pytest.param(1.234, "$1.23", id="TC6"),
        # TC7: 小数点以下3桁以上の値を切り上げて表示する。
        pytest.param(1.236, "$1.24", id="TC7"),
        # TC8: 負数の絶対値にも同じ丸めを適用する。
        pytest.param(-1.236, "-$1.24", id="TC8"),
        # TC9: 正確に表現できる境界値を偶数丸めで切り下げる。
        pytest.param(0.125, "$0.12", id="TC9"),
        # TC10: 正確に表現できる境界値を偶数丸めで切り上げる。
        pytest.param(0.375, "$0.38", id="TC10"),
        # TC11: 二進浮動小数点の表現誤差を含む丸め結果を確認する。
        pytest.param(2.675, "$2.67", id="TC11"),
        # TC12: 丸めによって整数部へ桁上がりする。
        pytest.param(9.999, "$10.00", id="TC12"),
        # TC13: ゼロに近い正数は表示上のゼロになる。
        pytest.param(0.004, "$0.00", id="TC13"),
        # TC14: ゼロに丸められる負数でも先頭の負号を保持する。
        pytest.param(-0.004, "-$0.00", id="TC14"),
        # TC15: 浮動小数点の正のゼロを表示する。
        pytest.param(0.0, "$0.00", id="TC15"),
        # TC16: 負のゼロは非負数の分岐に入り、ドル記号の後ろに負号が付く。
        pytest.param(-0.0, "$-0.00", id="TC16"),
        # TC17: 大きな整数にも桁区切りや指数表記を使用しない。
        pytest.param(1234567, "$1234567.00", id="TC17"),
        # TC18: 文字列から生成したDecimalを偶数丸めで表示する。
        pytest.param(Decimal("2.675"), "$2.68", id="TC18"),
        # TC19: 負のDecimalの絶対値と末尾のゼロを正しく表示する。
        pytest.param(Decimal("-12.30"), "-$12.30", id="TC19"),
        # TC20: 真の真偽値は整数の1として受理される。
        pytest.param(True, "$1.00", id="TC20"),
        # TC21: 偽の真偽値は整数の0として受理される。
        pytest.param(False, "$0.00", id="TC21"),
        # TC22: 正の無限大は拒否されず、そのまま表示される。
        pytest.param(float("inf"), "$inf", id="TC22"),
        # TC23: 負の無限大は負数の分岐で表示される。
        pytest.param(float("-inf"), "-$inf", id="TC23"),
        # TC24: 符号なしの浮動小数点NaNは非負数の分岐で表示される。
        pytest.param(float("nan"), "$nan", id="TC24"),
    ],
)
def test_format_currency_returns_expected_string(amount, expected):
    actual = format_currency(amount)

    assert isinstance(actual, str)
    assert actual == expected


@pytest.mark.parametrize(
    "amount",
    [
        # TC25: 数値文字列はゼロとの大小比較で型エラーになる。
        pytest.param("12.34", id="TC25"),
        # TC26: 空文字列もゼロとの大小比較で型エラーになる。
        pytest.param("", id="TC26"),
        # TC27: 未設定値はゼロとの大小比較で型エラーになる。
        pytest.param(None, id="TC27"),
        # TC28: 空リストはゼロとの大小比較で型エラーになる。
        pytest.param([], id="TC28"),
        # TC29: 空辞書はゼロとの大小比較で型エラーになる。
        pytest.param({}, id="TC29"),
        # TC30: 複素数は大小比較できず、絶対値取得より前に型エラーになる。
        pytest.param(1 + 2j, id="TC30"),
    ],
)
def test_format_currency_rejects_values_without_ordering(amount):
    with pytest.raises(TypeError):
        format_currency(amount)


def test_TC31_decimal_quiet_nan_raises_invalid_operation():
    # TC31: InvalidOperationトラップが有効な場合、Decimalのquiet NaNは比較で例外になる。
    with pytest.raises(InvalidOperation):
        format_currency(Decimal("NaN"))