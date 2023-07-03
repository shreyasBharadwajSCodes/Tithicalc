class RashiNakshatra:
    def __init__(self):
        self.NakshatraList = ["Ashvini", "Bharani","Krutika", "Rohini", "Mrugasirisha", 
                          "Ardra" , "Punarvasu" , "Pushya" , "Ashlesha" , "Magha",
                          "Purvaphalguni","UttaraPhalguni","Hasta","Chitra","Swati",
                          "Vishakha","Anuradha","Jyeshtha","Mula", "Purvaashadha",
                          "Uttaraashadha","Shravana" , "Dhanishta" , "Shatabhisha",
                          "Purvabadrapada","Uttarabadrapada","Revati"]
            
    def pada(self,deg):
        nakshatradeg = 4 * 3.333 # 4 times 3degrees 20 min
        i = 1
        p = lambda num: num%4 + 1
        while (deg - i * nakshatradeg > 0):
            i = i+1
        return p(i)