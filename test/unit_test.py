import unittest
from src import softdes


class UnitTest(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_lambda_handler_should_return_right_answer(self):
        test_code = "def desafio1(test_input):\n\treturn 1*3*4*int(test_input)"

        event = {
            "ndes": "1",
            "code": test_code,
            "args": ["3"],
            "resp": [36],
            "diag": ["36"],
        }

        context = ""
        errors = softdes.lambda_handler(event, context)
        assert errors == ""

    def test_lambda_handler_should_throw_error_with_invalid_function_name(self):
        test_code = "def desafio1(test_input):\n\treturn"

        event = {
            "ndes": "0",
            "code": test_code,
            "args": ["0"],
            "resp": "0",
            "diag": "0",
        }

        context = ""
        response = softdes.lambda_handler(event, context)
        assert response == "Nome da função inválido. Usar 'def desafio0(...)'"

    def test_lambda_handler_should_return_wrong_answer(self):
        test_code = "def desafio1(test_input):\n\treturn 1*3*4*int(test_input)"

        event = {
            "ndes": "1",
            "code": test_code,
            "args": ["3"],
            "resp": [10],
            "diag": ["Wrong result"],
        }

        context = ""
        errors = softdes.lambda_handler(event, context)
        assert errors == "Wrong result"
