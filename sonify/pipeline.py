import json
import time

from receptors.mock_generator.mock_generator import MockGenerator
from receptors.moon_receptor.moon_receptor import MoonReceptor
from normalizer.normalizer import Normalizer
from mapper.mapper import Mapper
from controller.osc.osc_controller import OscController

RECEPTORS = {
    "mock_generator": MockGenerator,
    "moon_receptor": MoonReceptor,
}


def build_receptor(config):
    return RECEPTORS[config["type"]](**config.get("args", {}))


def run():
    with open("pipeline_config.json") as f:
        config = json.load(f)

    tick_interval = 1 / config["tick_rate"]

    receptor = build_receptor(config["receptor"])
    normalizer = Normalizer("normalizer/normalizer_config.json")
    mapper = Mapper("mapper/mapper_config.json")
    controller = OscController("controller/osc/osc_config.json")

    print("[Pipeline] Starting...")

    try:
        while True:
            for signal in receptor.read():
                normalized = normalizer.process(signal)
                if normalized is None:
                    continue

                mapped = mapper.process(normalized)
                if mapped is None:
                    continue

                controller.send(mapped)

            time.sleep(tick_interval)

    except KeyboardInterrupt:
        print("[Pipeline] Stopped.")


if __name__ == "__main__":
    run()
