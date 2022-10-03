"""
This provides the flexibility to run the code in both FLIGHTMODE OR DEBUG
"""

import os


def is_flight_mode_on() -> bool:
    return is_env_var_on(env_var="FLIGHTMODE")


def is_debug_mode_on() -> bool:
    return is_env_var_on(env_var="DEBUG")


def is_env_var_on(env_var: str) -> bool:
    if os.getenv(key=env_var) == "1":
        return True

    return False
