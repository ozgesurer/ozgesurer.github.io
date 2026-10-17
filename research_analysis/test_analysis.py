import unittest
import importlib.util
import tempfile
from pathlib import Path
from analyze import token_windows, prepare_window


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


@unittest.skipUnless(importlib.util.find_spec('transformers') and importlib.util.find_spec('torch'),
                     'Install analysis dependencies to run tokenizer regression tests')
class TokenizerRegressionTest(unittest.TestCase):
    def test_long_document_is_batched_without_truncation(self):
        from transformers import BertTokenizerFast
        # Real BERT tokenizer, constructed locally: no model or tokenizer downloads.
        with tempfile.TemporaryDirectory() as directory:
            vocab = Path(directory) / 'vocab.txt'
            vocab.write_text('[PAD]\n[UNK]\n[CLS]\n[SEP]\n[MASK]\nresearch\nmethods\nsimulation\n')
            tokenizer = BertTokenizerFast(vocab_file=str(vocab), model_max_length=256)
            for count in [1, 254, 255, 284, 476, 477, 1200]:
                with self.subTest(tokens=count):
                    words = ['research', 'methods', 'simulation']
                    ids = tokenizer.encode(' '.join(words[i % len(words)] for i in range(count)),
                                           add_special_tokens=False, truncation=False, verbose=False)
                    self.assertEqual(len(ids), count)
                    capacity = 256 - tokenizer.num_special_tokens_to_add(pair=False)
                    windows = token_windows(ids, capacity, 32)
                    reconstructed = []
                    for tokens, weight in windows:
                        features = prepare_window(tokenizer, tokens, 256)
                        self.assertEqual(features['input_ids'].ndim, 2)
                        self.assertEqual(features['input_ids'].shape[0], 1)
                        self.assertLessEqual(features['input_ids'].shape[1], 256)
                        self.assertEqual(features['attention_mask'].shape, features['input_ids'].shape)
                        self.assertEqual(features['input_ids'][0].tolist(),
                                         tokenizer.build_inputs_with_special_tokens(tokens))
                        reconstructed.extend(tokens[-weight:])
                    self.assertEqual(reconstructed, ids)
                    self.assertEqual(sum(w for _, w in windows), count)
            with self.assertRaises(ValueError):
                prepare_window(tokenizer, [tokenizer.unk_token_id] * 255, 256)


if __name__ == '__main__':
    unittest.main()
