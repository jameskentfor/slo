#!/usr/bin/env python3
"""
Runs the pipeline and oscdump together, logging OSC output to the console.
Press Ctrl+C to stop.
"""

import subprocess
import threading
import sys
import time


def stream_output(process, label):
    for line in process.stdout:
        print(f"[{label}] {line}", end="")
        sys.stdout.flush()


def main():
    oscdump = subprocess.Popen(
        ["oscdump", "57120"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    time.sleep(0.5)  # give oscdump time to bind the port

    pipeline = subprocess.Popen(
        ["python3", "-u", "pipeline.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    threading.Thread(target=stream_output, args=(oscdump, "osc"), daemon=True).start()
    threading.Thread(target=stream_output, args=(pipeline, "pipeline"), daemon=True).start()

    print("[test] Running — press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[test] Stopping...")
    finally:
        pipeline.terminate()
        oscdump.terminate()
        pipeline.wait()
        oscdump.wait()


if __name__ == "__main__":
    main()
