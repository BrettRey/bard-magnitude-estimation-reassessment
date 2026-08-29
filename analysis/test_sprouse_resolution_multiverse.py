#!/usr/bin/env python3

import unittest

import numpy as np
import pandas as pd

import sprouse_resolution_multiverse as multiverse


class SprouseResolutionMultiverseTests(unittest.TestCase):
    def test_zero_me_response_is_retained_outside_log_branch(self) -> None:
        frame = pd.DataFrame(
            {
                "participant": ["a", "a", "a"],
                "condition": ["x", "y", "z"],
                "judgment": [0.0, 1.0, 2.0],
                "zscores": [-1.0, 0.0, 1.0],
            }
        )
        scored = multiverse.add_scores(frame, "participant", "me")
        self.assertEqual(scored.loc[0, "provided_z"], -1.0)
        self.assertTrue(np.isfinite(scored.loc[0, "subject_percentile"]))
        self.assertTrue(np.isnan(scored.loc[0, "log_subject_z"]))

    def test_endpoint_statistic_detects_two_sided_extra_spread(self) -> None:
        me = np.array([-3.0, 3.0, -0.1, 0.1, -4.0, 4.0])
        masks = (
            np.array([True, True, False, False, False, False]),
            np.array([False, False, True, True, False, False]),
            np.array([False, False, False, False, True, True]),
        )
        *_, lower_ratio, upper_ratio = multiverse.endpoint_statistic(me, masks, "sd")
        self.assertGreater(lower_ratio, 10.0)
        self.assertGreater(upper_ratio, 10.0)

    def test_cross_validation_detects_unique_me_prediction(self) -> None:
        rng = np.random.default_rng(17)
        n = 120
        ls = rng.normal(size=n)
        me = rng.normal(size=n)
        target = 2.0 * me + rng.normal(scale=0.15, size=n)
        r2_ls, r2_me, r2_full = multiverse.cv_model_scores(
            ls, me, target, "raw_ols", repeats=10, folds=5, seed=19
        )
        self.assertGreater(float((r2_full - r2_ls).mean()), 0.80)
        self.assertLess(abs(float((r2_full - r2_me).mean())), 0.02)

    def test_decision_family_can_clear_when_me_wins(self) -> None:
        rows = []
        for index in range(6):
            row = {
                "dataset": "2013",
                "pair_id": str(index + 1),
                "target_fc_sign": 0.4,
                "target_fc_logistic": 0.8,
            }
            row.update({f"me_{score}": 1.0 for score in multiverse.ME_SCORES})
            row.update({f"ls_{score}": -1.0 for score in multiverse.LS_SCORES})
            rows.append(row)
        result = multiverse.decision_multiverse(rows)
        self.assertEqual(len(result), 18)
        self.assertTrue(all(row["specification_support"] for row in result))


if __name__ == "__main__":
    unittest.main()
