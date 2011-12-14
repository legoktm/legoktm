#!/usr/bin/python

class request:
	def __init__(self, userinfo, debug = False):
		self.debug = debug
		self.loginpage = 'https://ic.sjusd.org/campus/verify.jsp'
		self.headers = {u'User-agent':u'Mozilla/4.0'}
		self.userinfo = userinfo
		self.cookiefile = 'cookies.txt'
		self.loggedin = os.path.exists(self.cookiefile)
		self.CJ = cookielib.LWPCookieJar()
		if self.loggedin:
			self.CJ.load(self.cookiefile)
			
	def login(self, force=False):
		"""
		Logs the user into IC. If force, it will override the current cookies and re-login.
		"""
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
	def get(self, url, use_cookies=True):
		"""
		Fetches the requested url using the IC cookies. If use_cookies is false, then the
		cookies will not be sent along. This maybe be useful for testing purposes.
		"""
		if use_cookies:
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.CJ))
		urllib2.install_opener(opener)
		request = urllib2.Request(url, headers=self.headers) #TODO: SET REFERER
		response = urllib2.urlopen(request)
		text = response.read()
		if self.debug:
			print text
		response.close()
		return text
