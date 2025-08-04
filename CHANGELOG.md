## v0.2.0 (2025-08-04)

### refactor

- **main.py**: rename cobot variable to robot

### ✨ Features

- apply blend rate from config and fix mode to real
- **replay_jb2_from_json.py**: add JB2 motion replay script using recorded joint angles
- **record_joint_data.py**: add blend_rate field to recorded joint trace JSON
- add interactive joint/tcp data recorder
- add web-based joint trace viewer
- add joint trajectory example

### 🐛 Fixes

- resolved joint trace viewer issue and corrected graph legend
