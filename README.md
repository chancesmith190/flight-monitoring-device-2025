# Flight Monitoring Device 2025

Flight monitoring system for MSU Rocketry's Spartacus MK III rocket at IREC 2025.

## Overview

Collects and transmits flight data:
- Acceleration (MPU6050)
- Altitude and temperature (MPL3115A2)
- GPS coordinates
- Air brake control at 8000ft

## Project Structure

```
flight-monitoring-device-2025/
├── raspberry-pi/           # Onboard flight computer code
│   ├── air.py             # Main flight control loop
│   ├── sensors.py         # Sensor interface class
│   ├── airbrakes.py       # Air brake servo controller
│   └── adafruit_gps.py    # GPS library
└── flight-dashboard/       # Ground station dashboard
    ├── backend/           # Flask API server
    │   └── server.py
    └── frontend/          # React web interface
        └── src/
```

## Hardware Requirements

### Raspberry Pi Components
- Raspberry Pi
- MPU6050 accelerometer
- MPL3115A2 pressure sensor
- Adafruit GPS module
- Servo motor for air brakes
- Serial radio for data transmission

### Ground Station
- Computer for dashboard
- Radio receiver (XBee devices)

## Installation

### Raspberry Pi Setup

1. Install dependencies:
   ```bash
   cd raspberry-pi
   python3 -m venv env
   source env/bin/activate
   pip install adafruit-circuitpython-mpu6050 adafruit-circuitpython-mpl3115a2 adafruit-circuitpython-gps
   ```

2. Connect hardware:
   - Sensors via I2C
   - Servo to GPIO pin 18
   - GPS to UART
   - Radio to USB

3. Run the flight system:
   ```bash
   python air.py
   ```

### Dashboard Setup

1. Start backend:
   ```bash
   cd flight-dashboard/backend
   pip install flask flask-cors pyserial
   python server.py
   ```

2. Start frontend:
   ```bash
   cd flight-dashboard/frontend
   npm install
   npm start
   ```

3. Open dashboard at `http://localhost:3000`

## Flight Sequence

1. Armed - System ready
2. Liftoff - Detected at 1000ft or high acceleration
3. Air brakes open and close at 8000ft
4. Apogee - Peak altitude detected
5. Descent
6. Landing

## Data Format

The system transmits data arrays via serial:
```python
[accX, accY, accZ, altitude, temperature, latitude, longitude]
# Example: [1.2, -0.5, 9.8, 8543.2, 25.6, 40.7128, -74.0060]
```

## Dashboard Features

- Real-time graphs
- Flight stage tracking
- GPS mapping
- Raw data view
- Sensor status

## Configuration

### Serial Ports
Update serial port in `backend/server.py`:
```python
SERIAL_PORT = "/dev/tty.usbserial-A10NX6XN"  # Mac
# or
SERIAL_PORT = "/dev/ttyUSB0"  # Raspberry Pi/Linux
```

### Air Brake Settings
Modify deployment altitude in `raspberry-pi/air.py`:
```python
if altitude >= 8000:  # Change deployment altitude here
    servo.open()
    servo.close()
```

### Sensor Calibration
Update sea level pressure in `sensors.py`:
```python
self.mpl.sealevel_pressure = 1022.5  # Current pressure at launch site
```

## Data Logging

Flight data is saved to:
- `data.csv` on Raspberry Pi
- `flight_log.txt` for system logs
- Dashboard displays real-time data

## Troubleshooting

### Common Issues
- No serial connection: Check cable and port
- GPS no fix: Wait for satellites outdoors
- Sensor errors: Check I2C connections
- Air brakes not moving: Check servo power

## IREC 2025

MSU Rocketry team rocket: Spartacus MK III
Target altitude: 10,000 feet
