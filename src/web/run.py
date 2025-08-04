"""
Entry Point for FastAPI Server

This script launches the FastAPI-based server for robot communication and monitoring.
Robot address and server port can be customized via CLI arguments.

Author    : Hansol Kang
Created   : 2025-08-01
Copyright : (c) 2025 HobbyLab. All rights reserved.
License   : MIT
"""

import uvicorn
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", default="10.0.2.7", help="Robot address (default: 10.0.2.7)")
    parser.add_argument("--port", type=int, default=10101, help="Port to run the server on (default: 10101)")
    args = parser.parse_args()

    os.environ["ROBOT_ADDR"] = args.address
    uvicorn.run("main:app", host="0.0.0.0", port=args.port, reload=False)
