from django.db import models

from datetime import datetime
from dateutil import tz
from time import strftime

#https://stackoverflow.com/questions/4770297/python-convert-utc-datetime-string-to-local-datetime?lq=1
# Create your models here.

from_zone = tz.tzutc()
to_zone = tz.tzlocal()

class Sample(models.Model):
	timestamp = models.DateTimeField(null=False)
	officetemp = models.FloatField(null=True)
	hvactemp = models.FloatField(null=True)
	garagetemp = models.FloatField(null=True)
	outsidesouthtemp = models.FloatField(null=True)

	def nicetimestamp(self):
		utc = self.timestamp.replace(tzinfo=from_zone)
                # Convert time zone
                central = utc.astimezone(to_zone)
                #return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
		return central.strftime("new Date(%Y, %m, %d, %H, %M, %S, 0)") 
		#return 'tyler'

	def __unicode__(self):
		utc = self.timestamp.replace(tzinfo=from_zone)
		# Convert time zone
		central = utc.astimezone(to_zone)
        	return str(central) + ' office: ' + str(self.officetemp) + ' hvac: ' + str(self.hvactemp) + ' outside: ' + str(self.outsidesouthtemp)
