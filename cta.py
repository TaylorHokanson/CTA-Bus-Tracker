# CTA bus tracker
# www.taylorhokanson.com
# Requires a Raspberry Pi and Adafruit 7-segment display
# Get API key:  http://www.transitchicago.com/developers/traintrackerapply.aspx
# Get bus stop info:  http://www.transitchicago.com/riding_cta/how_to_guides/bustrackerlookup_stoplists.aspx

from bs4 import BeautifulSoup
from lxml import etree
import urllib2
import string
import time
import datetime
from lxml import etree
from Adafruit_7Segment import SevenSegment

segment = SevenSegment(address=0x70)
segment.setColon(False)

# Grand & Noble Eastbound
routeNumber = "your route number goes here"
stopID = "your stop ID goes here" 		
apiKey = "your API key goes here"			
updateFreq = 10

# variables that will hold individual predictions returned by API
predictionString = ""
predictionString2 = ""

# loop that runs forever
while(True):
	# the list we'll store predictions in
	allPredictionsList = list("")	
	
	# query CTA system for predictions
	url = "http://www.ctabustracker.com/bustime/api/v1/getpredictions?key=" + apiKey + "&rt=" + routeNumber + "&stpid=" + stopID
	content = urllib2.urlopen(url).read()	
	soup = BeautifulSoup(content)
		
	# loop that loads each bus prediction into list
	for tag in soup("prdtm"): 		
		allPredictionsList.append(tag.contents)	
		
	# error handling for first bus
	try:
		predictionString = allPredictionsList[0]
	except:
		predictionString = 'null'
		
	# error handling for next bus
	try:
		predictionString2 = allPredictionsList[1]
	except:
		predictionString2 = 'null'				
		
	# load current time hours/minutes into variables
	currentTime = str(datetime.datetime.now().time())
	currentHours = currentTime[0:2]
	currentMins = currentTime[3:5]
	
	# split prediction strings out into useful chunks
	predictionHours = predictionString[0][9:11]	
	predictionMins = predictionString[0][12:14]	
	predictionHours2 = predictionString2[0][9:11]	
	predictionMins2 = predictionString2[0][12:14]	
	
	if predictionString == "null":
		print("no bus 1")
		segment.writeDigitRaw(0, 0x08)		# underscore means no busses but I'm still working
		segment.writeDigitRaw(1, 0x08)
	if predictionString2 == "null":
		print("no bus 2")		
		segment.writeDigitRaw(3, 0x08)
		segment.writeDigitRaw(4, 0x08)				

	# if predictionString contains anything but null
	if (predictionString != "null"):
		# if closest bus will arrive within current hour
		if (currentHours == predictionHours):
			minEstimate = int(predictionMins) - int(currentMins)
			print("first arrival in " + str(minEstimate))
			# if less than ten minutes, set first digit to zero
			if int(minEstimate) <= 9:
				segment.writeDigit(0, 0)			
				segment.writeDigit(1, minEstimate)
			# if more than ten minutes, figure both first and second digits
			if int(minEstimate) >= 10:
				segment.writeDigit(0, int(str(minEstimate)[0:1]))			
				segment.writeDigit(1, int(str(minEstimate)[1:2]))
				
		# if closest bus will arrive within the next hour
		# includes condition when next hour is tomorrow
		if (int(predictionHours) == int(currentHours) + 1) or (int(currentHours) == 24) and (int(predictionHours) == 0):
			minEstimate = int(predictionMins) + 60 - int(currentMins)
			print("first arrival in " + str(minEstimate))
			if int(minEstimate) <= 9:
				segment.writeDigit(0, 0)			
				segment.writeDigit(1, minEstimate)
			# if more than ten minutes, figure both first and second digits
			if int(minEstimate) >= 10:
				segment.writeDigit(0, int(str(minEstimate)[0:1]))			
				segment.writeDigit(1, int(str(minEstimate)[1:2]))
	
	# if predictionString2 contains anything but null
	if (predictionString2 != "null"):		
	# if second closest bus will arrive within current hour
		if (currentHours == predictionHours2):
			minEstimate2 = int(predictionMins2) - int(currentMins)
			print("second arrival in " + str(minEstimate2))
			# if less than ten minutes, set first digit to zero
			if int(minEstimate2) <= 9:
				segment.writeDigit(3, 0)			
				segment.writeDigit(4, minEstimate2)
			# if more than ten minutes, figure both first and second digits
			if int(minEstimate2) >= 10:
				segment.writeDigit(3, int(str(minEstimate2)[0:1]))			
				segment.writeDigit(4, int(str(minEstimate2)[1:2]))
				
		# if second closest bus will arrive within the next hour
		# includes condition when next hour is tomorrow
		if (int(predictionHours2) == int(currentHours) + 1) or (int(currentHours) == 24) and (int(predictionHours2) == 0):
			minEstimate2 = int(predictionMins2) + 60 - int(currentMins)
			print("second arrival in " + str(minEstimate2))
			if int(minEstimate2) <= 9:
				segment.writeDigit(3, 0)			
				segment.writeDigit(4, minEstimate2)
			# if more than ten minutes, figure both first and second digits
			if int(minEstimate2) >= 10:
				segment.writeDigit(3, int(str(minEstimate2)[0:1]))			
				segment.writeDigit(4, int(str(minEstimate2)[1:2]))					
					
	time.sleep(updateFreq)	



