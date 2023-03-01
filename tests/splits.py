"""
Test split jointness
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
import numpy as np

class SplitTests(unittest.TestCase):
    def setUp(self):
        self.organisms = ["hs", "mm", "dm", "sc"]
        self.splits = 1
        self.percents = (0.6, 0.2)


    def tearDown(self) -> None:
        pass

    def test_splits(self):
        for organism in self.organisms:
            for split in range(self.splits):
                train_mask = np.load(f"../splits/eppugnn_splits_{organism}_{self.percents[0]}_{self.percents[1]}_{split}.npz")["train_mask"]
                val_mask = np.load(f"../splits/eppugnn_splits_{organism}_{self.percents[0]}_{self.percents[1]}_{split}.npz")["val_mask"]
                test_mask = np.load(f"../splits/eppugnn_splits_{organism}_{self.percents[0]}_{self.percents[1]}_{split}.npz")["test_mask"]


                # Check that the train and val masks are disjoint
                self.assertTrue(np.all(train_mask + val_mask < 2), f"Train and val masks are not disjoint")

                # Check that train_mask is around train_percent
                self.assertTrue(np.abs(np.sum(train_mask) / len(train_mask) - self.percents[0]) < 0.01, f"Train percent: {np.sum(train_mask) / len(train_mask)}")

                # Check that val_mask is around val_percent
                self.assertTrue(np.abs(np.sum(val_mask) / len(val_mask) - self.percents[1]) < 0.01, f"Validation percent: {np.sum(val_mask) / len(val_mask)}")

                # check that all the masks are disjoint from each other and all indices are covered
                self.assertTrue(np.all(train_mask + val_mask + test_mask == 1), f"Train, val, and test masks are not disjoint from each other")

st = SplitTests()
st.setUp()
st.test_splits()
