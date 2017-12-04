# pypot dynamixel library
import pypot.dynamixel as pd
# threading for motor control
import threading

# get ports
# USB2AX will be the first result
ports = pd.get_available_ports()

# connect to port
motors = pd.DxlIO(ports[0], 1000000)
# motors = pd.DxlIO(ports[0], 57600)
# get list of motors
print 'Scanning for motors...'
motor_list = motors.scan()
print 'Found motors: ' + str(motor_list)


def set_speed(motor, speed):
    motors.set_moving_speed({motor:speed})

def move_wheel(motor, speed):
    # t = threading.Thread(target=set_speed,args=(motor,speed))
    # t.start()

    # motors.set_torque_limit({motor:100})
    # motors.set_moving_speed({motor: speed})
    motors.enable_torque({motor})
    motors.set_torque_limit({motor:100})
    motors.set_moving_speed({motor: speed})
    # t = threading.Thread(target=load_thread,args=(motor))
    # t.start()
    print "Moving motor "+str(motor)+" speed "+str(speed)
    while(1):
        try:
            load = motors.get_present_load({motor})[0]
            # print load
            # load == 100 indicates stalling at top or bottom
            if (abs(abs(load)-96)<2):
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            motors.set_moving_speed({motor: 0})
            break

def get_load(motor):
    return motors.get_present_load({motor})

# def load_thread(motor):
#     while(1):
#         try:
#             load = get_load(motor)
#             if (load==100):
#                 return 'up'
#             elif(load==-100):
#                 return 'down'
#         except KeyboardInterrupt:
#             break
