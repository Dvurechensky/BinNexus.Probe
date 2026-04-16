# app/args.py

import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Binary Analyzer (Neural Heatmap Prototype)"
    )

    parser.add_argument(
        "file",
        help="Path to target EXE/DLL"
    )

    parser.add_argument(
        "--config",
        default=None,
        help="Path to config file (json)"
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Override output file"
    )

    parser.add_argument(
        "--window",
        type=int,
        default=None,
        help="Override window size"
    )

    parser.add_argument(
        "--step",
        type=int,
        default=None,
        help="Override step size"
    )

    return parser.parse_args()