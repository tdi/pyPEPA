import httplib2
import urllib


http = httplib2.Http()
params = urllib.parse.urlencode({'model':'cipe'})
response, content = http.request('http://localhost:8080/add', 'POST', params,
        headers={ 'Content-type': 'application/x-www-form-urlencoded'}
        )
print(response)
