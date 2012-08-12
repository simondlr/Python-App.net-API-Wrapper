##Python App.net API Wrapper

Currently supports server-side authentication.

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

##To-Do:

- Add all available endpoints
- Error-checking
