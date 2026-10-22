import pytest

from order_service import OrderService


@pytest.fixture
def service():
    # 各テストで実際の対象クラスのインスタンスを生成する。
    return OrderService()


@pytest.mark.parametrize(
    ("total", "expected"),
    [
        # TC1: 整数の境界直前は送料無料にならない。
        pytest.param(99, False, id="TC1"),
        # TC2: 整数の境界値100は送料無料になる。
        pytest.param(100, True, id="TC2"),
        # TC3: 整数の境界直後は送料無料になる。
        pytest.param(101, True, id="TC3"),
        # TC4: 合計金額がゼロの場合は送料無料にならない。
        pytest.param(0, False, id="TC4"),
        # TC5: 負の金額でも例外を発生させずFalseを返す。
        pytest.param(-1, False, id="TC5"),
        # TC6: 小数の境界直前は送料無料にならない。
        pytest.param(99.99, False, id="TC6"),
        # TC7: 浮動小数点数の境界値100.0は送料無料になる。
        pytest.param(100.0, True, id="TC7"),
        # TC8: 小数の境界直後は送料無料になる。
        pytest.param(100.01, True, id="TC8"),
        # TC9: 表示上の丸めにかかわらず100未満として判定する。
        pytest.param(99.999, False, id="TC9"),
        # TC10: 100桁すべてが9の整数でも送料無料になる。
        pytest.param(int("9" * 100), True, id="TC10"),
        # TC11: 正の無限大は送料無料になる。
        pytest.param(float("inf"), True, id="TC11"),
        # TC12: 負の無限大は送料無料にならない。
        pytest.param(float("-inf"), False, id="TC12"),
        # TC13: NaNの比較結果はFalseであり例外は発生しない。
        pytest.param(float("nan"), False, id="TC13"),
        # TC14: Trueは整数1として比較される。
        pytest.param(True, False, id="TC14"),
        # TC15: Falseは整数0として比較される。
        pytest.param(False, False, id="TC15"),
    ],
)
def test_is_free_shipping_returns_expected_bool(service, total, expected):
    result = service.is_free_shipping(total)

    # 値だけでなく戻り値が厳密にboolであることも検証する。
    assert result is expected


@pytest.mark.parametrize(
    "total",
    [
        # TC16: Noneは整数と大小比較できない。
        pytest.param(None, id="TC16"),
        # TC17: 数値文字列は自動変換されず例外になる。
        pytest.param("100", id="TC17"),
        # TC18: 空リストはゼロ扱いされず例外になる。
        pytest.param([], id="TC18"),
        # TC19: 辞書は整数と大小比較できない。
        pytest.param({}, id="TC19"),
        # TC20: 虚部がゼロでも複素数は大小比較できない。
        pytest.param(100 + 0j, id="TC20"),
    ],
)
def test_is_free_shipping_rejects_non_orderable_inputs(service, total):
    with pytest.raises(TypeError):
        service.is_free_shipping(total)