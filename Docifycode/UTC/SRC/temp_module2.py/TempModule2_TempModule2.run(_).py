from copy import deepcopy

import pytest

from temp_module2 import TempModule2


@pytest.mark.parametrize(
    "initial_state",
    [
        {},
        {"status": "ready", "values": [1, 2], "metadata": {"enabled": True}},
    ],
    ids=["empty_state", "populated_state"],
)
def test_TC1_returns_exact_string_without_changing_state(initial_state):
    # TC1: 固定文字列を返し、空の状態でも属性を持つ状態でも変更しない。
    instance = TempModule2()
    instance.__dict__.update(deepcopy(initial_state))
    state_before = deepcopy(vars(instance))

    result = instance.run()

    assert type(result) is str
    assert result == "temp for debugging"
    assert vars(instance) == state_before


def test_TC2_unbound_call_accepts_none():
    # TC2: 非束縛呼び出しで self に None を渡しても正常に返す。
    result = TempModule2.run(None)

    assert type(result) is str
    assert result == "temp for debugging"


def test_TC3_unbound_call_accepts_integer():
    # TC3: 非束縛呼び出しで self に整数を渡しても正常に返す。
    result = TempModule2.run(42)

    assert type(result) is str
    assert result == "temp for debugging"


def test_TC4_unbound_call_without_self_raises_type_error():
    # TC4: 必須引数 self を省略すると、引数束縛時に TypeError が発生する。
    with pytest.raises(TypeError):
        TempModule2.run()


def test_TC5_three_consecutive_calls_return_same_string():
    # TC5: 同じインスタンスで３回連続して呼び出し、毎回の戻り値を確認する。
    instance = TempModule2()
    state_before = deepcopy(vars(instance))
    results = []

    for _ in range(3):
        result = instance.run()
        results.append(result)

        assert type(result) is str
        assert result == "temp for debugging"
        assert vars(instance) == state_before

    assert results == ["temp for debugging"] * 3