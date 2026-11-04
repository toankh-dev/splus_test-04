import functools

import pytest

from SRC.temp_module2 import TempModule2


EXPECTED_RESULT = "temp for debugging"


def test_run_without_arguments_returns_fixed_string():
    # TC1: 引数なしで呼び出すと固定文字列を返す
    instance = TempModule2()

    assert instance.run() == EXPECTED_RESULT


def test_run_with_unexpected_positional_argument_raises_type_error():
    # TC2: 未定義の位置引数を渡すとTypeErrorになる
    instance = TempModule2()

    with pytest.raises(TypeError):
        instance.run(1)


def test_run_with_unexpected_keyword_argument_raises_type_error():
    # TC3: 未定義のキーワード引数を渡すとTypeErrorになる
    instance = TempModule2()

    with pytest.raises(TypeError):
        instance.run(value=1)


def test_run_called_on_class_without_self_raises_type_error():
    # TC4: selfを渡さずクラスから呼び出すとTypeErrorになる
    with pytest.raises(TypeError):
        TempModule2.run()


def test_run_returns_fixed_string_for_different_instances():
    # TC5: 異なるインスタンスでも固定文字列を返す
    first_instance = TempModule2()
    second_instance = TempModule2()

    assert first_instance.run() == EXPECTED_RESULT
    assert second_instance.run() == EXPECTED_RESULT


def test_run_returns_fixed_string_when_called_repeatedly():
    # TC6: 同一インスタンスで繰り返し呼び出しても固定文字列を返す
    instance = TempModule2()

    assert instance.run() == EXPECTED_RESULT
    assert instance.run() == EXPECTED_RESULT
    assert instance.run() == EXPECTED_RESULT


def test_run_accepts_none_as_self():
    # TC7: selfとしてNoneを渡しても固定文字列を返す
    assert TempModule2.run(None) == EXPECTED_RESULT


def test_run_returns_fixed_string_when_self_is_partially_applied():
    # TC8: selfを部分適用した関数でも固定文字列を返す
    partially_applied_run = functools.partial(TempModule2.run, self=None)

    assert partially_applied_run() == EXPECTED_RESULT