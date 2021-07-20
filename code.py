from psychopy.visual import Window, TextStim
from psychopy.core import Clock
from psychopy.event import waitKeys, getKeys, clearEvents
from psychopy import visual, event, core
import random
import psychopy.gui as gui
import glob, pandas
from datetime import datetime


#Stimuli as images
path = "images/" 
images = glob.glob(path + "*kombi.png")
order_of_images = [0, 0, 1, 1, 2, 2, 3, 3] # total of 6 trials per Experiment 
random.shuffle(order_of_images) #randomization of stimuli
event.globalKeys.add(key = 't', modifiers = ["ctrl"], func = core.quit)
key_list = ['f', 'k']
my_win = Window( [1000, 600], color='white' )
#Fixation cross 
fixation = visual.ShapeStim(my_win, 
    vertices=((0, -0.05), (0, 0.05), (0,0), (-0.03,0), (0.03, 0)),
    lineWidth=3,
    closeShape=False,
    lineColor="black")
#Input Feedback 
feedback = visual.TextStim(my_win, text = "too late", color = "red", height = 0.1)
correct_feedback = visual.TextStim(my_win, text = "correct key", color = "green", height = 0.1)
wrong_feedback = visual.TextStim(my_win, text = "wrong key", color = "red", height = 0.1)
key_feedback = visual.TextStim(my_win, text = "press either k or f", color = "red", height = 0.1)
#Give Participant a name/number with date 
expName = "subliminal_perception"
expinfo = {'participant': ""}
dlg = gui.DlgFromDict(dictionary=expinfo, title=expName)
if dlg.OK == False:
    core.quit()
expinfo['date'] = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
expinfo['expName'] = expName
#Elements for instruction page/ Page after Test Runs 
instruction_page = TextStim(my_win, text = "Hello and welcome to the experiment! \n\nIn the following, you will see two different stimuli at a time. \
\nOne of them looks like a diamond, the other one like a square. \
\nYour task is to decide as quickly as possible whether the diamond shape is displayed on the right or on the left side of the screen. \
\nIf the diamond is on the right, press 'K'.\
\nIf the diamond is on the left press 'F'. \
\nWe start with a few test runs to make sure you understood the task correctly.\
\nPress 'space' when you are ready to start.", wrapWidth = 1.8, height = 0.09, color = 'black', pos = [0, 0.4])
intro_image = visual.ImageStim(my_win, images[4], pos = [0,-0.55])
after_testrun = TextStim(my_win, text = "Well done.\nNow get ready for the experiment\nTo continue press 'space'.", wrapWidth = 1.8, height = 0.09, color = 'black', pos = [0, 0])
#Draw Instruction Page
intro_image.draw() 
instruction_page.draw()
my_win.flip()
waitKeys( keyList = ['space'] )
timer = Clock()

#Every function I Wrote is called in the next function so I start from bottom -> top.

#First I need a function which draws the Stimuli and returns if a key is pressed, the reaction time and the first pressed key. 
def display_image_for_time(img, time, allow_key_press=True):
    stimulus = visual.ImageStim(my_win, image = img, pos = [0,0]) 
    stimulus.draw()
    my_win.flip()
    timer.reset(0)
    while timer.getTime() < time:
        pressd = getKeys(key_list, timeStamped = timer)
        if pressd and allow_key_press:
            return True, timer.getTime(), pressd[0]   
        else:
          continue
    return False, timer.getTime(), None 

#The experiment sarts with a test run à 3 trials. 
#The functions for the test run are similiar to the ones I use for the actual experiment, except that I want to give feedback to every input the particitpant gives and that I dont randomize the combination of prime/target stiumuli. 

#This function describes the designs of the experiment with the following sequence: Fixation cross, prime stimuli, ISI, target stimuli and a white blank page.
#The participiant is allowed to press a key when the target simuli are presented and up to 2 seconds after stimuli presentation. If this time was exceed the particitpant gets a feedback ("Too late")
#The function returns if a key was pressed (TRUE/FALSE), the reaction time and the pressed key (k/f).
#It also gives the particitpant feedback if the pressed key was correct or if the reaction was too slow. 
def display_test_procedure(img_1, img_2, correct_key):
    fixation.draw() 
    my_win.flip() 
    timer.reset(0)
    while timer.getTime() < 2:
        continue
    display_image_for_time(img_1, 0.032, allow_key_press=False) #Prime 
    display_image_for_time(images[5], 0.048, allow_key_press=False) #Interstimulus Intercept 
    key_pressed, passed_time_1, key = display_image_for_time(img_2, 0.080, allow_key_press=True) #Target Stimulus
    if key_pressed:
        if key[0] == correct_key:
            correct_feedback.draw()
            my_win.flip()
            timer.reset(0)
            while timer.getTime() < 2:
                continue #Feedback if input is correct
        else:
            wrong_feedback.draw()
            my_win.flip()
            timer.reset(0)
            while timer.getTime() < 2:
                continue #Feedback if input is wrong 
    if not key_pressed:
        key_pressed, passed_time_2, key = display_image_for_time(images[5], 2.00, allow_key_press=True) #time to react
        passed_time_1 = passed_time_1 + passed_time_2
        if key_pressed:
            if key[0] == correct_key:
                correct_feedback.draw()
                my_win.flip()
                timer.reset(0)
                while timer.getTime() < 2:
                    continue #Feedback if input is correct
            else:
                wrong_feedback.draw()
                my_win.flip()
                timer.reset(0)
                while timer.getTime() < 2:
                    continue #Feedback if input is wrong 
        if not key_pressed:
            feedback.draw()
            my_win.flip() 
            timer.reset(0)
            while timer.getTime() < 1:
                continue #Feedback if participant is too slow
    return key_pressed, passed_time_1, key   
   
#This function decides if the returned information "key_pressed" is correct.
def run_test_run(img_1, img_2, correct_key):
    key_pressed, passed_time, key = display_test_procedure(img_1, img_2, correct_key)

#These are the tree combinations of prime/target stimuli for the test run.
run_test_run(img_1 = images[0], img_2 = images[1], correct_key = key_list[0]) 
run_test_run(img_1 = images[2], img_2 = images[3], correct_key = key_list[1])
run_test_run(img_1 = images[0], img_2 = images[3], correct_key = key_list[1])

#Display a screen to get the participant ready for the actual experiment 
after_testrun.draw()
my_win.flip()
waitKeys( keyList = ['space'] )

#I slightly modified the functions for the actual experiment. 
#This function describes the designs of the experiment with the following sequence: Fixation cross, prime stimuli, ISI, target stimuli and a white blank page.
#The participiant is allowed to press a key when the target simuli are presented and up to 2 seconds after stimuli presentation. If this time was exceed the particitpant gets a feedback ("Too late").
#This time no feedback if the input was correct/wrong.
#The function returns if a key was pressed (TRUE/FALSE), the reaction time and the pressed key (k/f).
def display_procedure(img_1, img_2):
    fixation.draw() 
    my_win.flip() 
    timer.reset(0)
    while timer.getTime() < 2:
        continue
    display_image_for_time(img_1, 0.032, allow_key_press=False) #Prime 
    display_image_for_time(images[5], 0.048, allow_key_press=False) #Interstimulus Intercept 
    key_pressed, passed_time_1, key = display_image_for_time(img_2, 0.080, allow_key_press=True) #Target Stimulus
    if not key_pressed:
        key_pressed, passed_time_2, key = display_image_for_time(images[5], 2.00, allow_key_press=True) #time to react
        passed_time_1 = passed_time_1 + passed_time_2
        if not key_pressed:
            feedback.draw()
            my_win.flip() 
            timer.reset(0)
            while timer.getTime() < 1:
                continue
    return key_pressed, passed_time_1, key   

#This function decides if the returned information "key_pressed" is correct. If it is correct it appends it as TRUE in the list input_correct, if it is wrong as FALSE. The function also appends the reaction times.
def run_trial(img_1, img_2, correct_key):
    key_pressed, passed_time, key = display_procedure(img_1, img_2)
    reaction_times.append(passed_time)
    if key_pressed and key[0] == correct_key: 
        input_correct.append(True)
    else:
        input_correct.append(False)

#Lists for input. 
input_correct = []
reaction_times = []

#The possible combinations of prime/target stimuli with the correct key. 
for number in order_of_images:
    if number == 0:
        run_trial(img_1 = images[0], img_2 = images[1], correct_key = key_list[0]) #correct key for this combination would be f
    if number == 1:
        run_trial(img_1 = images[2], img_2 = images[1], correct_key = key_list[0]) #correct key for this combination would be f
    if number == 2:
        run_trial(img_1 = images[0], img_2 = images[3], correct_key = key_list[1]) #correct key for this combination would be k
    if number == 3:
        run_trial(img_1 = images[2], img_2 = images[3], correct_key = key_list[1]) #correct key for this combination would be k

#Save input in a csv file with two columns. Reaction Times over 2.08 seconds are trials with no reaction.  
df = pandas.DataFrame(data={"Key Input_Correct": input_correct, "Reaction Time": reaction_times})
df.to_csv(f"{expinfo['expName']}_{expinfo['participant']}_{expinfo['date']}.csv", sep=',',index=False)
mylist = [input_correct, reaction_times]


# GL
# good task, so far good code
# output missing
# data to be saved per trial
# small: reassignment of objects unnecessary
