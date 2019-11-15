import paho.mqtt.client as mqtt
import random
import json
import string
import datetime
import tkinter
from tkinter import *
from tkinter import ttk

top = tkinter.Tk()
top.title("A MQTT WeeWx Client")
## Setting Geometry and Layout
top.geometry("350x250+300+300")

showDate = StringVar()
showClient = StringVar()
showTemp = StringVar()
showOutH = StringVar()
showHumidex = StringVar()
showWindGust_kph = StringVar()
showWindGust_dir = StringVar()
showWindSpeed_kph = StringVar()
showWindDir = StringVar()

t_frame = LabelFrame(top, text="Temperature Info")
t_frame.grid(row = 0, column = 0, rowspan = 4, columnspan = 7, padx = 5, pady = 5, sticky = E+W+N+S)

w_frame = LabelFrame(top, text="Wind Info")
w_frame.grid(row = 0, column = 8, rowspan = 4, columnspan = 9, padx = 5, pady = 5, sticky = E+W+N+S)

s_frame = LabelFrame(top, text="Date & Client ID")
s_frame.grid(row = 10, column = 0, rowspan = 1, columnspan = 18, padx = 5, pady = 5, sticky = E+W+N+S)

showDate.set(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
showDate.set("Waiting for update")
dateLabel = Label(s_frame, textvariable = showDate)
dateLabel.grid(row = 0, column = 0, sticky = W)

clientLabel = Label(s_frame, textvariable = showClient)
clientLabel.grid(row = 0, column = 1, sticky = E)

tlabel_1 = Label(t_frame, text='Outdoor:')
tempLabel = Label(t_frame, textvariable = showTemp)
tlabel_1.grid(row = 1, column = 0, sticky = 'e')
tempLabel.grid(row = 1, column = 1, columnspan = 2, sticky = 'w')

tlabel_2 = Label(t_frame, text = 'Humidex:')
humidex = Label(t_frame, textvariable = showHumidex)
tlabel_2.grid(row = 2, column = 0, stick = 'e')
humidex.grid(row = 2, column = 1, columnspan = 2, sticky = 'w')

tlabel_3 = Label(t_frame, text = 'Humidity:')
humdLabel = Label(t_frame, textvariable = showOutH)
tlabel_3.grid(row = 3, column = 0, sticky = 'e')
humdLabel.grid(row = 3, column = 1, columnspan = 2, sticky = 'w')

wlabel_1 = Label(w_frame, text = 'Wind Gust (kph):')
windGustLabel = Label(w_frame, textvariable = showWindGust_kph)
wlabel_1.grid(row = 4, column = 0, sticky = 'e')
windGustLabel.grid(row = 4, column = 1, columnspan = 2, sticky = 'w')
windGustDirLabel = Label(w_frame, textvariable = showWindGust_dir)
windGustDirLabel.grid(row = 4, column = 3, sticky = 'w')

wlabel_2 = Label(w_frame, text = 'Wind Speed (kph):')
windSpeedLabel = Label(w_frame, textvariable = showWindSpeed_kph)
wlabel_2.grid(row = 5, column = 0, sticky = 'e')
windSpeedLabel.grid(row = 5, column = 1, columnspan = 2, sticky = 'w')
windDirLabel = Label(w_frame, textvariable = showWindDir)
windDirLabel.grid(row = 5, column = 3, sticky = 'w')
        
def on_message(client, userdata, message):
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message topic=",message.topic)
        print("message qos=",message.qos)
        print("message retain flag=",message.retain)
        print("client id=",userdata)
        #
        # convert payload to json
        #
        jmessage = json.loads(str(message.payload.decode("utf-8")))
        display_message(jmessage, userdata)
        
def display_message(jmessage,userdata):
        # date and time of readings
        dateTime = jmessage["dateTime"]
        dateTime = int(dateTime[0:-2])
        theTime = datetime.datetime.fromtimestamp(dateTime).strftime('%Y-%m-%d %H:%M:%S')
        # client id
        clientId = str(userdata)
        print(clientId)
        # current temperature
        outTempC = jmessage["outTemp_C"]
        outTempC = round(float(outTempC), 1)
        outTempCstr = str(outTempC) + "\u2103"
        # current humidity
        outHumd = jmessage["outHumidity"]
        outHumd = round(float(outHumd), 1)
        outHumdstr = str(outHumd) + "%"
        # current humidex
        outHumidex = jmessage["humidex_C"]
        outHumidex = round(float(outHumidex), 1)
        outHumidex = str(outHumidex) + "\u2103"
        # wind gust since last  update
        outWindGust_kph = jmessage["windGust_kph"]
        outWindGust_kph = round(float(outWindGust_kph), 1)
        #if outWindGust_kph <= 0.25:
        #        outWindGust_kph = "Calm"
        outWindGust_kph = str(outWindGust_kph)
        # wind gust direction
        if "windGustDir" in jmessage:
                outWindGust_dir = jmessage["windGustDir"]
                outWindGust_dir = round(float(outWindGust_dir),1)
                outWindGust_dir = str(outWindGust_dir)
                outWindGust_dir = degrees_to_cardinal(outWindGust_dir)
        else:
                outWindGust_dir = "-"
                
        # wind speed
        outWindSpeed_kph = jmessage["windSpeed_kph"]
        outWindSpeed_kph = round(float(outWindSpeed_kph), 1)
        outWindSpeed_kph = str(outWindSpeed_kph)
        #if outWindSpeed_kph <= 0.25:
        #        outWindSpeed_kph = "Calm"
        # wind direction
        if "windDir" in jmessage:
                outWindDir = jmessage["windDir"]
                #print(outWindDir)
                outWindDir = round(float(outWindDir),1)
                outWindDir = str(outWindDir)
                outWindDir = degrees_to_cardinal(outWindDir)
        else:
                outWindDir = "-"
        #
        # udpate labels
        #
        showDate.set(theTime)
        showClient.set(clientId)
        showTemp.set(outTempCstr)
        showOutH.set(outHumdstr)
        showHumidex.set(outHumidex)
        showWindGust_kph.set(outWindGust_kph)
        showWindGust_dir.set(outWindGust_dir)
        showWindSpeed_kph.set(outWindSpeed_kph)
        showWindDir.set(outWindDir)
        
def degrees_to_cardinal(degrees):
        if (float(degrees) > 348.75) and (float(degrees) <= 11.25):
                cardinal = 'N'
        if (float(degrees) > 11.25) and (float(degrees) <= 33.75):
                cardinal = 'NNE'
        if (float(degrees) > 33.75) and (float(degrees) <= 56.25):
                cardinal = 'NE'
        if (float(degrees) > 56.25) and (float(degrees) <= 78.75):
                cardinal = 'ENE'
        if (float(degrees) > 78.75) and (float(degrees) <= 101.25):
                cardinal = 'E'
        if (float(degrees) > 101.25) and (float(degrees) <= 123.75):
                cardinal = 'ESE'
        if (float(degrees) > 123.75) and (float(degrees) <= 146.25):
                cardinal = 'SE'
        if (float(degrees) > 146.25) and (float(degrees) <= 168.75):
                cardinal = 'SSE'
        if (float(degrees) > 168.75) and (float(degrees) <= 191.25):
                cardinal = 'S'
        if (float(degrees) > 191.25) and (float(degrees) <= 213.75):
                cardinal = 'SSW'
        if (float(degrees) > 213.75) and (float(degrees) <= 236.25):
                cardinal = 'SW'
        if (float(degrees) > 236.25) and (float(degrees) <= 258.75):
                cardinal = 'WSW'
        if (float(degrees) > 258.75) and (float(degrees) <= 281.25):
                cardinal = 'W'
        if (float(degrees) > 281.25) and (float(degrees) <= 303.75):
                cardinal = 'WNW'
        if (float(degrees) > 303.75) and (float(degrees) <= 326.25):
                cardinal = 'NW'
        if (float(degrees) > 326.25) and (float(degrees) <= 348.75):
                cardinal = 'NNW'
        #else:
        #        cardinal = 'N/A'
        
        return(cardinal)
        

broker_address="192.168.1.78"

#broker_port = 8883

#broker_address="iot.eclipse.org"

def generate_client():
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(8))

def main():
            
        print("creating new instance")
        uniqueId = generate_client()
        client = mqtt.Client(uniqueId)
        client.user_data_set(uniqueId)
        #create new instance
        client.on_message=on_message #attach function to callback
        print("connecting to broker")
        client.connect(broker_address) #connect to broker
        #client.loop_start() #start the loop
        client.loop()
        print("Subscribing to topic","weather/loop")
        client.subscribe("weather/loop")
        #print("Publishing message to topic","SYS$")
        #client.publish("SYS$","OFF")
        client.loop_start() #stop the loop
        top.mainloop()
        

if __name__=='__main__':
        main()
