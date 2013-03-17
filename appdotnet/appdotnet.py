import json
import requests

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
    GET/POST/DELETE requests
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
        return r.text

    #POST REQUESTS
    def postRequest(self, url, data=None, headers=None):
        if not data:
            data = {}

        if not headers:
            headers = {}

        headers['Authorization'] = 'Bearer %s' % self.access_token
        url = url
        r  = requests.post(url,data=json.dumps(data),headers=headers)
        return r.text

    #DELETE request
    def deleteRequest(self, url):
        url = url + "?access_token=" + self.access_token
        r = requests.delete(url)
        return r.text

    #todo: PUT Request

    '''
    ENDPOINTS: Grouped according to endpoint categories.
    http://developers.app.net/docs/resources/
    '''

    '''
    USER: http://developers.app.net/docs/resources/user/
    '''

    def getUser(self, user_id):
        url = "https://%s/stream/0/users/%s" % (self.public_api_anchor,
                                                user_id)
        return self.getRequest(url)

    #todo: def updateUser()
    #todo: def getAvatar()
    #todo: def updateAvatar()
    #todo: def getCover()
    #todo: def updateCover()

    def followUser(self,user_id):
        url = "https://%s/stream/0/users/%s/follow" % (self.public_api_anchor, user_id)
        return self.postRequest(url)

    def unfollowUser(self, user_id):
        url = "https://%s/stream/0/users/%s/follow" % (self.public_api_anchor,user_id)
        return self.deleteRequest(url)

    def muteUser(self,user_id):
        url = "https://%s/stream/0/users/%s/mute" % (self.public_api_anchor, user_id)
        return self.postRequest(url)

    def unmuteUser(self, user_id):
        url = "https://%s/stream/0/users/%s/mute" % (self.public_api_anchor,user_id)
        return self.deleteRequest(url)

    #todo: def getMultipleUsers()

    def searchUsers(self,q):
        url = "https://%s/stream/0/users/search" % (self.public_api_anchor)
        return self.getRequest(url,getParameters={'q':q})

    def getUserFollowing(self, user_id):
        url = "https://%s/stream/0/users/%s/following" % (self.public_api_anchor, user_id)
        return self.getRequest(url)

    def getUserFollowers(self, user_id):
        url = "https://%s/stream/0/users/%s/followers" % (self.public_api_anchor, user_id)
        return self.getRequest(url)

    #todo: def getUserFollowingIDs()
    #todo: def getUserFollowerIDs()

    def getMutedUsers(self):
        url = "https://%s/stream/0/users/me/muted" % self.public_api_anchor
        return self.getRequest(url)

    #todo: def getMultipleMutedUsersIDs()

    def getReposters(self, post_id):
        url ="https://%s/stream/0/posts/%s/reposters" % (self.public_api_anchor,post_id)
        return self.getRequest(url)

    def getStars(self, post_id):
        url ="https://%s/stream/0/posts/%s/stars" % (self.public_api_anchor,post_id)
        return self.getRequest(url)

    '''
    POSTS: http://developers.app.net/docs/resources/post/
    '''
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

    def getPost(self, post_id):
        url = "https://%s/stream/0/posts/%s" % (self.public_api_anchor,post_id)
        return self.getRequest(url)

    def deletePost(self, post_id):
        url = "https://%s/stream/0/posts/%s" % (self.public_api_anchor,post_id)
        return self.deleteRequest(url)

    def repostPost(self,post_id):
        url = "https://%s/stream/0/posts/%s/repost" % (self.public_api_anchor, post_id)
        return self.postRequest(url)

    def unrepostPost(self, post_id):
        url = "https://%s/stream/0/posts/%s/repost" % (self.public_api_anchor,post_id)
        return self.deleteRequest(url)

    def starPost(self,post_id):
        url = "https://%s/stream/0/posts/%s/star" % (self.public_api_anchor, post_id)
        return self.postRequest(url)

    def unstarPost(self, post_id):
        url = "https://%s/stream/0/posts/%s/star" % (self.public_api_anchor,post_id)
        return self.deleteRequest(url)

    #todo: def getMultiplePosts()

    def getUserPosts(self, user_id):
        url = "https://%s/stream/0/users/%s/posts" % (self.public_api_anchor,
                                                      user_id)
        return self.getRequest(url)

    def getUserStars(self, user_id):
        url = "https://%s/stream/0/users/%s/stars" % (self.public_api_anchor,
                                                      user_id)
        return self.getRequest(url)

    def getUserMentions(self, user_id):
        url = "https://%s/stream/0/users/%s/mentions" % (self.public_api_anchor,user_id)
        return self.getRequest(url)
        
    def getPostsByTag(self, tag):
        url = "https://%s/stream/0/posts/tag/%s" % (self.public_api_anchor, tag)
        return self.getRequest(url)

    def getPostReplies(self, post_id):
        url = "https://%s/stream/0/posts/%s/replies" % (self.public_api_anchor,post_id)
        return self.getRequest(url)

    def getUserStream(self):
        url = "https://%s/stream/0/posts/stream" % self.public_api_anchor
        return self.getRequest(url)

    def getUserStreamUnified(self):
        url = "https://%s/stream/0/posts/stream/unified" % self.public_api_anchor
        return self.getRequest(url)

    def getGlobalStream(self):
        url = "https://%s/stream/0/posts/stream/global" % self.public_api_anchor
        return self.getRequest(url)

    '''
    CHANNEL: http://developers.app.net/docs/resources/channel/ 
    Reminder: if you include ids="id,id,id" it reads those ids.
    Otherwise it defaults to those you are subscribed to
    http://developers.app.net/docs/resources/channel/subscriptions/#get-current-users-subscribed-channels
    '''

    def getChannels(self, **args):
        url = "https://%s/stream/0/channels" % self.public_api_anchor
        return self.getRequest(url, args)

    def createChannel(self, **args):
        url = "https://%s/stream/0/channels" % self.public_api_anchor
        return self.postRequest(url, args)

    def getAChannel(self, chan, **args):
        url = "https://%s/stream/0/channels/%s" % (self.public_api_anchor, chan)
        return self.getRequest(url, args)

    def getMyChannels(self, **args):
        url = "https://%s/stream/0/users/me/channels" % self.public_api_anchor
        return self.getRequest(url, args)

    #todo: getMultipleChannels()

    def getUnreadPMChannels(self, **args):
        url = "https://%s/stream/0/users/me/channels/pm/num_unread" % self.public_api_anchor
        return self.getRequest(url, args)

    def updateChannel(self, channel_id, **args):
        url = "https://%s/stream/0/channels/%s" % (self.public_api_anchor, channel_id)
        return self.putRequest(url, args)

    def subscribeChannel(self, channel_id):
        url = "https://%s/stream/0/channels/%s/subscribe" % (self.public_api_anchor, channel_id)
        return self.postRequest(url)

    def unsubscribeChannel(self, channel_id):
        url = "https://%s/stream/0/channels/%s/subscribe" % (self.public_api_anchor, channel_id)
        return self.deleteRequest(url)

    def getChannelSubscribers(self, chan, **args):
        url = "https://%s/stream/0/channels/%s/subscribers" % (self.public_api_anchor, chan)
        return self.getRequest(url, args)

    def getChannelSubscribeIds(self, chan, **args):
        url = "https://%s/stream/0/channels/%s/subscribers/ids" % (self.public_api_anchor, chan)
        return self.getRequest(url, args)

    def getMultipleChannelSubscribeIds(self, **args):
        url = "https://%s/stream/0/channels/subscribers/ids" % (self.public_api_anchor)
        return self.getRequest(url, args)

    def muteChannel(self, chan, **args):
        url = "https://%s/stream/0/channels/%s/mute" % (self.public_api_anchor, chan)
        return self.postRequest(url, args)

    def unmuteChannel(self, chan):
        url = "https://%s/stream/0/channels/%s/mute" % (self.public_api_anchor, chan)
        return self.deleteRequest(url)

    def getMutedChannels(self, **args):
        url = "https://%s/stream/0/users/me/channels/muted" % self.public_api_anchor
        return self.getRequest(url, args)

    '''
    MESSAGE: http://developers.app.net/docs/resources/message/
    '''

    def getMessageChannel(self, chan, **args):
        url = "https://%s/stream/0/channels/%s/messages" % (self.public_api_anchor, chan)
        return self.getRequest(url, args)

    def createMessage(self, chan, **args):
        url = "https://%s/stream/0/channels/%s/messages" % (self.public_api_anchor, chan)
        return self.postRequest(url, args,headers={'content-type':'application/json'})

    def getMessage(self, chan, msg,  **args):
        url = "https://%s/stream/0/channels/%s/messages/%s" % (self.public_api_anchor, chan, msg)
        return self.getRequest(url, args)

    def getMultipleMessages(self, **args):
        url = "https://%s/stream/0/channels/messages" % self.public_api_anchor
        return self.getRequest(url, args)

    def getMyMessages(self, **args):
        url = "https://%s/stream/0/users/me/messages" % self.public_api_anchor
        return self.getRequest(url, args)

    def deleteMessage(self, chan, msg):
        url = "https://%s/stream/0/channels/%s/messages/%s" % (self.public_api_anchor, chan, msg)
        return self.deleteRequest(url)

    '''
    FILE: http://developers.app.net/docs/resources/file/
    '''

    #todo: def createFile()
    #todo: def getFile()
    #todo: def getMultipleFiles()
    #todo: def deleteFile()
    #todo: def getMyFiles()
    #todo: def updateFile()
    #todo: def getFileContent()
    #todo: def setFileContent() 

    '''
    STREAM: http://developers.app.net/docs/resources/stream/
    '''

    #todo: def createStream()
    #todo: def getStream()
    #todo: def updateStream()
    #todo: def deleteStream()
    #todo: def getAllStreamsPerCurrentToken()
    #todo: def deleteAllStreamsPerCurrentToken()

    '''
    FILTER: http://developers.app.net/docs/resources/filter/
    '''

    #todo: def createFilter()
    #todo: def getFilter()
    #todo: def updateFilter()
    #todo: def deleteFilter()
    #todo: def getCurrentUserFilters()
    #todo: def deleteCurrentUserFilters()

    '''
    INTERACTIONS: http://developers.app.net/docs/resources/interaction/
    '''

    #todo: def getMyInteractions()

    '''
    STREAM MARKERS: http://developers.app.net/docs/resources/stream-marker/
    '''

    #todo: def updateStreamMarker()

    '''
    TEXT PROCESSOR: http://developers.app.net/docs/resources/text-processor/
    '''

    #todo: def processText()

    '''
    TOKEN: http://developers.app.net/docs/resources/token/
    '''

    def getCurrentToken(self):
        url = "https://%s/stream/0/token" % self.public_api_anchor
        return self.getRequest(url)

    #todo: getAuthorisedIDsForApp
    #todo: getAuthorisedTokensForApp

    '''
    PLACES: http://developers.app.net/docs/resources/place/
    '''

    #todo: getPlace()
    #todo: searchPlaces()

    '''
    EXPLORE: http://developers.app.net/docs/resources/explore/
    '''

    #todo: getAllExploreStreams()
    #todo: getExploreStream()

