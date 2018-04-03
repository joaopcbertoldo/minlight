import unittest as ut
from src.math_entities import Vec3
from numpy import matrix


class InitializationTest(ut.TestCase):

    def test_new(self):

        v = Vec3(0.0, 0.0, 0.0)

        self.subTest('type Vec3')
        self.assertEqual(type(v), Vec3)

        self.subTest('is matrix')
        self.assertTrue(isinstance(v, matrix))

        self.subTest('shape')
        self.assertEqual(v.shape, (3, 1))


def suite():
    st = ut.TestSuite()
    st.addTest(InitializationTest())
    return st


def main():
    runner = ut.TextTestRunner()
    runner.run(suite())


if __name__ == '__main__':
    main()
