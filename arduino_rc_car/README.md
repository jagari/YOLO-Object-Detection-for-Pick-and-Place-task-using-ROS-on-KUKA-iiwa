# Arduino RC Car with Robot Arm - Pick and Place System

## 프로젝트 개요 (Project Overview)

이 프로젝트는 KUKA iiwa 상업용 로봇 대신 **Arduino로 제어하는 로봇 팔을 장착한 무선 RC 자동차**를 사용하여 화물을 운반하고 픽앤플레이스 작업을 수행하는 시스템입니다.

This project adapts the YOLO-based pick-and-place system to use an **Arduino-controlled robot arm mounted on an RC car** instead of the commercial KUKA iiwa robot, for autonomous cargo transportation and pick-and-place operations.

### 주요 특징 (Key Features)

- ✅ **YOLO 객체 인식**: YOLOv4를 사용한 실시간 물체 감지
- ✅ **색상 영역 인식**: HSV 기반 색상 분할로 배치 위치 감지
- ✅ **4륜 RC 카**: 전후좌우 이동 가능한 RC 카 제어
- ✅ **4자유도 로봇 팔**: 서보 모터 기반 로봇 팔과 그리퍼
- ✅ **독립 실행형**: ROS 없이 Python과 Arduino로 구동
- ✅ **저비용**: 총 제작 비용 $200-400

---

- ✅ **YOLO Object Detection**: Real-time object detection using YOLOv4
- ✅ **Color Region Detection**: HSV-based color segmentation for placement zones
- ✅ **4-Wheel RC Car**: Omnidirectional RC car control
- ✅ **4-DOF Robot Arm**: Servo-based arm with gripper
- ✅ **Standalone System**: Runs on Python and Arduino without ROS
- ✅ **Low Cost**: Total build cost $200-400

## 빠른 시작 (Quick Start)

### 1. 필요한 하드웨어 (Hardware Requirements)

핵심 부품:
- Arduino Mega 2560
- L298N 모터 드라이버 x2
- DC 모터 x4 (RC 카 바퀴용)
- 서보 모터 x5 (로봇 팔용)
- 7.4V LiPo 배터리
- USB 웹캠

자세한 부품 목록: [`docs/BOM.md`](docs/BOM.md)

---

Core components:
- Arduino Mega 2560
- L298N Motor Driver x2
- DC Motors x4 (for wheels)
- Servo Motors x5 (for arm)
- 7.4V LiPo Battery
- USB Webcam

Full parts list: [`docs/BOM.md`](docs/BOM.md)

### 2. 소프트웨어 설치 (Software Installation)

```bash
# Python 패키지 설치
cd python_control
pip install -r requirements.txt

# Arduino 펌웨어 업로드
# Arduino IDE에서 arduino_code/rc_car_robot_arm.ino 파일을 열고 업로드
```

### 3. 하드웨어 조립 (Hardware Assembly)

배선 가이드: [`docs/WIRING.md`](docs/WIRING.md)

Wiring guide: [`docs/WIRING.md`](docs/WIRING.md)

### 4. 실행 (Run)

```bash
cd python_control

# 기본 테스트
python arduino_interface.py

# YOLO 픽앤플레이스 실행
python yolo_arduino_controller.py
```

## 프로젝트 구조 (Project Structure)

```
arduino_rc_car/
├── arduino_code/
│   └── rc_car_robot_arm.ino      # Arduino 펌웨어
├── python_control/
│   ├── arduino_interface.py       # Arduino 통신 인터페이스
│   ├── yolo_arduino_controller.py # YOLO 통합 메인 컨트롤러
│   └── requirements.txt           # Python 의존성
├── docs/
│   ├── README.md                  # 상세 문서
│   ├── BOM.md                     # 부품 목록
│   └── WIRING.md                  # 배선 다이어그램
└── README.md                      # 이 파일
```

## 시스템 아키텍처 (System Architecture)

```
┌──────────────┐
│   컴퓨터      │
│  (PC/Laptop) │
│              │
│ ┌──────────┐ │
│ │  Camera  │ │  ← 웹캠으로 물체 인식
│ └──────────┘ │
│              │
│ ┌──────────┐ │
│ │   YOLO   │ │  ← 물체 감지
│ └──────────┘ │
│              │
│ ┌──────────┐ │
│ │  Python  │ │  ← 제어 로직
│ │  Control │ │
│ └──────────┘ │
└──────┬───────┘
       │ USB/Serial
       │
┌──────▼───────┐
│   Arduino    │  ← 모터/서보 제어
│   Mega 2560  │
└──────┬───────┘
       │
   ┌───┴────┐
   │        │
┌──▼──┐  ┌─▼────┐
│모터  │  │서보  │
│제어  │  │제어  │
└──┬──┘  └─┬────┘
   │        │
┌──▼──┐  ┌─▼────┐
│RC카 │  │로봇팔│
└─────┘  └──────┘
```

## 기능 (Features)

### RC 카 제어 (RC Car Control)
- 전진/후진 (Forward/Backward)
- 좌회전/우회전 (Turn Left/Right)
- 측면 이동 (Strafe - mecanum wheel)
- 속도 제어 (Speed control)

### 로봇 팔 제어 (Robot Arm Control)
- 4자유도 관절 제어 (4-DOF joint control)
- 그리퍼 열기/닫기 (Gripper open/close)
- 사전 정의된 포즈 (Predefined poses)
  - Home 위치
  - Pick 위치
  - Place 위치

### 비전 시스템 (Vision System)
- YOLO 물체 감지 (Object detection)
- 색상 영역 감지 (Color region detection)
- 실시간 처리 (Real-time processing)

## 지원 객체 (Supported Objects)

- `cir` - 원형 (Circle)
- `hex` - 육각형 (Hexagon)
- `rec` - 직사각형 (Rectangle)
- `rng` - 링/도넛 (Ring)
- `slt` - 별 (Star)
- `sqr` - 정사각형 (Square)

## 색상 영역 (Color Regions)

- `R` - 빨강 (Red)
- `B` - 파랑 (Blue)
- `Y` - 노랑 (Yellow)

## 사용 예시 (Usage Examples)

### 예제 1: 수동 제어 (Manual Control)

```python
from arduino_interface import ArduinoRCCar

car = ArduinoRCCar(port='/dev/ttyACM0')
car.connect()

# 전진 1초
car.move_forward(150, duration=1.0)

# 좌회전
car.turn_left(150, duration=0.5)

# 물체 잡기
car.pick_position()
car.grip()

# 물체 놓기
car.place_position()
car.release()

car.disconnect()
```

### 예제 2: 자동 픽앤플레이스 (Automatic Pick and Place)

```python
from yolo_arduino_controller import YOLOArduinoController

controller = YOLOArduinoController(
    arduino_port="/dev/ttyACM0"
)

controller.initialize()

# 작업 정의: (물체, 색상)
tasks = [
    ('cir', 'R'),  # 원형을 빨간 영역에
    ('sqr', 'B'),  # 사각형을 파란 영역에
    ('hex', 'Y'),  # 육각형을 노란 영역에
]

controller.run_pick_and_place_task(tasks)
controller.cleanup()
```

## 문서 (Documentation)

자세한 문서는 [`docs/README.md`](docs/README.md)를 참조하세요.

For detailed documentation, see [`docs/README.md`](docs/README.md).

### 문서 목록 (Documentation Files)

- 📖 [상세 가이드](docs/README.md) - 설치, 사용법, 문제 해결
- 🛒 [부품 목록](docs/BOM.md) - 필요한 모든 부품과 가격
- 🔌 [배선 가이드](docs/WIRING.md) - 상세한 배선 다이어그램

---

- 📖 [Detailed Guide](docs/README.md) - Installation, usage, troubleshooting
- 🛒 [Bill of Materials](docs/BOM.md) - Complete parts list with prices
- 🔌 [Wiring Guide](docs/WIRING.md) - Detailed wiring diagrams

## 비용 (Cost)

- **최소**: ~$200 USD (기본 구성)
- **권장**: ~$285 USD (표준 구성)
- **프리미엄**: ~$395 USD (고급 부품)

---

- **Minimum**: ~$200 USD (basic build)
- **Recommended**: ~$285 USD (standard build)
- **Premium**: ~$395 USD (high-end components)

## 안전 주의사항 (Safety Notes)

⚠️ **중요** / **Important**:
- 배터리 극성 확인 (Check battery polarity)
- 작동 중 손가락 주의 (Keep fingers away from moving parts)
- 충분한 작업 공간 확보 (Use in clear, safe area)
- 테스트는 낮은 속도로 시작 (Start testing at low speed)

## 문제 해결 (Troubleshooting)

### Arduino 연결 안됨 (Can't connect to Arduino)
- USB 케이블 확인 (Check USB cable)
- 올바른 COM 포트 선택 (Select correct COM port)
- Arduino 전원 확인 (Check Arduino power)

### 모터가 작동하지 않음 (Motors not working)
- 배선 확인 (Check wiring)
- 배터리 충전 상태 확인 (Check battery charge)
- L298N 전원 LED 확인 (Check L298N power LED)

### 서보가 떨림 (Servos jittering)
- 5V 전원 안정화 (Stabilize 5V power)
- 커패시터 추가 (Add capacitor)
- 서보 전원 분리 (Separate servo power)

더 많은 문제 해결 방법: [`docs/README.md`](docs/README.md#troubleshooting)

More troubleshooting: [`docs/README.md`](docs/README.md#troubleshooting)

## 원본 프로젝트 (Original Project)

이 프로젝트는 다음 프로젝트를 기반으로 합니다:

This project is based on:

[YOLO Object Detection for Pick and Place task using ROS on KUKA iiwa](https://github.com/jagari/YOLO-Object-Detection-for-Pick-and-Place-task-using-ROS-on-KUKA-iiwa)

### 주요 차이점 (Key Differences)

| 항목 | 원본 프로젝트 | 이 프로젝트 |
|------|-------------|------------|
| 로봇 | KUKA iiwa (상업용) | Arduino + 서보 |
| 통신 | ROS | Serial (USB/Bluetooth) |
| 플랫폼 | 고정형 워크스테이션 | 이동식 RC 카 |
| 비용 | ~$50,000+ | ~$200-400 |
| 프로그래밍 | C++ + ROS | Python + Arduino |

---

| Feature | Original | This Project |
|---------|----------|--------------|
| Robot | KUKA iiwa (commercial) | Arduino + Servos |
| Communication | ROS | Serial (USB/Bluetooth) |
| Platform | Fixed workstation | Mobile RC car |
| Cost | ~$50,000+ | ~$200-400 |
| Programming | C++ + ROS | Python + Arduino |

## 향후 개선 사항 (Future Enhancements)

- [ ] Bluetooth 무선 제어 (Bluetooth wireless control)
- [ ] 초음파 센서로 장애물 회피 (Ultrasonic obstacle avoidance)
- [ ] IMU로 안정성 향상 (IMU for stability)
- [ ] 폐루프 서보 제어 (Closed-loop servo control)
- [ ] 음성 제어 인터페이스 (Voice control interface)
- [ ] 경로 계획 알고리즘 (Path planning algorithms)
- [ ] 라즈베리파이 통합 (Raspberry Pi integration)

## 기여 (Contributing)

기여를 환영합니다! Pull Request를 보내주세요.

Contributions are welcome! Please submit pull requests.

## 라이선스 (License)

원본 프로젝트의 라이선스를 따릅니다.

Same license as the original project (see main repository LICENSE).

## 참고 자료 (References)

- [Arduino Documentation](https://www.arduino.cc/reference/en/)
- [OpenCV Python Tutorial](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [YOLOv4 Paper](https://arxiv.org/abs/2004.10934)
- [Servo Library](https://www.arduino.cc/reference/en/libraries/servo/)

## 지원 (Support)

질문이나 문제가 있으시면:
1. 문서를 먼저 확인하세요 ([`docs/README.md`](docs/README.md))
2. GitHub Issues에 문의하세요
3. 원본 프로젝트 문서를 참조하세요

---

For questions or issues:
1. Check the documentation first ([`docs/README.md`](docs/README.md))
2. Open an issue on GitHub
3. Refer to the original project documentation

## 감사의 글 (Acknowledgments)

원본 KUKA iiwa 프로젝트를 만들어주신 분들께 감사드립니다.

Thanks to the creators of the original KUKA iiwa project.

---

**제작일 (Created)**: 2024
**언어 (Languages)**: Korean (한국어) / English
**플랫폼 (Platform)**: Arduino Mega 2560 + Python
