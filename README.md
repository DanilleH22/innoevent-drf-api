# Innovevent 

Innoevent is a tech networking platform designed to connect professionals across the technology industry. Our mission is to facilitate meaningful interactions and opportunities for collaboration by hosting a wide range of tech events, from workshops and webinars to full-scale conferences. Event organisers are able to share there event with people all accrross the world.

- The repository for the DRF-API associated with this project is available [HERE](https://github.com/DanilleH22/innoevent-drf-api). The installation, set up, and deployment steps for this section of the project have also been included in the README linked to the DRF-API. 

#### DEPLOYED BACKEND API[LINK](https://innoevent-7b1d2e7d15e7.herokuapp.com/)
#### DEPLOYED FRONTEND [LINK - LIVE SITE](https://innoevent-react-93e74f3a4351.herokuapp.com/)
#### DEPLOYED FRONTEND GITHUB [REPOSITORY](https://github.com/DanilleH22/innovevent)


The live link for "Innovevent" can be found [HERE](https://innoevent-7b1d2e7d15e7.herokuapp.com/)

## Table of Contents
+ [User Stories](#user-stories "User Stories")
+ [Database](#database "Database")
+ [Testing](#testing "Testing")
  + [Validator Testing](#validator-testing "Validator Testing")
  + [Unfixed Bugs](#unfixed-bugs "Unfixed Bugs")
+ [Technologies Used](#technologies-used "Technologies Used")
  + [Main Languages Used](#main-languages-used "Main Languages Used")
  + [Frameworks, Libraries & Programs Used](#frameworks-libraries-programs-used "Frameworks, Libraries & Programs Used")
+ [Deployment](#deployment "Deployment")
+ [Credits](#credits "Credits")
  + [Content](#content "Content")
  + [Media](#media "Media")

## User Stories:

I have included links to the [GitHub Issues](https://github.com/DanilleH22/innoevent-drf-api/issues) for this project, as well as the [KANBAN board](https://github.com/users/DanilleH22/projects/8/views/1).

## Database:
![SQL Database model](/static/images-readme/readme-models.png)

## Testing:
### Validator Testing: 
All files passed through [PEP8](http://pep8online.com/) without error.

![PEP8](/static/images-readme/readme-pep8.png)

### Manual Testing:
1. Manually verified each url path created works & opens without error.
2. Verified that the CRUD functionality is available in each app via the development version: Events, Profiles, Signup, Contact
 - Checked this by going to each link.
 - Creating a new item.
 - Checking new item URL path. 
 - Editing the items details (Not available for Contact or Sign up)
 - Deleting the item (Not available for Contact, Sign up or Profiles)
3. Ensured search feature for Events apps returns results. Results not filtered for events:
 - Checked the views file for filtering the event by name

### Unfixed Bugs
- None so far.

## Technologies Used:
### Main Languages Used:
- Python

### Frameworks, Libraries & Programs Used:
- Django
- Django RestFramework
- Cloudinary
- Heroku
- Pillow
- Django Rest Auth
- Django Filter
- PostgreSQL
- Cors Headers
- DrawSQL: An interactive ERD platform that allows you to set up your database tables, & build the connections between them for a visual layout.

## Deployment:
### Project creation:
1. Create the GitHub repository.
2. Create the project app on [Heroku](heroku.com).
3. Add the Postgres package to the Heroku app via the Resources tab.
4. Once the GitHub repository was launched on GitPod, installed the following packages using the `pip install` command:
```
'django<4'
dj3-cloudinary-storage
Pillow
djangorestframework
django-filter
dj-rest-auth
'dj-rest-auth[with_social]'
djangorestframework-simplejwt
dj_database_url psycopg2
gunicorn
django-cors-headers
```
5. Created the Django project with the following command:
```
django-admin startproject innoevent .
```
6. Navigated back to [Heroku](heroku.com), and under the Settings tab, added the following configvars:
 - Key: SECRET_KEY | Value: hidden
 - Key: CLOUDINARY_URL | Value: cloudinary://hidden
 - Key: DISABLE_COLLECTSTATIC | Value: 1
 - Key: ALLOWED_HOST | Value: innoevent-7b1d2e7d15e7.herokuapp.com
7. Add two additional configvars once the ReactApp has been created:
 - Key: CLIENT_ORIGIN | Value: https://innoevent-react-93e74f3a4351.herokuapp.com
 - Key: CLIENT_ORIGIN_DEV | Value: https://3000-danilleh22-innovevent-iytf49xaeyl.w
  - Check that the trailing slash `\` at the end of both links has been removed.

8. Created the env.py file, and added the following variables. The value for DATABASE_URL was obtained from the Heroku configvars in the previous step:
```
import os

os.environ['CLOUDINARY_URL'] = 'cloudinary://hidden'
os.environ['DEV'] = '1'
os.environ['SECRET_KEY'] = 'hidden'
os.environ['DATABASE_URL'] = 'postgres://hidden'
```
### In settings.py: 

9. Add the following to INSTALLED_APPS to support the newly installed packages:
```
'cloudinary_storage',
'django.contrib.staticfiles',
'cloudinary',
'rest_framework',
'django_filters',
'rest_framework.authtoken',
'dj_rest_auth',
'django.contrib.sites',
'allauth',
'allauth.account',
'allauth.socialaccount',
'dj_rest_auth.registration',
'corsheaders',
```
10. Import the database, the regular expression module & the env.py
```
import dj_database_url
import re
import os
if os.path.exists('env.py')
    import env
```

11. Below the import statements, add the following variable for Cloudinary:
```
CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ.ger('CLOUDINARY_URL')
}

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinartStorage'
```
- Below INSTALLED_APPS, set site ID:
```
SITE_ID = 1
```
12. Below BASE_DIR, create the REST_FRAMEWORK, and include page pagination to improve app loading times, pagination count, and date/time format:
```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [(
        'rest_framework.authentication.SessionAuthentication'
        if 'DEV' in os.environ
        else 'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    )],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DATETIME_FORMAT': '%d %b %Y',
}
```
13. Set the default renderer to JSON:
```
if 'DEV' not in os.environ:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]
```
14. Beneath that, added the following:
```
REST_USE_JWT = True
JWT_AUTH_SECURE = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
JWT_AUTH_SAMESITE = 'None'
```
15. Then added:
```
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'innoevent.serializers.CurrentUserSerializer'
}
```
16. Updated DEBUG variable to:
```
DEBUG = 'DEV' in os.environ
```
17. Updated the DATABASES variable to:
```
DATABASES = {
    'default': ({
       'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    } if 'DEV' in os.environ else dj_database_url.parse(
        os.environ.get('DATABASE_URL')
    )
    )
}
```
18. Added the Heroku app to the ALLOWED_HOSTS variable:
```
os.environ.get('ALLOWED_HOST'),
'localhost',
```
19. Below ALLOWED_HOST, added the CORS_ALLOWED variable:
```
if 'CLIENT_ORIGIN' in os.environ:
    CORS_ALLOWED_ORIGINS = [
        os.environ.get('CLIENT_ORIGIN')
    ]

if 'CLIENT_ORIGIN_DEV' in os.environ:
    extracted_url = re.match(r'^.+-', os.environ.get('CLIENT_ORIGIN_DEV', ''), re.IGNORECASE).group(0)
    CORS_ALLOWED_ORIGIN_REGEXES = [
        rf"{extracted_url}(eu|us)\d+\w\.gitpod\.io$",
    ]
```
20. Also added to the top of MIDDLEWARE:
```
'corsheaders.middleware.CorsMiddleware',
```
- During a deployment issue, it was suggested by a fellow student, Johan, to add the following lines of code below CORS_ALLOW_CREDENTIALS:
```
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = list(default_headers)
CORS_ALLOW_METHODS = list(default_methods)
CSRF_TRUSTED_ORIGINS = [os.environ.get(
    'CLIENT_ORIGIN_DEV', 'CLIENT_ORIGIN',
)]
```
- In addition, Johan also suggested to add the following import statement at the top of the settings.py file:
```
from corsheaders.defaults import default_headers, default_methods
```

### Final requirements:
21. Created a Procfile, & added the following two lines:
```
release: python manage.py migrate
web: gunicorn innoevent.wsgi
```
22. Migrated the database:
```
python3 manage.py makemigrations
python3 manage.py migrate
```
23. Froze requirements:
```
pip3 freeze --local > requirements.txt
```
24. Added, committed & pushed the changes to GitHub
25. Navigated back to heroku, and under the ‘Deploy’ tab, connect the GitHub repository.
26. Deployed the branch.

### Deploy to ElephantSQL:
* To take the data sent by users for profile I had deployed to Elephant SQL using the following [instructions](https://code-institute-students.github.io/deployment-docs/41-pp5-adv-fe/pp5-adv-fe-drf-01-create-a-database)

## CREDITS:

### Content:
- The creation of this API database was provided through the step by step guide of the C.I. DRF-API walkthrough project for Events and profiles.
- All classes & functions have been credited.
- Modifications have been made to the 'Profiles' & 'Events' app models, and an additional two apps along with models, serializers & views have been created by me.

### Media:
- Default media used for testing had been the images downloaded from the walkthrough of Moments in Code institute