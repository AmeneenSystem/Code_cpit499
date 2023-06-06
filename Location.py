from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS #pip install pillow , PIL ,exif
from gmplot import gmplot #pip install gmplot
from geopy.geocoders import Nominatim #pip install geopy
import webbrowser
def get_exif(filename):
    exif_data = {}
    image = Image.open(filename)
    info = image._getexif()
    value = 0
    gps_data = {}
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for gps_tag in value:
                    sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded] = value[gps_tag]
                exif_data[decoded] = gps_data
                value = 1
                
            else:
                exif_data[decoded] = value

    return gps_data,value    
def calculatecoor(filename): 
    exif,num = get_exif(filename)
    if num == 0 :
        return 0,0
    else :
     la = str(exif["GPSLatitude"])
    
     long = str(exif["GPSLongitude"])
    
     values1 =la.strip('()').split(', ')
     values2 =long.strip('()').split(', ')
   
     firstnum = float(values1[0])
     secondnum = float(values1[1])/60
     thirdnum = float(values1[2])/3600
     finalnumber = firstnum+secondnum+thirdnum
     firstnum1 = float(values2[0])
     secondnum1 = float(values2[1])/60
     thirdnum1 = float(values2[2])/3600
     finalnumber1 = firstnum1+secondnum1+thirdnum1
     return finalnumber ,finalnumber1# store this

 
    
    

   
    
    print(latitude,longtitude)
    