from datetime import date,timedelta
import requiredfunctionality  as rf

def standardizedhms(h,m,s):
    days = 0
    if h >= 24:
        days = h//24
        h = h%24
    return [days,h,m,s]

def extendedhours(days,h,m,s):
    return [abs(days)*24 + h,m,s]

def nakshatra_deg(cdate):
    return rf.lunar_longitude(rf.gregorian_to_jd(cdate))

class hora:
    def __init__(self):
        self.quanta = [24,0,0]
        n = 0
        # Difference of 24 hours
        self.vaar = rf.vaar(rf.gregorian_to_jd(date.today() + timedelta(days = n)))
        self.sr1 = rf.sunrise(rf.gregorian_to_jd(date.today() + timedelta(days = n)),rf.place_details)
        self.sr2 = rf.sunrise(rf.gregorian_to_jd(date.today()+timedelta(days=1+n)),rf.place_details)
        self.quanta = timedelta(hours = self.sr2[1][0] + 24,minutes = self.sr2[1][1],seconds = self.sr2[1][2]) - timedelta(hours = self.sr1[1][0],minutes = self.sr1[1][1],seconds = self.sr1[1][2])
        self.quanta = self.quanta / 24
        #extendedhours(self.quanta.days, self.quanta.hours)
        

class CalculateTithiPeriodically:
    def __init__(self):
        self.flag = False
        #self.today = date.today()
        self.today = date(2023,5,15) #yyyy mm dd
        self.tithi = rf.tithi(rf.gregorian_to_jd(self.today),rf.place_details)
        self.end_date = standardizedhms(self.tithi[1][0],self.tithi[1][1],self.tithi[1][2]) 
        self.tithi_end_date = self.today + timedelta(days=self.end_date[0])
        self.tithi_end_time = self.end_date[1:]
        self.current_tithi = self.tithi[0]
        if len(self.tithi) > 2:
            self.flag = True
        
    def update_tithi(self):
        #Check For Flag
        #if (not self.flag) or (self.today != date.today()):
        if (not self.flag):
            self.flag = False
            #self.today = date.today()
            self.tithi = rf.tithi(rf.gregorian_to_jd(self.today),rf.place_details)
            self.end_date = standardizedhms(self.tithi[1][0],self.tithi[1][1],self.tithi[1][2]) 
            self.tithi_end_date = self.today + timedelta(days=self.end_date[0])
            self.tithi_end_time = self.end_date[1:]
            self.current_tithi = self.tithi[0]
            if len(self.tithi) > 2:
                self.flag = True
            
        else:
            self.end_date = standardizedhms(self.tithi[3][0],self.tithi[3][1],self.tithi[3][2]) 
            self.tithi_end_date = self.today + timedelta(days=self.end_date[0])
            self.tithi_end_time = self.end_date[1:]
            self.current_tithi = self.tithi[2]
            self.flag = False
            

'''
    Tests below
'''
ctp = CalculateTithiPeriodically()
print(ctp.tithi_end_date)
print(ctp.current_tithi)
print(ctp.tithi_end_time)
print(ctp.tithi)

def test_tithi():
    paksha = None
    for yyyy in range(2023,2024):
        for mm in range(1,13):
            for dd in range(1,27):
                ctp.today = date(yyyy,mm,dd)
                ctp.update_tithi()
                if ctp.flag == True:
                    if ctp.current_tithi > 14:
                        paksha = "Krishna"
                    else :
                        paksha = "Shukla"
                    print("Date : ",ctp.today,",Tithi : ",ctp.tithi_end_time,ctp.current_tithi," ",paksha)
                    ctp.update_tithi()
                    if ctp.current_tithi > 14:
                        paksha = "Krishna"
                    else :
                        paksha = "Shukla"
                    print("Date : ",ctp.today,",Tithi : ",ctp.tithi_end_time,ctp.current_tithi," ",paksha)
                else: 
                    if ctp.current_tithi > 14:
                        paksha = "Krishna"
                    else :
                        paksha = "Shukla"
                    print("Date : ",ctp.today,",Tithi : ",ctp.tithi," ",paksha)
    
def nakshatra_name(deg):
    import datastorage as ds
    return {"Nakshatra Name" : ds.RashiNakshatra().NakshatraList[int(deg * 27/360)],"Pada":ds.RashiNakshatra().pada(deg)}
#Use this For Nakshatra Predcition
#print(rf.lunar_longitude(rf.gregorian_to_jd(ctp.today)))
#print(nakshatra_deg(date(2023,5,15)))
print(nakshatra_name(nakshatra_deg(date(2023,5,16))))
print("Experiment: ------")
print(nakshatra_name(nakshatra_deg(date(2023,11,27))))
print(nakshatra_name(nakshatra_deg(date(2023,11,28))))
print("---")

test_tithi()

h = hora()
print(h.vaar,h.sr1, h.sr2," Quanta :",h.quanta)
vaarlist = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
print(vaarlist[h.vaar])
""" For Hora : 0 - Sunday, 1 - Monday,.... 6 - Saturday """

'''
To - Do : 
    Test for two tithis  - Vridhi tithi done !
    Make arc for tithi based on the pictures
'''

