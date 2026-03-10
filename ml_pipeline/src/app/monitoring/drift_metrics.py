# -*- coding: utf-8 -*-

import numpy as np


class DriftMetrics:

    @staticmethod
    def zscore_shift(train_mean, train_std, prod_mean):
        if train_std == 0:
            return 0.0
        return abs(prod_mean - train_mean) / train_std

    @staticmethod
    def psi(expected, actual, buckets=10):
        expected = np.array(expected)
        actual = np.array(actual)

        def scale(arr):
            return np.histogram(arr, bins=buckets)[0] / len(arr)

        e_perc = scale(expected)
        a_perc = scale(actual)

        psi = np.sum(
            (a_perc - e_perc) * np.log((a_perc + 1e-6) / (e_perc + 1e-6))
        )
        return float(psi)
