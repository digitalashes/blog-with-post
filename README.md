## 1. Install

### Using Vagrant:

1. ``git clone https://github.com/digitalashes/blog-with-post``
1. ``cd blog-with-post``
1. ``vagrant up``
1. ``vagrant ssh``
1. ``./manage.py runserver 0.0.0.0:8000``
1. open localhost:8000 in browser

### Using Docker:

1. ``git clone https://github.com/digitalashes/blog-with-post``
1. ``cd blog-with-post``
1. ``cp env.example ./config/.env``
1. open ./config/.env file
1 find and replace `DJANGO_DATABASE_URL=postgres:///blog` to `DJANGO_DATABASE_URL=postgres://postgres:pg_pass@db:5432/postgres`
1. ``docker-compose up``
1. open localhost:8000 in browser

## 2. Credentials:

* admin
    * url to admin panel - `http://localhost:8000/admin`
    * username = `admin`
    * password = `admin`
* user with verified email
    * username = `ckelly`
    * password = `password`
* user with unverified email:
    * username = `tatejulia`
    * password = `password`
   
## 3. The assignments:

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


