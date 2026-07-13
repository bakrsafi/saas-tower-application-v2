


## start the application by running the following command in the terminal:

# create a virtual environment
python -m venv venv
# activate the virtual environment
venv\Scripts\activate
# install the dependencies
pip install -r requirements.txt
# run the following commands to apply migrations and start the server
python manage.py make migrations
# apply the migrations
python manage.py migrate
# run the server
python manage.py runserver

# generate requirements file
pip freeze > requirements.txt
