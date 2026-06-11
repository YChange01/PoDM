#!/usr/bin/env python3
"""Compatibility wrapper for scripts/promote_podm_bmc_baseline.py."""
from __future__ import annotations

from promote_podm_bmc_baseline import *  # noqa: F401,F403
from promote_podm_bmc_baseline import main


if __name__ == "__main__":
    main()
