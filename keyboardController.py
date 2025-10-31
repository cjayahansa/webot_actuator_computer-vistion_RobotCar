
from controller import Robot
import numpy as np
import cv2

robot = Robot()

timestep = int(robot.getBasicTimeStep())

motor1 = robot.getDevice('motor1')
motor2 = robot.getDevice('motor2')
motor3 = robot.getDevice('motor3')
motor4 = robot.getDevice('motor4')
#left_motor = robot.getDevice('left wheel motor')

# right_motor.setPosition(float('inf'))
# left_motor.setVelocity(0.0)
motor1.setPosition(float('inf'))
motor2.setPosition(float('inf'))
motor4.setPosition(float('inf'))
motor3.setPosition(float('inf'))

#set motor speed 
#mekedi kiyanne rad/s kiyala
#positive forward
#negetive backword
#max speed is 6.28 is min is the same 
#max_speed , min_speed 
motor1.setVelocity(0.0)
motor2.setVelocity(0.0)
motor4.setVelocity(0.0)
motor3.setVelocity(0.0)

# keyboard
keyboard = robot.getKeyboard()
keyboard.enable(timestep)

# Gps sensor Enable
gps=robot.getDevice('gps')
gps.enable(timestep)


# IMU sensor Enable
imu = robot.getDevice('imu')
imu.enable(timestep)


# LinearMotor
linear_M = robot.getDevice('linear_m')
linear_M.setPosition(0.0)
linear_M.setVelocity(0.1)

#cammara
Camera = robot.getDevice('camera')
Camera.enable(timestep)

# linear_r_m motor
linear_r_m = robot.getDevice('linear_r_m')
linear_r_m.setPosition(float('inf'))
linear_r_m.setVelocity(0.0)
# speeds (tweak these numbers)

FORWARD_SPEED = 3.0
TURN_SPEED = 2.0
STOP_SPEED = 0.0

def FORWARD(FORWARD_SPEED):
     motor1.setVelocity(-1*FORWARD_SPEED)
     motor2.setVelocity(-1*FORWARD_SPEED)
     motor4.setVelocity(-1*FORWARD_SPEED)
     motor3.setVelocity(-1*FORWARD_SPEED)
    
    
def REVERSE(FORWARD_SPEED):
     motor1.setVelocity(FORWARD_SPEED)
     motor2.setVelocity(FORWARD_SPEED)
     motor4.setVelocity(FORWARD_SPEED)
     motor3.setVelocity(FORWARD_SPEED)
     
     
     
def TURN_LEFT(TURN_SPEED):
     motor1.setVelocity(-1*TURN_SPEED)
     motor2.setVelocity(-1*TURN_SPEED)
     motor4.setVelocity(TURN_SPEED)
     motor3.setVelocity(TURN_SPEED)
  
  
def TURN_RIGHT(TURN_SPEED):
     motor1.setVelocity(TURN_SPEED)
     motor2.setVelocity(TURN_SPEED)
     motor4.setVelocity(-1*TURN_SPEED)
     motor3.setVelocity(-1*TURN_SPEED)
  

# --- Motion control variables ---
current_position = 0.0     # starting position
step_size = 0.01           # how much to move each key press
max_position = 0.05        # max stop
min_position = 0.01       # min stop
linear_M.setPosition(current_position)  
  
while robot.step(timestep) != -1:

    FORWARD_SPEED = 10.0
    TURN_SPEED = 3.0
    STOP_SPEED = 0.0
    step_size = 0.01 
    
    #get the key values
    key = keyboard.getKey()
    print(key)
    
    position = gps.getValues()
    x, y, z = position
    print(f"Robot GPS Position -> x: {x:.2f}, y: {y:.2f}, z: {z:.2f}")
    
   # IMU orientation
    orientation = imu.getRollPitchYaw()  # Returns (roll, pitch, yaw)
    roll, pitch, yaw = orientation
    print(f"IMU -> roll: {roll:.2f}, pitch: {pitch:.2f}, yaw: {yaw:.2f}")

    motor1.setVelocity(0.0)
    motor2.setVelocity(0.0)
    motor4.setVelocity(0.0)
    motor3.setVelocity(0.0)
    
    linear_r_m.setVelocity(0.0)
    
    if key == 315:
       FORWARD(FORWARD_SPEED)
    elif key == 317:
        REVERSE(FORWARD_SPEED)
    elif key == 316:
        TURN_LEFT(TURN_SPEED)
    elif key == 314:
        TURN_RIGHT(TURN_SPEED)

        
    if key == ord('W'):
        current_position += step_size
        if current_position > max_position:
            current_position = max_position
        print(f"UP pressed: position = {current_position:.2f}")
        linear_M.setPosition(current_position)

    elif key == ord('S'):
        current_position -= step_size
        if current_position < min_position:
            current_position = min_position
        print(f"DOWN pressed: position = {current_position:.2f}")
        linear_M.setPosition(current_position)

    if key == ord('A'):
        linear_r_m.setVelocity(1.0)
    elif key == ord('B'):
        linear_r_m.setVelocity(-1.0)
        
    # image = Camera.getImage()
    # width = Camera.getWidth()
    # height = Camera.getHeight()

    # red_pixels = 0

    # for x in range(width):
        # for y in range(height):
            # r = Camera.imageGetRed(image, width, x, y)
            # g = Camera.imageGetGreen(image, width, x, y)
            # b = Camera.imageGetBlue(image, width, x, y)

            # Detect red color
            # if r > 150 and g < 100 and b < 100:
                # red_pixels += 1

    # print("Red pixels:", red_pixels)
    image = Camera.getImage()
    width = Camera.getWidth()
    height = Camera.getHeight()

    # Convert Webots image to OpenCV format
    img_array = np.frombuffer(image, np.uint8).reshape((height, width, 4))
    frame = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)

    # Convert to HSV (better for color detection)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red color ranges
     # --- RED COLOR ---
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)

    # --- YELLOW COLOR ---
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # --- BLUE COLOR ---
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

   # --- GREEN ---
    lower_green = np.array([40, 100, 100])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    # --- Dictionary of masks and rectangle colors ---
    color_masks = {
        "Red": (red_mask, (0, 0, 255)),
        "Yellow": (yellow_mask, (0, 255, 255)),
        "Blue": (blue_mask, (255, 0, 0)),
        "Green": (green_mask, (0, 255, 0))
    }

    # Detect and draw bounding boxes
    for color_name, (mask, bgr) in color_masks.items():
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 200:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), bgr, 2)
                cv2.putText(frame, color_name, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, bgr, 2)

    # Show camera view
    cv2.imshow("Color Detection", frame)
    cv2.waitKey(1)

cv2.destroyAllWindows()
