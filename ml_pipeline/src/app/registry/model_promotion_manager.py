# -*- coding: utf-8 -*-

import os
import shutil


class ModelPromotionManager:
    """
    Gerencia promoção e rollback de modelos.
    """

    def __init__(self, registry_base: str):
        self.alias_path = os.path.join(registry_base, "aliases")

    def promote(
        self,
        *,
        experiment_path: str,
        model_name: str,
        alias: str = "production",
    ):
        os.makedirs(self.alias_path, exist_ok=True)

        target = os.path.join(self.alias_path, alias)
        source = os.path.join(experiment_path, model_name)

        if not os.path.exists(source):
            raise RuntimeError(f"Modelo não encontrado: {source}")

        # backup do alias atual
        if os.path.islink(target):
            previous = os.path.join(self.alias_path, "previous")
            if os.path.exists(previous):
                os.unlink(previous)
            os.symlink(os.readlink(target), previous)

            os.unlink(target)

        os.symlink(source, target)

    def rollback(self):
        prod = os.path.join(self.alias_path, "production")
        prev = os.path.join(self.alias_path, "previous")

        if not os.path.islink(prev):
            raise RuntimeError("Nenhum modelo anterior para rollback")

        os.unlink(prod)
        os.symlink(os.readlink(prev), prod)
