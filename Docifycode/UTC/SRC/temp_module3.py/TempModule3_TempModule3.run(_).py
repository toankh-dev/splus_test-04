from temp_module3 import TempModule3


def test_tc1_run_on_instance():
    # TC1: 通常のインスタンスメソッド呼び出しで、戻り値と型を確認する。
    instance = TempModule3()

    result = instance.run()

    assert result == "temp for mock test"
    assert type(result) is str


def test_tc2_run_with_none_as_self():
    # TC2: クラスから取得した未束縛の関数に、selfとしてNoneを明示的に渡す。
    unbound_run = TempModule3.run

    result = unbound_run(None)

    assert result == "temp for mock test"
    assert type(result) is str