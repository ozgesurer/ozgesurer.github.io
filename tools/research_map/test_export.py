import tempfile
import unittest
from pathlib import Path
from export import THEMES, finite, load_artifacts


class ExportValidationTest(unittest.TestCase):
    def test_themes_partition_exact_original_ids(self):
        ids = [p for theme in THEMES for p in theme['publications']]
        self.assertEqual(len(ids), 15)
        self.assertEqual(set(ids), {f'P{i:02d}' for i in range(1, 16)})

    def test_nonfinite_inputs_rejected(self):
        for value in ['nan', 'inf', '-inf']:
            with self.assertRaises(ValueError):
                finite(value)

    def test_missing_results_never_generate_substitute_data(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(FileNotFoundError):
                load_artifacts(Path(directory))


if __name__ == '__main__':
    unittest.main()
