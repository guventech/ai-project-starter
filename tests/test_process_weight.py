"""Classification checks for Lite / Standard / Strict process weights."""
import unittest

from scripts.process_weight import infer_process_weight


class ProcessWeightTests(unittest.TestCase):
    def test_typo_selects_lite(self):
        self.assertEqual(infer_process_weight('fix a typo in the README title'), 'lite')

    def test_symbol_rename_selects_lite(self):
        self.assertEqual(infer_process_weight('rename the helper function to load_config'), 'lite')

    def test_payment_feature_selects_strict(self):
        self.assertEqual(
            infer_process_weight('Add a payment checkout flow with Stripe billing'),
            'strict',
        )

    def test_auth_selects_strict_over_docs_wording(self):
        self.assertEqual(
            infer_process_weight('document the authentication password reset path'),
            'strict',
        )

    def test_ordinary_feature_is_undetermined(self):
        self.assertIsNone(infer_process_weight('Add a weekly summary email for completed tasks'))


if __name__ == '__main__':
    unittest.main()
