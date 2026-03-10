# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass(frozen=True)
class MLTrainContract:
    dataset_name: str
    dataset_version: str
    target_name: str
    problem_type: str
    metric: str
    random_seed: int
