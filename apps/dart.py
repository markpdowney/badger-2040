import badger2040
import urequests
import xmltok
import io

WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT
URL = "http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML?StationDesc=Malahide"

display = badger2040.Badger2040()
display.set_font("bitmap8")
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)
display.connect()

class Train:
    def __init__(self, prop1, prop2, prop3, prop4, prop5, prop6):
        self.Refreshtime = prop1
        self.Traincode = prop2
        self.Destination = prop3
        self.Expdepart = prop4
        self.Schdepart = prop5
        self.Direction = prop6
       
def format_date_time(iso_date_time):
    # Split the date and time parts
    date_part, time_part = iso_date_time.split('T')
    # Split the date into year, month, and day
    year, month, day = map(int, date_part.split('-'))
    # Split the time into hour, minute, and second
    hour, minute, second = time_part.split(':')
    second, _ = second.split('.')  # Split the seconds into whole seconds and fractional seconds
    hour, minute, second = map(int, [hour, minute, second])  # Convert to integers

    # Format the date and time in the desired format
    formatted_date_time = "{:02d}:{:02d} {:02d}{}".format(hour, minute, day, month)

    return formatted_date_time

def get_data():
    trains = []
    
    print(f"Requesting URL: {URL}")
    xml_response = urequests.get(URL)
    xml_str = xml_response.content.decode()  # Convert bytes to string
    tokenizer = xmltok.tokenize(io.StringIO(xml_str))
    
    token, value, *_ = next(tokenizer)

    while True:
        #is this next token the start of a train
        if token == xmltok.START_TAG and value[1] == "objStationData":                      
            train = Train(xmltok.text_of(tokenizer,'Servertime'), xmltok.text_of(tokenizer,'Traincode'),xmltok.text_of(tokenizer,'Destination'),xmltok.text_of(tokenizer,'Expdepart'),xmltok.text_of(tokenizer,'Schdepart'),xmltok.text_of(tokenizer,'Direction'))
            trains.append(train)
        
        try:
            token, value, *_ = next(tokenizer)
        except StopIteration:
            print("err")
            break

    trains = [train for train in trains if train.Direction != 'Northbound']
    return trains

def draw_dart():
    trains = get_data()
    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    
    # Title Text
    pretty_date  = format_date_time(trains[0].Refreshtime)
    display.text(f"Next South Trains {pretty_date}",0,0)
    
    
    # Header Row
    display.rectangle(0,20,WIDTH,20)
    display.set_pen(15)
    display.text("No.",0,22,WIDTH,1)
    display.text("Dest.",60,22)
    display.text("Sch.",180,22)
    display.text("Est.",240,22)
    display.set_pen(0)
    
    # Display Train info
    display.text(trains[0].Traincode,0,42,WIDTH,2)
    display.text(trains[0].Destination,60,42,WIDTH,2)
    display.text(trains[0].Expdepart,180,42,WIDTH,2)
    display.text(trains[0].Schdepart,240,42,WIDTH,2)
    
   
    
    
    
    display.update()
    
#get_data()
draw_dart()

while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    display.keepalive()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()
