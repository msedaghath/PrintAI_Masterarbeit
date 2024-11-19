
## Run Locally

Clone the project

```bash
  git clone https://CGI-ITC@dev.azure.com/CGI-ITC/CGI.ITC.Octorestapi/_git/CGI.ITC.Octorestapi
```

Go to the project directory

```bash
  cd CGI.ITC.Octorestapi
```
Make a virtual enviorment 

```bash
  python -m venv venv
```
Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Start the server

```bash
cd apidashboard
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

