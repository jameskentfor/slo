import json


class Normalizer:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = json.load(f)

    def process(self, signal: dict) -> dict | None:
        sid = signal["id"]

        if sid not in self.config:
            print(f"[Normalizer] WARNING: no config for signal '{sid}', skipping.")
            return None

        cfg = self.config[sid]
        lo, hi = cfg["min"], cfg["max"]
        normalized = (signal["value"] - lo) / (hi - lo)

        if normalized < 0.0 or normalized > 1.0:
            print(f"[Normalizer] WARNING: '{sid}' value {signal['value']} out of range [{lo}, {hi}], clamping.")
            normalized = max(0.0, min(1.0, normalized))

        return {"id": sid, "value": normalized, "ts": signal["ts"]}
