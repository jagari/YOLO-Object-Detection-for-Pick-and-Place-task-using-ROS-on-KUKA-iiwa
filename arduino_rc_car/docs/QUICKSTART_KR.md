# 빠른 시작 가이드 (Quick Start Guide)

## Arduino RC Car 로봇 팔 프로젝트

이 가이드는 Arduino RC Car 프로젝트를 빠르게 시작하는 방법을 설명합니다.

### 1단계: 필요한 것 준비하기

#### 하드웨어
- [ ] Arduino Mega 2560
- [ ] L298N 모터 드라이버 2개
- [ ] DC 모터 4개 (RC 카용)
- [ ] 서보 모터 5개 (로봇 팔용)
- [ ] 7.4V LiPo 배터리
- [ ] 5V 전압 레귤레이터 (LM2596)
- [ ] USB 웹캠
- [ ] 점퍼 와이어, 브레드보드

전체 부품 목록: [docs/BOM.md](docs/BOM.md)

#### 소프트웨어
- [ ] Arduino IDE
- [ ] Python 3.7 이상
- [ ] USB 케이블 (Arduino 연결용)

### 2단계: 하드웨어 조립

1. **RC 카 조립**
   - 4개 DC 모터를 섀시에 장착
   - L298N 모터 드라이버 2개 연결
   - 배터리 홀더 설치

2. **로봇 팔 조립**
   - 서보 모터로 4자유도 팔 조립
   - 그리퍼 메커니즘 부착
   - RC 카 위에 로봇 팔 고정

3. **전자 부품 연결**
   - Arduino에 모터 드라이버 연결 (핀 2-13)
   - Arduino에 서보 연결 (핀 22-26)
   - 5V 레귤레이터 연결
   - 전원 배선

⚠️ **주의**: 배선 전에 반드시 [docs/WIRING.md](docs/WIRING.md)를 확인하세요!

### 3단계: Arduino 펌웨어 업로드

1. **Arduino IDE 열기**
   ```
   arduino_code/rc_car_robot_arm.ino 파일을 엽니다
   ```

2. **보드 선택**
   - 도구 → 보드 → Arduino Mega 2560

3. **포트 선택**
   - 도구 → 포트 → COM3 (Windows) 또는 /dev/ttyACM0 (Linux/Mac)

4. **업로드**
   - 업로드 버튼 클릭 (→)
   - "업로드 완료" 메시지 확인

5. **테스트**
   - 시리얼 모니터 열기 (Ctrl+Shift+M)
   - 보레이트를 115200으로 설정
   - `PING` 입력 → `PONG` 응답 확인

### 4단계: Python 환경 설정

```bash
# python_control 디렉토리로 이동
cd arduino_rc_car/python_control

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# 패키지 설치
pip install -r requirements.txt
```

### 5단계: 기본 테스트

```bash
# Arduino 인터페이스 테스트
python test_arduino.py
```

프롬프트가 나타나면:
1. Arduino 포트 입력 (예: COM3 또는 /dev/ttyACM0)
2. 테스트 모드 선택:
   - 1: 전체 테스트 (권장)
   - 2: 모터만 테스트
   - 3: 로봇 팔만 테스트
   - 4: 대화형 모드
   - 5: 상태 확인만

### 6단계: YOLO 설정 (선택사항)

완전한 자율 픽앤플레이스를 위해 YOLO를 설정합니다.

1. **YOLO 가중치 다운로드**
   - 학습된 가중치 파일이 필요합니다
   - 또는 darknet으로 직접 학습

2. **경로 확인**
   ```python
   # yolo_arduino_controller.py에서 확인
   config_file = "../../darknet/cfg/custom-yolov4-detector.cfg"
   data_file = "../../darknet/cfg/coco.data"
   weights_file = "../../best.weights"
   ```

3. **실행**
   ```bash
   python yolo_arduino_controller.py
   ```

### 7단계: 첫 픽앤플레이스 작업

```python
from yolo_arduino_controller import YOLOArduinoController

# 컨트롤러 생성
controller = YOLOArduinoController(
    arduino_port="/dev/ttyACM0"  # 본인의 포트로 변경
)

# 초기화
controller.initialize()

# 작업 정의
tasks = [
    ('cir', 'R'),  # 원형 → 빨간 영역
    ('sqr', 'B'),  # 사각형 → 파란 영역
]

# 실행
controller.run_pick_and_place_task(tasks)

# 정리
controller.cleanup()
```

## 일반적인 문제 해결

### 문제: Arduino에 연결할 수 없음
**해결방법:**
- USB 케이블이 제대로 연결되었는지 확인
- Arduino가 전원을 받고 있는지 확인 (전원 LED 확인)
- 올바른 COM 포트를 선택했는지 확인
- 드라이버가 설치되었는지 확인 (CH340 또는 FTDI)

### 문제: 모터가 작동하지 않음
**해결방법:**
- L298N의 전원 LED 확인
- 배터리가 충전되었는지 확인 (7.4V 이상)
- 배선이 올바른지 확인 ([docs/WIRING.md](docs/WIRING.md) 참조)
- 모터를 배터리에 직접 연결하여 테스트

### 문제: 서보가 떨리거나 작동하지 않음
**해결방법:**
- 5V 레귤레이터가 충분한 전류를 공급하는지 확인 (최소 3A)
- 서보 전원에 1000µF 커패시터 추가
- 서보와 모터 전원을 분리
- 신호선이 모터 케이블에서 멀리 있는지 확인

### 문제: 카메라가 감지되지 않음
**해결방법:**
- USB 웹캠이 연결되었는지 확인
- 카메라 ID 확인 (기본값: 0)
  ```python
  controller = YOLOArduinoController(camera_id=0)  # 또는 1, 2...
  ```
- 다른 프로그램이 카메라를 사용 중이 아닌지 확인

## 다음 단계

1. **문서 읽기**
   - [docs/README.md](docs/README.md) - 전체 가이드
   - [docs/WIRING.md](docs/WIRING.md) - 배선 상세
   - [docs/BOM.md](docs/BOM.md) - 부품 목록

2. **캘리브레이션**
   - 서보 위치 조정
   - 카메라 위치 및 각도 조정
   - 색상 임계값 조정

3. **커스터마이징**
   - 본인만의 작업 추가
   - 새로운 객체 클래스 학습
   - 제어 알고리즘 개선

4. **고급 기능**
   - Bluetooth 무선 제어 추가
   - 초음파 센서로 장애물 회피
   - 더 많은 자유도 추가

## 도움말

문제가 계속되면:
- GitHub Issues에 질문하기
- [docs/README.md](docs/README.md)의 문제 해결 섹션 확인
- Arduino 포럼이나 커뮤니티에 문의

## 안전 주의사항

⚠️ **항상 안전을 최우선으로!**

- 작업 중 전원 차단하기
- 배터리 극성 확인하기
- 노출된 전선 절연하기
- 작동 중 손가락 주의하기
- 충분한 작업 공간 확보하기
- 테스트는 낮은 속도로 시작하기

## 성공 체크리스트

프로젝트가 제대로 작동하는지 확인:

- [ ] Arduino가 PING에 PONG으로 응답
- [ ] 모든 4개 모터가 올바른 방향으로 회전
- [ ] 서보가 부드럽게 움직임 (떨림 없음)
- [ ] 그리퍼가 열리고 닫힘
- [ ] 카메라가 이미지를 캡처함
- [ ] YOLO가 객체를 감지함
- [ ] 색상 영역이 감지됨
- [ ] 픽앤플레이스 작업이 성공함

모두 체크되었다면 축하합니다! 🎉

## 추가 리소스

- Arduino 공식 문서: https://www.arduino.cc/reference/
- OpenCV Python 튜토리얼: https://docs.opencv.org/
- YOLO 논문: https://arxiv.org/abs/2004.10934
- 원본 프로젝트: https://github.com/jagari/YOLO-Object-Detection-for-Pick-and-Place-task-using-ROS-on-KUKA-iiwa

---

**즐거운 로봇 제작 되세요!** 🤖🚗
