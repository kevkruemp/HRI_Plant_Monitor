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

import datetime
test_file = open("./eval/eval"+str(datetime.datetime.now())+".txt",'w')

# debug flag
testing = 1

# typing tests
typing_tests = range(28,36)
# test conditions
# 1 = A:X, B:X
# 2 = A:O, B:X
# 3 = A:X, B:O
# 4 = A:O, B:O
test_cases = [1, 2, 3, 4]
test_cond = 0

# random time delays
# time_del = [10, 15, 20, 25, 30]
time_del = [15]
# subsys_list = ['Plants','Blinds']
subsys_list = ['Plants']
plants_cmd = ['1','2','3','4']
blinds_cmd = ['Raise','Lower']
# test for 2 min
time_test = 120
if (testing):
    time_del = [3]
    time_test = 10

# init current time
cur_time = 0

# give prompt
def cmd_prompt(subsys):
    global test_cond
    global test_file
    prompt_time = time.time()
    test_file.write(str(prompt_time)+" ")

    msg = "\"Alexa, tell smart lab to "
    if (subsys == 'Plants'):
        num_plants = random.choice([1,2])
        num_plants = 1
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

    # write end time to file
    end_time = time.time()
    test_file.write(str(end_time)+" "+str(end_time-prompt_time)+"\n")

if __name__ == "__main__":
    os.system('clear')
    global test_cond
    global test_file

    # tutorial
    while(1):
        e = raw_input("Tutorial: test evaluation modes (enter 1, 2, 3, 4). Enter \'e\' to continue. ")
        if (e == 'e' or e == ''):
            break
        else:
            test_cond = int(e)
            gal9000.put('evaluation','cond',e)
            if (test_cond>=3):
                blossom.cmd_blossom('happy2')
            else:
                blossom.cmd_blossom('reset')
            cmd_prompt(random.choice(subsys_list))

    print "Take typing tests 26 and 27"
    test_file.write(raw_input("Test 26 WPM: ")+"\n")
    test_file.write(raw_input("Test 27 WPM: ")+"\n\n")

    # start test
    print "Start test"
    num_tests = len(test_cases)
    if (testing):
        num_tests = 1
    for i in range(0,num_tests):

        # get the test condition
        test_cond = random.choice(test_cases)
        test_cases.remove(test_cond)
        # get the typing test
        type_test = random.choice(typing_tests)

        # write to test file
        test_file.write(str(test_cond)+"\n")
        
        # update firebase
        gal9000.put('evaluation', 'cond', str(test_cond))
        print raw_input("Test condition: "+str(test_cond)+". Press 'Enter' to continue")

        # start blossom if necessary (cond 3 or 4) and update fb
        if (test_cond>=3):
            blossom.cmd_blossom('happy','calm')
        else:
            blossom.cmd_blossom('reset')

        # init timer
        start = time.time()

        # check if test should end
        while (time.time()-start<time_test):
            cur_time = time.time()

            # choose random prompt time
            time_pause = random.choice(time_del)
            # override with uniform time delay
            # time_pause = 15
            
            # block until time to prompt
            while(time.time()-cur_time<time_pause):
                if (time.time()-start>time_test):
                    break
                pass

            # move blossom if necessary
            if (test_cond>=3):
                blossom.cmd_blossom('happy2')
            else:
                blossom.cmd_blossom('reset')

            # give command prompt
            cmd_prompt(random.choice(subsys_list))
        test_file.write(raw_input("Condition "+str(test_cond)+" WPM: ")+"\n\n")

    test_file.close()
