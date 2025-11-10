/*
 * Arduino RC Car with Robot Arm Control
 * 
 * This sketch controls:
 * - 4-wheel RC car using L298N motor driver
 * - 4-DOF robot arm using servo motors
 * - Gripper servo for pick and place operations
 * 
 * Communication: Serial interface (115200 baud)
 * Command format: <COMMAND>:param1,param2,...\n
 * 
 * Hardware Requirements:
 * - Arduino Mega 2560 (recommended for multiple servos)
 * - L298N Motor Driver Module x2
 * - Servo Motors x5 (Base, Shoulder, Elbow, Wrist, Gripper)
 * - DC Motors x4 (for wheels)
 * - Power supply (7.4V LiPo battery recommended)
 */

#include <Servo.h>

// ========== Pin Definitions ==========

// Motor Driver Pins (L298N)
#define MOTOR_FL_FWD 2    // Front Left Forward
#define MOTOR_FL_BWD 3    // Front Left Backward
#define MOTOR_FL_PWM 4    // Front Left Speed (PWM)

#define MOTOR_FR_FWD 5    // Front Right Forward
#define MOTOR_FR_BWD 6    // Front Right Backward
#define MOTOR_FR_PWM 7    // Front Right Speed (PWM)

#define MOTOR_BL_FWD 8    // Back Left Forward
#define MOTOR_BL_BWD 9    // Back Left Backward
#define MOTOR_BL_PWM 10   // Back Left Speed (PWM)

#define MOTOR_BR_FWD 11   // Back Right Forward
#define MOTOR_BR_BWD 12   // Back Right Backward
#define MOTOR_BR_PWM 13   // Back Right Speed (PWM)

// Servo Pins (Robot Arm)
#define SERVO_BASE 22      // Base rotation (0-180°)
#define SERVO_SHOULDER 23  // Shoulder joint (0-180°)
#define SERVO_ELBOW 24     // Elbow joint (0-180°)
#define SERVO_WRIST 25     // Wrist rotation (0-180°)
#define SERVO_GRIPPER 26   // Gripper open/close (0-180°)

// ========== Servo Objects ==========
Servo servoBase;
Servo servoShoulder;
Servo servoElbow;
Servo servoWrist;
Servo servoGripper;

// ========== Configuration ==========
#define SERIAL_BAUD 115200
#define COMMAND_BUFFER_SIZE 64
#define DEFAULT_SPEED 150      // Default motor speed (0-255)
#define SERVO_DELAY 15         // Delay between servo steps (ms)

// ========== Current State ==========
int currentSpeed = DEFAULT_SPEED;

// Current servo positions
int posBase = 90;
int posShoulder = 90;
int posElbow = 90;
int posWrist = 90;
int posGripper = 90;  // 90 = open, 0 = closed

// ========== Home/Default Positions ==========
#define HOME_BASE 90
#define HOME_SHOULDER 90
#define HOME_ELBOW 90
#define HOME_WRIST 90
#define HOME_GRIPPER 90

// Pick position offsets
#define PICK_SHOULDER 45
#define PICK_ELBOW 45

// ========== Command Buffer ==========
char commandBuffer[COMMAND_BUFFER_SIZE];
int bufferIndex = 0;

// ========== Function Declarations ==========
void initializeMotors();
void initializeServos();
void processCommand(String cmd);
void stopAllMotors();
void moveForward(int speed);
void moveBackward(int speed);
void turnLeft(int speed);
void turnRight(int speed);
void strafeLeft(int speed);
void strafeRight(int speed);
void setMotor(int pinFwd, int pinBwd, int pinPWM, int speed);
void moveServoSmoothly(Servo &servo, int &currentPos, int targetPos);
void setArmPosition(int base, int shoulder, int elbow, int wrist);
void setGripperPosition(int angle);
void homePosition();
void pickPosition();
void placePosition();

// ========== Setup ==========
void setup() {
  Serial.begin(SERIAL_BAUD);
  
  // Initialize motors and servos
  initializeMotors();
  initializeServos();
  
  // Move to home position
  homePosition();
  
  Serial.println("RC Car with Robot Arm initialized");
  Serial.println("Ready for commands");
}

// ========== Main Loop ==========
void loop() {
  // Read serial commands
  while (Serial.available() > 0) {
    char c = Serial.read();
    
    if (c == '\n' || c == '\r') {
      if (bufferIndex > 0) {
        commandBuffer[bufferIndex] = '\0';
        processCommand(String(commandBuffer));
        bufferIndex = 0;
      }
    } else if (bufferIndex < COMMAND_BUFFER_SIZE - 1) {
      commandBuffer[bufferIndex++] = c;
    }
  }
}

// ========== Initialization Functions ==========

void initializeMotors() {
  // Set motor pins as outputs
  pinMode(MOTOR_FL_FWD, OUTPUT);
  pinMode(MOTOR_FL_BWD, OUTPUT);
  pinMode(MOTOR_FL_PWM, OUTPUT);
  
  pinMode(MOTOR_FR_FWD, OUTPUT);
  pinMode(MOTOR_FR_BWD, OUTPUT);
  pinMode(MOTOR_FR_PWM, OUTPUT);
  
  pinMode(MOTOR_BL_FWD, OUTPUT);
  pinMode(MOTOR_BL_BWD, OUTPUT);
  pinMode(MOTOR_BL_PWM, OUTPUT);
  
  pinMode(MOTOR_BR_FWD, OUTPUT);
  pinMode(MOTOR_BR_BWD, OUTPUT);
  pinMode(MOTOR_BR_PWM, OUTPUT);
  
  // Stop all motors initially
  stopAllMotors();
}

void initializeServos() {
  // Attach servos to pins
  servoBase.attach(SERVO_BASE);
  servoShoulder.attach(SERVO_SHOULDER);
  servoElbow.attach(SERVO_ELBOW);
  servoWrist.attach(SERVO_WRIST);
  servoGripper.attach(SERVO_GRIPPER);
  
  // Initialize to current positions
  servoBase.write(posBase);
  servoShoulder.write(posShoulder);
  servoElbow.write(posElbow);
  servoWrist.write(posWrist);
  servoGripper.write(posGripper);
}

// ========== Command Processing ==========

void processCommand(String cmd) {
  cmd.trim();
  
  // Parse command and parameters
  int colonIndex = cmd.indexOf(':');
  String command = (colonIndex != -1) ? cmd.substring(0, colonIndex) : cmd;
  String params = (colonIndex != -1) ? cmd.substring(colonIndex + 1) : "";
  
  // Motor commands
  if (command == "FORWARD") {
    int speed = params.length() > 0 ? params.toInt() : currentSpeed;
    moveForward(speed);
    Serial.println("OK:FORWARD:" + String(speed));
  }
  else if (command == "BACKWARD") {
    int speed = params.length() > 0 ? params.toInt() : currentSpeed;
    moveBackward(speed);
    Serial.println("OK:BACKWARD:" + String(speed));
  }
  else if (command == "LEFT") {
    int speed = params.length() > 0 ? params.toInt() : currentSpeed;
    turnLeft(speed);
    Serial.println("OK:LEFT:" + String(speed));
  }
  else if (command == "RIGHT") {
    int speed = params.length() > 0 ? params.toInt() : currentSpeed;
    turnRight(speed);
    Serial.println("OK:RIGHT:" + String(speed));
  }
  else if (command == "STRAFE_LEFT") {
    int speed = params.length() > 0 ? params.toInt() : currentSpeed;
    strafeLeft(speed);
    Serial.println("OK:STRAFE_LEFT:" + String(speed));
  }
  else if (command == "STRAFE_RIGHT") {
    int speed = params.length() > 0 ? params.toInt() : currentSpeed;
    strafeRight(speed);
    Serial.println("OK:STRAFE_RIGHT:" + String(speed));
  }
  else if (command == "STOP") {
    stopAllMotors();
    Serial.println("OK:STOP");
  }
  else if (command == "SPEED") {
    currentSpeed = constrain(params.toInt(), 0, 255);
    Serial.println("OK:SPEED:" + String(currentSpeed));
  }
  
  // Arm commands
  else if (command == "ARM") {
    // Format: ARM:base,shoulder,elbow,wrist
    int pos[4];
    int count = 0;
    int startIdx = 0;
    
    for (int i = 0; i <= params.length(); i++) {
      if (i == params.length() || params.charAt(i) == ',') {
        if (count < 4) {
          pos[count++] = params.substring(startIdx, i).toInt();
        }
        startIdx = i + 1;
      }
    }
    
    if (count == 4) {
      setArmPosition(pos[0], pos[1], pos[2], pos[3]);
      Serial.println("OK:ARM:" + String(pos[0]) + "," + String(pos[1]) + "," + String(pos[2]) + "," + String(pos[3]));
    } else {
      Serial.println("ERROR:ARM:Invalid parameters");
    }
  }
  else if (command == "GRIPPER") {
    int angle = params.toInt();
    setGripperPosition(angle);
    Serial.println("OK:GRIPPER:" + String(angle));
  }
  else if (command == "GRIP") {
    setGripperPosition(0);  // Close gripper
    Serial.println("OK:GRIP");
  }
  else if (command == "RELEASE") {
    setGripperPosition(90);  // Open gripper
    Serial.println("OK:RELEASE");
  }
  else if (command == "HOME") {
    homePosition();
    Serial.println("OK:HOME");
  }
  else if (command == "PICK_POS") {
    pickPosition();
    Serial.println("OK:PICK_POS");
  }
  else if (command == "PLACE_POS") {
    placePosition();
    Serial.println("OK:PLACE_POS");
  }
  
  // Status commands
  else if (command == "STATUS") {
    Serial.print("STATUS:ARM:");
    Serial.print(posBase); Serial.print(",");
    Serial.print(posShoulder); Serial.print(",");
    Serial.print(posElbow); Serial.print(",");
    Serial.print(posWrist); Serial.print(",");
    Serial.print(posGripper);
    Serial.println();
  }
  else if (command == "PING") {
    Serial.println("PONG");
  }
  else {
    Serial.println("ERROR:Unknown command: " + command);
  }
}

// ========== Motor Control Functions ==========

void setMotor(int pinFwd, int pinBwd, int pinPWM, int speed) {
  if (speed > 0) {
    digitalWrite(pinFwd, HIGH);
    digitalWrite(pinBwd, LOW);
    analogWrite(pinPWM, abs(speed));
  } else if (speed < 0) {
    digitalWrite(pinFwd, LOW);
    digitalWrite(pinBwd, HIGH);
    analogWrite(pinPWM, abs(speed));
  } else {
    digitalWrite(pinFwd, LOW);
    digitalWrite(pinBwd, LOW);
    analogWrite(pinPWM, 0);
  }
}

void stopAllMotors() {
  setMotor(MOTOR_FL_FWD, MOTOR_FL_BWD, MOTOR_FL_PWM, 0);
  setMotor(MOTOR_FR_FWD, MOTOR_FR_BWD, MOTOR_FR_PWM, 0);
  setMotor(MOTOR_BL_FWD, MOTOR_BL_BWD, MOTOR_BL_PWM, 0);
  setMotor(MOTOR_BR_FWD, MOTOR_BR_BWD, MOTOR_BR_PWM, 0);
}

void moveForward(int speed) {
  setMotor(MOTOR_FL_FWD, MOTOR_FL_BWD, MOTOR_FL_PWM, speed);
  setMotor(MOTOR_FR_FWD, MOTOR_FR_BWD, MOTOR_FR_PWM, speed);
  setMotor(MOTOR_BL_FWD, MOTOR_BL_BWD, MOTOR_BL_PWM, speed);
  setMotor(MOTOR_BR_FWD, MOTOR_BR_BWD, MOTOR_BR_PWM, speed);
}

void moveBackward(int speed) {
  setMotor(MOTOR_FL_FWD, MOTOR_FL_BWD, MOTOR_FL_PWM, -speed);
  setMotor(MOTOR_FR_FWD, MOTOR_FR_BWD, MOTOR_FR_PWM, -speed);
  setMotor(MOTOR_BL_FWD, MOTOR_BL_BWD, MOTOR_BL_PWM, -speed);
  setMotor(MOTOR_BR_FWD, MOTOR_BR_BWD, MOTOR_BR_PWM, -speed);
}

void turnLeft(int speed) {
  setMotor(MOTOR_FL_FWD, MOTOR_FL_BWD, MOTOR_FL_PWM, -speed);
  setMotor(MOTOR_FR_FWD, MOTOR_FR_BWD, MOTOR_FR_PWM, speed);
  setMotor(MOTOR_BL_FWD, MOTOR_BL_BWD, MOTOR_BL_PWM, -speed);
  setMotor(MOTOR_BR_FWD, MOTOR_BR_BWD, MOTOR_BR_PWM, speed);
}

void turnRight(int speed) {
  setMotor(MOTOR_FL_FWD, MOTOR_FL_BWD, MOTOR_FL_PWM, speed);
  setMotor(MOTOR_FR_FWD, MOTOR_FR_BWD, MOTOR_FR_PWM, -speed);
  setMotor(MOTOR_BL_FWD, MOTOR_BL_BWD, MOTOR_BL_PWM, speed);
  setMotor(MOTOR_BR_FWD, MOTOR_BR_BWD, MOTOR_BR_PWM, -speed);
}

void strafeLeft(int speed) {
  // For mecanum wheels (if applicable)
  setMotor(MOTOR_FL_FWD, MOTOR_FL_BWD, MOTOR_FL_PWM, -speed);
  setMotor(MOTOR_FR_FWD, MOTOR_FR_BWD, MOTOR_FR_PWM, speed);
  setMotor(MOTOR_BL_FWD, MOTOR_BL_BWD, MOTOR_BL_PWM, speed);
  setMotor(MOTOR_BR_FWD, MOTOR_BR_BWD, MOTOR_BR_PWM, -speed);
}

void strafeRight(int speed) {
  // For mecanum wheels (if applicable)
  setMotor(MOTOR_FL_FWD, MOTOR_FL_BWD, MOTOR_FL_PWM, speed);
  setMotor(MOTOR_FR_FWD, MOTOR_FR_BWD, MOTOR_FR_PWM, -speed);
  setMotor(MOTOR_BL_FWD, MOTOR_BL_BWD, MOTOR_BL_PWM, -speed);
  setMotor(MOTOR_BR_FWD, MOTOR_BR_BWD, MOTOR_BR_PWM, speed);
}

// ========== Servo Control Functions ==========

void moveServoSmoothly(Servo &servo, int &currentPos, int targetPos) {
  targetPos = constrain(targetPos, 0, 180);
  
  if (currentPos < targetPos) {
    for (int pos = currentPos; pos <= targetPos; pos++) {
      servo.write(pos);
      delay(SERVO_DELAY);
    }
  } else {
    for (int pos = currentPos; pos >= targetPos; pos--) {
      servo.write(pos);
      delay(SERVO_DELAY);
    }
  }
  
  currentPos = targetPos;
}

void setArmPosition(int base, int shoulder, int elbow, int wrist) {
  moveServoSmoothly(servoBase, posBase, base);
  moveServoSmoothly(servoShoulder, posShoulder, shoulder);
  moveServoSmoothly(servoElbow, posElbow, elbow);
  moveServoSmoothly(servoWrist, posWrist, wrist);
}

void setGripperPosition(int angle) {
  moveServoSmoothly(servoGripper, posGripper, angle);
}

void homePosition() {
  setArmPosition(HOME_BASE, HOME_SHOULDER, HOME_ELBOW, HOME_WRIST);
  setGripperPosition(HOME_GRIPPER);
}

void pickPosition() {
  // Lower arm for picking
  setArmPosition(posBase, PICK_SHOULDER, PICK_ELBOW, posWrist);
}

void placePosition() {
  // Raise arm for placing
  setArmPosition(posBase, HOME_SHOULDER, HOME_ELBOW, posWrist);
}
