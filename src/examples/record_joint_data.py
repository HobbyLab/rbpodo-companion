"""
Interactive Joint/TCP Data Recorder

This script provides an interactive CLI tool to capture joint angles and TCP positions
from the robot in real time. Each press of [Enter] stores the current state, and the
data is saved as a JSON file upon exit.

Author    : Hansol Kang
Created   : 2025-08-01
Copyright : (c) 2025 HobbyLab. All rights reserved.
License   : MIT
"""

import argparse
import sys
import os
import json
import datetime

from loguru import logger
import rbpodo as rb


def _main(address, port):
    data_channel = rb.CobotData(address, port)
    collected = []

    logger.info("Interactive joint trace recording started.")

    try:
        while True:
            print("👉 Press [Enter] to record the current point. Type 'q' to quit and save.")
            user_input = input()
            if user_input.strip().lower() == "q":
                break

            data = data_channel.request_data()
            entry = {
                "jnt_ang": data.sdata.jnt_ang.astype(float).tolist(),
                "tcp_pos": data.sdata.tcp_pos.astype(float).tolist(),
            }
            collected.append(entry)
            logger.success(f"Recorded point #{len(collected)}")
    except KeyboardInterrupt:
        logger.warning("KeyboardInterrupt detected. Saving data before exit...")
    finally:
        if collected:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            base_dir = os.path.dirname(os.path.abspath(__file__))
            save_dir = os.path.join(base_dir, "joint_capture")
            os.makedirs(save_dir, exist_ok=True)

            filename = os.path.join(save_dir, f"joint_trace_{timestamp}.json")
            with open(filename, "w") as f:
                json.dump(collected, f, indent=2)

            logger.info(f"Saved {len(collected)} entries to {filename}")
        else:
            logger.info("No data was recorded. Exiting without saving.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'SUCCESS'],
        type=str.upper,
        help='Set the logging level'
    )
    parser.add_argument(
        '--address',
        default='10.0.2.7',
        help='Set robot IP address (default: 10.0.2.7)'
    )
    parser.add_argument(
        '--port',
        default=5001,
        type=int,
        help='Set robot data port (default: 5001)'
    )
    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stdout, level=args.log_level)

    _main(args.address, args.port)
