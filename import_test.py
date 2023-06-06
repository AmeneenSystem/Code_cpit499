import unittest
import etractlocation

class testDetect(unittest.TestCase):
  
     lat,long = etractlocation.calculatecoor("IMG_1132.jpg")
     lat,long = etractlocation.calculatecoor("IMG_1132.jpg")
     assert lat==21.515905555555555
 

 