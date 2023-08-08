Django E-Commerce Backend Project uses DRF <br>

First you need to install packages
```
pip install -r requirements.txt
```
Create DB schemas
```
python manage.py makemigrations user order product store
```
Apply them
```
python manage.py migrate
```
Create a super user for testing
```
python manage.py createsuperuser
```
Good to go !
```
python manage.py runserver
```
