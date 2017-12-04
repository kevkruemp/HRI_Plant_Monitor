# pypot dynamixel library
import pypot.dynamixel as pd

# get ports
# USB2AX will be the first result
ports = pd.get_available_ports()

# connect to port
motors = pd.DxlIO(ports[0], 1000000)
# get list of motors
print 'Scanning for motors...'
motor_list = motors.scan()
print 'Found motors: ' + str(motor_list)

def move_wheel(motor, speed):
    motors.set_moving_speed({motor: speed})
    print "Moving motor "+str(motor)+" speed "+str(speed)
    while(1):
        try:
            load = motors.get_present_load({motor})[0]
            # load == 100 indicates stalling at top or bottom
            if (abs(load)==100):
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            motors.set_moving_speed({motor: 0})
            break

def get_load(motor):
    return motors.get_present_load({motor})