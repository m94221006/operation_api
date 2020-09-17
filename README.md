#  python django resful api for operation data

Topics:
- Environment
- Introduction
- run and testing

## Environment
1.python:3.5
2.django==2.1.2
3.djangorestframework==3.8.2
4.djangorestframework-jwt==1.11.0

## Introduction

### JWT authentication ###
This api is to use the JWT Token to make the authentication:
python jwt authentication example: 

apihost = 'https://127.0.0.1:8080/api-token-auth/'
data = {"username": username, "password": password}
header = {"Content-Type": "application/x-www-form-urlencoded"}
res = requests.post(apihost, data=data, headers=header)
token = res.json()['token']


### Using api with token  ###
Once you get the jwt token that you could use to access operation data api.
api get data with jwt token example :
  header = {'Authorization':'JWT {}'.format(token),'Content-type':'application/json'}
  get_url = "{}api/customer/{}".format(self.apihost,cid)
  res = requests.get(get_url, headers=header, timeout=20)
  data =  res.json()

## Run and Testing?
step 1.build images
  docker-compose build
  
step 2.run service:
  docker-compose up -d


## restful framework doc:

* [Django-REST-framework](http://www.django-rest-framework.org/)
