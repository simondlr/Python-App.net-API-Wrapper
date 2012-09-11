##Python App.net API Wrapper

A simple Python wrapper for App.net's API.

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
api = appdotnet(access_token='<access_token>')
#eg
api.getUser(2803)

```

Example post (after authentication):

```python
api = appdotnet(access_token='<access_token>')
#eg
api.createPost('Hi. This is a simple post. Ke Nako! App.net is here.')
api.createPost('Testing annotations. Adding meta info.',annotations={'meta':'some info'})

```

##To-Do:

- More error-checking
- Add stream/filter/subscription endpoints when it becomes available.
- Add mute endpoints (they are live).

##NOTE:

Annotations don't seem to be working. Unsure whether it is an API issue. Will fix once I find out.

##License:

License

Copyright (c) 2012 Simon de la Rouviere

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
