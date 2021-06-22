from psychopy.visual import Window, TextStim
from psychopy.core import Clock
from psychopy.event import waitKeys, getKeys, clearEvents
from psychopy import visual, event, core
import random
import glob, pandas

#Stimuli as images
path = "images/" 
images = glob.glob(path + "*kombi.png")
order_of_images = [0, 0, 1, 1, 2, 2, 3, 3] 
random.shuffle(order_of_images) 
event.globalKeys.add(key = 't', modifiers = ["ctrl"], func = core.quit)
key_list = ['f', 'k']
my_win = Window( [1000, 600], color='white' )
fixation = visual.ShapeStim(my_win, 
    vertices=((0, -0.05), (0, 0.05), (0,0), (-0.03,0), (0.03, 0)),
    lineWidth=3,
    closeShape=False,
    lineColor="black") #fixation cross 
instruction_page = TextStim(my_win, wrapWidth = 1.8, height = 0.09, color = 'black')
instruction_page.setText("Hello and welcome to the experiment! \n\nIn the following, you will see two different stimuli at a time. \
\nOne of them looks like a diamond, the other one like a square. \
\nYour task is to decide as quickly as possible whether the diamond shape is displayed on the right or on the left side of the screen. \
\nIf the diamond is on the right, press 'K'.\
\nIf the diamond is on the left press 'F'. \
\nWe start with a few test runs to make sure you understood the task correctly.\
\nPress 'space' when you are ready to start.")
instruction_page.draw()
my_win.flip()
waitKeys( keyList = ['space'] )
timer = Clock()

def display_procedure(img_1, img_2):
    fixation.draw() 
    my_win.flip() 
    timer.reset(0)
    while timer.getTime() < 2:
        continue
    display_image_for_time(img_1, 0.032, allow_key_press=False) #Prime 
    display_image_for_time(images[4], 0.048, allow_key_press=False) #Interstimulus Intercept 
    key_pressed, passed_time_1, key = display_image_for_time(img_2, 0.080, allow_key_press=True) #Target Stimulus
    if not key_pressed:
        key_pressed, passed_time_2, key = display_image_for_time(images[4], 2.00, allow_key_press=True) #time to react
        passed_time_1 = passed_time_1 + passed_time_2
        if not key_pressed:
            feedback = visual.TextStim(my_win, text = "too late", color = "red", height = 0.1)
            feedback.draw()
            my_win.flip() 
            timer.reset(0)
            while timer.getTime() < 1:
                continue
    return key_pressed, passed_time_1, key   #wenn key None = no answer


# Stimuli presentation, reaction time, keypressed
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
#Combination of experimental conditions


def run_trial(img_1, img_2, correct_key):
    key_pressed, passed_time, key = display_procedure(img_1, img_2)
    reaction_times.append(passed_time)
    if key_pressed and key[0] == correct_key: 
        input_correct.append(True)
    else:
        input_correct.append(False)
    
input_correct = []
reaction_times = []

for number in order_of_images:
    if number == 0:
        run_trial(img_1 = images[0], img_2 = images[1], correct_key = key_list[0])
    if number == 1:
        run_trial(img_1 = images[2], img_2 = images[1], correct_key = key_list[0])
    if number == 2:
        run_trial(img_1 = images[0], img_2 = images[3], correct_key = key_list[1])
    if number == 3:
        run_trial(img_1 = images[2], img_2 = images[3], correct_key = key_list[1])
      
    
            
print(reaction_times)
print(input_correct)
print(order_of_images)


# GL
# good task, so far good code
# output missing
# data to be saved per trial
# small: reassignment of objects unnecessary
