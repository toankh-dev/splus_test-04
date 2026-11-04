import pytest

from order_service import OrderService


@pytest.fixture
def service():
    return OrderService()


def test_apply_discount_tc1_rate_near_zero(service):
    # TC1: 下限0に近い割引率を適用する
    assert service.apply_discount(100, 0.0001) == 99.99


def test_apply_discount_tc2_rate_near_one(service):
    # TC2: 上限1に近い割引率を適用し、丸め後の金額を確認する
    assert service.apply_discount(100, 0.9999) == 0.01


def test_apply_discount_tc3_python_rounding_at_midpoint(service):
    # TC3: Pythonのroundによる中間値の丸めを確認する
    assert service.apply_discount(2.01, 0.5) == 1.0


def test_apply_discount_tc4_decimal_total(service):
    # TC4: 小数を含む合計金額に10%割引を適用する
    assert service.apply_discount(99.99, 0.1) == 89.99


def test_apply_discount_tc5_python_rounding_for_2675(service):
    # TC5: Pythonのroundによる2.675の丸めを確認する
    assert service.apply_discount(2.675, 0) == 2.67


def test_apply_discount_tc6_negative_total(service):
    # TC6: 負の合計金額も拒否せず計算する
    assert service.apply_discount(-10, 0.5) == -5.0


def test_apply_discount_tc7_rate_below_zero_raises_value_error(service):
    # TC7: 割引率が下限0未満の場合はValueErrorを送出する
    with pytest.raises(ValueError):
        service.apply_discount(100, -0.01)


def test_apply_discount_tc8_rate_above_one_raises_value_error(service):
    # TC8: 割引率が上限1を超える場合はValueErrorを送出する
    with pytest.raises(ValueError):
        service.apply_discount(100, 1.01)


def test_apply_discount_tc9_zero_total(service):
    # TC9: 合計金額が0の場合も割引計算できる
    assert service.apply_discount(0, 0.15) == 0


def test_apply_discount_tc10_none_rate_raises_type_error(service):
    # TC10: 割引率がNoneの場合はTypeErrorを送出する
    with pytest.raises(TypeError):
        service.apply_discount(100, None)


def test_apply_discount_tc11_string_rate_raises_type_error(service):
    # TC11: 割引率が文字列の場合はTypeErrorを送出する
    with pytest.raises(TypeError):
        service.apply_discount(100, "0.1")


def test_apply_discount_tc12_none_total_raises_type_error(service):
    # TC12: 合計金額がNoneの場合はTypeErrorを送出する
    with pytest.raises(TypeError):
        service.apply_discount(None, 0.1)


def test_apply_discount_tc13_string_total_raises_type_error(service):
    # TC13: 合計金額が文字列の場合はTypeErrorを送出する
    with pytest.raises(TypeError):
        service.apply_discount("100", 0.1)