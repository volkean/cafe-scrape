# Flask Web App Starter

A Flask starter template as per [these docs](https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application).

## Getting Started

Previews should run automatically when starting a workspace.

## Database

You should create the database in your environment. Default connection parameters are set accordingly idx environment as username="user", password="user", dbname="user"

For idx environment create the database as

CREATE DATABASE "user" WITH OWNER "user" ENCODING 'UTF8';

ALTER USER "user" WITH PASSWORD 'user';

and run create.sql in the project.