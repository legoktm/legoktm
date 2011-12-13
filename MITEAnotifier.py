#!/usr/bin/python
"""
Script written by Legoktm for purposes of automatically sending his MIT admission status to his phone when it comes out.
(C) Legoktm, 2011, under the terms of the MIT License. (No, I'm not trying to be cool, thats what most of my code is.)
This script is not endorsed by MIT, and may be against their terms of service. Use at your own risk.
Syntax: "python MITEAnotifier.py"
It uses a timedelta object to figure out when the admissions will be released, but is based on PST. You may need to modify it based on your timezone.
Make sure you modify the global configuration below.
Enjoy, and good luck!
"""
#GLOBAL CONFIGURATION
userinfo = {'username':'username','password':'password'}
eusername='emailusername' #must be a Gmail account.
epassword='emailpassword'


import sys, urllib, urllib2, cookielib, os, time, smtplib, re, datetime


class MIT:
	def __init__(self, userinfo, eusername=None, epassword=None):
		self.loginpage = 'https://decisions.mit.edu/verify.php'
		self.email = True
		self.headers = {u'User-agent':u'Mozilla/4.0'}
		self.userinfo = userinfo
		self.cookiefile = 'cookies.txt'
		self.CJ = cookielib.LWPCookieJar()
		if self.email:
			self.eusername = eusername
			self.epassword = epassword
			
	def check(self):
		self.CJ = cookielib.LWPCookieJar() #clear any cookies that may exist
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.CJ))
		parameters = {
			'username':self.userinfo['username'],
			'password':self.userinfo['password'],
			'buttonClick':'Confirm',
		}
		encoded = urllib.urlencode(parameters)
		urllib2.install_opener(opener)
		request = urllib2.Request(self.loginpage, encoded, self.headers)
		response = urllib2.urlopen(request)
		self.resp = response.read()
		if 'successfully confirmed' in self.resp:
			print 'Not out yet...'
			return False
		self.notify(self.resp)
		response.close()
		self.CJ.save(self.cookiefile, ignore_discard=True)
		self.CJ.load(self.cookiefile) #refresh
		print 'Notified.'
		return True
	def notify(self, msg):
		self.server = smtplib.SMTP('smtp.gmail.com:587')
		self.server.starttls()
		self.server.login(self.eusername, self.epassword)
		self.emailaddr = self.eusername+'@gmail.com'
		self.server.sendmail(self.emailaddr, self.emailaddr, msg)
		self.server.quit()

def main():
	opening =datetime.datetime(2010, 12, 19, 9, 19)
	cur = time.localtime(time.time())
	curdt = datetime.datetime(cur.tm_year, cur.tm_mon, cur.tm_mday, cur.tm_hour, cur.tm_min, cur.tm_sec)
	delta = (opening - curdt).total_seconds()
	if not delta < 0:
		print 'Will sleep for %s seconds....' %delta
		time.sleep(int(delta)-2)
	w = MIT(userinfo, eusername=eusername, epassword=epassword)
	x = False
	while not x:
		x = w.check()
		time.sleep(30)

if __name__ == "__main__":
	main()
