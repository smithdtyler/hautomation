import math
import re
import time

from time import gmtime, strftime

import MySQLdb
time.sleep(10)

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="temperature", # your username
                      passwd="temp", # your password
                      db="temperature") # name of the data base

print 'db= ' +  str(db)

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 
print 'opening..'
office = open('/sys/devices/w1_bus_master1/28-000005ab9297/w1_slave','r')
hvac = open('/sys/devices/w1_bus_master1/28-000005abeae1/w1_slave','r')
outsidesouth = open('/sys/devices/w1_bus_master1/28-000005aad85d/w1_slave','r')

sensors = [office,hvac,outsidesouth]
header = 'timestamp,officetemp,hvactemp,outsidesouthtemp'
print header
while True:
	line = '\'' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\''
	for sensor in sensors:
		s = sensor.read()
		if s:
			print s
			m = re.search('\d{5}', s)
			tempstr = m.group(0)
			temp = float(tempstr)
			tempf = ((9.0/5.0) * (temp/1000)) + 32
			line = line + ',\'' + str(tempf) + '\''
		sensor.seek(0)
	time.sleep(30)
	statement = 'INSERT INTO `temperature`.`simpletemp_sample` (`id` ,`timestamp`,`officetemp` ,`hvactemp` ,`outsidesouthtemp`)VALUES (NULL,'
	statement = statement + line
	statement = statement + ');'
	print cur.execute(statement)
	db.commit()
