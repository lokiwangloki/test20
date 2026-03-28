import os
from typing import Any, Dict, Optional


def env_override(config: Dict[str, Any], key: str, default_env_name: str) -> Optional[str]:
    mapped_env_name = str(config.get(f"{key}_env", "") or "").strip()
    if mapped_env_name:
        mapped_value = os.environ.get(mapped_env_name)
        if mapped_value is not None:
            return mapped_value
    return os.environ.get(default_env_name)
