# Phones


Goal: to search US phone numbers based on area code and email a customer. \

Setup  a Django 4 project. \
Using PosgtreSQL, create a table with 20 customers. \
Using Django Rest Framework, create an API that: \
a. Accepts an area code the URL \
b. Checks if the area code is valid i.e it's a US area code. \
c. Searches phone numbers available within the given area code. \
d. Emails(using an emailing service of your choice) a customer the first phone number found in the search. \
e. Makes the phone number emailed to a customer unavailable for other customers. \
d. Returns the emailed phone number or None in the response.

US area codes are available online. Also, you can get a list of random US phone numbers for use in this exercise. \

# Authentication
The API Phones uses Token Authentication to authenticate.

# To run Unit Tests (through Docker Compose)
docker-compose run --rm app sh -c "python manage.py test"

# To run the application (through Docker Compose)


# Endpoints
http://localhost:8000/admin/ \
http://localhost:8000/api/schema/ \
http://localhost:8000/api/docs/

