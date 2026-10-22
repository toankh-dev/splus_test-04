import unittest

from temp_module import TempModule


class TestTempModuleRun(unittest.TestCase):
    def test_tc1_instance_returns_exact_string(self):
        # TC1: インスタンスから呼び出し、戻り値と型の完全一致を確認する。
        instance = TempModule()

        result = instance.run()

        self.assertEqual(result, "temp for testing")
        self.assertIs(type(result), str)

    def test_tc2_none_self_returns_exact_string(self):
        # TC2: self に None を明示的に渡しても例外なく同じ文字列を返す。
        result = TempModule.run(None)

        self.assertEqual(result, "temp for testing")
        self.assertIs(type(result), str)

    def test_tc3_integer_self_returns_exact_string(self):
        # TC3: self に整数 0 を明示的に渡しても例外なく同じ文字列を返す。
        result = TempModule.run(0)

        self.assertEqual(result, "temp for testing")
        self.assertIs(type(result), str)


if __name__ == "__main__":
    unittest.main()