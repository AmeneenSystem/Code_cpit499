from Ameneen import get_count_alarms
import unittest

class testDetect(unittest.TestCase):
    def testing(self):
      count,alarms,img = get_count_alarms("static/uploaded/2023-05-30_204746.258149_2023-05-30_160238.740558_2023-05-30_155224.058136_2023-05-29_202503.063414_2023-05-29_032243.961228_img_1214_jpg.rf.17e6bf103c9b6757670d06a65a56c997.jpg")

      self.assertEquals(count, 357)
       