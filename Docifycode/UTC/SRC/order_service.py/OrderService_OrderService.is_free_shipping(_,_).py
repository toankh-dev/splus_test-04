import pytest

from order_service import OrderService


@pytest.fixture
def service():
    return OrderService()


def test_TC1_negative_integer_is_not_free_shipping(service):
    # TC1: 100未満の負の整数では送料無料にならないことを確認する。
    assert service.is_free_shipping(-1) is False


def test_TC2_value_just_below_threshold_is_not_free_shipping(service):
    # TC2: 基準額100に近い100未満の値では送料無料にならないことを確認する。
    assert service.is_free_shipping(99.99) is False


def test_TC3_integer_at_threshold_is_free_shipping(service):
    # TC3: 基準額ちょうどの整数は送料無料の対象になることを確認する。
    assert service.is_free_shipping(100) is True


def test_TC4_float_at_threshold_is_free_shipping(service):
    # TC4: 基準額と等しい浮動小数点数も送料無料の対象になることを確認する。
    assert service.is_free_shipping(100.0) is True


def test_TC5_value_just_above_threshold_is_free_shipping(service):
    # TC5: 基準額をわずかに超える値は送料無料の対象になることを確認する。
    assert service.is_free_shipping(100.01) is True


def test_TC6_integer_above_threshold_is_free_shipping(service):
    # TC6: 基準額を超える整数は送料無料の対象になることを確認する。
    assert service.is_free_shipping(101) is True


def test_TC7_nan_is_not_free_shipping(service):
    # TC7: NaNは100以上の比較がFalseになるため、送料無料にならないことを確認する。
    assert service.is_free_shipping(float("nan")) is False


def test_TC8_positive_infinity_is_free_shipping(service):
    # TC8: 正の無限大は100以上と判定されることを確認する。
    assert service.is_free_shipping(float("inf")) is True


def test_TC9_negative_infinity_is_not_free_shipping(service):
    # TC9: 負の無限大は100未満と判定されることを確認する。
    assert service.is_free_shipping(float("-inf")) is False


def test_TC10_string_total_raises_type_error(service):
    # TC10: 文字列は整数との大小比較に対応しないためTypeErrorになることを確認する。
    with pytest.raises(TypeError):
        service.is_free_shipping("100")


def test_TC11_none_total_raises_type_error(service):
    # TC11: NoneTypeは整数と大小比較できずTypeErrorになることを確認する。
    with pytest.raises(TypeError):
        service.is_free_shipping(None)


def test_TC12_list_total_raises_type_error(service):
    # TC12: listは整数と大小比較できずTypeErrorになることを確認する。
    with pytest.raises(TypeError):
        service.is_free_shipping([])