#!/usr/bin python3
from collections import OrderedDict
from teacher import PiggyParent
import sys
import time

class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 80
        self.RIGHT_DEFAULT = 80
        self.SAFE_DISTANCE = 300
        self.close_distance  = 30
        self.MIDPOINT = 1600  # what servo command (1000-2000) is straight forward for your bot?
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)
        self.load_defaults()
        
    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        
    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "s": ("Shy", self.shy),
                "f": ("Follow", self.follow),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''

    def dance(self):
        """A higher-ordered algorithm to make your robot dance"""
        print("Dance Time")
        if not self.safe_to_dance():
            return False #shut down the dance
        #dance methods
        self.forward_serpintine()
        self.forward_twirl_backward_twirl()
        self.Shuffle()
        self.spin()
        self.fwd_look_left_back_look_right_spin()
    def safe_to_dance(self):
        """ does a 360 distance check and returns true if safe"""
        #check for all fail/early-termination conditions
        for _ in range(4):
            if self.read_distance()< 300:
                print("not safe to dance!")
                return False
            else:
                self.turn_by_deg(90)
        print("safe to dance, Brah!")        
        return True

    #first dance
    def forward_serpintine(self):
        """moves forward and turns slightly left and right while going forward"""    
        for x in range(4):
            self.left(primary=100, counter=0)
            time.sleep(1)
            self.stop() 
            self.right(primary=100, counter=0)
            time.sleep(1)
            self.stop()

    #second dance
    def forward_twirl_backward_twirl(self):
        """goes forward and spins then stops and goes back and spins again"""
        for x in range(4):
            self.left(primary=100, counter=0)
            time.sleep(1)
            self.stop() 
            self.right(primary=100, counter=0)
            time.sleep(1)
            self.stop()

    #third dance
    #from Quinn
    def Shuffle(self):
        """shuffles backward"""    
        for x in range(35):
            self.right(primary=-60, counter=0)
            time.sleep(.1)
            self.left(primary=-60, counter=0)
            time.sleep(.1)
            self.stop()

    #fourth dance       
    def spin(self):
        """goes in a forward spin then stops and goes in a backward spin"""    
        for x in range(4):
            self.right(primary=100,counter=0)
            time.sleep(2)
            self.back()
            time.sleep(2)
            self.left(primary=100, counter=0)
            self.stop()

    #fith dance
    def fwd_look_left_back_look_right_spin(self):
        """goes forward then servo looks left then goes backward and looks right"""    
        for x in range(4):
            self.fwd()
            time.sleep(2)
            self.servo(2000)
            time.sleep(1)
            self.back()
            time.sleep(2)
            self.servo(1000)
            self.stop()

    
    def shake(self):  
        self.deg_fwd(720)
        self.stop()

    def example_move(self):
        """this is an example dance move that should be replaced by student-created content"""
        self.right() # start rotating right
        time.sleep(1) # turn for a second
        self.stop() # stop
        self.servo(1000) # look right
        time.sleep(.25) # give your head time to move
        self.servo(2000) # look left



    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 20):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()
        # sort the scan data for easier analysis
        self.scan_data = OrderedDict(sorted(self.scan_data.items()))

    def right_or_left(self):
        """ Should i turn left or right? returns a 'r' or 'l' based on scan data """
        self.scan()
        # avarage up the distances on the right side
        right_sum = 0
        right_avg =0
        left_sum = 0
        left_avg = 0

        # analyze scan results
        for angle in self.scan_data:
            # average up the distances on the right side
            if angle < self.MIDPOINT:
                right_sum += self.scan_data[angle]
                right_avg += 1
            else:
                left_sum += self.scan_data[angle]
                left_avg += 1
        
        # calculate averages
        left_avg = left_sum / left_avg
        right_avg = right_sum / right_avg

        if left_avg > right_avg:
            return 'l'
        else:
            return 'r'

        



    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        # do a scan of the area in front of the robot
        for x in range(4):
            self.turn_by_deg(90)

        self.scan()
        # Figure out how many obstacles there are 
        see_an_object = False
        count = 0
          
        # print the results
        for angle in self.scan_data:
            dist = self.scan_data[angle]
            if dist < self.SAFE_DISTANCE and not see_an_object:
                see_an_object = True
                count += 1
                print("~~~ I SEE SOMETHING!!! ~~~~")
            elif dist > self.SAFE_DISTANCE and see_an_object:
                see_an_object = False
                print(" I geuss the object ended")

            print("ANGLE: %d | DIST %d" % (angle, dist))
        print("\inI saw %d objects" % count)
            

    def quick_check(self):
        """ Moves the servo to three angles and preforns a distance check """
        # loop three times and move the servo
        for ang in range(self.MIDPOINT- 100, self.MIDPOINT + 101, 100):
            self.servo(ang)
            time.sleep(.1)
            if self.read_distance() < self.SAFE_DISTANCE:
                return False 

        # if the three-part check didnt freak out 
        return True

    def turn_until_clear(self):
        """ Rotate right until no obsticle is seen """
        print ("---!!!Turning until clear!!")
        # make sure we are looking straight
        self.servo(self.MIDPOINT)
        while self.read_distance() < self.SAFE_DISTANCE:
            self.left(primary=40, counter=-40)
            time.sleep(0.5)



        self.stop()

    def nav(self):
        """ Auto pilot """
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")

        exit_ang = self.get_heading()
        # because ive written down the exits angle, at anytime i can use:
        # self.turn_to_deg(exit_ang)
        turn_count = 0
        
        while True:
            if not self.quick_check():
                self.stop()
               # self.turn_until_clear()
                if turn_count > 3 and turn_count % 5 == 0:
                    self.turn_to_deg(exit_ang)
                elif'l' in self.right_or_left():
                    self.turn_by_deg(-45)
                else:
                    self.turn_by_deg(45)

                turn_count += 1

            else:
                self.fwd()

        # TODO: scan so we can decide left or right
        # TODO: average the right side of the scan dict
        # TODO: average the left side of the scan dict
        


###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
