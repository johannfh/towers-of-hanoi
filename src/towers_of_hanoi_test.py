import typing
import towers_of_hanoi as toh
import unittest
import dataclasses

@dataclasses.dataclass
class TestCase:
    result: typing.List[toh.Move]
    expected: typing.List[toh.Move]

class TestTowersOfHanoi(unittest.TestCase):
    SOURCE = 0
    AUXILARY = 1
    DESTINATION = 2

    def test_optimal(self):

        test_cases: typing.List[TestCase] = [
            TestCase(
                result=toh.towers_of_hanoi(1, self.SOURCE, self.DESTINATION, self.AUXILARY),
                expected=[
                    (self.SOURCE, self.DESTINATION),
                ],
            ),
            TestCase(
                result = toh.towers_of_hanoi(2, self.SOURCE, self.DESTINATION, self.AUXILARY),
                expected = [
                    (self.SOURCE, self.AUXILARY),
                    (self.SOURCE, self.DESTINATION),
                    (self.AUXILARY, self.DESTINATION),
                ],
            ),
            TestCase(
                result = toh.towers_of_hanoi(3, self.SOURCE, self.DESTINATION, self.AUXILARY),
                expected = [
                    (self.SOURCE, self.DESTINATION),
                    (self.SOURCE, self.AUXILARY),
                    (self.DESTINATION, self.AUXILARY),
                    (self.SOURCE, self.DESTINATION),
                    (self.AUXILARY, self.SOURCE),
                    (self.AUXILARY, self.DESTINATION),
                    (self.SOURCE, self.DESTINATION),
                ],
            ),
            # TestCase(
            #     result = toh.towers_of_hanoi(4, self.SOURCE, self.DESTINATION, self.AUXILARY),
            #     expected = [
            #         (self.SOURCE, self.DESTINATION),
            #         (self.SOURCE, self.AUXILARY),
            #         (self.DESTINATION, self.AUXILARY),
            #         (self.SOURCE, self.DESTINATION),
            #         (self.AUXILARY, self.SOURCE),
            #         (self.AUXILARY, self.DESTINATION),
            #         (self.SOURCE, self.DESTINATION),
            #     ],
            # ),
        ]

        for test_case in test_cases:
            self.assertEqual(test_case.result, test_case.expected)
