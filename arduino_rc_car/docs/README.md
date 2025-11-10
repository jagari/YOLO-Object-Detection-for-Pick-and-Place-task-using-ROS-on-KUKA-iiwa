# Arduino RC Car with Robot Arm - Pick and Place Project

## Overview

This project adapts the YOLO-based pick-and-place system to work with an Arduino-controlled RC car and robot arm, instead of the commercial KUKA iiwa robot. The system can autonomously detect objects using computer vision, navigate to them, pick them up, and place them in designated colored regions.

## Features

- **Autonomous Object Detection**: YOLOv4-based object recognition
- **Color Region Detection**: HSV-based color segmentation for placement zones
- **RC Car Control**: 4-wheel drive with directional control
- **4-DOF Robot Arm**: Servo-based arm with gripper
- **Wireless Operation**: Serial communication via Bluetooth (optional)
- **Standalone System**: No ROS required - pure Python and Arduino

## Hardware Requirements

### Electronics
- **Arduino Mega 2560** (recommended for multiple servos and PWM channels)
- **L298N Motor Driver Module** x2 (for 4 DC motors)
- **Servo Motors** x5:
  - MG996R or similar (for Base, Shoulder, Elbow)
  - SG90 or similar (for Wrist, Gripper)
- **DC Motors** x4 (for RC car wheels)
- **USB Camera** or **Raspberry Pi Camera** (for vision)
- **Power Supply**:
  - 7.4V 2S LiPo battery (2000-3000mAh) for motors
  - 5V voltage regulator for Arduino and servos
- **Breadboard and jumper wires**

### Optional Components
- **HC-05 Bluetooth Module** (for wireless control)
- **Voltage/Current sensors** (for monitoring)
- **LED indicators**

## Mechanical Components

### RC Car Base
- 4-wheel chassis (20-30cm length recommended)
- Mounting plate for robot arm
- Battery compartment

### Robot Arm
- 4-DOF arm structure
- Gripper mechanism
- Mounting bracket for camera

You can 3D print parts or use:
- Aluminum or acrylic mounting plates
- Standard servo brackets
- Gripper mechanism (3D printed or mechanical)

## Software Requirements

### Python Environment
```bash
# Required Python packages
pip install opencv-python numpy pyserial
```

### Arduino IDE
- Arduino IDE 1.8.x or newer
- Servo library (included with Arduino IDE)

### YOLO Setup
This project uses the existing YOLO configuration from the parent project:
- YOLOv4 weights trained on custom shapes dataset
- Configuration files in `darknet/cfg/`

## System Architecture

```
┌─────────────────┐
│   PC/Laptop     │
│  - YOLO Vision  │
│  - Python Ctrl  │
│  - Camera Input │
└────────┬────────┘
         │ USB/Serial
         │
┌────────▼────────┐
│  Arduino Mega   │
│  - Motor Ctrl   │
│  - Servo Ctrl   │
│  - Serial Comm  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│Motors │ │ Servos  │
│(L298N)│ │(Arm+Grip)│
└───┬───┘ └──┬──────┘
    │        │
┌───▼───┐ ┌──▼──────┐
│RC Car │ │Robot Arm│
│Wheels │ │         │
└───────┘ └─────────┘
```

## Wiring Diagram

### Motor Driver Connections (L298N x2)

#### Driver 1 (Front Motors)
```
Arduino Pin → L298N → Motor
    2       → IN1   → Front Left +
    3       → IN2   → Front Left -
    4       → ENA   → Speed Control FL

    5       → IN3   → Front Right +
    6       → IN4   → Front Right -
    7       → ENB   → Speed Control FR
```

#### Driver 2 (Back Motors)
```
Arduino Pin → L298N → Motor
    8       → IN1   → Back Left +
    9       → IN2   → Back Left -
    10      → ENA   → Speed Control BL

    11      → IN3   → Back Right +
    12      → IN4   → Back Right -
    13      → ENB   → Speed Control BR
```

### Servo Connections
```
Arduino Pin → Servo Function
    22      → Base Rotation
    23      → Shoulder Joint
    24      → Elbow Joint
    25      → Wrist Rotation
    26      → Gripper Open/Close
```

### Power Connections
```
Battery (+7.4V) → Motor Driver VCC
Battery (GND)   → Common Ground
                → Motor Driver GND
                → Arduino GND
                → Servo GND (through 5V regulator)

5V Regulator    → Arduino 5V (if not USB powered)
                → Servo VCC (all servos)
```

**Important**: 
- Never power servos directly from Arduino 5V pin
- Use external 5V power supply or voltage regulator for servos
- Ensure common ground between all components

## Installation

### 1. Hardware Setup

1. **Assemble RC Car Base**
   - Mount motors to chassis
   - Connect wheels
   - Install battery holder

2. **Mount Robot Arm**
   - Secure arm base to car chassis
   - Ensure stable mounting (center of mass)
   - Leave space for electronics

3. **Wire Electronics**
   - Follow wiring diagram above
   - Use cable ties for organization
   - Label wires for debugging

4. **Mount Camera**
   - Position camera at arm end or front of car
   - Ensure clear view of workspace
   - Secure with bracket or mount

### 2. Arduino Setup

1. **Install Arduino IDE**
   ```bash
   # Download from: https://www.arduino.cc/en/software
   ```

2. **Upload Firmware**
   - Open `arduino_rc_car/arduino_code/rc_car_robot_arm.ino`
   - Select Board: "Arduino Mega 2560"
   - Select correct COM port
   - Click Upload

3. **Test Connection**
   - Open Serial Monitor (115200 baud)
   - Type: `PING`
   - Should receive: `PONG`

### 3. Python Environment Setup

1. **Install Dependencies**
   ```bash
   cd arduino_rc_car/python_control
   pip install opencv-python numpy pyserial
   ```

2. **Configure Serial Port**
   - Linux: Usually `/dev/ttyACM0` or `/dev/ttyUSB0`
   - Windows: Check Device Manager for COM port
   - Mac: Usually `/dev/cu.usbmodem*`

3. **Update Configuration**
   Edit `yolo_arduino_controller.py`:
   ```python
   arduino_port = "/dev/ttyACM0"  # Change to your port
   ```

### 4. YOLO Model Setup

Use the existing YOLO configuration from the parent project:
```bash
# Ensure these files exist:
# - darknet/cfg/custom-yolov4-detector.cfg
# - darknet/cfg/coco.data
# - best.weights (trained model)
```

## Usage

### Basic Arduino Control Test

```bash
cd arduino_rc_car/python_control
python arduino_interface.py
```

This will test:
- Forward/backward movement
- Turning left/right
- Arm movement
- Gripper operation

### Full YOLO Pick and Place

```bash
cd arduino_rc_car/python_control
python yolo_arduino_controller.py
```

The system will:
1. Initialize camera and YOLO
2. Connect to Arduino
3. Detect objects (circle, square, hexagon, etc.)
4. Navigate to objects
5. Pick them up
6. Place them in colored regions (Red, Blue, Yellow)

### Custom Tasks

Edit `yolo_arduino_controller.py` to define custom tasks:

```python
tasks = [
    ('cir', 'R'),  # Pick circle, place in red region
    ('sqr', 'B'),  # Pick square, place in blue region
    ('hex', 'Y'),  # Pick hexagon, place in yellow region
]
```

Available object classes:
- `'cir'` - Circle
- `'hex'` - Hexagon
- `'rec'` - Rectangle
- `'rng'` - Ring
- `'slt'` - Star
- `'sqr'` - Square

Available color regions:
- `'R'` - Red
- `'B'` - Blue
- `'Y'` - Yellow

## Command Reference

### Movement Commands
```
FORWARD:speed     - Move forward (speed: 0-255)
BACKWARD:speed    - Move backward
LEFT:speed        - Turn left
RIGHT:speed       - Turn right
STRAFE_LEFT:speed - Strafe left (mecanum wheels)
STRAFE_RIGHT:speed- Strafe right
STOP              - Stop all motors
SPEED:value       - Set default speed
```

### Arm Commands
```
ARM:base,shoulder,elbow,wrist - Set arm joint angles (0-180)
GRIPPER:angle                  - Set gripper angle (0-180)
GRIP                           - Close gripper (angle=0)
RELEASE                        - Open gripper (angle=90)
HOME                           - Move to home position
PICK_POS                       - Move to picking position
PLACE_POS                      - Move to placing position
```

### Status Commands
```
STATUS            - Get current arm positions
PING              - Test connection (returns PONG)
```

## Calibration

### 1. Servo Calibration

Test each servo individually:

```python
from arduino_interface import ArduinoRCCar

car = ArduinoRCCar(port='/dev/ttyACM0')
car.connect()

# Test base rotation
car.set_arm_position(0, 90, 90, 90)    # Base left
car.set_arm_position(180, 90, 90, 90)  # Base right
car.set_arm_position(90, 90, 90, 90)   # Base center
```

Adjust servo positions in Arduino code if needed:
```cpp
#define HOME_BASE 90      // Adjust as needed
#define HOME_SHOULDER 90
#define HOME_ELBOW 90
```

### 2. Camera Calibration

Position the camera to have a clear view of:
- Object detection area (for picking)
- Colored regions (for placing)

Adjust camera:
- Height: 20-40cm above ground
- Angle: Slightly downward (30-45°)
- Focus: Manual focus on workspace

### 3. Color Thresholds

Adjust HSV color ranges in `yolo_arduino_controller.py`:

```python
self.color_regions = {
    'R': {'lower': np.array([0, 100, 100]), 
          'upper': np.array([10, 255, 255])},
    # Adjust values based on lighting conditions
}
```

Use `color_calibration_tool.py` (create if needed) to find optimal values.

### 4. Pick and Place Positions

Adjust arm positions for your specific hardware:

In Arduino code (`rc_car_robot_arm.ino`):
```cpp
#define PICK_SHOULDER 45   // Lower for picking
#define PICK_ELBOW 45

// Test and adjust these values
```

## Troubleshooting

### Connection Issues

**Problem**: `Failed to connect to Arduino`
- Check USB cable connection
- Verify correct COM port
- Check Arduino is powered on
- Try unplugging and reconnecting

**Problem**: `Timeout waiting for response`
- Check baud rate (must be 115200)
- Verify Arduino sketch is uploaded
- Check Serial Monitor works in Arduino IDE

### Motor Issues

**Problem**: Motors not moving
- Check L298N connections
- Verify power supply voltage (7-12V)
- Test motors directly with battery
- Check motor driver enable pins

**Problem**: Motors move but weak
- Increase PWM speed value
- Check battery charge level
- Verify motor driver can handle current

### Servo Issues

**Problem**: Servos jittering
- Check power supply (need stable 5V)
- Add capacitor (100-1000µF) near servo power
- Reduce servo speed in code

**Problem**: Arm can't lift objects
- Use stronger servos (MG996R recommended)
- Reduce arm length
- Lighten gripper mechanism

### Vision Issues

**Problem**: Objects not detected
- Check YOLO model is loaded correctly
- Verify weights file path
- Adjust detection threshold
- Improve lighting conditions

**Problem**: Color regions not detected
- Adjust HSV thresholds
- Ensure good lighting
- Use solid colored markers/regions
- Avoid shadows and reflections

## Performance Tips

1. **Power Management**
   - Use separate power supplies for motors and servos
   - Monitor battery voltage
   - Add low voltage cutoff

2. **Mechanical Stability**
   - Secure all components firmly
   - Balance weight distribution
   - Use dampers to reduce vibration

3. **Software Optimization**
   - Reduce camera resolution for faster processing
   - Adjust YOLO confidence threshold
   - Implement PID control for smoother movement

4. **Vision Improvements**
   - Use better lighting
   - Add camera lens with appropriate focal length
   - Calibrate camera intrinsics

## Safety Considerations

⚠️ **Important Safety Notes**:

1. **Power Safety**
   - Never exceed servo voltage ratings
   - Use proper fuses
   - Avoid short circuits
   - Monitor battery temperature

2. **Mechanical Safety**
   - Keep fingers away from moving parts
   - Use emergency stop button
   - Test in safe, clear area
   - Secure all moving components

3. **Electrical Safety**
   - Double-check polarity before powering
   - Insulate exposed connections
   - Use appropriate wire gauge
   - Keep electronics away from water

## Future Enhancements

Possible improvements:
- Add ultrasonic sensors for obstacle avoidance
- Implement closed-loop servo control
- Add wireless control (Bluetooth/WiFi)
- Improve path planning algorithms
- Add IMU for stability control
- Implement SLAM for navigation
- Add voice control interface

## Contributing

This project is adapted from the KUKA iiwa YOLO pick-and-place project. Contributions are welcome!

## License

Same as parent project (check main repository LICENSE file)

## References

- Original project: [YOLO Object Detection for Pick and Place using ROS on KUKA iiwa](https://github.com/jagari/YOLO-Object-Detection-for-Pick-and-Place-task-using-ROS-on-KUKA-iiwa)
- YOLOv4: [https://github.com/AlexeyAB/darknet](https://github.com/AlexeyAB/darknet)
- Arduino Servo Library: [https://www.arduino.cc/reference/en/libraries/servo/](https://www.arduino.cc/reference/en/libraries/servo/)

## Support

For issues and questions:
1. Check troubleshooting section
2. Review original project documentation
3. Open an issue on GitHub

---

**Note**: This is an educational/hobby project. For production use, consider safety features, error handling, and thorough testing.
