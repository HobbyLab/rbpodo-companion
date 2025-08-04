# Examples
## List of Examples
> [!WARNING]
> Ensure the robot is in a safe state before running any scripts.

### `joint_trajectory_test.py`
Demonstrates two types of joint trajectory control:
- `move_servo_j`: smooth streaming control.
- `move_j`: discrete planning control (more jerky).
Highlights the difference in motion smoothness and responsiveness.

```bash
python joint_trajectory_test.py
```

### `record_joint_data.py`
Provides an interactive CLI tool to manually record joint angles and TCP positions.  
Each time you press `[Enter]`, the current state is saved.  
Press `q` or `Ctrl+C` to stop and export the collected data to a `.json` file.

```bash
python record_joint_data.py
```

### `replay_jb2.py`

Replays a previously recorded joint trajectory using `move_jb2_*` commands.
The entire motion is queued and executed smoothly via the JB2 interface.

```bash
python replay_jb2.py --json path/to/your_record.json
```