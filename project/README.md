###Flask Service in Serverless

All the repositories within serverless_flask are supposed to be independent projects.
This is a flask project that can be deployed with serverless on lambda.
It connects to RDS as its db (via RDS proxy if needed).

It is supposed to be served via aws alb. 
Go through serverless.yml to understand the setup.

To Run Locally

```bash
> clone serverless_flask
> cd project
# > pyenv virualenv 3.7.x env_project
# > pyenv local
# Only needed if you don't have pyenv, pyenv takes care of venv automatically 
> pip install requirements.txt
> flask run
```

Run Migrations

```bash
> flask db migrate
> flask db upgrade
```

To Deploy (if you have correct aws keys)
```bash
> serverless deploy --stage dev/stagin/prod
# Otherwise use deployment service
```

To Push Changes with git, you need to understand that you are one level down the git root.
So if you have changes in this directory only (normal case) you can

```bash
> git add . # only adds changes in this folder. 
> git commit -m 'message'
> git push
``` 

Pending Tasks:
1. swagger setup
2. Deployment setup & Migrations
3. Test Setup
4. Fix pre-commit-config to track right files