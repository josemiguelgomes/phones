# Phones 


Goal: to search US phone numbers based on area code and email a customer. \
Setup  a Django 4 project. \
    - python -m pip install --upgrade pip
    - python -m pip install Django
    
Using PosgtreSQL, create a table with 20 customers. \
    - brew install postgresql
    - brew services restart postgresql as background
    - /usr/local/opt/postgresql/bin/postgres -D /usr/local/var/postgres as online
    - psql postgres
     
    
Using Django Rest Framework, create an API that: \
a. Accepts an area code the URL \
b. Checks if the area code is valid i.e it's a US area code. \
c. Searches phone numbers available within the given area code. \
d. Emails(using an emailing service of your choice) a customer the first phone number found in the search. \
e. Makes the phone number emailed to a customer unavailable for other customers. \
d. Returns the emailed phone number or None in the response.

US area codes are available online. Also, you can get a list of random US phone numbers for use in this exercise.

This task can be accomplished in 1 day or so.
