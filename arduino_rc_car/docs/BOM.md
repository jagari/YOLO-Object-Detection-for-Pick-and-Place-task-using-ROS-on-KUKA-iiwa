# Bill of Materials (BOM)

## Complete Parts List for Arduino RC Car with Robot Arm

### Core Electronics

| Item | Quantity | Specifications | Estimated Cost (USD) | Notes |
|------|----------|----------------|---------------------|-------|
| Arduino Mega 2560 | 1 | ATmega2560, 54 digital I/O pins | $20-30 | Recommended for multiple servos |
| L298N Motor Driver | 2 | Dual H-Bridge, 2A per channel | $6-10 (total) | One for front motors, one for back |
| DC Motors | 4 | 6V-12V, 100-200 RPM | $16-24 (total) | With mounting brackets |
| Servo Motor (Large) | 3 | MG996R or similar, 10kg-cm torque | $15-21 (total) | Base, Shoulder, Elbow |
| Servo Motor (Small) | 2 | SG90 or similar, 2kg-cm torque | $4-6 (total) | Wrist, Gripper |
| USB Webcam | 1 | 720p or higher, 30fps | $15-30 | Or Raspberry Pi camera |
| LiPo Battery | 1 | 7.4V 2S, 2200-3000mAh | $15-25 | With XT60 connector |
| Voltage Regulator | 1 | 5V 3A step-down (LM2596) | $5-8 | For servos and Arduino |
| USB Cable | 1 | Type A to Type B (for Arduino Mega) | $3-5 | Or Bluetooth module for wireless |

**Core Electronics Total: $99-159**

### Optional Electronics

| Item | Quantity | Specifications | Estimated Cost (USD) | Notes |
|------|----------|----------------|---------------------|-------|
| HC-05 Bluetooth Module | 1 | For wireless control | $5-8 | Alternative to USB cable |
| Ultrasonic Sensor | 2-4 | HC-SR04, for obstacle detection | $4-8 (total) | Optional enhancement |
| Battery Monitor | 1 | Voltage/current sensor | $3-5 | For battery monitoring |
| Power Switch | 1 | Heavy duty, 10A rating | $2-4 | For main power control |
| LED Indicators | 5 | Various colors | $2-3 (total) | Status indicators |
| Buzzer | 1 | 5V active buzzer | $1-2 | Audio feedback |

**Optional Electronics Total: $17-30**

### Mechanical Components

| Item | Quantity | Specifications | Estimated Cost (USD) | Notes |
|------|----------|----------------|---------------------|-------|
| RC Car Chassis | 1 | 4WD, 20-30cm length | $25-40 | With wheel mounts |
| Wheels | 4 | 65-80mm diameter | Usually included | Often comes with chassis |
| Acrylic/Aluminum Plate | 2-3 | 15x15cm or 20x20cm | $10-15 (total) | For mounting surfaces |
| Servo Brackets | 1 set | Standard servo horn brackets | $8-12 | For arm construction |
| Gripper Mechanism | 1 | 3D printed or metal | $5-15 | Can be DIY |
| Camera Mount | 1 | Adjustable bracket | $5-10 | Or 3D print |
| Standoffs/Spacers | 1 set | M3, various lengths | $5-8 | For mounting boards |
| Screws & Nuts | 1 set | M3, M4 assortment | $5-8 | Various lengths |
| Zip Ties | 1 pack | Various sizes | $3-5 | Cable management |
| Velcro Straps | 1 pack | For battery mounting | $3-5 | Reusable |

**Mechanical Total: $69-118**

### Electrical Components

| Item | Quantity | Specifications | Estimated Cost (USD) | Notes |
|------|----------|----------------|---------------------|-------|
| Breadboard | 1 | Half-size or full-size | $3-5 | For prototyping |
| Jumper Wires | 1 set | Male-Male, Male-Female, Female-Female | $5-8 | Various lengths |
| Power Cables | 3-4 | 18-20 AWG, with connectors | $5-10 (total) | For high current paths |
| Heat Shrink Tubing | 1 set | Various sizes | $5-8 | For insulation |
| Capacitors | 2-3 | 1000µF, 25V electrolytic | $2-4 (total) | For servo power filtering |
| Resistors | 5-10 | 220Ω, 1kΩ, 10kΩ | $1-2 (total) | For LEDs and voltage dividers |
| Fuse Holder | 1 | Inline, 10A | $2-3 | Safety |
| Fuses | 3-5 | 5A, 10A blade fuses | $2-3 (total) | Spares included |
| Solder & Flux | 1 set | Lead-free solder | $8-12 | If not already owned |
| Electrical Tape | 1 roll | Vinyl insulation tape | $2-3 | For wire bundling |

**Electrical Total: $35-58**

### 3D Printed Parts (Optional)

If you have access to a 3D printer:

| Item | Material | Estimated Cost | Notes |
|------|----------|----------------|-------|
| Robot Arm Base | PLA/PETG | $2-5 | Connects arm to car |
| Arm Segments | PLA/PETG | $5-10 | Upper arm, forearm |
| Gripper Mechanism | PLA/PETG | $3-5 | Two-finger or three-finger |
| Camera Mount | PLA | $1-3 | Adjustable angle mount |
| Electronics Enclosure | PLA | $3-5 | Protects Arduino and drivers |
| Servo Horn Adapters | PLA | $1-2 | Custom connections |

**3D Printing Total: $15-30** (material cost only)

STL files can be found on Thingiverse or designed custom for your needs.

### Tools Required

You'll need these tools for assembly (not included in cost):

| Tool | Notes |
|------|-------|
| Soldering Iron | For permanent connections |
| Wire Cutters/Strippers | For cable preparation |
| Screwdriver Set | Phillips and flathead |
| Hex Key Set | For servo horns and brackets |
| Multimeter | For testing connections and voltage |
| Hot Glue Gun | For temporary mounting |
| Drill (optional) | For making mounting holes |
| 3D Printer (optional) | For custom parts |

### Software (Free)

| Software | Purpose | Cost |
|----------|---------|------|
| Arduino IDE | Programming Arduino | Free |
| Python 3.x | Control scripts | Free |
| OpenCV | Computer vision | Free |
| YOLO (Darknet) | Object detection | Free |
| Fusion 360/FreeCAD | CAD (optional) | Free (for students/hobbyists) |

## Cost Summary

| Category | Minimum | Maximum | Recommended |
|----------|---------|---------|-------------|
| Core Electronics | $99 | $159 | $120 |
| Optional Electronics | $0 | $30 | $15 |
| Mechanical Components | $69 | $118 | $85 |
| Electrical Components | $35 | $58 | $45 |
| 3D Printed Parts | $0 | $30 | $20 |
| **TOTAL** | **$203** | **$395** | **$285** |

## Budget Options

### Minimum Viable Build (~$200)
- Skip optional electronics
- Use basic chassis kit
- Use cardboard/wood instead of acrylic
- Basic gripper mechanism
- No 3D printed parts

### Recommended Build (~$285)
- All core components
- Some optional electronics (Bluetooth, sensors)
- Quality mechanical parts
- Some 3D printed parts for better finish

### Premium Build (~$395)
- All components including optional
- Metal chassis and parts
- High-quality servos
- Full 3D printed custom parts
- Better camera

## Where to Buy

### Online Retailers (International)
- **Amazon** - Wide selection, fast shipping
- **AliExpress** - Cheapest options, slower shipping
- **Banggood** - Good for electronics and RC parts
- **eBay** - Mixed sellers, good for deals
- **Adafruit** - Quality components, good support
- **SparkFun** - Quality components, tutorials

### Specialized Stores
- **RobotShop** - Robot-specific components
- **Pololu** - Motors and drivers
- **ServoCity** - Servo brackets and mechanical parts
- **HobbyKing** - RC parts and batteries

### Local Options
- Electronics supply stores
- RC hobby shops
- Maker spaces (for 3D printing)
- University surplus sales

## Money-Saving Tips

1. **Buy Kits**: Complete chassis kits are often cheaper than individual parts
2. **Bundle Deals**: Buy servo sets, wire assortments
3. **Used Parts**: Check eBay, Facebook Marketplace for Arduino boards
4. **Alternative Brands**: Chinese brands (Arduino compatibles) work fine
5. **Group Buys**: Order with friends to save on shipping
6. **Wait for Sales**: Black Friday, Prime Day, etc.
7. **DIY Parts**: 3D print or fabricate what you can
8. **Salvage**: Reuse parts from old projects or electronics

## Alternatives and Substitutions

### Arduino Mega → Arduino Uno + PCA9685
- **Cost**: Similar
- **Pros**: PCA9685 provides 16 PWM channels for servos
- **Cons**: More complex wiring

### Metal Gear Servos → Standard Servos
- **Cost**: Save $10-15
- **Pros**: Cheaper
- **Cons**: Less torque, less durable

### LiPo Battery → NiMH Battery Pack
- **Cost**: Similar or cheaper
- **Pros**: Safer, simpler charging
- **Cons**: Heavier, lower capacity

### L298N → TB6612FNG
- **Cost**: Similar
- **Pros**: More efficient, less heat
- **Cons**: Slightly more complex

### Webcam → Raspberry Pi Camera
- **Cost**: Similar ($15-30)
- **Pros**: Better integration if using Pi
- **Cons**: Need Raspberry Pi

## What You Might Already Have

Check your workshop/parts bin for:
- Arduino boards
- Breadboard and wires
- Basic tools
- Old USB cables
- Power supplies
- Servos from old projects
- Batteries and chargers

This can reduce your cost significantly!

## Estimated Build Time

- **Hardware Assembly**: 4-6 hours
- **Wiring**: 2-3 hours
- **Software Setup**: 1-2 hours
- **Testing & Calibration**: 2-4 hours
- **Total**: ~10-15 hours for first-time build

## Notes

1. Prices are approximate and vary by location and retailer
2. Shipping costs not included
3. Tool costs not included (assume already owned)
4. Some items may be available in multipacks (better value)
5. Consider buying spares of commonly broken items (wires, connectors)

---

**Last Updated**: 2024
**Currency**: USD (adjust for your local currency)
