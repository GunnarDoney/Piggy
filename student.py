#!/usr/bin python3
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
        self.safe_distance = 300
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
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 3):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        pass

    def nav(self):
        """ Auto pilot """
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        
        # TODO: build self.quick_check() that does a fast, 3-part check instead of read_distance
        self.fwd()
        while True:
            if self.read_distance() < self.close_distance:
                self.stop()
                print("OH NO SOMETHING IS IN THE WAY!!")
                self.turn_by_deg(90)
                time.sleep(.1)
            else:
                self.fwd()
            time.sleep(.01)
        self.stop()
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
