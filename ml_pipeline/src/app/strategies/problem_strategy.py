# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ProblemStrategy(ABC):
    """
    Estratégia científica base para problemas de ML.

    Responsabilidades:
    - Definir metodologia científica permitida
    - Governar split, CV, métricas, modelos e reduções
    - NÃO executar treino
    - NÃO transformar dados
    """

    def __init__(self, *, problem_type: str):
        self.problem_type = problem_type

    # --------------------------------------------------
    # Identidade
    # --------------------------------------------------
    @abstractmethod
    def name(self) -> str:
        """Nome canônico da estratégia"""
        pass

    # --------------------------------------------------
    # Split
    # --------------------------------------------------
    @abstractmethod
    def split_policy(self) -> Dict[str, Any]:
        """
        Define como os dados podem ser divididos.
        Ex: random, stratified, temporal, walk-forward
        """
        pass

    # --------------------------------------------------
    # Cross-Validation
    # --------------------------------------------------
    @abstractmethod
    def cv_policy(self) -> Dict[str, Any]:
        """
        Define se CV é permitido e como.
        Ex: kfold, stratified_kfold, none
        """
        pass

    # --------------------------------------------------
    # Métricas
    # --------------------------------------------------
    @abstractmethod
    def allowed_metrics(self) -> List[str]:
        """
        Métricas cientificamente válidas para o problema.
        """
        pass

    # --------------------------------------------------
    # Modelos
    # --------------------------------------------------
    @abstractmethod
    def allowed_models(self) -> List[str]:
        """
        Lista de modelos permitidos.
        Ex: logistic, random_forest, gbm
        """
        pass

    # --------------------------------------------------
    # Redução de dimensionalidade
    # --------------------------------------------------
    @abstractmethod
    def dimensionality_reduction_policy(self) -> Dict[str, Any]:
        """
        Define se PCA, FA, MCA etc. são permitidos.
        """
        pass

    # --------------------------------------------------
    # Avaliação
    # --------------------------------------------------
    @abstractmethod
    def evaluation_policy(self) -> Dict[str, Any]:
        """
        Define regras de aprovação/reprovação do modelo.
        """
        pass

    # --------------------------------------------------
    # Re-treino
    # --------------------------------------------------
    @abstractmethod
    def retraining_policy(self) -> Dict[str, Any]:
        """
        Define condições para re-treino (drift, degradação etc.)
        """
        pass
