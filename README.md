##Python App.net API Wrapper

A simple wrapper for App.net's API.

##To use

Example usage to generate URL

```python
from appdotnet import *

scope = ['messages','email']
api = appdotnet('client_id','client_secret','redirect_uri',scope)

url = api.generateAuthUrl()

```

Example usage to get authentication code after callback.

```python
scope = ['messages','email']
api = appdotnet('client_id','client_secret','redirect_uri',scope)

#get code parameter

api.getAuthResponse(code)

```

Scope = list of parameters.

If it has already been authenticated, you can create it simply by passing the access token.

```python
api = appdotnet('<access_token>')
#eg
api.getUser('2803')

```

Example post (after authentication):

```python
api = appdotnet('<access_token>')
#eg
api.createPost('Hi. This is a simple post. Ke Nako! App.net is here.')
api.createPost('Testing annotations. Adding meta info.',annotations={'meta':'some info'})

```


##To-Do:

- More error-checking
- Add stream/filter/subscription endpoints when it becomes available.

##NOTE:

Annotations don't seem to be working. Unsure whether it is an API issue. Will fix once I find out.
