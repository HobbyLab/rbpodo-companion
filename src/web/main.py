"""
FastAPI Application for Robot Web Interface

This module defines the FastAPI app, serving both API endpoints and static files.
It includes a WebSocket interface for streaming robot data such as joint angles.

Author    : Hansol Kang
Created   : 2025-08-01
Copyright : (c) 2025 HobbyLab. All rights reserved.
License   : MIT
"""

from pathlib import Path
import asyncio
import os
import logging

import orjson
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import rbpodo as rb  # Custom robot SDK

# Robot IP address from environment variable or default
ROBOT_ADDRESS = os.getenv("ROBOT_ADDR", "10.0.2.7")

# Robot control and data interface
robot = rb.asyncio.Cobot(ROBOT_ADDRESS)
robot_data = rb.asyncio.CobotData(ROBOT_ADDRESS)

# WebSocket client set
clients = set()
uvicorn_logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start data broadcast loop on app startup
    asyncio.create_task(data_broadcast_loop())
    yield

app = FastAPI(
    title="Cobot Web Interface",
    lifespan=lifespan,
)

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving (frontend)
BASE_DIR = Path(__file__).resolve().parent
WEB_ROOT = BASE_DIR
app.mount("/", StaticFiles(directory=WEB_ROOT, html=True), name="static")

# Serve index.html at root path
@app.get("/")
async def serve_root():
    return FileResponse(WEB_ROOT / "index.html")

# WebSocket endpoint for real-time joint data streaming
@app.websocket("/ws/data_stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    uvicorn_logger.info(f"Client connected. Total: {len(clients)}")

    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        clients.discard(websocket)
        uvicorn_logger.warning(f"Client disconnected. Remaining: {len(clients)}")

# Broadcast robot state to all connected clients
async def data_broadcast_loop():
    while True:
        if clients:
            data = await robot_data.request_data()
            payload = {
                "jnt_ang": list(data.sdata.jnt_ang),
                "jnt_ref": list(data.sdata.jnt_ref),
                "tcp_ref": list(data.sdata.tcp_ref),
                "tcp_pos": list(data.sdata.tcp_pos),
                "is_freedrive_mode": bool(data.sdata.is_freedrive_mode),
                "real_vs_simulation": "Sim" if data.sdata.real_vs_simulation_mode == 1 else "Real",
            }
            message = orjson.dumps(payload, option=orjson.OPT_SERIALIZE_NUMPY).decode()

            disconnected = set()
            for ws in clients:
                try:
                    await ws.send_text(message)
                except WebSocketDisconnect:
                    disconnected.add(ws)
            clients.difference_update(disconnected)

        await asyncio.sleep(0.2)  # Broadcast at 5 Hz
