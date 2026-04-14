#this file is just to keep track of angles so that the AI model can read the angles and get to 
#know about its physical apperance

class ServoStates:
    def __init__(self):
        self.neck_left = 90
        self.neck_right = 90

    def get(self):
        return self.neck_left , self.neck_right
    
    def set(self,servo, angle):
        servo = angle       #remember the servo name must be taken out from class before using this
    