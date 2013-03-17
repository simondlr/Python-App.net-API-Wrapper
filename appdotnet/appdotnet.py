import json
import requests

# To add
# - Identity Delegation
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
    def getRequest(self, url, getParameters=None):
        if not getParameters:
            getParameters = {}
        #access token
        url = url + "?access_token=" + self.access_token

        #if there are any extra get parameters aside from the access_token, append to the url
        if getParameters != {}:
            for key,value in getParameters.iteritems():
                url = url + "&" + key + "=" + value

        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            return r.text
        else:
            print r.text
            #j = json.loads(r.text)
            #resp = {'error_code': r.status_code, 'message' : j['error']['message']}
            #print j
            #return json.dumps(resp)
            return r.text


    def getUser(self, user_id):
        url = "https://%s/stream/0/users/%s" % (self.public_api_anchor,
                                                user_id)
        return self.getRequest(url)

    def getUserPosts(self, user_id):
        url = "https://%s/stream/0/users/%s/posts" % (self.public_api_anchor,
                                                      user_id)
        return self.getRequest(url)

    def getUserStars(self, user_id):
        url = "https://%s/stream/0/users/%s/stars" % (self.public_api_anchor,
                                                      user_id)
        return self.getRequest(url)

    def getGlobalStream(self):
        url = "https://%s/stream/0/posts/stream/global" % self.public_api_anchor
        return self.getRequest(url)

    def getUserStream(self):
        url = "https://%s/stream/0/posts/stream" % self.public_api_anchor
        return self.getRequest(url)

    def getUserStreamUnified(self):
        url = "https://%s/stream/0/posts/stream/unified" % self.public_api_anchor
        return self.getRequest(url)

    def getUserMentions(self, user_id):
        url = "https://%s/stream/0/users/%s/mentions" % (self.public_api_anchor,user_id)
        return self.getRequest(url)

    def getPost(self, post_id):
        url = "https://%s/stream/0/posts/%s" % (self.public_api_anchor,post_id)
        return self.getRequest(url)

    def getReposters(self, post_id):
        url ="https://%s/stream/0/posts/%s/reposters" % (self.public_api_anchor,post_id)
        return self.getRequest(url)

    def getStars(self, post_id):
        url ="https://%s/stream/0/posts/%s/stars" % (self.public_api_anchor,post_id)
        return self.getRequest(url)

    def getPostReplies(self, post_id):
        url = "https://%s/stream/0/posts/%s/replies" % (self.public_api_anchor,post_id)
        return self.getRequest(url)

    def getPostsByTag(self, tag):
        url = "https://%s/stream/0/posts/tag/%s" % (self.public_api_anchor, tag)
        return self.getRequest(url)

    def getUserFollowing(self, user_id):
        url = "https://%s/stream/0/users/%s/following" % (self.public_api_anchor, user_id)
        return self.getRequest(url)

    def getUserFollowers(self, user_id):
        url = "https://%s/stream/0/users/%s/followers" % (self.public_api_anchor, user_id)
        return self.getRequest(url)

    def getMutedUsers(self):
        url = "https://%s/stream/0/users/me/muted" % self.public_api_anchor
        return self.getRequest(url)

    def searchUsers(self,q):
        url = "https://%s/stream/0/users/search" % (self.public_api_anchor)
        return self.getRequest(url,getParameters={'q':q})

    def getCurrentToken(self):
        url = "https://%s/stream/0/token" % self.public_api_anchor
        return self.getRequest(url)



    # Reminder: if you include ids="id,id,id" it reads those ids.
    # Otherwise it defaults to those you are subscribed to
    # http://developers.app.net/docs/resources/channel/subscriptions/#get-current-users-subscribed-channels
    # http://developers.app.net/docs/resources/channel/lookup/#retrieve-multiple-channels
    def getChannels(self, **args):
        url = "https://%s/stream/0/channels" % self.public_api_anchor
        return self.getRequest(url, args)

    # http://developers.app.net/docs/resources/channel/lookup/#retrieve-a-channel
    def getAChannel(self, chan, **args):
        url = "https://%s/stream/0/channels/%s" % (self.public_api_anchor, chan)
        return self.getRequest(url, args)

    # http://developers.app.net/docs/resources/channel/lifecycle/#create-a-channel
    def createChannel(self, **args):
        url = "https://%s/stream/0/channels" % self.public_api_anchor
        return self.postRequest(url, args)

    # http://developers.app.net/docs/resources/channel/lookup/#retrieve-my-channels
    def getMyChannels(self, **args):
        url = "https://%s/stream/0/users/me/channels" % self.public_api_anchor
        return self.getRequest(url, args)

    # http://developers.app.net/docs/resources/channel/lookup/#retrieve-number-of-unread-pm-channels
    def getUnreadPMChannels(self, **args):
        url = "https://%s/stream/0/users/me/channels/pm/num_unread" % self.public_api_anchor
        return self.getRequest(url, args)

    # http://developers.app.net/docs/resources/channel/lifecycle/#update-a-channel
    def updateChannel(self, channel_id, **args):
        url = "https://%s/stream/0/channels/%s" % (self.public_api_anchor, channel_id)
        return self.putRequest(url, args)

    # http://developers.app.net/docs/resources/channel/subscriptions/#subscribe-to-a-channel
    def subscribeChannel(self, channel_id):
        url = "https://%s/stream/0/channels/%s/subscribe" % (self.public_api_anchor, channel_id)
        return self.postRequest(url)

    # http://developers.app.net/docs/resources/channel/subscriptions/#unsubscribe-from-a-channel
    def unsubscribeChannel(self, channel_id):
        url = "https://%s/stream/0/channels/%s/subscribe" % (self.public_api_anchor, channel_id)
        return self.deleteRequest(url)

    # http://developers.app.net/docs/resources/channel/subscriptions/#retrieve-users-subscribed-to-a-channel
    def getChannelSubscribes(self, chan, **args):
        url = "https://%s/stream/0/channels/%s/subscribers" % (self.public_api_anchor, chan)
        return self.getRequest(url, args)

    # http://developers.app.net/docs/resources/channel/subscriptions/#retrieve-user-ids-subscribed-to-a-channel
    def getChannelSubscribeIds(self, chan, **args):
        url = "https://%s/stream/0/channels/%s/subscribers/ids" % (self.public_api_anchor, chan)
        return self.getRequest(url, args)

    # http://developers.app.net/docs/resources/channel/subscriptions/#retrieve-user-ids-subscribed-to-a-channel
    # Note: required: use ids=...
    def getMultipleChannelSubscribeIds(self, **args):
        url = "https://%s/stream/0/channels/subscribers/ids" % (self.public_api_anchor)
        return self.getRequest(url, args)

    # http://developers.app.net/docs/resources/channel/muting/#mute-a-channel
    def muteChannel(self, chan, **args):
        url = "https://%s/stream/0/channels/%s/mute" % (self.public_api_anchor, chan)
        return self.postRequest(url, args)

    # http://developers.app.net/docs/resources/channel/muting/#unmute-a-channel
    def unmuteChannel(self, chan):
        url = "https://%s/stream/0/channels/%s/mute" % (self.public_api_anchor, chan)
        return self.deleteRequest(url)

    # http://developers.app.net/docs/resources/channel/muting/#get-current-users-muted-channels
    def getMutedChannels(self, **args):
        url = "https://%s/stream/0/users/me/channels/muted" % self.public_api_anchor
        return self.getRequest(url, args)


    # http://developers.app.net/docs/resources/message/lifecycle/#retrieve-the-messages-in-a-channel
    def getMessageChannel(self, chan, **args):
        url = "https://%s/stream/0/channels/%s/messages" % (self.public_api_anchor, chan)
        return self.getRequest(url, args)
        
    # http://developers.app.net/docs/resources/message/lifecycle/#create-a-message
    def createMessage(self, chan, **args):
        url = "https://%s/stream/0/channels/%s/messages" % (self.public_api_anchor, chan)
        return self.postRequest(url, args,headers={'content-type':'application/json'})

    # http://developers.app.net/docs/resources/message/lookup/#retrieve-a-message
    def getMessage(self, chan, msg,  **args):
        url = "https://%s/stream/0/channels/%s/messages/%s" % (self.public_api_anchor, chan, msg)
        return self.getRequest(url, args)

    # http://developers.app.net/docs/resources/message/lookup/#retrieve-multiple-messages
    # Note: ids= required
    def getMultiMessages(self, **args):
        url = "https://%s/stream/0/channels/messages" % self.public_api_anchor
        return self.getRequest(url, args)

    # http://developers.app.net/docs/resources/message/lookup/#retrieve-my-messages
    def getMyMessages(self, **args):
        url = "https://%s/stream/0/users/me/messages" % self.public_api_anchor
        return self.getRequest(url, args)

    # http://developers.app.net/docs/resources/message/lifecycle/#delete-a-message
    def deleteMessage(self, chan, msg):
        url = "https://%s/stream/0/channels/%s/messages/%s" % (self.public_api_anchor, chan, msg)
        return self.deleteRequest(url)
    



    #POST REQUESTS
    def postRequest(self, url, data=None, headers=None):
        if not data:
            data = {}

        if not headers:
            headers = {}

        headers['Authorization'] = 'Bearer %s' % self.access_token
        url = url
        r  = requests.post(url,data=json.dumps(data),headers=headers)
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
        url = "https://%s/stream/0/users/%s/follow" % (self.public_api_anchor, user_id)
        return self.postRequest(url)

    def repostPost(self,post_id):
        url = "https://%s/stream/0/posts/%s/repost" % (self.public_api_anchor, post_id)
        return self.postRequest(url)

    def starPost(self,post_id):
        url = "https://%s/stream/0/posts/%s/star" % (self.public_api_anchor, post_id)
        return self.postRequest(url)

    def muteUser(self,user_id):
        url = "https://%s/stream/0/users/%s/mute" % (self.public_api_anchor, user_id)
        return self.postRequest(url)

    #requires: text
    #optional: reply_to, annotations, links
    def createPost(self, text, reply_to = None, annotations=None, links=None):
        url = "https://%s/stream/0/posts" % self.public_api_anchor
        if annotations != None:
            url = url + "?include_annotations=1"

        data = {'text':text}
        if reply_to != None:
            data['reply_to'] = reply_to
        if annotations != None:
            data['annotations'] = annotations
        if links != None:
            data['links'] = links

        return self.postRequest(url,data,headers={'content-type':'application/json'})

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
        url = "https://%s/stream/0/posts/%s" % (self.public_api_anchor,post_id)
        return self.deleteRequest(url)

    def unrepostPost(self, post_id):
        url = "https://%s/stream/0/posts/%s/repost" % (self.public_api_anchor,post_id)
        return self.deleteRequest(url)

    def unstarPost(self, post_id):
        url = "https://%s/stream/0/posts/%s/star" % (self.public_api_anchor,post_id)
        return self.deleteRequest(url)

    def unfollowUser(self, user_id):
        url = "https://%s/stream/0/users/%s/follow" % (self.public_api_anchor,user_id)
        return self.deleteRequest(url)

    def unmuteUser(self, user_id):
        url = "https://%s/stream/0/users/%s/mute" % (self.public_api_anchor,user_id)
        return self.deleteRequest(url)

