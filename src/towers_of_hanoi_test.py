import typing
from towers_of_hanoi import (
    Move,
    towers_of_hanoi,
)
import unittest
import dataclasses

SOURCE = 0
AUXILARY = 1
DESTINATION = 2


@dataclasses.dataclass
class TestCase:
    result: typing.List[Move]
    expected: typing.List[Move]


class TestCaseListBuilder:
    test_cases: typing.List[TestCase]

    def append_case(self, result: typing.List[Move], expected: typing.List[Move]):
        self.test_cases.append(TestCase(result, expected))
        return self

    def append_cases(
        self,
        cases: typing.List[typing.Tuple[typing.List[Move], typing.List[Move]]],
    ):

        for c in cases:
            self.test_cases.append(TestCase(result=c[0], expected=c[1]))

        return self

    def build(self) -> typing.List[TestCase]:
        return self.test_cases


class TestTowersOfHanoi(unittest.TestCase):
    def test_optimal(self):
        test_cases = []

        test_cases = [
            TestCase(
                result=towers_of_hanoi(1, SOURCE, DESTINATION, AUXILARY),
                expected=[Move(SOURCE, DESTINATION)],
            ),
            TestCase(
                result=towers_of_hanoi(2, SOURCE, DESTINATION, AUXILARY),
                expected=[
                    Move(SOURCE, AUXILARY),
                    Move(SOURCE, DESTINATION),
                    Move(AUXILARY, DESTINATION),
                ],
            ),
            TestCase(
                result=towers_of_hanoi(3, SOURCE, DESTINATION, AUXILARY),
                expected=[
                    Move(SOURCE, DESTINATION),
                    Move(SOURCE, AUXILARY),
                    Move(DESTINATION, AUXILARY),
                    Move(SOURCE, DESTINATION),
                    Move(AUXILARY, SOURCE),
                    Move(AUXILARY, DESTINATION),
                    Move(SOURCE, DESTINATION),
                ],
            ),
        ]

        for test_case in test_cases:
            self.assertEqual(test_case.result, test_case.expected)
