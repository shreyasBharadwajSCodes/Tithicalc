from datetime import date,datetime,timedelta
import requiredfunctionality as rf


class VaarHora:
    __actual_divisions = 168
    def __init__(self,steps_per_division):
        self.steps_per_division = steps_per_division
        self.small_angle = 360 /(self.__actual_divisions * self.steps_per_division)
        pass
    
    def setParameters(self,steps_per_division):
        self.steps_per_division = steps_per_division
        pass
    
    def update(self):
        self.vaar = rf.vaar(rf.gregorian_to_jd())
        pass
    
    def performCalculation(self,dt,tm):
        self.dateobj = date(dt[0],dt[1],dt[2]) #Make Changes Here
        self.sr1 = rf.sunrise(rf.gregorian_to_jd(self.dateobj),rf.place_details)
        if (timedelta(hours = self.sr1[1][0],minutes = self.sr1[1][1],seconds = self.sr1[1][2]) >=
            timedelta(hours = tm[0],minutes=tm[1],seconds = tm[2])):
            self.sr2 = rf.sunrise(rf.gregorian_to_jd(date(dt[0],dt[1],dt[2])+timedelta(days = 1)),rf.place_details)
        else:
            self.sr2,self.sr1 = self.sr1 ,rf.sunrise(rf.gregorian_to_jd(date(dt[0],dt[1],dt[2]) - timedelta(days = 1)),rf.place_details)
        self.quanta = timedelta(hours = self.sr2[1][0] + 24,minutes = self.sr2[1][1],seconds = self.sr2[1][2]) - timedelta(hours = self.sr1[1][0],minutes = self.sr1[1][1],seconds = self.sr1[1][2])
        self.quanta = self.quanta / (24 * self.steps_per_division)
        #print(self.quanta)
        pass
    
    def timeQuanta(self):
        """ Returns answer in time quantum terms """
        pass

"""
    Circle Util returns value in degrees for the spoke to point at.
    
    *Variables
    
    -> offset : Starting offset (Can be used to caliberate the device's base angle)
                ** does NOT depend on rotateaxis **
                
    -> rotateaxis : -1 in case of anti-clockwise movements, any other value is taken as clockwise
    
    -> deg : Stores actual degree ---> initialized based on rotation axis
    
    -> exceptionflag : set to False, made true when Exception occurs 
    
    
    
    *Functions
    
    -> __init__ : Initializer
    
    -> actualDeg : Gives actual answer in degrees.
    
    -> spokeDeg : Returns where the spoke must point at presently.
    
    -> _moveDeg: Move by a certain degree from current position, always returns spokedeg
                 not actual degree
    -> _setDeg : Set a degree (Use Only if a system failure occurs)
    
    -> _setOffset : Set an offset (Use Only if a system failure occurs)
    
    -> _setRotateAxis : Set Rotation direction (Can be upgraded to speed rotations if required)
    
    -> _resetFlag : Reset exception flag to false
    
    
    *Lambdas
    
    -> _norm360 : fits final value in the range of [0,360) degrees
    
    
    *If Exception occurs
    
        -> __exceptionflag is set to true
        
        -> In __init__  (deg = 0 , offset = 0 , rotateaxis = 1 ) are set by default
        
        -> In setDeg deg is set to 0 
        
        -> In setOffset offset is set to 0
        
        -> In setRotateAxis Axis default is set to 1
    
"""
class CircleUtil:
    
    _norm360 = lambda self,degrees : degrees % 360
    
    __exceptionflag = False
    
    def __init__(
            self,offset = 0, 
            rotateaxis = 1,deg = 0):
        
        try :    
            self.__offset = self._norm360(float(offset))
            if rotateaxis != -1:
                self.__rotateaxis = 1
            else :
                self.__rotateaxis = -1
            
            self.__deg = self._norm360(self.__rotateaxis * float(deg))
        except :
            self.__deg = 0
            self.__offset = 0
            self.__rotateaxis = 1
            self.__exceptionflag = True
        
    
    def actualDeg(self):
        return self.__deg
    
    def spokeDeg(self):
        return self._norm360(self.__deg + self.__offset)
    
    def _moveDeg(self,move_deg):
        self.__deg = self._norm360(self.__deg + self.__rotateaxis * move_deg)
        return self.spokeDeg()
    
    def _setDeg(self,deg):
        try:
            self.__deg = self._norm360(float(deg))
            
        except :
            self.__deg = 0 
            self.__exceptionflag = True
            
        finally:
            return [self.__exceptionflag,self.__deg]
        
        
    def _setOffset(self,offset):
        try:
            self.__offset = self._norm360(float(offset))
            
        except:
            self.__offset = 0
            self.__exceptionflag = True
            
        finally:
            return [self.__exceptionflag,self.__offset]
    
    
    def _setRotateAxis(self,ra):
        try:
            if ra != -1:
                self.__rotateaxis = 1
            else:
                self.__rotateaxis = -1
        except : 
            self.__rotateaxis = 1      
            self.__exceptionflag = True
            
        finally:
            return [self.__exceptionflag,self.__rotateaxis]
        
    
    def _resetFlag(self):
        self.__exceptionflag = False
    
"""
    Yantra Util manages time , uses circle util to generate required degrees 
    
    
    *Variables and instances
    
    -> __cu : CircleUtil instance
    
    -> __yantra : holds Yantra Object
    
    -> __cdate : current date list -> yyyy , mm , dd
    
    -> __ctime : current time -> H , M , S
    
    *Functions
    
    -> yantraMoveNext : Call when spoke-trigger is necessary
"""

class YantraUtil:
    
    def __init__(self,yantraObject):
        self.getCurrentDateAndTime()
        #print(self.__ctime,self.__cdate)
        self.__cu = CircleUtil()
        self.__yantra = yantraObject
        #print(self.__cu._moveDeg(80))
    
    def getCurrentDateAndTime(self):
        """ Store Current Date and time """
        self.__cdate = datetime.now()
        self.__ctime = list(self.__cdate.timetuple())[3:6]
        self.__cdate = list(self.__cdate.timetuple())[:3]
        
    
    def yantraMoveNext(self):
        """ Move to next angle on the yantra """
        self.__yantra.performCalculation(self.__cdate,self.__ctime)
        #print(self.__cdate)
        #rint(self.__ctime)
        pass
    
    def checkLag(self):
        """ 
        Programatically check if there is any lag between current value 
        and actual degree being shown 
        Lag can exist due to decimals as well
        Note : To be done post disruption Calculations
        """
        pass

yu = YantraUtil(VaarHora(steps_per_division=3))
yu.yantraMoveNext()