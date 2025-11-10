#!/usr/bin/env python3
"""
Simple test script for Arduino RC Car interface

This script provides a basic test of the Arduino RC car without requiring
YOLO or camera setup. Useful for initial hardware testing.
"""

import time
import sys

try:
    from arduino_interface import ArduinoRCCar
except ImportError:
    print("Error: Cannot import arduino_interface")
    print("Make sure you're in the python_control directory")
    sys.exit(1)


def test_connection(car):
    """Test basic connection"""
    print("\n=== Testing Connection ===")
    if car.ping():
        print("✓ Connection successful!")
        return True
    else:
        print("✗ Connection failed")
        return False


def test_motors(car):
    """Test motor movements"""
    print("\n=== Testing Motors ===")
    
    tests = [
        ("Forward", lambda: car.move_forward(100, 1.0)),
        ("Backward", lambda: car.move_backward(100, 1.0)),
        ("Turn Left", lambda: car.turn_left(100, 0.5)),
        ("Turn Right", lambda: car.turn_right(100, 0.5)),
    ]
    
    for name, test_func in tests:
        print(f"Testing {name}...")
        if test_func():
            print(f"✓ {name} OK")
        else:
            print(f"✗ {name} failed")
        time.sleep(0.5)
    
    car.stop()
    print("✓ Motors test complete")


def test_arm(car):
    """Test robot arm movements"""
    print("\n=== Testing Robot Arm ===")
    
    print("Moving to home position...")
    if car.home_position():
        print("✓ Home position OK")
    else:
        print("✗ Home position failed")
    
    time.sleep(1)
    
    print("Testing gripper...")
    car.release()
    time.sleep(1)
    car.grip()
    time.sleep(1)
    car.release()
    print("✓ Gripper test OK")
    
    time.sleep(1)
    
    print("Moving to pick position...")
    if car.pick_position():
        print("✓ Pick position OK")
    else:
        print("✗ Pick position failed")
    
    time.sleep(1)
    
    print("Moving to place position...")
    if car.place_position():
        print("✓ Place position OK")
    else:
        print("✗ Place position failed")
    
    time.sleep(1)
    
    print("Returning to home...")
    car.home_position()
    print("✓ Arm test complete")


def test_status(car):
    """Test status reporting"""
    print("\n=== Testing Status ===")
    status = car.get_status()
    if status:
        print("Current arm positions:")
        for key, value in status.items():
            print(f"  {key}: {value}°")
        print("✓ Status retrieval OK")
    else:
        print("✗ Failed to get status")


def interactive_mode(car):
    """Interactive control mode"""
    print("\n=== Interactive Mode ===")
    print("Commands:")
    print("  w - Forward")
    print("  s - Backward")
    print("  a - Turn Left")
    print("  d - Turn Right")
    print("  h - Home position")
    print("  p - Pick position")
    print("  l - Place position")
    print("  g - Grip")
    print("  r - Release")
    print("  q - Quit")
    print("\nPress Enter after each command:")
    
    while True:
        try:
            cmd = input("> ").strip().lower()
            
            if cmd == 'q':
                break
            elif cmd == 'w':
                car.move_forward(150, 0.5)
            elif cmd == 's':
                car.move_backward(150, 0.5)
            elif cmd == 'a':
                car.turn_left(150, 0.3)
            elif cmd == 'd':
                car.turn_right(150, 0.3)
            elif cmd == 'h':
                car.home_position()
            elif cmd == 'p':
                car.pick_position()
            elif cmd == 'l':
                car.place_position()
            elif cmd == 'g':
                car.grip()
            elif cmd == 'r':
                car.release()
            else:
                print("Unknown command")
                
        except KeyboardInterrupt:
            break
    
    print("\nExiting interactive mode...")


def main():
    """Main test function"""
    print("="*50)
    print("Arduino RC Car Test Script")
    print("="*50)
    
    # Configuration
    port = input("Enter Arduino port (default: /dev/ttyACM0): ").strip()
    if not port:
        port = "/dev/ttyACM0"
    
    # Create interface
    car = ArduinoRCCar(port=port)
    
    try:
        # Connect
        print(f"\nConnecting to Arduino on {port}...")
        if not car.connect():
            print("\nFailed to connect to Arduino!")
            print("Please check:")
            print("  1. Arduino is connected")
            print("  2. Correct port specified")
            print("  3. Firmware uploaded to Arduino")
            print("  4. Arduino is powered on")
            return
        
        # Run tests
        if not test_connection(car):
            return
        
        print("\nSelect test mode:")
        print("  1 - Run all tests")
        print("  2 - Test motors only")
        print("  3 - Test arm only")
        print("  4 - Interactive mode")
        print("  5 - Status check only")
        
        choice = input("Enter choice (1-5): ").strip()
        
        if choice == '1':
            test_motors(car)
            time.sleep(1)
            test_arm(car)
            time.sleep(1)
            test_status(car)
        elif choice == '2':
            test_motors(car)
        elif choice == '3':
            test_arm(car)
        elif choice == '4':
            interactive_mode(car)
        elif choice == '5':
            test_status(car)
        else:
            print("Invalid choice")
        
        print("\n" + "="*50)
        print("Testing complete!")
        print("="*50)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        print("\nCleaning up...")
        car.stop()
        car.home_position()
        car.disconnect()
        print("Done!")


if __name__ == "__main__":
    main()
