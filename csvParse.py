import csv
import os
import subprocess
import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET


# class for obtaining list of geolocations form addresses
#provide input Csv file, input read colum (i.e. column in csv with addresses), output csv file

class GeoLocator(object):

    # create location request object
    def __init__(self, inputFile, inputReadColumn, outputFile):
        self.serviceurl = 'http://maps.googleapis.com/maps/api/geocode/xml?'
        self.name_row = 6
        # csv diles
        self.csv_read = inputFile
        self.csv_write = outputFile
        self.name_row = inputReadColumn
        self.print_output = True
        self.count = 0

        
    def get_geo_location(self, name):
        url = self.serviceurl + urllib.parse.urlencode({'address': name})
        uh =  urllib.request.urlopen(url)
        data = uh.read()
        tree = ET.fromstring(data)

        results = tree.findall('result')
        lat = results[0].find('geometry').find('location').find('lat').text
        lng = results[0].find('geometry').find('location').find('lng').text
        loc = results[0].find('formatted_address').text

        returnObject = {"latitude": lat, "longitude": lng, "location": loc }

        return returnObject


    def begin_queries(self):
         with open(self.csv_read, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', )
            print("successfully opened" + str(self.csv_read))
                        
            for row in reader:
                # just to skip top row - change in future
                if self.count != 0:
                    try:
                        locationObj = self.get_geo_location(row[self.name_row])
                        self.write_to_output(locationObj)
                        successful_add = True
                    except:
                        print('Failed write - added to fail.csv')
                        self.failed_writes(row[self.name_row])
                        
                self.count = self.count + 1

    # locationData is the object containing all the data
    def write_to_output(self, locationData):
         with open(self.csv_write, 'a') as csvfileWrite:
            writer = csv.writer(csvfileWrite, delimiter=',')
            writer.writerow([locationData["location"], locationData["longitude"], locationData["latitude"]])
            if self.print_output:
                print("Row added: ")
                print(locationData["location"], locationData["longitude"], locationData["latitude"])
                print("-" * 20)

    def failed_writes(self, name):
        with open("failed.csv", 'a') as csvfileWrite:
            writer = csv.writer(csvfileWrite, delimiter=',')
            writer.writerow([[name]])


            
        

    
# using main class
locator = GeoLocator("input.csv", 2, "out.csv")

locator.begin_queries()
