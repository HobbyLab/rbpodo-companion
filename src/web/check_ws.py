"""
WebSocket Test Client for Robot State Streaming

This script connects to the WebSocket server and prints real-time robot state messages.
Useful for verifying that the FastAPI WebSocket endpoint is broadcasting correctly.

Author    : Hansol Kang
Created   : 2025-08-01
Copyright : (c) 2025 HobbyLab. All rights reserved.
License   : MIT
"""

import asyncio
import websockets

async def receive_robot_state():
    uri = "ws://localhost:10101/ws/data_stream"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"Received: {message}")

asyncio.get_event_loop().run_until_complete(receive_robot_state())