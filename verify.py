#!/usr/bin/env python3
"""verify.py -- CI gate. Runs the oracle over the labelled corpus; exit 0 IFF recall==1.0 AND FP==0 AND non-degenerate."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "oracle"))
import web_crawl_attestation_oracle as oracle  # noqa: E402
if __name__ == "__main__":
    sys.exit(oracle._run_probes(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probes", "probes.jsonl")))
