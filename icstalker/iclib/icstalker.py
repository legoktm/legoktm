#!/usr/bin/python

#GLOBAL CONFIGURATION
userinfo = {'username':'username','password':'pw'}
eusername='username'
epassword='pw'


import sys, urllib, urllib2, cookielib, os, growl, time, smtplib, re


class IC:
	def __init__(self, userinfo, notify, eusername=None, epassword=None, debug=False, ):
		self.notify = notify
		self.debug = debug
		self.loginpage = 'https://ic.sjusd.org/campus/verify.jsp'
		self.stalkpage = 'classpageurl'
		self.email = True
		self.headers = {u'User-agent':u'Mozilla/4.0'}
		self.userinfo = userinfo
		self.stalkedpage = 'stalkedpage.txt'
		self.alreadystalked = os.path.exists(self.stalkedpage)
		self.cookiefile = 'ICcookies.txt'
		self.loggedin = os.path.exists(self.cookiefile)
		self.CJ = cookielib.LWPCookieJar()
		if self.loggedin:
			self.CJ.load(self.cookiefile)
		if self.email:
			self.eusername = eusername
			self.epassword = epassword
			
	def login(self, force=False):
		if self.loggedin and (not force):
			print 'Already logged in'
			return
		self.CJ = cookielib.LWPCookieJar() #clear any cookies that may exist
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.CJ))
		parameters = {
			'username':self.userinfo['username'],
			'password':self.userinfo['password'],
			'btnLogin':'Login',
			'appName':'sanjose',
			'screen':'',
		}
		encoded = urllib.urlencode(parameters)
		urllib2.install_opener(opener)
		request = urllib2.Request(self.loginpage, encoded, self.headers)
		response = urllib2.urlopen(request)
		text = response.read()
		if self.debug:
			print text
		response.close()
		self.CJ.save(self.cookiefile, ignore_discard=True)
		self.CJ.load(self.cookiefile) #refresh
		print 'Logged in.'
	def stalk(self):
		if self.alreadystalked:
			old = open(self.stalkedpage, 'r')
			oldt = old.read()
			old.close()
		else:
			oldt = ''
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.CJ))
		urllib2.install_opener(opener)
		request = urllib2.Request(self.stalkpage, headers=self.headers) #TODO: SET REFERER
		response = urllib2.urlopen(request)
		text = response.read()
		scraped = self.scrape(text)
		if self.debug:
			print text
			print scraped
		if 'loginBanner' in text:
			print 'Error, not logged in?'
			self.login(force=True)
			return False
		response.close()
		new = open(self.stalkedpage, 'w')
		new.write(scraped)
		new.close()
		self.alreadystalked = True
		if oldt != scraped:
			self.notify.notify('Your grade has changed to a %s!' %(scraped))
	def scrape(self, text):
		#only tested on non-category classes.....
		#set = re.findall("""                                 <td colspan="4" align="right">Term SM1 Semester Grade Totals</td>\n                                 <td align="right">(.*?)</td>\n                                 <td align="right">(.*?)</td>\n                                 <td align="right">(.*?)<br>(.*)""", text)
#		print text
		set = re.findall("""                                 <td colspan="4" align="right">Term SM1 Semester Grade Totals</td>\n                                 <td align="right">&nbsp;</td>\n                                 <td align="right">&nbsp;</td>\n                                 <td align="right">(.*?)<br>(.*)""", text)
#		print set
		return set[0][0]

class Notify:
	def __init__(self, methods, email=None, sms=None, pw=None):
		self.growl = False
		self.email = False
		self.sms = False
		if 'growl' in methods:
			self.growl = True
		if 'email' in methods:
			self.email = True
		if 'sms' in methods:
			self.sms = True
		if 'print' in methods:
			self.p = True
		if self.email:
			self.username = email
			self.emailaddr = email+'@gmail.com'
			self.pw = pw
			self.server = smtplib.SMTP('smtp.gmail.com:587')
			self.server.starttls()
			self.server.login(self.username,self.pw)	
		if self.sms:
			self.smsaddr = sms
			#set up gmail configuration
	#	print self.growl, self.email, self.sms
	def notify(self, message):
		if self.growl:
			self._growl(message)
		if self.email:
			self._email(message)
		if self.sms:
			self._sms(message)
		if self.p:
			print message
	def _growl(self, message):
		growl.notify(message, 'IC Stalker')
	def _email(self, message):
		self.server.sendmail(self.emailaddr, 'emailaddr', message)
		print 'Email sent.'
	def end(self):
		self.server.quit()
		

if __name__ == "__main__":
	n = Notify(['growl','email','print'],email='email',pw='pw')
	w = IC(userinfo, notify=n)
	w.login(force=True)
	while True:
		w.stalk()
		print 'Sleeping 5 minutes...'
		time.sleep(300)
