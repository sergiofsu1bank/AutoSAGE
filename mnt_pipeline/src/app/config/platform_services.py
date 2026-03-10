import os

PLATFORM_SERVICES = {
    "orc": os.getenv("MNT_ORC_URL"),
    "dcp": os.getenv("MNT_DCP_URL"),
    "eda_explore": os.getenv("MNT_EDA_EXPLORE_URL"),
    "eda_prepare": os.getenv("MNT_EDA_PREPARE_URL"),
    "ml": os.getenv("MNT_ML_URL"),
    "llm": os.getenv("MNT_LLM_URL"),
    "metrics": os.getenv("MNT_METRICS_URL"),
    "monitor": os.getenv("MNT_MONITOR_URL"),
}
