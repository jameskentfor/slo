# Sonify

Modular sonification middleware that translates real-world data into musical control signals. Connects sensors, cameras, astronomical data, and other sources to synthesizers and music software via OSC.

## How it works

Data flows through a four-stage pipeline:

```
Receptor → Normalizer → Mapper → Controller
```

1. **Receptor** — reads raw data from a source (sensor, moon phase, mock generator, etc.) and emits `{id, value, ts}` signals
2. **Normalizer** — scales raw values to a 0–1 range using configured min/max bounds; clamps and warns if a value falls outside the configured range
3. **Mapper** — translates source signal IDs to musical target IDs (e.g. `brightness` → `filter_cutoff`)
4. **Controller** — sends the mapped values as OSC messages to a synthesizer or DAW

## Setup

Requires Python 3 and the packages in `sonify/requirements.txt`:

```bash
pip3 install -r sonify/requirements.txt
```

If using the dev container, this is handled automatically by `.devcontainer/postCreate.sh`.

`liblo-tools` is also installed system-wide via the dev container for OSC debugging.

## Running

From the `sonify/` directory:

```bash
python3 pipeline.py
```

The pipeline reads `pipeline_config.json` to determine the tick rate and which receptor to use.

**Mock generator** (for testing):
```json
{
  "tick_rate": 30,
  "receptor": {
    "type": "mock_generator",
    "args": { "config_path": "receptors/mock_generator/mock_config.json" }
  }
}
```

**Moon receptor**:
```json
{
  "tick_rate": 30,
  "receptor": {
    "type": "moon_receptor",
    "args": { "timezone": "UTC" }
  }
}
```

## Configuration

| File | Purpose |
|------|---------|
| `sonify/pipeline_config.json` | Tick rate and receptor selection |
| `sonify/normalizer/normalizer_config.json` | Min/max bounds per signal ID |
| `sonify/mapper/mapper_config.json` | Source → target ID mappings |
| `sonify/controller/osc/osc_config.json` | OSC host, port, and address prefix |
| `sonify/receptors/mock_generator/mock_config.json` | Mock signal ranges |

## Receptors

| Receptor | Description |
|----------|-------------|
| `mock_generator` | Generates random-walking test signals |
| `moon_receptor` | Calculates moon phase and illumination using Meeus astronomical algorithms (Chapters 25 & 47) |

### Moon receptor signals

| Signal ID | Range | Description |
|-----------|-------|-------------|
| `moon_phase` | 0–360° | Ecliptic longitude difference between Moon and Sun |
| `moon_illumination` | 0–100% | Percentage of lunar disk illuminated |

To add a new receptor, implement a class with a `read()` method that yields `{id, value, ts}` dicts, then register it in `pipeline.py`.

## Testing OSC output

The `test_osc.py` script runs the pipeline and `oscdump` together in a single terminal, logging all OSC output as it arrives. Run it from the `sonify/` directory:

```bash
python3 test_osc.py
```

Output looks like:

```
[osc] 0.000 /synth/filter_cutoff ,f 0.472
[osc] 0.033 /synth/pan ,f 0.651
[pipeline] [Pipeline] Starting...
```

Press `Ctrl+C` to stop both processes.

Alternatively, run `oscdump` manually to monitor messages without the pipeline wrapper:

```bash
oscdump 57120
```

## OSC output

Messages are sent to `localhost:57120` with the prefix `/synth/` by default. For example, a signal mapped to `filter_cutoff` is sent as `/synth/filter_cutoff <value>`.
