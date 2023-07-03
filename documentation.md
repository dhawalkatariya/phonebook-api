### How to start server
```bash
    python3 mange.py makemigrations
    python3 mange.py migrate
    python3 mange.py runserver
```
The above commands will start the server in development mode

## Steps to access
### Authentication
#### Register
```bash
curl -X POST \
  'http://127.0.0.1:8000/api/register/' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "phone_number": "09090909090",
  "password": "test@test123",
  "name": "test"
}'
```

#### Login
```bash
curl -X GET \
  'http://127.0.0.1:8000/api/login/' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "phone_number": "09090909090",
  "password": "test@test123"
}'
```
- Both Login and Regiter will return an Auth token which needs to be set as the Authorization header in subsequent requests

### Spam
- All the Spam queries take the phone number as the url param to mark the number as spam
#### Mark user as spam
```bash
curl -X POST \
  'http://127.0.0.1:8000/api/spam/0000000000' \
  --header 'Authorization: Token c0aff86556648074374bb972713d955abfcd4e81'
```

#### UnMark user as spam
```bash
curl -X DELETE \
  'http://127.0.0.1:8000/api/spam/0000000000' \
  --header 'Authorization: Token c0aff86556648074374bb972713d955abfcd4e81'
```

#### Check If the phone_number is marked by user
```bash
curl -X GET \
  'http://127.0.0.1:8000/api/spam/0000000000' \
  --header 'Authorization: Token c0aff86556648074374bb972713d955abfcd4e81'
```

### Search Queries
#### SearchBy Name
```bash
curl -X GET \
  'http://127.0.0.1:8000/api/contacts/?searchBy=name&value=o' \
  --header 'Authorization: Token c0aff86556648074374bb972713d955abfcd4e81'
```
#### SearchBy Phone Number
```bash
curl -X GET \
  'http://127.0.0.1:8000/api/contacts/?searchBy=phone_number&value=9090909090' \
  --header 'Authorization: Token c0aff86556648074374bb972713d955abfcd4e81'
```

### Profile
- The profile query takes the id(for conatact) and phone_number(for user).
- If the user wants to see the profile of the user then send the phone_number as the id param
- otherwise send the contact number's id
```bash
curl -X GET \
  'http://127.0.0.1:8000/api/profile/0000000000' \
  --header 'Authorization: Token c0aff86556648074374bb972713d955abfcd4e81'
```