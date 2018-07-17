# Cardforge #

## Development Environment ##

### Requirements ###

This application at this moment has 3 parts:

- the frontend application: that requires `nvm` or the current nodejs lts.
- the backend application: that requires python3.6 and pipenv
- the web server: caddy (or nginx on production environment)


### Setting up NVM ###

In order to install **nvm** follow the installation steps from the
nvm documentation readme: https://github.com/creationix/nvm
If you already has nvm installed, this step can be skiped.


### Setting up PIPENV ###

Install it on the user space:

```bash
pip install --user pipenv
```

Then add `$HOME/.local/bin` to your `$PATH`.


### Setting up Caddy ###

Download a caddy binary from the official website: https://caddyserver.com/download

Then, put the binary under `$HOME/.local/bin`

Alternativelly you can install it from the package manager of your
linux distribution if it is provided.


### Getting Started ###

This guide assumes that you already have installed all the required
dependencies.

Clone the repository:

```bash
git clone https://github.com/pabloalba/cardforge.git
```

Set up and start the backend application with the following commands
in a new terminal:

```bash
cd cardforge
pipenv shell
pipenv install
python manage.py migrate
python manage.py runserver
```

Set up and start the frontend development server (in an other terminal):

```bash
cd cardforge/front
nvm use
nvm install # only if node version is not previously installed
npm install
npm run start
```

And finally, start the web server (in an other terminal):

```bash
cd cardforge
caddy
```

Then, open the browser under http://localhost:3000

