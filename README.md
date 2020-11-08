# Project Title

SayLess

http://sayless.azurewebsites.net/

## Getting Started

This project is about creating an interactive medium for teenagers where emojis are targetted as a common text.

### Prerequisites

1. [Install pip](https://pip.pypa.io/en/stable/) - Install pip
2. Have Python accessible from terminal 
3. Have [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) if using Azure.

### Running the server locally

In order to run the server, you simply need to follow these steps.

1. Clone the repository locally
2. Navigate to the root of the project folder
3. Make sure you have pip installed
4. Run `pip install -r requirements.txt` from root directory
5. Do `python run.py` command from root directory in terminal

Caution: The DB is accessed from keyvault so you will not be able to access the project's database. Contact repo owners or Comment 36,39 and 42 out of __init__.py and put your own DB link there.

This application was tested and mainly developed via chrome. So all features might not be available for other browsers.

From here you will be able to got to http://localhost:8000 to view the webpage.

## How to test

Run `pytest -v` from the home directory of sayless. All the tests with verbose should run from the `/Tests` directory.

### Languages structures Used

1) HTML
2) Flask
3) CSS
4) AJAX
5) Flask-SocketIO
6) Flask-SQLAlchemy
7) Pytest

## Deployment

Any changes merged to development is auto-deployed to azure webapp.

## Built With

* [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) - Web Design 
* [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) - Styles for HTML
* [AJAX](https://api.jquery.com/category/ajax/) - Client Side framework
* [Flask](https://palletsprojects.com/p/flask/) - Web Framework
* [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - Database query
* [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) - Sockets for chatting
* [Azure WebApp](https://azure.microsoft.com/en-us/services/app-service/web/) - Azure WebApp
* [Azure KeyVault](https://azure.microsoft.com/en-us/services/key-vault/) - Azure keyvault
* [Pytest](https://docs.pytest.org/en/stable/) - Pytest for testing

## Authors

* **Shreya Lakhar** - *Initial work* - [Shreya](https://github.com/shreyala)
* **Riley** - *Initial work* - [Riley](https://github.com/rileyb123)
* **Shristy Jha** - *Initial work* - [Shristy](https://github.com/shrishtyy)
* **Moulid** - *Initial work* - [Moulid](https://github.com/moulid15)
* **Shazmaan Malek** - *Initial work* - [Shazmaan](https://github.com/Shazmaan)

## License 

<if needed>
This project is licensed under the <license> - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thank you CSE442 and Dr. Jesse Hartloff :)
