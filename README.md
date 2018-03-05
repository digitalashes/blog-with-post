# Status

Under development.

## 1. Install requirements

Local requirements:

    pip install -r requirements/local.txt

Production requirements:

    pip install -r requirements/production.txt

## 2. Django Management commands

* ``./manage.py migrate``
* ``./manage.py createsuperuser``

### 3. The assignments:

#### First part

* Add users to the blog (users can create an account, they should have a username, email address and password).

* Users should verify their email address via a token that is sent by email, upon clicking on the token the user should be verified.

* Add comments to the blog (only logged-in users can place comments, everyone can see them though).

* Add a migration that will create some test comments in DB (should be reversable).

* Cover code with unit tests (hint: use `factory_boy` library) (a big plus).


* Every models should be manageable in admin.

#### Second part

* Blog should have REST API for creating users and retrieving posts implemented using Django REST Framework (Only registered users and with verified email can retrieve data from blog).

#### Extra part (big plus)

* Project can be running using Docker.


