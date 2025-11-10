"""
YOLO Object Detection for Arduino RC Car Pick and Place

This script integrates YOLOv4 object detection with Arduino-controlled
RC car and robot arm for autonomous pick and place operations.
"""

import cv2
import numpy as np
import time
import sys
import os
from typing import List, Tuple, Optional

# Add darknet path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../darknet'))
import darknet

from arduino_interface import ArduinoRCCar


class YOLOArduinoController:
    """
    Controller class integrating YOLO detection with Arduino RC car
    """
    
    def __init__(self, 
                 config_file: str = "./cfg/custom-yolov4-detector.cfg",
                 data_file: str = "./cfg/coco.data",
                 weights_file: str = "./best.weights",
                 arduino_port: str = '/dev/ttyACM0',
                 camera_id: int = 0):
        """
        Initialize YOLO and Arduino controller
        
        Args:
            config_file: Path to YOLO config file
            data_file: Path to YOLO data file
            weights_file: Path to YOLO weights file
            arduino_port: Serial port for Arduino
            camera_id: Camera device ID
        """
        self.config_file = config_file
        self.data_file = data_file
        self.weights_file = weights_file
        self.arduino_port = arduino_port
        self.camera_id = camera_id
        
        # YOLO network
        self.network = None
        self.class_names = None
        self.class_colors = None
        
        # Arduino interface
        self.arduino = ArduinoRCCar(port=arduino_port)
        
        # Camera
        self.cap = None
        
        # Detection parameters
        self.detection_threshold = 0.7
        
        # Color regions for placing (HSV ranges)
        self.color_regions = {
            'R': {'name': 'Red', 'lower': np.array([0, 100, 100]), 'upper': np.array([10, 255, 255])},
            'B': {'name': 'Blue', 'lower': np.array([100, 100, 100]), 'upper': np.array([130, 255, 255])},
            'Y': {'name': 'Yellow', 'lower': np.array([20, 100, 100]), 'upper': np.array([30, 255, 255])}
        }
        
    def initialize(self) -> bool:
        """
        Initialize YOLO network, Arduino, and camera
        
        Returns:
            True if initialization successful
        """
        print("Initializing YOLO Arduino Controller...")
        
        # Initialize YOLO
        print("Loading YOLO network...")
        try:
            self.network, self.class_names, self.class_colors = darknet.load_network(
                self.config_file,
                self.data_file,
                self.weights_file,
                batch_size=1
            )
            print(f"YOLO network loaded. Classes: {self.class_names}")
        except Exception as e:
            print(f"Failed to load YOLO network: {e}")
            return False
        
        # Initialize Arduino
        print("Connecting to Arduino...")
        if not self.arduino.connect():
            print("Failed to connect to Arduino")
            return False
        
        # Move to home position
        print("Moving to home position...")
        self.arduino.home_position()
        self.arduino.release()
        
        # Initialize camera
        print("Initializing camera...")
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            print("Failed to open camera")
            return False
        
        print("Initialization complete!")
        return True
    
    def cleanup(self):
        """Clean up resources"""
        if self.cap:
            self.cap.release()
        if self.arduino:
            self.arduino.stop()
            self.arduino.home_position()
            self.arduino.disconnect()
        cv2.destroyAllWindows()
    
    def detect_objects(self, frame: np.ndarray, target_class: Optional[str] = None) -> List[dict]:
        """
        Detect objects in frame using YOLO
        
        Args:
            frame: Input frame
            target_class: Specific class to detect (None = all classes)
            
        Returns:
            List of detected objects with bbox and center coordinates
        """
        frame_width = darknet.network_width(self.network)
        frame_height = darknet.network_height(self.network)
        
        # Resize frame
        frame_resized = cv2.resize(frame, (frame_width, frame_height), 
                                   interpolation=cv2.INTER_LINEAR)
        
        # Create darknet image
        darknet_image = darknet.make_image(frame_width, frame_height, 3)
        darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
        
        # Detect
        detections = darknet.detect_image(self.network, self.class_names, 
                                         darknet_image, thresh=self.detection_threshold)
        
        # Parse detections
        objects = []
        for label, confidence, bbox in detections:
            if target_class and label != target_class:
                continue
            
            x, y, w, h = bbox
            center_x = int(x)
            center_y = int(y)
            
            objects.append({
                'class': label,
                'confidence': confidence,
                'bbox': bbox,
                'center': (center_x, center_y)
            })
        
        darknet.free_image(darknet_image)
        return objects
    
    def detect_color_region(self, frame: np.ndarray, color_code: str) -> Optional[Tuple[int, int]]:
        """
        Detect colored region in frame
        
        Args:
            frame: Input frame
            color_code: Color code ('R', 'B', 'Y')
            
        Returns:
            (center_x, center_y) of color region or None
        """
        if color_code not in self.color_regions:
            return None
        
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get color range
        lower = self.color_regions[color_code]['lower']
        upper = self.color_regions[color_code]['upper']
        
        # Create mask
        mask = cv2.inRange(hsv, lower, upper)
        
        # Morphology operations
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            # Get largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            if cv2.contourArea(largest_contour) > 1000:  # Minimum area threshold
                # Get center
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    return (cx, cy)
        
        return None
    
    def pick_object(self, object_class: str) -> bool:
        """
        Pick up object of specified class
        
        Args:
            object_class: Class name of object to pick
            
        Returns:
            True if pick successful
        """
        print(f"\n=== Picking {object_class} ===")
        
        # Move to pick position
        self.arduino.pick_position()
        time.sleep(2)
        
        # Detect object
        print("Detecting object...")
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame")
            return False
        
        objects = self.detect_objects(frame, target_class=object_class)
        
        if len(objects) == 0:
            print(f"No {object_class} detected")
            return False
        
        # Get first detected object
        obj = objects[0]
        print(f"Detected {obj['class']} at {obj['center']} with confidence {obj['confidence']:.2f}")
        
        # Calculate offset from center (simple proportional control)
        frame_center_x = frame.shape[1] // 2
        frame_center_y = frame.shape[0] // 2
        
        offset_x = obj['center'][0] - frame_center_x
        offset_y = obj['center'][1] - frame_center_y
        
        print(f"Offset: ({offset_x}, {offset_y})")
        
        # Move car to align with object
        # Simple proportional control
        if abs(offset_x) > 20:
            if offset_x > 0:
                self.arduino.strafe_right(100, 0.2)
            else:
                self.arduino.strafe_left(100, 0.2)
            time.sleep(0.5)
        
        # Lower arm and grip
        print("Gripping object...")
        self.arduino.release()
        time.sleep(0.5)
        
        # Fine positioning (lower arm)
        current_status = self.arduino.get_status()
        if current_status:
            self.arduino.set_arm_position(
                current_status['base'],
                45,  # Lower shoulder
                45,  # Lower elbow
                current_status['wrist']
            )
        
        time.sleep(1)
        
        # Close gripper
        self.arduino.grip()
        time.sleep(1)
        
        # Raise arm
        self.arduino.place_position()
        time.sleep(1)
        
        print("Pick complete!")
        return True
    
    def place_object(self, color_code: str) -> bool:
        """
        Place object in colored region
        
        Args:
            color_code: Target color region ('R', 'B', 'Y')
            
        Returns:
            True if place successful
        """
        print(f"\n=== Placing in {self.color_regions[color_code]['name']} region ===")
        
        # Move to place position
        self.arduino.place_position()
        time.sleep(2)
        
        # Detect color region
        print("Detecting color region...")
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame")
            return False
        
        region_center = self.detect_color_region(frame, color_code)
        
        if region_center is None:
            print(f"No {self.color_regions[color_code]['name']} region detected")
            return False
        
        print(f"Detected region at {region_center}")
        
        # Calculate offset
        frame_center_x = frame.shape[1] // 2
        frame_center_y = frame.shape[0] // 2
        
        offset_x = region_center[0] - frame_center_x
        offset_y = region_center[1] - frame_center_y
        
        print(f"Offset: ({offset_x}, {offset_y})")
        
        # Move car to align with region
        if abs(offset_x) > 20:
            if offset_x > 0:
                self.arduino.strafe_right(100, 0.2)
            else:
                self.arduino.strafe_left(100, 0.2)
            time.sleep(0.5)
        
        # Lower arm and release
        print("Placing object...")
        current_status = self.arduino.get_status()
        if current_status:
            self.arduino.set_arm_position(
                current_status['base'],
                45,  # Lower shoulder
                45,  # Lower elbow
                current_status['wrist']
            )
        
        time.sleep(1)
        
        # Release gripper
        self.arduino.release()
        time.sleep(1)
        
        # Raise arm
        self.arduino.place_position()
        time.sleep(1)
        
        print("Place complete!")
        return True
    
    def run_pick_and_place_task(self, tasks: List[Tuple[str, str]]):
        """
        Run pick and place tasks
        
        Args:
            tasks: List of (object_class, color_code) tuples
        """
        print("\n" + "="*50)
        print("Starting Pick and Place Tasks")
        print("="*50)
        
        for i, (object_class, color_code) in enumerate(tasks, 1):
            print(f"\n--- Task {i}/{len(tasks)} ---")
            print(f"Object: {object_class}, Target: {self.color_regions[color_code]['name']}")
            
            # Pick
            if self.pick_object(object_class):
                time.sleep(1)
                
                # Place
                if self.place_object(color_code):
                    print(f"Task {i} completed successfully!")
                else:
                    print(f"Task {i} failed at placing")
            else:
                print(f"Task {i} failed at picking")
            
            # Return to home
            self.arduino.home_position()
            time.sleep(2)
        
        print("\n" + "="*50)
        print("All tasks completed!")
        print("="*50)


def main():
    """Main function"""
    # Configuration
    config_file = "../../darknet/cfg/custom-yolov4-detector.cfg"
    data_file = "../../darknet/cfg/coco.data"
    weights_file = "../../best.weights"
    arduino_port = "/dev/ttyACM0"  # Change for Windows (e.g., "COM3")
    
    # Create controller
    controller = YOLOArduinoController(
        config_file=config_file,
        data_file=data_file,
        weights_file=weights_file,
        arduino_port=arduino_port
    )
    
    try:
        # Initialize
        if not controller.initialize():
            print("Initialization failed!")
            return
        
        # Define tasks: (object_class, target_color)
        # Classes: 'cir', 'hex', 'rec', 'rng', 'slt', 'sqr'
        # Colors: 'R' (Red), 'B' (Blue), 'Y' (Yellow)
        tasks = [
            ('cir', 'R'),  # Pick circle, place in red region
            ('sqr', 'B'),  # Pick square, place in blue region
            ('hex', 'Y'),  # Pick hexagon, place in yellow region
        ]
        
        # Run tasks
        controller.run_pick_and_place_task(tasks)
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        controller.cleanup()
        print("Cleanup complete")


if __name__ == "__main__":
    main()
