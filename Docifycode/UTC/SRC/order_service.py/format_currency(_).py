import pytest

from main import format_currency


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        # TC1: 正の整数を小数点以下2桁で整形する。
        (12, "$12.00"),
        # TC2: 整数のゼロを通常側の形式で整形する。
        (0, "$0.00"),
        # TC3: 負の整数を負数側の形式で整形する。
        (-12, "-$12.00"),
        # TC4: 正の小数を小数点以下2桁で整形する。
        (12.5, "$12.50"),
        # TC5: 負の小数を負数側の形式で整形する。
        (-12.5, "-$12.50"),
        # TC6: 浮動小数点のゼロを通常側の形式で整形する。
        (0.0, "$0.00"),
        # TC7: 負のゼロは負数側ではなく通常側の形式で整形する。
        (-0.0, "$-0.00"),
        # TC8: 丸め後に0.00となる正の小数を確認する。
        (0.004, "$0.00"),
        # TC9: 丸め後に0.00となる負の小数も負数側の形式で整形する。
        (-0.004, "-$0.00"),
        # TC10: Pythonの浮動小数点書式指定による丸めを確認する。
        (2.675, "$2.67"),
        # TC11: 小数第3位が5の値をPythonの書式指定で丸める。
        (0.005, "$0.01"),
        # TC12: 負数の丸め境界でも負数側の形式を使う。
        (-0.005, "-$0.01"),
        # TC13: 非常に大きな正の整数を整形する。
        (10**100, "$" + str(10**100) + ".00"),
        # TC14: 正の無限大を通常側の形式で整形する。
        (float("inf"), "$inf"),
        # TC15: 負の無限大を負数側の形式で整形する。
        (float("-inf"), "-$inf"),
        # TC16: NaNは負数判定が偽となるため通常側の形式で整形する。
        (float("nan"), "$nan"),
        # TC17: boolがintのサブクラスであることを確認する。
        (True, "$1.00"),
        # TC18: boolがintのサブクラスであることを確認する。
        (False, "$0.00"),
        # TC24: ties-to-evenで偶数側の1.12に丸める。
        (1.125, "$1.12"),
        # TC25: ties-to-evenで偶数側の1.38に丸める。
        (1.375, "$1.38"),
    ],
    ids=[
        "TC1",
        "TC2",
        "TC3",
        "TC4",
        "TC5",
        "TC6",
        "TC7",
        "TC8",
        "TC9",
        "TC10",
        "TC11",
        "TC12",
        "TC13",
        "TC14",
        "TC15",
        "TC16",
        "TC17",
        "TC18",
        "TC24",
        "TC25",
    ],
)
def test_format_currency_returns_expected_string(amount, expected):
    assert format_currency(amount) == expected


@pytest.mark.parametrize(
    "amount",
    [
        # TC19: 文字列は数値として扱えずTypeErrorになる。
        "12.5",
        # TC20: Noneは数値として扱えずTypeErrorになる。
        None,
        # TC21: listは数値として扱えずTypeErrorになる。
        [],
        # TC22: dictは数値として扱えずTypeErrorになる。
        {},
        # TC23: complexは実数との大小比較ができずTypeErrorになる。
        1 + 2j,
    ],
    ids=["TC19", "TC20", "TC21", "TC22", "TC23"],
)
def test_format_currency_raises_type_error_for_unsupported_values(amount):
    with pytest.raises(TypeError):
        format_currency(amount)