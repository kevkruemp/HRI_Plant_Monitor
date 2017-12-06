# pypot dynamixel library
import pypot.dynamixel as pd
# threading for motor control
import threading
import time
import numpy as np

# get ports
# USB2AX will be the first result
ports = pd.get_available_ports()

# connect to port
motors = pd.DxlIO(ports[0], 1000000)
# get list of motors
print 'Scanning for motors...'
motor_list = motors.scan()
print 'Found motors: ' + str(motor_list)


def set_speed(motor, speed):
    motors.set_moving_speed({motor:speed})

# move wheel to limits
def move_to_limit(motor, speed):
    # while (abs(motors.get_moving_speed({motor})[0])<1):
    #     motors.set_torque_limit({motor:100})
    #     time.sleep(0.2)
    #     motors.set_moving_speed({motor: speed})
    #     time.sleep(0.2)
    #     print motors.get_moving_speed({motor})[0]

    print "Moving motor "+str(motor)+" speed "+str(speed)
    while(1):
        try:
            # keep trying to move the motors
            motors.set_torque_limit({motor:100})
            time.sleep(0.2)
            motors.set_moving_speed({motor: speed})
            time.sleep(0.2)
            load = motors.get_present_load({motor})[0]
            # print motors.get_moving_speed({motor})[0]
            # print load

            # load = +-96 indicates stalling 
            if (abs(load+np.sign(speed)*96)<2):
                raise KeyboardInterrupt

        # catch either keyboard interrupts or motor errors
        except KeyboardInterrupt, DxlTimeoutError:
            # stop the motor
            motors.set_moving_speed({motor: 0})
            break

def get_load(motor):
    return motors.get_present_load({motor})
