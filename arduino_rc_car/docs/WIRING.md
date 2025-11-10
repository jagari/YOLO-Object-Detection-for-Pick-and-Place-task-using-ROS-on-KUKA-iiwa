# Wiring Diagrams

## Complete System Wiring

This document provides detailed wiring diagrams for connecting all components of the Arduino RC Car with Robot Arm system.

## Power Distribution Diagram

```
                    7.4V LiPo Battery (2S)
                           |
                    [Power Switch]
                           |
            ┌──────────────┴──────────────┐
            |                             |
    [L298N Motor Driver 1]        [L298N Motor Driver 2]
      (Front Motors)                 (Back Motors)
            |                             |
    ┌───────┴───────┐             ┌───────┴───────┐
    |               |             |               |
  [FL Motor]    [FR Motor]     [BL Motor]    [BR Motor]


                    7.4V LiPo Battery (2S)
                           |
                    [Power Switch]
                           |
                    [5V Regulator]
                     (LM2596 3A)
                           |
            ┌──────────────┴──────────────────┐
            |              |                   |
     [Arduino 5V]    [Servo VCC]    [Servo VCC] (All 5 servos)
                     (Base/Shoulder/Elbow/Wrist/Gripper)


Common Ground:
Battery GND ─┬─ Arduino GND
             ├─ Motor Driver 1 GND
             ├─ Motor Driver 2 GND
             ├─ All Servo GND
             └─ 5V Regulator GND
```

## Arduino Mega Pin Assignment Map

```
┌─────────────────────────────────────────┐
│         Arduino Mega 2560               │
│                                         │
│  Digital Pins:                          │
│  ┌────────────────────────────────┐    │
│  │ 0   - [Reserved: Serial RX]    │    │
│  │ 1   - [Reserved: Serial TX]    │    │
│  │ 2   - Motor FL Forward         │    │
│  │ 3   - Motor FL Backward        │    │
│  │ 4   - Motor FL PWM             │    │
│  │ 5   - Motor FR Forward         │    │
│  │ 6   - Motor FR Backward        │    │
│  │ 7   - Motor FR PWM             │    │
│  │ 8   - Motor BL Forward         │    │
│  │ 9   - Motor BL Backward        │    │
│  │ 10  - Motor BL PWM             │    │
│  │ 11  - Motor BR Forward         │    │
│  │ 12  - Motor BR Backward        │    │
│  │ 13  - Motor BR PWM             │    │
│  │ 14-21 - [Available]            │    │
│  │ 22  - Servo Base               │    │
│  │ 23  - Servo Shoulder           │    │
│  │ 24  - Servo Elbow              │    │
│  │ 25  - Servo Wrist              │    │
│  │ 26  - Servo Gripper            │    │
│  │ 27-53 - [Available]            │    │
│  └────────────────────────────────┘    │
│                                         │
│  Power:                                 │
│  ┌────────────────────────────────┐    │
│  │ 5V  - From regulator (optional)│    │
│  │ GND - Common ground            │    │
│  │ VIN - [Not used]               │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

## Motor Driver Wiring (L298N)

### Driver 1: Front Motors

```
┌─────────────────────────┐
│   L298N Motor Driver 1  │
│                         │
│  IN1 ← Pin 2            │ ──┐
│  IN2 ← Pin 3            │   │  Control
│  ENA ← Pin 4  (PWM)     │ ──┘
│                         │
│  OUT1 → Motor FL +      │ ──┐
│  OUT2 → Motor FL -      │   │  Front Left Motor
│                         │ ──┘
│  IN3 ← Pin 5            │ ──┐
│  IN4 ← Pin 6            │   │  Control
│  ENB ← Pin 7  (PWM)     │ ──┘
│                         │
│  OUT3 → Motor FR +      │ ──┐
│  OUT4 → Motor FR -      │   │  Front Right Motor
│                         │ ──┘
│  +12V ← Battery +7.4V   │
│  GND  ← Battery GND     │
│  +5V  → [Not used]      │
└─────────────────────────┘
```

### Driver 2: Back Motors

```
┌─────────────────────────┐
│   L298N Motor Driver 2  │
│                         │
│  IN1 ← Pin 8            │ ──┐
│  IN2 ← Pin 9            │   │  Control
│  ENA ← Pin 10 (PWM)     │ ──┘
│                         │
│  OUT1 → Motor BL +      │ ──┐
│  OUT2 → Motor BL -      │   │  Back Left Motor
│                         │ ──┘
│  IN3 ← Pin 11           │ ──┐
│  IN4 ← Pin 12           │   │  Control
│  ENB ← Pin 13 (PWM)     │ ──┘
│                         │
│  OUT3 → Motor BR +      │ ──┐
│  OUT4 → Motor BR -      │   │  Back Right Motor
│                         │ ──┘
│  +12V ← Battery +7.4V   │
│  GND  ← Battery GND     │
│  +5V  → [Not used]      │
└─────────────────────────┘
```

## Servo Wiring

All servos have 3 wires:
- **Brown/Black** = Ground (GND)
- **Red** = Power (VCC) - 5V
- **Orange/Yellow/White** = Signal (PWM)

```
┌──────────────────────────────────────────────┐
│  Servo Connections                           │
│                                              │
│  Base Servo (MG996R):                        │
│    Signal ← Pin 22                           │
│    VCC    ← 5V Regulator                     │
│    GND    ← Common GND                       │
│                                              │
│  Shoulder Servo (MG996R):                    │
│    Signal ← Pin 23                           │
│    VCC    ← 5V Regulator                     │
│    GND    ← Common GND                       │
│                                              │
│  Elbow Servo (MG996R):                       │
│    Signal ← Pin 24                           │
│    VCC    ← 5V Regulator                     │
│    GND    ← Common GND                       │
│                                              │
│  Wrist Servo (SG90):                         │
│    Signal ← Pin 25                           │
│    VCC    ← 5V Regulator                     │
│    GND    ← Common GND                       │
│                                              │
│  Gripper Servo (SG90):                       │
│    Signal ← Pin 26                           │
│    VCC    ← 5V Regulator                     │
│    GND    ← Common GND                       │
└──────────────────────────────────────────────┘
```

## 5V Voltage Regulator (LM2596)

```
┌─────────────────────┐
│  LM2596 Module      │
│                     │
│  IN+  ← Battery +   │
│  IN-  ← Battery -   │
│                     │
│  OUT+ → Arduino 5V  │
│       → Servo VCC   │
│  OUT- → Common GND  │
│                     │
│  [Adjust pot to 5V] │
└─────────────────────┘

Note: Add 1000µF capacitor between
      OUT+ and OUT- for stability
```

## Optional: Bluetooth Module (HC-05)

For wireless control instead of USB:

```
┌─────────────────────┐
│   HC-05 Module      │
│                     │
│  VCC ← Arduino 5V   │
│  GND ← Common GND   │
│  TXD ← Pin 0 (RX)   │
│  RXD ← Pin 1 (TX)   │
│       (via voltage  │
│        divider)     │
└─────────────────────┘

Voltage Divider for RXD:
Arduino TX (5V) ─┬─ 1kΩ ─┬─ HC-05 RXD (3.3V)
                 │        │
                 └─ 2kΩ ─┴─ GND
```

## Safety Components

### Fuse Installation

```
Battery + ──[10A Fuse]── Power Switch ── System
```

### Emergency Stop Button (Optional)

```
Power Switch ──[E-Stop Button]── Motor Drivers
(Cuts power to motors but not Arduino)
```

## Complete Wiring Checklist

### Power Connections
- [ ] Battery to power switch
- [ ] Power switch to motor drivers
- [ ] Power switch to 5V regulator
- [ ] 5V regulator to Arduino
- [ ] 5V regulator to servos
- [ ] All grounds connected (common ground)
- [ ] Fuse installed
- [ ] Capacitor on servo power line

### Motor Connections
- [ ] L298N Driver 1 control pins (2-7)
- [ ] L298N Driver 2 control pins (8-13)
- [ ] Front Left motor to Driver 1 OUT1/OUT2
- [ ] Front Right motor to Driver 1 OUT3/OUT4
- [ ] Back Left motor to Driver 2 OUT1/OUT2
- [ ] Back Right motor to Driver 2 OUT3/OUT4
- [ ] Motor polarity correct (test direction)

### Servo Connections
- [ ] Base servo signal to Pin 22
- [ ] Shoulder servo signal to Pin 23
- [ ] Elbow servo signal to Pin 24
- [ ] Wrist servo signal to Pin 25
- [ ] Gripper servo signal to Pin 26
- [ ] All servo VCC to 5V regulator
- [ ] All servo GND to common ground

### Communication
- [ ] USB cable to Arduino
- [ ] OR Bluetooth module connected (if wireless)

### Safety Checks Before Power On

1. **Visual Inspection**
   - [ ] No exposed wire connections
   - [ ] No short circuits possible
   - [ ] All connections tight
   - [ ] Proper polarity (red=+, black=-)

2. **Continuity Tests** (with multimeter, power OFF)
   - [ ] Check for shorts between VCC and GND
   - [ ] Verify ground continuity
   - [ ] Check motor driver connections

3. **Voltage Tests** (with multimeter, power ON)
   - [ ] Battery voltage: 7.4V nominal
   - [ ] 5V regulator output: 4.9-5.1V
   - [ ] Arduino 5V pin: ~5V
   - [ ] Servo VCC: 4.9-5.1V

4. **Initial Power On**
   - [ ] Connect Arduino to PC first (USB power)
   - [ ] Upload test sketch
   - [ ] Test servos one at a time
   - [ ] Then connect battery power
   - [ ] Test motors one at a time

## Troubleshooting Wire Issues

### Motor Not Moving
1. Check control pins connected to correct Arduino pins
2. Verify motor driver powered (LED on L298N)
3. Test motor directly with battery
4. Check PWM pins (must be PWM-capable)

### Servo Jittering
1. Check power supply stable (use capacitor)
2. Verify 5V regulator output
3. Separate servo power from motor power
4. Check signal wire not near motor wires

### No Communication
1. Check USB cable
2. Verify correct COM port selected
3. Check TX/RX not swapped
4. Test with Serial Monitor

### System Resets
1. Check for voltage drop (weak battery)
2. Verify sufficient current capacity
3. Add capacitors for noise filtering
4. Check for loose connections

## Cable Management Tips

1. **Use Cable Ties**
   - Bundle wires by function (power, signal, motor)
   - Secure to chassis to prevent movement
   - Leave some slack for servo movement

2. **Color Coding**
   - Red: Positive power
   - Black: Ground
   - Yellow/White: Signals
   - Blue: Motor wires

3. **Labeling**
   - Label both ends of long wires
   - Use heat shrink with labels
   - Mark motor driver outputs

4. **Routing**
   - Keep motor wires away from signal wires
   - Twist motor wire pairs
   - Use shielding if interference occurs

## Wire Gauge Recommendations

| Connection | Wire Gauge | Note |
|------------|------------|------|
| Battery to Switch | 18 AWG | High current |
| Switch to Drivers | 18 AWG | High current |
| Driver to Motors | 20 AWG | Medium current |
| 5V Power | 22 AWG | Low current |
| Servo Signals | 24-26 AWG | Very low current |
| Servo Power | 20-22 AWG | Medium current (multiple servos) |

## Final Notes

- **Always disconnect battery** when working on wiring
- **Test incrementally** - don't connect everything at once
- **Document changes** - take photos before and after
- **Keep spare parts** - extra wires, connectors, fuses
- **Safety first** - if unsure, ask for help

---

For questions about wiring, consult:
- Arduino Forums
- Electronics Stack Exchange
- Local maker space
- Electronics instructor
