# Setup
mkdir Project
cd Project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
django-admin startproject testproject .
django-admin startapp timeclock
python3 manage.py makemigrations timeclock
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser

# Start Server
python3 manage.py runserver

Access API at `http://127.0.0.1:8000/graphql/`

# Create Account
```
mutation{
  createUser(
    username: "user123"
    email: "user123@user.com"
    password1: "!@#qwe!@#qwe"
    password2: "!@#qwe!@#qwe"
  ){
    success
    errors
  }
}
```
# Activate account 
Copy the Token as displayed on the terminal.
`http://127.0.0.1:8000/activate/YOUR_TOKEN`

```
mutation{
  verifyAccount(
      token:"YOUR_TOKEN"
  ){
    success
    errors
  }
}
```

# Obtain JWT Token

```
mutation{
  obtainToken(username:"user123",
  password:"!@#qwe!@#qwe"){
    token
  }
}
```

Copy the Token in the Response. we will use it for following query authentication.

# Use Insomnia API CLient to test the API 

* Download using `https://insomnia.rest/`
* In your environment, add your token to use as variable `_.TOKEN` in the queries

`{
	"TOKEN": "YOUR_JWT_TOKEN"
}`
* Create the following queries by setting body as `GraphQL Query`
* In the Header, set 
    * `Content-Type`  : `application/json`
    * `Authorization` : `JWT _.TOKEN`

# Me

```
query{
  me{
    username
    email
  }
}
```

# ClockIn

```
mutation{
  clockIn{
    clock{
      clockedIn
      clockedOut
    }
  }
}
```

# CurrentClock

```
query{
  currentClock{
    clockedIn
    clockedOut
  }
}
```

# ClockOut 

```
mutation{
  clockOut{
    clock{
      clockedIn
      clockedOut
    }
  }
}
```

# ClockedHours

```
query{
  clockedHours
}
```