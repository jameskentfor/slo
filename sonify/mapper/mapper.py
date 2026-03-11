import json


class Mapper:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = json.load(f)

    def process(self, signal: dict) -> dict | None:
        sid = signal["id"]

        if sid not in self.config:
            print(f"[Mapper] WARNING: no mapping for signal '{sid}', skipping.")
            return None

        return {"id": self.config[sid], "value": signal["value"], "ts": signal["ts"]}
