#!/usr/bin/env python3
"""Compatibility wrapper for scripts/compare_podm_bmc_to_baseline.py."""
from __future__ import annotations

from compare_podm_bmc_to_baseline import *  # noqa: F401,F403
from compare_podm_bmc_to_baseline import main


if __name__ == "__main__":
    main()
