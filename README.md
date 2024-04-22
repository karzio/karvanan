# karvanan
Case Study for Data Loss Prevention tool.

### Introduction 

Project consists of three docker containers. 
* An image of mysql database.
* Two of containers use the same image to share the codebase
  * A django server
  * A task distribution app

### Environment

File .env.example contains all environment variables that are 
needed for the project. 
* DEBUG should be set to 'true' only if the project is developed
* SLACK_BOT_TOKEN should be set to a token found in a slack app settings - more about this below
* MYSQL_* variables are for database connection. To run the project in a local environment, it's enough to use the default variables.
* ALLOWED_HOSTS is a list of hosts separated by a coma allowed to connect to the django app. When the personal computer will be exposed by for example ngrok,
please add it after a comma to this list, don't remove the localhost entries or the admin will be accessible only by the external url

To quickly start the project, copy the .env.example file, name it as '.env' and change the SLACK_BOT_TOKEN 
and preferably the DEBUG option to true. 

#### OBTAIN SLACK_BOT_TOKEN

As this is just a case study, the app for this project is not distributed, so the app has to be created for
development. This instruction helps with the app creation and obtaining the needed token.

1. Login at https://api.slack.com/apps
2. Click `Create New App`
3. Choose option "From an app manifest" and copy-paste the content of the slack_app_manifest.yml file from this repository into the editor. 
**IMPORTANT** update `request_url` field before clicking `Next`. I was using ngrok to expose my port 8000 of the app to the world.
The url should end with the `/slack/` endpoint. 
4. Create the app in the workspace in which it should be tested in
5. Click `Install to Workspace`
6. In the menu on the left find tab OAuth & Permissions
7. Copy `User OAuth Token`
8. Set `SLACK_BOT_TOKEN` env variable as the copied token

Also, the url used for the project must be subscribed by slack app. Although, it should be done after running the project, because slack sends
a request to the provided url. Url should be accessible from the internet, I'm using ngrok to expose my computer. The instruction is below:

1. Make sure to expose your 8000 to internet
2. Copy the url and add /slack/ endpoint to it so it looks like this: ngrok.example.eu/slack/
3. In the slack app settings find `Event Subscriptions`
4. Paste the url into the `Request URL` bracket - the request should be sent automatically
5. If it's ok - click `Save Changes` on the bottom of the page

If the server has been running, the project should ready to be used.

#### OBTAIN AWS CREDENTIALS

User account that is going to be used in these projects needs at least `AmazonSQSFullAccess`
permission policy. Also, SQS queue needs to be named `slack-messages`. To use the account in the project,
copy the file `credentials` example and name it `credentials` (leave it in aws directory). In the copied file change the secrets to 
those of the AWS user that is going to be used (if you're using AWS CLI, credentials are usually in a `~/.aws/credentials` file on your local computer).

### Run the application

To run the application with docker-compose just use the standard commands to build and up the containers. 
Be sure to have port 8000 available and remember to run migrations and create a superuser to access the admin.
Here are commands that should be run. 

```shell
docker-compose build
docker-compose run django python manage.py migrate
docker-compose run django python manage.py createsuperuser
docker-compose up
```

### Tests

To test the application, just build the app first and then test.

```shell

docker-compose build
docker-compose run django python manage.py test
```

### Add patterns

Go to the localhost:8000/admin and login with your superuser credentials. Go to Patterns and add one.
Now, the project is fully set up and should be catching messages on the server you've added the app to and 
should swap the message if it contains the pattern's information. To use an example pattern, here's a regex 
for email: 

```regexp
[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}
```

The message should be edited if it contains the pattern or if the attached file or snippet contains the pattern.
Files should also be deleted. If the message contains multiple patterns, only the first one is logged in caught messages.