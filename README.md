# metamask-user-auth

This project's purpose is to serve as an example of an implementation of user authentication using [Metamask](https://metamask.io/)

- Uses [Django](https://www.djangoproject.com/) for the backend
- Uses [React](https://reactjs.org/) bootstrapped with [create-react-app](https://create-react-app.dev/) for the frontend
- Requires the Metamask wallet extension to be installed to work
- Purposefully did not style the app at all so anyone could take this and make it look how they want

## Installation

Requires both python (> 3.11) and the package manager [pip](https://pip.pypa.io/en/stable/) to be installed

```shell
pipenv install
pipenv shell
python manage.py runserver
```

> The application will now be running on **_127.0.0.1:8000/_**

### Potential Future Improvements

#### Backend

- Adding check to make sure address sent to backend is a valid ETH address
- Moving sensitive data to env vars

#### Frontend

- Creating button to request 'connect' to Metmask wallet rather than requesting this right away (this would allow a user to browse the website before authenticating)
- Moving sensitive data to env vars
