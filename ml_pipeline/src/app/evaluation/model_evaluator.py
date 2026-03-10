# -*- coding: utf-8 -*-

from typing import List
import numpy as np
from scipy.stats import ttest_rel, wilcoxon


class ModelEvaluator:
    """
    Avaliador científico de modelos.

    Responsabilidades:
    - Comparar modelos contra baseline
    - Aplicar testes estatísticos
    - Decidir aprovação / reprovação
    """

    def __init__(self, *, alpha: float = 0.05):
        self.alpha = alpha

    # --------------------------------------------------
    # Aprovação de modelo
    # --------------------------------------------------
    def approve(self, candidate_report, baseline_report) -> bool:
        """
        Decide se um modelo é aprovado contra o baseline.
        """
        candidate_scores = candidate_report.scores
        baseline_scores = baseline_report.scores

        # Métrica média mínima
        if np.mean(candidate_scores) <= np.mean(baseline_scores):
            return False

        # Teste estatístico
        return self._statistical_test(
            candidate_scores,
            baseline_scores,
        )

    # --------------------------------------------------
    # Testes estatísticos
    # --------------------------------------------------
    def _statistical_test(
        self,
        candidate: List[float],
        baseline: List[float],
    ) -> bool:
        """
        Executa teste estatístico pareado.
        """
        if len(candidate) < 2:
            # Sem poder estatístico
            return False

        # Teste de normalidade simples (heurístico)
        diff = np.array(candidate) - np.array(baseline)

        if self._is_normal(diff):
            _, p_value = ttest_rel(candidate, baseline)
        else:
            _, p_value = wilcoxon(candidate, baseline)

        return p_value < self.alpha

    def _is_normal(self, diff: np.ndarray) -> bool:
        """
        Heurística simples de normalidade.
        """
        return np.abs(np.mean(diff)) < np.std(diff)
