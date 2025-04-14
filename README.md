# Dependencies

Install pillow before you go:
> pip install pillow

# Usage

To open the website, type:
> mkdir -p media/posts media/comments
> python manage.py makemigrations
> python manage.py migrate
> python manage.py createsuperuser
> python manage.py runserver

and visit http://127.0.0.1:8000 in your browser.