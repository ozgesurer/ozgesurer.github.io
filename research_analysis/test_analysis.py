import unittest
from analyze import token_windows


class WindowCoverageTest(unittest.TestCase):
    def test_no_lost_tokens_at_boundaries(self):
        for count in [1, 254, 255, 476, 477, 1200]:
            tokens = list(range(count))
            windows = token_windows(tokens, 254, 32)
            self.assertEqual(set().union(*(set(w) for w, _ in windows)), set(tokens))
            self.assertEqual(sum(weight for _, weight in windows), count)
            self.assertTrue(all(len(w) <= 254 for w, _ in windows))

    def test_invalid_overlap(self):
        for overlap in [-1, 254, 255]:
            with self.assertRaises(ValueError):
                token_windows([1], 254, overlap)


if __name__ == '__main__':
    unittest.main()
