import json
import requests

#endpoints still to add.
# - Annotations don't seem to be implemented yet. Doesn't seem to work.
# - General parameters (in dev by app.net)
# - Streams (in dev by app.net)
# - Filters (in dev by app.net)

class appdotnet:
    ''' Once access has been given, you don't have to pass through the
    client_id, client_secret, redirect_uri, or scope. These are just
    to get the authentication token.

    Once authenticated, you can initialise appdotnet with only the
    access token: ie

    api = appdotnet(access_token='<insert token here>')
    '''

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None,
                 scope=None, access_token=None):
        #for server authentication flow
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

        self.access_token = access_token

        self.api_anchor = "alpha.app.net" #for when the versions change
        #anchors currently different
        self.public_api_anchor = "alpha-api.app.net"

        #scopes provided by app.net API
        self.allowed_scopes = ['stream', 'email', 'write_post',
                               'follow', 'messages','export']

    def generateAuthUrl(self):
        url = "https://" + self.api_anchor + "/oauth/authenticate?client_id="+\
                self.client_id + "&response_type=code&redirect_uri=" +\
                self.redirect_uri + "&scope="

        for scope in self.scope:
            if scope in self.allowed_scopes:
                url += scope + " "

        return url

    def getAuthResponse(self, code):
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

    #GET REQUESTS
    def getRequest(self, url):
        #access token
        url = url + "?access_token=" + self.access_token
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            return r.text
        else:
            j = json.loads(r.text)
            resp = {'error_code': r.status_code,
                        'message' : j['error']['message']}
            return json.dumps(resp)


    def getUser(self, user_id):
        url = "https://%s/stream/0/users/%i" % (self.public_api_anchor,
                                                user_id)
        return self.getRequest(url)

    def getUserPosts(self, user_id):
        url = "https://%s/stream/0/users/%i/posts" % (self.public_api_anchor,
                                                      user_id)
        return self.getRequest(url)

    def getGlobalStream(self):
        url = "https://%s/stream/0/posts/stream/global" % self.public_api_anchor
        return self.getRequest(url)

    def getUserStream(self):
        url = "https://%s/stream/0/posts/stream" % self.public_api_anchor
        return self.getRequest(url)

    def getUserMentions(self, user_id):
        url = "https://"+self.public_api_anchor+"/stream/0/users/"+user_id+"/mentions"
        return self.getRequest(url)

    def getPost(self, post_id):
        url = "https://"+self.public_api_anchor+"/stream/0/posts/"+post_id
        return self.getRequest(url)

    def getPostReplies(self, post_id):
        url = "https://"+self.public_api_anchor+"/stream/0/posts/"+post_id+"/replies"
        return self.getRequest(url)

    def getPostsByTag(self, tag):
        url = "https://"+self.public_api_anchor+"/stream/0/posts/tag/"+tag
        return self.getRequest(url)

    def getUserFollowing(self, user_id):
        url = "https://"+self.public_api_anchor+"/stream/0/users/"+user_id+"/following"
        return self.getRequest(url)

    def getUserFollowers(self, user_id):
        url = "https://"+self.public_api_anchor+"/stream/0/users/"+user_id+"/followers"
        return self.getRequest(url)

    #POST REQUESTS
        url = url
        data['access_token'] = self.access_token
        r  = requests.post(url,data=data)
        if r.status_code == requests.codes.ok:
            return r.text
        else:
            try:
                j = json.loads(r.text)
                resp = {'error_code': r.status_code,
                            'message' : j['error']['message']}
                return resp
            except: #generic error
                print r.text
                return "{'error':'There was an error'}"


    def followUser(self,user_id):
        url = "https://" + self.public_api_anchor + "/stream/0/users/" +\
                user_id + "/follow"

        return self.postRequest(url)

    #requires: text
    #optional: reply_to, annotations, links
    def createPost(self, text, reply_to = None, annotations=None, links=None):
        url = "https://"+self.public_api_anchor+"/stream/0/posts"
        data = {'text':text}
        if reply_to != None:
            data['reply_to'] = reply_to
        if annotations != None:
            data['annotations'] = annotations
        if links != None:
            data['links'] = links

        return self.postRequest(url,data)

    #DELETE request
    def deleteRequest(self, url):
        url = url + "?access_token=" + self.access_token
        r = requests.delete(url)
        if r.status_code == requests.codes.ok:
            return r.text
        else:
            try:
                j = json.loads(r.text)
                resp = {'error_code': r.status_code,
                            'message' : j['error']['message']}
                return resp
            except: #generic error
                print r.text
                return "{'error':'There was an error'}"

    def deletePost(self, post_id):
        url = "https://"+self.public_api_anchor+"/stream/0/posts/"+post_id
        return self.deleteRequest(url)

    def unfollowUser(self, user_id):
        url = "https://"+self.public_api_anchor+"/stream/0/users/"+user_id+"/follow"
        return self.deleteRequest(url)

