from urllib.request import urlopen
import json
import time
from neopixel import *

apikey="YOUNEEDYOUROWNKEYHERE" # get a key from https://developer.forecast.io/register
lati ="52.11394"  #find your latitude and longitude from google maps. 
longi = "0.08045"


LED_COUNT   = 240     # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

#function that colours in the strip given the colour and the range
def goColour(strip, color, start, end):       
    for i in range(start, end+1):        
        strip.setPixelColor(i, color)
        strip.show()	        
		
#setup the strip
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

try:  
    goColour(strip, Color(0, 0, 0), 0, 239) #clear the strip
    oldTemp = 0   
        
    #get the data from the api website
    url="https://api.forecast.io/forecast/"+apikey+"/"+lati+","+longi+"?units=si"
        
    #in case the Internet is not working: try it but then use the oldTemp just in case
    try:
        meteo=urlopen(url).read()
        meteo = meteo.decode('utf-8')
        weather = json.loads(meteo)        
        currentTemp = weather['currently']['temperature']        
    except IOError:           
        currentTemp = oldTemp
    
    oldTemp = currentTemp #set oldTemp to last known temperature
        
    #let's colour! It's always going to be < 0, white:
    goColour(strip, Color(255, 255, 255), 0,34)  #white    
    
    if currentTemp > 0:
        goColour(strip, Color(0, 0, 255), 35, 69)  # blue
    if currentTemp > 5:
        goColour(strip, Color(0, 255, 255), 70, 99)  # purple
    if currentTemp > 10:
        goColour(strip, Color(255, 0, 0), 100, 134) # green
    if currentTemp > 15:
        goColour(strip, Color(255, 255, 0), 135, 169)  # yellow
    if currentTemp > 20:
        goColour(strip, Color(100, 255, 0), 170, 209)  #orange
    if currentTemp > 25: #will this ever happen in Yorkshire??
        goColour(strip, Color(0, 255, 0), 210, 239)  # Red                  
	
except KeyboardInterrupt:
	print("Exit")
	goColour(strip, Color(0,0,0), 0, 240)