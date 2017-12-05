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

# typing tests
typing_tests = range(26,36)
# test conditions
# 1 = A:X, B:X
# 2 = A:O, B:X
# 3 = A:X, B:O
# 4 = A:O, B:O
test_cases = [1, 2, 3, 4]
test_cond = 0

time_del = [10, 15, 20, 25, 30]
# time_del = [2]
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

    msg = "\"Alexa, tell smart lab to "
    if (subsys == 'Plants'):
        num_plants = random.choice([1,2])
        msg = msg+"water plant"
        if (num_plants == 2):
            msg = msg+"s"
        msg = msg+":"
        for i in range(0,num_plants):
            if (i == 1):
                msg = msg+" and"
            msg = msg+" "+random.choice(plants_cmd)
        msg = msg+"\""
    elif (subsys == 'Blinds'):
        blinds_state = gal9000.get('blinds','state')
        if (blinds_state == 'up'):
            blinds_cmd = 'lower '
        elif(blinds_state == 'down'):
            blinds_cmd = 'raise '
        else:
            return
        msg = msg+blinds_cmd+"the blinds"

    # show prompt in new box if cond 1 or 2
    if (test_cond<3):
        tkm.showwarning('Command',msg+"\nPress 'OK' when you are sure the action is being performed.",parent=tl)
    # show prompt in terminal if cond 3 or 4
    else:
        raw_input(msg+"\nPress 'Enter' in this window when you are sure the action is being performed.")

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
        # get the typing test
        type_test = random.choice(typing_tests)
        
        # update firebase
        gal9000.put('evaluation', 'cond', str(test_cond))
        print raw_input("Test condition: "+str(test_cond)+". Press 'Enter' to continue")

        # start blossom if necessary (cond 3 or 4) and update fb
        if (test_cond>=3):
            blossom.cmd_blossom('happy','calm')

        # init timer
        start = time.time()

        # check if test should end
        while (time.time()-start<time_test):
            cur_time = time.time()

            # choose random prompt time
            time_pause = random.choice(time_del)
            # print time_pause
            
            # block until time to prompt
            while(time.time()-cur_time<time_pause):
                pass

            # move blossom if necessary
            if (test_cond>=3):
                blossom.cmd_blossom('happy2')

            # give command prompt
            cmd_prompt(random.choice(subsys_list))
