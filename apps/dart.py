import badger2040
import urequests

WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT
URL = "https://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML?StationDesc=Malahide&NumMins=90&format=xml"

display = badger2040.Badger2040()
display.set_font("bitmap8")
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)

def get_data():
    print(f"Requesting URL: {URL}")
    r = urequests.get(URL)
    

def draw_dart():
    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    
    # Title Text
    display.text("Next Malahide Departures",0,0)
    
    
    # Header Row
    display.rectangle(0,20,WIDTH,20)
    display.set_pen(15)
    display.text("No.",0,22,WIDTH,1)
    display.text("Dest.",60,22)
    display.text("Sch.",140,22)
    display.text("Est.",200,22)
    display.set_pen(0)
    
    # Display Train info
    display.text("D829",0,42,WIDTH,2)
    display.text("Dundalk",60,42,WIDTH,2)
    display.text("23:04",140,42,WIDTH,2)
    display.text("23:05",200,42,WIDTH,2)
    display.text("E706",0,62,WIDTH,2)
    display.text("Connolly",60,62,WIDTH,2)
    display.text("23:40",140,62,WIDTH,2)
    display.text("23:40",200,62,WIDTH,2)
    display.text("D830",0,82,WIDTH,2)
    display.text("Dundalk",60,82,WIDTH,2)
    display.text("00:08",140,82,WIDTH,2)
    display.text("00:08",200,82,WIDTH,2)
    
    display.update()
    
draw_dart()

while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    display.keepalive()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()
