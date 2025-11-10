"""
Arduino RC Car Interface Module

This module provides a Python interface to communicate with Arduino-based
RC car with robot arm via serial connection.
"""

import serial
import time
import threading
from typing import Optional, Tuple


class ArduinoRCCar:
    """
    Interface class for Arduino RC Car with Robot Arm
    
    Handles serial communication and provides high-level control methods
    for both the car movement and robot arm operations.
    """
    
    def __init__(self, port: str = '/dev/ttyACM0', baudrate: int = 115200, timeout: float = 1.0):
        """
        Initialize Arduino interface
        
        Args:
            port: Serial port (e.g., '/dev/ttyACM0' on Linux, 'COM3' on Windows)
            baudrate: Serial communication speed (default: 115200)
            timeout: Serial read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection: Optional[serial.Serial] = None
        self.connected = False
        self.lock = threading.Lock()
        
    def connect(self) -> bool:
        """
        Establish serial connection with Arduino
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(2)  # Wait for Arduino to reset
            
            # Clear any initial data
            self.serial_connection.flushInput()
            
            # Test connection with PING
            response = self.send_command("PING")
            if response and "PONG" in response:
                self.connected = True
                print(f"Connected to Arduino on {self.port}")
                return True
            else:
                print("Arduino not responding to PING")
                return False
                
        except serial.SerialException as e:
            print(f"Failed to connect to Arduino: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Close serial connection"""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.connected = False
            print("Disconnected from Arduino")
    
    def send_command(self, command: str, wait_response: bool = True, timeout: float = 2.0) -> Optional[str]:
        """
        Send command to Arduino and optionally wait for response
        
        Args:
            command: Command string to send
            wait_response: Whether to wait for response
            timeout: Response timeout in seconds
            
        Returns:
            Response string from Arduino or None
        """
        if not self.connected or not self.serial_connection:
            print("Not connected to Arduino")
            return None
        
        try:
            with self.lock:
                # Send command
                cmd = command.strip() + '\n'
                self.serial_connection.write(cmd.encode())
                
                if not wait_response:
                    return None
                
                # Wait for response
                start_time = time.time()
                while (time.time() - start_time) < timeout:
                    if self.serial_connection.in_waiting > 0:
                        response = self.serial_connection.readline().decode().strip()
                        return response
                    time.sleep(0.01)
                
                print(f"Timeout waiting for response to: {command}")
                return None
                
        except Exception as e:
            print(f"Error sending command '{command}': {e}")
            return None
    
    # ========== Movement Commands ==========
    
    def move_forward(self, speed: int = 150, duration: float = 0) -> bool:
        """
        Move car forward
        
        Args:
            speed: Motor speed (0-255)
            duration: Duration in seconds (0 = continuous)
            
        Returns:
            True if command sent successfully
        """
        response = self.send_command(f"FORWARD:{speed}")
        if duration > 0:
            time.sleep(duration)
            self.stop()
        return response is not None and "OK" in response
    
    def move_backward(self, speed: int = 150, duration: float = 0) -> bool:
        """Move car backward"""
        response = self.send_command(f"BACKWARD:{speed}")
        if duration > 0:
            time.sleep(duration)
            self.stop()
        return response is not None and "OK" in response
    
    def turn_left(self, speed: int = 150, duration: float = 0) -> bool:
        """Turn car left"""
        response = self.send_command(f"LEFT:{speed}")
        if duration > 0:
            time.sleep(duration)
            self.stop()
        return response is not None and "OK" in response
    
    def turn_right(self, speed: int = 150, duration: float = 0) -> bool:
        """Turn car right"""
        response = self.send_command(f"RIGHT:{speed}")
        if duration > 0:
            time.sleep(duration)
            self.stop()
        return response is not None and "OK" in response
    
    def strafe_left(self, speed: int = 150, duration: float = 0) -> bool:
        """Strafe left (for mecanum wheels)"""
        response = self.send_command(f"STRAFE_LEFT:{speed}")
        if duration > 0:
            time.sleep(duration)
            self.stop()
        return response is not None and "OK" in response
    
    def strafe_right(self, speed: int = 150, duration: float = 0) -> bool:
        """Strafe right (for mecanum wheels)"""
        response = self.send_command(f"STRAFE_RIGHT:{speed}")
        if duration > 0:
            time.sleep(duration)
            self.stop()
        return response is not None and "OK" in response
    
    def stop(self) -> bool:
        """Stop all motors"""
        response = self.send_command("STOP")
        return response is not None and "OK" in response
    
    def set_speed(self, speed: int) -> bool:
        """
        Set default motor speed
        
        Args:
            speed: Speed value (0-255)
        """
        response = self.send_command(f"SPEED:{speed}")
        return response is not None and "OK" in response
    
    # ========== Robot Arm Commands ==========
    
    def set_arm_position(self, base: int, shoulder: int, elbow: int, wrist: int) -> bool:
        """
        Set robot arm joint positions
        
        Args:
            base: Base rotation angle (0-180)
            shoulder: Shoulder angle (0-180)
            elbow: Elbow angle (0-180)
            wrist: Wrist rotation angle (0-180)
            
        Returns:
            True if command sent successfully
        """
        response = self.send_command(f"ARM:{base},{shoulder},{elbow},{wrist}")
        time.sleep(2)  # Wait for arm to move
        return response is not None and "OK" in response
    
    def set_gripper(self, angle: int) -> bool:
        """
        Set gripper position
        
        Args:
            angle: Gripper angle (0=closed, 90=open)
        """
        response = self.send_command(f"GRIPPER:{angle}")
        time.sleep(0.5)
        return response is not None and "OK" in response
    
    def grip(self) -> bool:
        """Close gripper"""
        response = self.send_command("GRIP")
        time.sleep(0.5)
        return response is not None and "OK" in response
    
    def release(self) -> bool:
        """Open gripper"""
        response = self.send_command("RELEASE")
        time.sleep(0.5)
        return response is not None and "OK" in response
    
    def home_position(self) -> bool:
        """Move arm to home position"""
        response = self.send_command("HOME")
        time.sleep(2)
        return response is not None and "OK" in response
    
    def pick_position(self) -> bool:
        """Move arm to picking position"""
        response = self.send_command("PICK_POS")
        time.sleep(2)
        return response is not None and "OK" in response
    
    def place_position(self) -> bool:
        """Move arm to placing position"""
        response = self.send_command("PLACE_POS")
        time.sleep(2)
        return response is not None and "OK" in response
    
    # ========== Status Commands ==========
    
    def get_status(self) -> Optional[dict]:
        """
        Get current arm status
        
        Returns:
            Dictionary with arm positions or None
        """
        response = self.send_command("STATUS")
        if response and response.startswith("STATUS:ARM:"):
            try:
                positions = response.split(":")[2].split(",")
                return {
                    'base': int(positions[0]),
                    'shoulder': int(positions[1]),
                    'elbow': int(positions[2]),
                    'wrist': int(positions[3]),
                    'gripper': int(positions[4])
                }
            except (IndexError, ValueError) as e:
                print(f"Error parsing status: {e}")
                return None
        return None
    
    def ping(self) -> bool:
        """Test connection with Arduino"""
        response = self.send_command("PING")
        return response is not None and "PONG" in response


# ========== Example Usage ==========
if __name__ == "__main__":
    # Create interface instance
    car = ArduinoRCCar(port='/dev/ttyACM0')
    
    try:
        # Connect to Arduino
        if car.connect():
            print("Testing Arduino RC Car...")
            
            # Test movement
            print("\n1. Testing movement...")
            car.move_forward(150, 1.0)
            time.sleep(0.5)
            car.move_backward(150, 1.0)
            time.sleep(0.5)
            car.turn_left(150, 0.5)
            time.sleep(0.5)
            car.turn_right(150, 0.5)
            time.sleep(0.5)
            
            # Test arm
            print("\n2. Testing robot arm...")
            car.home_position()
            time.sleep(1)
            
            car.pick_position()
            time.sleep(1)
            
            car.grip()
            time.sleep(1)
            
            car.place_position()
            time.sleep(1)
            
            car.release()
            time.sleep(1)
            
            car.home_position()
            
            # Get status
            print("\n3. Getting status...")
            status = car.get_status()
            if status:
                print(f"Arm status: {status}")
            
            print("\nTest completed!")
        else:
            print("Failed to connect to Arduino")
            
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        # Clean up
        car.stop()
        car.disconnect()
