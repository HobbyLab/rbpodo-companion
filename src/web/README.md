
# Web Interface

**Cobot Web Interface** is a lightweight FastAPI-based backend for controlling and monitoring collaborative robots.  
It provides both a REST API (with built-in Swagger UI) and a real-time WebSocket streaming interface for joint visualization.

## 🚀 Run the Server

Start the FastAPI server with:

```bash
python run.py --address <YOUR_ROBOT_IP>
```
* `--address`: Robot IP address (default: `10.0.2.7`)
* `--port`: Server port (default: `10101`)

## 🧪 Swagger UI for API Testing
Once the server is running, open:
```
http://localhost:10101/docs
```
This opens the built-in **Swagger UI**, where you can:

* View available API endpoints
* Send basic control or query commands
* Test your connection to the robot

> [!WARNING]
> Swagger UI is **under development** — Not all endpoints are fully implemented yet.


## 📈 Joint Trace: Real-Time Visualization
To monitor robot joint angles in real time, open:
```
http://localhost:10101
```
This loads the **Joint Trace** viewer, which displays live charts of the robot's joint positions (J0–J5) via WebSocket.

![Joint Trace Viewer](/docs/imgs/joint_trace_viewer.gif)