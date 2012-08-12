import urllib2
import urllib

class appdotnet:
	def __init__(self,client_id,client_secret,redirect_uri,scope):
		#for server authentication flow
		#check for invalid formats.
		self.client_id = client_id
		self.client_secret = client_secret
		self.redirect_uri = redirect_uri
		self.scope = scope
		self.api_anchor = "alpha.app.net" #for when the versions change

		#scopes provided by app.net API
		self.allowed_scopes = ['stream','email','write_post','follow','messages','export']

	def generateAuthUrl(self):
		#question: if scope is empty, but not just ommitted, does it ask for permission to nothing?
		url = "https://"+self.api_anchor+"/oauth/authenticate?client_id="+self.client_id+"&response_type=code&redirect_uri="+self.redirect_uri+"&scope="

		for scope in self.scope:
			if scope in self.allowed_scopes:
				url += scope + " "

		return url
	
	def getAuthResponse(self,code):
		#generate POST request
		url = "https://alpha.app.net/oauth/access_token"
		post_data = {'client_id':self.client_id,
		'client_secret':self.client_secret,
		'grant_type':'authorization_code',
		'redirect_uri':self.redirect_uri,
		'code':code}

		data = urllib.urlencode(post_data)

		req = urllib2.Request(url,data)
		response = urllib2.urlopen(req)
		
		return response.read()
	
