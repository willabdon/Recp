> ### Recp - A recipe manager project

![recp banner](https://github.com/willabdon/Recp/blob/master/recp_banner.png)

## Installation

1. Clone this repository: `git clone https://github.com/willabdon/Recp.git`.
2. `cd` into `Recp`.
3. Install [pipenv](https://github.com/pypa/pipenv) (creation of virtualenv, there are other ways, choose the best one for you)
4. Install the requirements: `pipenv install` or `pip install -r requirements.txt`.
5. Activate the virtualenv: `pipenv shell`
6. Create a database and configure in the `settings.py` file
7. Run the migrations: `python manage.py migrate`
8. The you can run the application: `python manage.py runserver`
9. Access the url [http://127.0.0.1:8000](http://127.0.0.1:8000)

