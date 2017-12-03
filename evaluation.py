import tkinter
root = tkinter.Tk()
tl = tkinter.Toplevel(root)
root.withdraw()
tl.withdraw()
tl.attributes('-topmost',True)
tl.lift()
tl.focus_force()

import tkMessageBox as tkm
import random
import time
import os

import firebase_control
from firebase_control import fb as gal9000

import blossom_control as blossom
blossom_add = blossom.blossom_add

# test conditions
# 1 = A:X, B:X
# 2 = A:O, B:X
# 3 = A:X, B:O
# 4 = A:O, B:O
test_cases = [1, 2, 3, 4]
test_cond = 0

time_del = [10, 15, 20, 25, 30]
time_del = [2]
# subsys_list = ['Plants','Blinds']
subsys_list = ['Plants']
plants_cmd = ['1','2','3','4']
blinds_cmd = ['Raise','Lower']
# test for 2 min
time_test = 120

cur_time = 0

# give prompt
def cmd_prompt(subsys):
    global test_cond

    msg = "Alexa, tell smart lab to "
    if (subsys == 'Plants'):
        msg = msg+"water plants: "
        for i in range(0,random.choice([1,2])):
            msg = msg+random.choice(plants_cmd)+" "
    elif (subsys == 'Blinds'):
        blinds_state = gal9000.get('blinds','state')
        if (blinds_state == 'up'):
            blinds_cmd = 'lower '
        elif(blinds_state == 'down'):
            blinds_cmd = 'raise '
        else:
            return
        msg = msg+blinds_cmd+"the blinds"

    if (test_cond<3):
        tkm.showwarning('Command',msg+"\nPress 'OK' when you are sure the action is being performed.",parent=tl)
    else:
        raw_input(msg+"\nPress 'Enter' when you are sure the action is being performed.")

    # move window to the top
    root.lift()
    root.update()
    tl.lift()
    tl.focus_force()

if __name__ == "__main__":
    global test_cond

    print "Start test"

    for i in range(0,4):
        # get the test condition
        test_cond = random.choice(test_cases)
        test_cases.remove(test_cond)
        # update firebase
        gal9000.put('evaluation', 'cond', str(test_cond))
        print raw_input("Test condition: "+str(test_cond)+". Press 'Enter' to continue")

        # start blossom if necessary (cond 3 or 4) and update fb
        if (test_cond>=3):
            blossom.cmd_blossom('happy','slow_look')

        # init timer
        start = time.clock()

        # check if test should end
        while (time.clock()-start<time_test):
            cur_time = time.clock()

            # choose random prompt time
            time_pause = random.choice(time_del)
            print time_pause
            
            # block until time to prompt
            while(time.clock()-cur_time<time_pause):
                pass

            # move blossom if necessary
            if (test_cond>=3):
                blossom.cmd_blossom('happy')

            # give command prompt
            cmd_prompt(random.choice(subsys_list))
