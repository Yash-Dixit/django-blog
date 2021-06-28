# Introduction

The goal of this project is to provide minimalistic django blogging app template with all the basic features so that everyone can use, which _just works_ out of the box. 

### Main features

* User Model (Django Default)
1) First Name
2) Last Name
3) Email
4) Password
5) Number of Logins by the user.(Login Count)
6) Last login date and time
7) Account creation date and time

* Post Model
1) Post Title
2) Post Title_tag(similar to html title tag)
3) Post Category
4) Post Content
5) Post Timestamp
6) Post snippet(Part of the Post content to be shown on the main page)
7) Post Author

* A user can sign up using a new user name and password and also edit the profile credentials (username, first name, last name, email address, password) later on.

* Only a registered can add new posts.

* All users can view blogs posts (whether registered or unregistered). All posts have the relevant name of the author, Category and timestamp.

* Registered users can like any of the posts in the home page and also the users can view the like count near the like button.

* Registered users can add a new category.(Somewhat similar to hashtags used in Twitter)

* MySQL integration


# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/USERNAME/{{ project_name }}.git
    $ cd {{ project_name }}
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
