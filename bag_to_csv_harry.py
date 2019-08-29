#!/usr/bin/env python

#Originally written by Nick Speal in May 2013 at McGill University's Aerospace Mechatronics Laboratory
#www.speal.ca
#Supervised by Professor Inna Sharf, Professor Meyer Nahon 
#Modified by Harry Nguyen (duongnavy@gmail.com)



import rosbag, sys, csv
import time
import string
import os #for file management make directory
import shutil #for file management, copy file

#verify correct input arguments: 1 or 2
def list_bags():
	listOfBagFiles = [f for f in os.listdir(".") if f[-4:] == ".bag"]	#get list of only bag files in current dir.
	numberOfFiles = str(len(listOfBagFiles))
	print "reading all " + numberOfFiles + " bagfiles in current directory: \n"
	return listOfBagFiles

#input: -bagFile : Bagfile name
#       -listOfTopics: a list of topics want to retrieve


def list_topics(bagFile):
	bag = rosbag.Bag(bagFile)
        bagContents = bag.read_messages()
        bagName = bag.filename


        listOfTopics = []
        for topic, msg, t in bagContents:
                if topic not in listOfTopics:
                	listOfTopics.append(topic)
	return listOfTopics

def bag2csv(bagFile, listOfTopics= None):
	bag = rosbag.Bag(bagFile)
	bagContents = bag.read_messages()
	bagName = bag.filename


	#create a new directory
	folder = string.rstrip(bagName, ".bag")
	try:	#else already exists
		os.makedirs(folder)
	except:
		pass
	shutil.copyfile(bagName, folder + '/' + bagName)


	#get list of topics from the bag
	if (listOfTopics == []):
		print "plot all topics"
		listOfTopics = list_topics(bagFile)
#		for topic, msg, t in bagContents:
#			if topic not in listOfTopics:
#				listOfTopics.append(topic)
	
	for topicName in listOfTopics:
		#Create a new CSV file for each topic
		filename = folder + '/' + string.replace(topicName, '/', '_slash_') + '.csv'
		with open(filename, 'w+') as csvfile:
			filewriter = csv.writer(csvfile, delimiter = ',')
			firstIteration = True	#allows header row
			for subtopic, msg, t in bag.read_messages(topicName):	# for each instant in time that has data for topicName
				#parse data from this instant, which is of the form of multiple lines of "Name: value\n"
				#	- put it in the form of a list of 2-element lists
				msgString = str(msg)
				msgList = string.split(msgString, '\n')
				instantaneousListOfData = []
				for nameValuePair in msgList:
					splitPair = string.split(nameValuePair, ':')
					for i in range(len(splitPair)):	#should be 0 to 1
						splitPair[i] = string.strip(splitPair[i])
					instantaneousListOfData.append(splitPair)
				#write the first row from the first element of each pair
				if firstIteration:	# header
					headers = ["rosbagTimestamp"]	#first column header
					for pair in instantaneousListOfData:
						headers.append(pair[0])
					filewriter.writerow(headers)
					firstIteration = False
				# write the value from each pair to the file
				values = [str(t)]	#first column will have rosbag timestamp
				for pair in instantaneousListOfData:
					if len(pair) > 1:
						values.append(pair[1])
				filewriter.writerow(values)
	bag.close()
	print "Finished"
	return 0


if __name__ == "__main__":
	if (len(sys.argv) == 1):
        	print "Usage"
		print "bag2csv.py bags_list : to list all bag files in current folder"
		print "bag2csv.py topics_list bagName : to list all topics of a bag file"
        	print "bag2csv.py read bagName topics : to convert specific topics to csv e.g: bag2csv.py read bagName /topic1 /topic2"
        	sys.exit(1)
	
	elif (sys.argv[1] == "topics_list"):
		bagFile_name = sys.argv[2]
		listofTopics = list_topics(bagFile_name)
		for topic in listofTopics:
			print(topic)
		sys.exit(1)

	elif (sys.argv[1] == "read"):
        	bagFile_name = sys.argv[2]
		listofTopics = []
		for i in range(3,len(sys.argv)):
			listofTopics.append(sys.argv[i])
        	print "reading bagfile: " + str(bagFile_name)
		bag2csv(bagFile_name, listofTopics)
		print "Done"
	elif (sys.argv[1] == "bags_list"):
        	listOfBagFiles = list_bags()
        	for f in listOfBagFiles:
                	print f
	else:
        	print "bad argument(s): " + str(sys.argv)       #shouldnt really come up
        	sys.exit(1)

