import pytest

from SRC.temp_module import TempModule


def test_TC1_run_without_arguments_returns_fixed_string():
    # TC1: 引数なしで呼び出すと、固定文字列を返す。
    instance = TempModule()

    assert instance.run() == "temp for testing"


def test_TC2_run_repeatedly_returns_same_fixed_string():
    # TC2: 同じインスタンスで続けて呼び出しても、毎回同じ文字列を返す。
    instance = TempModule()

    assert instance.run() == "temp for testing"
    assert instance.run() == "temp for testing"


def test_TC3_run_with_unsupported_positional_argument_raises_type_error():
    # TC3: 未対応の位置引数を渡すと、TypeErrorが発生する。
    instance = TempModule()

    with pytest.raises(TypeError):
        instance.run(1)


def test_TC4_run_with_unsupported_keyword_argument_raises_type_error():
    # TC4: 未対応のキーワード引数を渡すと、TypeErrorが発生する。
    instance = TempModule()

    with pytest.raises(TypeError):
        instance.run(x="value")