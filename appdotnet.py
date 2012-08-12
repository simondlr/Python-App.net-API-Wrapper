import requests
import json

#endpoints still to add.
# - POST/DELETE endpoints
# - Retrieve replies to post (in development by app.net)
# - General parameters (in dev by app.net)
# - Streams (in dev by app.net)
# - Filters (in dev by app.net)

class appdotnet:
	'''
	Once access has been given, you don't have to pass through the client_id, client_secte, redirect_uri, or scope. These are just to get the authentication token.

	Once authenticated, you can initialise appdotnet with only the access token: ie

	api = appdotnet(access_token='<insert token here>')
	'''

	def __init__(self,client_id=None,client_secret=None,redirect_uri=None,scope=None,access_token=None):
		#for server authentication flow
		self.client_id = client_id
		self.client_secret = client_secret
		self.redirect_uri = redirect_uri
		self.scope = scope

		self.access_token = access_token

		self.api_anchor = "alpha.app.net" #for when the versions change
		#anchors currently different
		self.public_api_anchor = "alpha-api.app.net" #for when the versions change

		#scopes provided by app.net API
		self.allowed_scopes = ['stream','email','write_post','follow','messages','export']

	def generateAuthUrl(self):
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

		r = requests.post(url,data=post_data)
		
		return r.text
	
	'''
	API Calls
	'''

	def getCall(self,url):
		#access token
		url = url+"?access_token="+self.access_token
		r = requests.get(url)
		if r.status_code == requests.codes.ok:
			return r.text
		else:
			j = json.loads(r.text)
			return "{'error_code':"+(str)(r.status_code)+",'message':'"+j['error']['message']+"'}"
		

	def getUser(self,user_id):
		url = "https://"+self.public_api_anchor+"/stream/0/users/"+user_id
		return self.getCall(url)

	def getUserPosts(self,user_id):
		url = "https://"+self.public_api_anchor+"/stream/0/users/"+user_id+"/posts"
		return self.getCall(url)
	
	def getGlobalStream(self):
		url = "https://"+self.public_api_anchor+"/stream/0/posts/stream/global"
		return self.getCall(url)

	def getUserStream(self):
		url = "https://"+self.public_api_anchor+"/stream/0/posts/stream"
		return self.getCall(url)

	def getUserMentions(self,user_id):
		url = "https://"+self.public_api_anchor+"/stream/0/users/"+user_id+"/mentions"
		return self.getCall(url)

	def getPost(self,post_id):
		url = "https://"+self.public_api_anchor+"/stream/0/posts/"+post_id
		return self.getCall(url)




