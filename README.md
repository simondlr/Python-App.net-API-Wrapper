##Python App.net API Wrapper

Currently supports server-side authentication and some get requests.

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

##To-Do:

- Add POST/DELETE endpoints
- More error-checking
