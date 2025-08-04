"""
Replay recorded joint trajectory using JB2 motion

This script replays a joint trajectory stored in a JSON file using move_jb2_* commands.
The trajectory is sent all at once and executed smoothly using the JB2 interface.

Author    : Hansol Kang
Created   : 2025-08-01
Copyright : (c) 2025 HobbyLab. All rights reserved.
License   : MIT
"""

import argparse
import sys
import json
import numpy as np
from loguru import logger

import rbpodo as rb


def _main(address, port, json_path):
    robot = rb.Cobot(address, port)
    rc = rb.ResponseCollector()

    try:
        logger.warning("Setting operation mode to Real")
        robot.set_operation_mode(rc, rb.OperationMode.Real)
        rc = rc.error().throw_if_not_empty()

        # -----------------------------
        # Load joint trajectory data
        # -----------------------------
        logger.info(f"Loading joint data from: {json_path}")
        with open(json_path, 'r') as f:
            data = json.load(f)

        logger.info(f"Loaded {len(data)} trajectory points")

        # -----------------------------
        # JB2 Motion Execution
        # -----------------------------
        logger.info("Sending joint data to JB2 queue")
        robot.move_jb2_clear(rc)
        for idx, point in enumerate(data):
            joint_angles = np.array(point["jnt_ang"])
            blend_rate = point["blend_rate"]
            logger.debug(f"[Step {idx+1}] joint = {joint_angles}")
            robot.move_jb2_add(rc, joint_angles, 100, 100, blend_rate)
        robot.flush(rc)

        logger.info("Starting JB2 motion")
        robot.move_jb2_run(rc)
        if robot.wait_for_move_started(rc, 0.5).is_success():
            robot.wait_for_move_finished(rc)
        rc = rc.error().throw_if_not_empty()

        logger.success("Motion completed successfully.")

    except Exception as e:
        logger.error(f"Error occurred: {e}")


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
        default=5000,
        type=int,
        help='Set robot port (default: 5000)'
    )
    parser.add_argument(
        '--json',
        required=True,
        help='Path to joint angle JSON file'
    )
    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stdout, level=args.log_level)

    _main(args.address, args.port, args.json)
