# Network Connection Monitor

A Python application for monitoring internet connection status and logging network connectivity interruptions. This tool also displays real-time ping data, including periods of disconnection, on a live graph.

## Features

- **Real-time Monitoring**: Continuously checks internet connection status and logs any connection failures.
- **Graphical Display**: Displays ping times on a graph, with visual indicators for failed connection attempts (marked by bars at `-1`).
- **Connection Log**: Logs details about network disconnections, including the timestamp, network SSID, and router IP.
- **Customizable Interface**: Allows for theme selection, including a dark mode for nighttime viewing.

## Requirements

- **Python 3.x**
- **Libraries**:
  - `ping3` - for pinging external servers
  - `matplotlib` - for plotting ping data in real time
  - `psutil` - for retrieving network information
  - `tkinter` - for GUI components (usually included with Python)
  
  Install dependencies with:
  ```bash
  pip install ping3 matplotlib psutil
