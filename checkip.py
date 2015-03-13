#!/bin/python
import os
import subprocess
import sys
from email_utils import EmailConnection, Email

name = 'Your name'
email = 'Your e-mail'
password = 'Your password'
mail_server = 'Your mail server'
to_email = 'Destination email'
to_name = 'Name of destination'
subject = 'Change IP'
message = 'Your new IP is:'

fileaddress = os.path.dirname(os.path.abspath(__file__))+'/address'

if os.path.isfile(fileaddress):
	f = open(fileaddress, 'r')
	old_ip = f.readline()
else:
	old_ip = 'new'

new_ip = subprocess.check_output(['curl ifconfig.me'], shell=True)


print "Your old IP " + old_ip
print "Your new IP " + new_ip

if old_ip != new_ip:
	print 'change the address in the file'
	f = open(fileaddress, "w")
	f.write(new_ip)
	print 'Connecting to server...'
	server = EmailConnection(mail_server, email, password)
	print 'Preparing the email...'
	email = Email(from_='"%s" <%s>' % (name, email), #you can pass only email
              to='"%s" <%s>' % (to_name, to_email), #you can pass only email
              subject=subject, message='%s %s' % (message,new_ip))
	print 'Sending...'
	server.send(email)
	print 'Disconnecting...'
	server.close()
	print 'Done!'
else:
	print "Same IP" + new_ip
