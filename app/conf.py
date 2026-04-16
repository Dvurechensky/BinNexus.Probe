# app/conf.py

import json
import os


DEFAULT_CONFIG = {
    "window_size": 32,
    "step": 4,
    "output": "build/heatmap.json",

    "log_level": "INFO",
    "log_file": "logs/analyzer.log"
}

def ensure_output_path(path: str):
    directory = os.path.dirname(path)

    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def load_config(path: str | None):
    config = DEFAULT_CONFIG.copy()

    ensure_output_path(config["output"])

    if path and os.path.exists(path):
        with open(path, "r") as f:
            user_conf = json.load(f)
            config.update(user_conf)

    return config


def apply_overrides(config, args):
    if args.output:
        config["output"] = args.output

    if args.window:
        config["window_size"] = args.window

    if args.step:
        config["step"] = args.step

    return config