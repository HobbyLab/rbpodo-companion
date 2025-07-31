"""
Compare move_j vs move_servo_j Trajectory Control

This script demonstrates the difference in motion behavior when controlling trajectory
via move_j (discrete planning) vs move_servo_j (continuous streaming).

Author    : Hansol Kang
Created   : 2025-07-31
Copyright : (c) 2025 HobbyLab. All rights reserved.
License   : MIT
"""

import argparse
import sys
import os
import time

import numpy as np
from loguru import logger

import rbpodo as rb

HOME_POSE = np.zeros(6)
TARGET_POSE = [
    np.array([i, 0, -i * 0.4, 0, 0, i * 0.6])
    for i in range(0, 100, 1)
]

TOTAL_DURATION = 10.0
STEP_DURATION = TOTAL_DURATION / len(TARGET_POSE)

def _main(address, port):
    robot = rb.Cobot(address, port)
    rc = rb.ResponseCollector()

    try:
        logger.warning("Setting operation mode to Real")
        robot.set_operation_mode(rc, rb.OperationMode.Real)
        rc = rc.error().throw_if_not_empty()

        logger.info("Moving to home pose")
        robot.move_j(rc, HOME_POSE, 60, 80)
        rc = rc.error().throw_if_not_empty()
        if robot.wait_for_move_started(rc, 0.5).is_success():
            robot.wait_for_move_finished(rc)
        rc = rc.error().throw_if_not_empty()

        # -----------------------------
        # Phase 1: move_servo_j
        # -----------------------------
        logger.info("Starting Phase 1: move_servo_j")
        robot.disable_waiting_ack(rc)
        for idx, joint in enumerate(TARGET_POSE):
            logger.debug(f"[Phase 1 | Step {idx+1}] joint = {joint}")
            robot.move_servo_j(rc, joint, STEP_DURATION, 0.1, 1.0, 1.0)
            time.sleep(STEP_DURATION)
        robot.move_speed_j(rc, np.zeros(6), 1, 0.1, 1.0, 0.2)
        robot.enable_waiting_ack(rc)
        robot.wait_for_move_finished(rc)
        rc.clear()

        logger.info("Returning to home pose after Phase 1")
        robot.move_j(rc, HOME_POSE, 50, 100)
        if robot.wait_for_move_started(rc, 0.5).is_success():
            robot.wait_for_move_finished(rc)
        rc = rc.error().throw_if_not_empty()

        # -----------------------------
        # Phase 2: move_j (Motion is shaky)
        # -----------------------------
        logger.warning("Starting Phase 2: move_j(Motion is shaky)")
        for idx, joint in enumerate(TARGET_POSE):
            logger.debug(f"[Phase 2 | Step {idx+1}] joint = {joint}")
            robot.move_j(rc, joint, 10, 300)
            if robot.wait_for_move_started(rc, 0.5).is_success():
                robot.wait_for_move_finished(rc)
            rc = rc.error().throw_if_not_empty()
        robot.move_speed_j(rc, np.zeros(6), 1, 0.1, 1.0, 0.2)
        robot.wait_for_move_finished(rc)
        rc.clear()

        logger.info("Returning to home pose after Phase 2")
        robot.move_j(rc, HOME_POSE, 50, 100)
        if robot.wait_for_move_started(rc, 0.5).is_success():
            robot.wait_for_move_finished(rc)
        rc = rc.error().throw_if_not_empty()

    finally:
        logger.success("Finished all phases. Exiting...")


if __name__ == '__main__':
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
        help='Set robot port (default: 5000)'
    )
    args = parser.parse_args()

    logger.remove()
    logger.add(sys.stdout, level=args.log_level)

    _main(args.address, args.port)