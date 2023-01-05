![Logo of the project](C:\projects\kitchen\static\assets\img\favicon.png)


# Kitchen-service
> Django project for managing cooks, dishes and tasks in restaurant kitchen


## Installing / Getting started

You have to install Python 3!

```shell
git clone https://github.com/artemkazakov947/-Restaurant-Kitchen-Service.git
cd kitchen
pip install virtualenv venv
venv\Scripts\activate
pip install -r requirementes.txt
set DJANGO_DEBUG=TRUE
set DJANGO_SECRET_KEY=<your secret key>
set DATABASE_URL=<your database url>
python manage.py migrate
python manage.py runserver 
```

  - You can use following superuser (or create another one by yourself):
  - Login: `chef`
  - Password: `chef12345`


### Deploying / Publishing

[taxi-service project deployed to Render](https://kitchen-service-qvqc.onrender.com)



## Features

* Managing cars and drivers directly on the website
* You can also make a task for your staff, monitoring for task completion
* Authentication functionality for Cook/User
* Strong Django admin panel for deep managing