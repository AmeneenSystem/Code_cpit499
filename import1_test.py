import unittest
import etractlocation

class testing(unittest.TestCase):
   lat,long = etractlocation.calculatecoor("IMG_1132.jpg")
   assert lat== 23.515905555555555