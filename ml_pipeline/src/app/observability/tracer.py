# -*- coding: utf-8 -*-

import uuid


class MLTracer:
    """
    Gerador simples de trace_id.
    """

    @staticmethod
    def new_trace_id() -> str:
        return f"ml-{uuid.uuid4().hex[:16]}"
