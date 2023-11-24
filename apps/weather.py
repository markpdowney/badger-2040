# This example grabs current weather details from Open Meteo and displays them on Badger 2040 W.
# Find out more about the Open Meteo API at https://open-meteo.com

import badger2040
from badger2040 import WIDTH
import urequests
import jpegdec
import io
import xmltok
import gc



WIDTH = badger2040.WIDTH


# Set your latitude/longitude here (find yours by right clicking in Google Maps!)
LAT = 53.450722
LNG = -6.1542727

URL = "http://metwdb-openaccess.ichec.ie/metno-wdb2ts/locationforecast?lat=" + str(LAT) + ";long=" + str(LNG)
# Display Setup
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(2)
jpeg = jpegdec.JPEG(display.display)
# Connects to the wireless network. Ensure you have entered your details in WIFI_CONFIG.py :).
display.connect()

class weather_hour:
    def __init__(self, prop1, prop2, prop3, prop4, prop5, prop6, prop7, prop8, prop9):
        self.start_time = prop1,
        self.end_time = prop2
        self.temp = prop3
        self.beaufort = prop4
        self.rain_min = prop5
        self.rain_max = prop6
        self.rain_prob = prop7
        self.desc = prop8
        self.desc_code = prop9


def get_data():   
    weathers = []
    
    print(f"Requesting URL: {URL}")
    xml_bytes = urequests.get(URL)
    
    xml_str = xml_bytes.content.decode()  # Convert bytes to string
    tokenizer = xmltok.tokenize(io.StringIO(xml_str))
    print("Data obtained!")

    i = 0
    in_block_a = False
    in_block_b = False
        
    while i < 4:        
        
        
        gc.collect()
        
        tmp_start = ""
        tmp_end = ""
        tmp_temp = ""
        tmp_wind = ""
        tmp_pcp_min = ""
        tmp_pcp_max = ""
        tmp_pcp_prb = ""
        tmp_desc = ""
        temp_desc_code = ""
        
        token, tag, *attr = next(tokenizer)
        
        if token == xmltok.START_TAG and tag[1] == "time":
            in_block_a = True
            
            #skip tag
            token, tag, *attr = next(tokenizer)
            token, tag, *attr = next(tokenizer)
            tmp_start = attr[0]
            token, tag, *attr = next(tokenizer)
            tmp_end = attr[0]
            token, tag, *attr = next(tokenizer)
            
            while in_block_a:
                
                if token == xmltok.START_TAG and tag[1] == "temperature":
                    token, tag, *attr = next(tokenizer)
                    token, tag, *attr = next(tokenizer)
                    token, tag, *attr = next(tokenizer)
                    tmp_temp = attr[0]
                    token, tag, *attr = next(tokenizer)
                
                if token == xmltok.START_TAG and tag[1] == "windSpeed":
                    token, tag, *attr = next(tokenizer)
                    token, tag, *attr = next(tokenizer)
                    token, tag, *attr = next(tokenizer)
                    tmp_wind = attr[0]
                
                
                if token == xmltok.END_TAG and tag[1] == "time":
                    in_block_a = False
                
                token, tag, *attr = next(tokenizer)
                
        
        if token == xmltok.START_TAG and tag[1] == "time":
            in_block_b = True
            
            while in_block_b:                
                if token == xmltok.START_TAG and tag[1] == "precipitation":
                    token, tag, *attr = next(tokenizer)
                    token, tag, *attr = next(tokenizer)
                    token, tag, *attr = next(tokenizer)
                    tmp_pcp_min = attr[0]
                    token, tag, *attr = next(tokenizer)
                    tmp_pcp_max = attr[0]
                    token, tag, *attr = next(tokenizer)
                    tmp_pcp_prb = attr[0]
                    token, tag, *attr = next(tokenizer)
                    token, tag, *attr = next(tokenizer)
                    
                if token == xmltok.START_TAG and tag[1] == "symbol":
                    token, tag, *attr = next(tokenizer)
                    tmp_desc = attr[0]
                    token, tag, *attr = next(tokenizer)
                    tmp_desc_code = attr[0]
                    tmp_weather = weather_hour(tmp_start,tmp_end,tmp_temp, tmp_wind,tmp_pcp_min,tmp_pcp_max,tmp_pcp_prb,tmp_desc,tmp_desc_code)
                    weathers.append(tmp_weather)
                    i += 1
                    
                
                if token == xmltok.END_TAG and tag[1] == "time":
                    in_block_b = False
                    break
        
                token, tag, *attr = next(tokenizer)
        
    
    return weathers

# Approximate center lines for four sections
centers = (30,90,150,210,270)

def draw_page():
    weathers = get_data()
    
    # Clear the display
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

    # Draw the page header
    display.set_font("bitmap6")
    display.set_pen(0)
    display.rectangle(0, 0, centers[0]*2, badger2040.HEIGHT)
    display.rectangle(0, 0, WIDTH, 20)
    display.set_pen(15)
    display.text("Malahide Weather", 3, 4)
    display.set_pen(0)

    display.set_font("bitmap8")
    
    # row values
    display.set_pen(15)
    x = centers[0]
    label = "Hour"
    w = display.measure_text(label, 2)
    display.text(label,int(x - (w / 2)),22, 3, 2)
    label = "Temp"
    w = display.measure_text(label, 2)
    display.text(label,int(x - (w / 2)),44, 3, 2)
    label = "Rain"
    w = display.measure_text(label, 2)
    display.text(label,int(x - (w / 2)),66, 3, 2)
    label = "Prob%"
    w = display.measure_text(label, 2)
    display.text(label,int(x - (w / 2)),88, 3, 2)
    
    display.set_pen(0)
    
    
    count = 1
    
    for i in weathers:
        
        x = centers[count]
        
        label = i.start_time[0][11:13]
        w = display.measure_text(label, 2)
        display.text(label,int(x - (w / 2)),22,WIDTH,2)
        
        label = i.temp
        w = display.measure_text(label, 2)
        display.text(label,int(x - (w / 2)),44,WIDTH,2)
        
        label = i.rain_max
        w = display.measure_text(label, 2)
        display.text(label,int(x - (w / 2)),66,WIDTH,2)
        
        label = i.rain_prob
        w = display.measure_text(label, 2)
        display.text(label,int(x - (w / 2)),88,WIDTH,2)
        
        count += 1

    display.update()

draw_page()

# Call halt in a loop, on battery this switches off power.
# On USB, the app will exit when A+C is pressed because the launcher picks that up.
while True:
    display.keepalive()
    display.halt()
