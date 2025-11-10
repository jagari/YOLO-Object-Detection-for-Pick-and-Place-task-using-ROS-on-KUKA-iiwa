[[Video]](https://www.youtube.com/watch?v=7nD9INKZuLk)
## YOLO-Object-Detection-for-Pick-and-Place-task-using-ROS-on-KUKA-iiwa
Robots use computer vision in many operations. In this repository, we are going to address one of these operations, pick and place, which is the most widely used in production lines and assembly processes. The aim of this project is to select 3 objects out of 6 objects in robot work environment, and place them in specific-colored regions, so that each object will be placed in colored region initially specified by the operator.

<p align="left"><img src="https://user-images.githubusercontent.com/90580636/162748319-1fc91285-5d85-4501-b2fd-9bae62f6d7af.png" width="600" height="280" /></p>


### The challenges of this project go as follows:
- **Object Detection**: YOLOv4 
- **Box Detection**: Color Segmentation in HSI and Morphology operations
- **Pick and Place**: Object center and orientation and Box center and orientation
- **Localization w.r.t Robot Base**: Eye-In-Hand Camera Calibration and Transformations
- **Hardware Implementation**: KUKA iiwa and ROS

### Workplace Setup (Objects)
<p align="left"><img src="https://user-images.githubusercontent.com/90580636/162749872-b8e22f37-6889-4952-b363-8e2a41be1263.png" width="400" height="280" /></p>

**Dataset** is attached above. 

Labelling is done on [roboflow](https://roboflow.com/)

### Dataset preprocessing and augmentations 
<p align="left"><img src="https://user-images.githubusercontent.com/90580636/162843034-79c7fc70-a615-4cde-a105-39089ea2c5f3.png" width="500" height="280" /></p>

### YOLO Model Testing for Object Detection
- Test1
<p align="left"><img src="https://user-images.githubusercontent.com/90580636/162844006-b72dc54b-8f00-44b7-b4e8-284ade53c485.gif" width="250" height="140" /></p>
                                    
Problems arise due to illumination change, camera orientation, false positive results (detect the gripper as an object, detect background as an object).  

Solution: Applying thresholding on detection confidence score.

- Test2
<p align="left"><img src="https://user-images.githubusercontent.com/90580636/162844601-5b23ccc4-eaec-4402-b841-1047a62ac1ee.gif" width="250" height="140" /></p>

### Object Center and Orientation 
<p align="left"><img src="https://user-images.githubusercontent.com/90580636/162844828-a24be0e2-37f9-4fe2-b5c4-9c12115d80aa.png" width="500" height="200" /></p>

### Box Detection
    - Color Segmentation in HSI
    - Morphology operations
    - Box center and orientation

<p align="left"><img src="https://user-images.githubusercontent.com/90580636/162845161-c5263d62-3fb4-417c-a40c-b67fa56fac89.png" width="1000" height="200" /></p>

### Localization w.r.t Robot Base
    - Camera Intrinsics
    - Eye-In-Hand Camera Calibration
    - Transformations

<p align="left"><img src="https://user-images.githubusercontent.com/90580636/162845702-f06cb3eb-bd89-42bc-8fab-6a26bfeab38c.png" width="400" height="250" /></p>

### Hardware Implementation
   KUKA iiwa robot [iiwa_stack](https://github.com/IFL-CAMP/iiwa_stack) 
   
### Demo
   Full video is attached [Demo](https://www.youtube.com/watch?v=7nD9INKZuLk)
   <p align="left"><img src="https://user-images.githubusercontent.com/90580636/162852885-e3f6555a-0ca9-4b32-9a09-b5625bc02146.gif" width="400" height="300" /></p>

---

## 🚗 Arduino RC Car Adaptation

**새 프로젝트!** / **New Project!**

이 저장소에 **Arduino 기반 RC 카 버전**이 추가되었습니다! 상업용 KUKA iiwa 로봇 대신 저비용으로 제작할 수 있는 Arduino 제어 로봇 팔을 사용합니다.

An **Arduino-based RC car version** has been added to this repository! Use a low-cost Arduino-controlled robot arm instead of the commercial KUKA iiwa robot.

### Key Features
- 💰 **Low Cost**: $200-400 USD (vs $50,000+ for KUKA)
- 🤖 **Arduino Mega 2560**: Servo-based 4-DOF robot arm
- 🚗 **Mobile Platform**: 4-wheel RC car for cargo transport
- 🎯 **Same Vision System**: Uses YOLOv4 object detection
- 🔌 **No ROS Required**: Pure Python + Arduino
- 📚 **Complete Documentation**: Full build guide, wiring diagrams, BOM

### Quick Start

```bash
# Navigate to Arduino RC Car project
cd arduino_rc_car

# See detailed README
cat README.md

# Install Python dependencies
cd python_control
pip install -r requirements.txt

# Upload Arduino firmware (use Arduino IDE)
# Open: arduino_code/rc_car_robot_arm.ino

# Run the system
python yolo_arduino_controller.py
```

### Documentation
- 📖 [Arduino RC Car README](arduino_rc_car/README.md) - Main documentation (한국어/English)
- 🛒 [Bill of Materials](arduino_rc_car/docs/BOM.md) - Complete parts list
- 🔌 [Wiring Guide](arduino_rc_car/docs/WIRING.md) - Detailed wiring diagrams
- 📚 [Full Guide](arduino_rc_car/docs/README.md) - Installation, usage, troubleshooting

### Comparison

| Feature | KUKA iiwa (Original) | Arduino RC Car (New) |
|---------|---------------------|---------------------|
| **Cost** | ~$50,000+ | ~$200-400 |
| **Platform** | Fixed workstation | Mobile RC car |
| **Control** | ROS + C++ | Python + Arduino |
| **Robot Arm** | 7-DOF industrial | 4-DOF servo-based |
| **Setup Difficulty** | High | Moderate |
| **Portability** | Fixed installation | Portable |
| **Learning Curve** | Steep | Gentle |
| **Ideal For** | Research labs, Industry | Education, Hobbyists |

**Perfect for**: Students, hobbyists, educators, and anyone wanting to learn robotics without breaking the bank!

---
