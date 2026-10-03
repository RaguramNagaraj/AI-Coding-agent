from tools.test_runner import TestRunner


runner = TestRunner()

result = runner.run_tests(
    "test_calculator.py"
)

print(result)