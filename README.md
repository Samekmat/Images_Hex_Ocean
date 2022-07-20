# PROJECT SETUP

## After clone:
 - Firstly run : python(py) manage.py migrate
 - Second thing is to createsuperuser and load fixtures by running: py manage.py loaddata fixtures.json
 - Before upload image you need to create profile which is combination of user and an existing plan

## Uploading via HTTP request 
 - Run postman and set 3 parameters in body as form-data:
    - image_url - image file
    - name - name of object
    - profile - pk of existing profile to connect image to the user

## Endpoints available
 - /admin - admin panel
 - /upload - view for image upload
 - /list - list view of every image uploaded on a current profile
 - 