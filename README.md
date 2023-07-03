# Phonebook API
The Phonebook API provides a centralized and accessible platform for managing and retrieving contact information, and Spam reports.

## Prerequisites
Before running the application, ensure that you have the following installed:

* Python (version 3.6 or higher)
* Django (version 3.2 or higher)

## Installation
1. Clone the repository to your local machine:
```
  $ git clone https://github.com/dhawalkatariya/phonebook-api
```
2. Change to the project's directory:
```
  $ cd phonebook-api
```
3. Install the required dependencies using pip:
```
  $ pip install -r requirements.txt
```

## Database Setup
By default, the application uses a SQLite database. If you prefer to use a different database, update the DATABASES configuration in the settings.py file.

1. Create the necessary database tables by running the following command:
```
  $ python manage.py migrate
```

## Usage
1. To start the development server, run the following command:
```
  $ python manage.py runserver
```
2. You should see output similar to the following:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Open your web browser and visit http://127.0.0.1:8000/ to access the blog application.


## Documentaion

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


## Contributing
Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.
