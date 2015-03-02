#!/bin/python
import subprocess
import sys
from email_utils import EmailConnection, Email
import sqlite3
conn = sqlite3.connect('/var/tmp/casa.sqlite')


sql = "SELECT Ip, Id FROM `mio_ip` ORDER BY Id DESC"

c = conn.cursor()

c.execute(sql)

old_ip = c.fetchone()[0]


new_ip = subprocess.check_output(['curl ifconfig.me'], shell=True)

print "Your old IP " + old_ip
print "Your new IP " + new_ip

if new_ip != old_ip:
	print 'esegui query cambio IP'
	c.execute("INSERT INTO  `mio_ip` (`id` ,`ip` ,`data`)VALUES ((SELECT max(id) FROM mio_ip)+1 ,  '%s', date('now'));" % (new_ip))
	conn.commit()
        conn.close
        print 'Connecting to server...'
	server = EmailConnection()
	print 'Preparing the email...'
	email = Email(from_='"Raspberry" <yourmail@gmail.com>', to='"yourname" <yourmail@gmail.com>',subject='Change IP', message='Your new IP address ' + new_ip)
	print 'Sending...'
	server.send(email)
	print 'Disconnecting...'
	server.close()
	print 'Done!'
else:
	print 'IP Uguale'	
