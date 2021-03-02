
import click 
import os
import psycopg2  
from flask import current_app, g
from flask.cli import with_appcontext 

def get_db():
    if 'db' not in g:       
        g.db = psycopg2.connect(
            host=os.getenv('host'),
            database=os.getenv('database'),
            user=os.getenv('user'),
            password=os.getenv("password"),
            port=os.getenv('port')
        )
    
    return g.db 

def close_db(e=None):
    db =g.pop('db',None)

    if db is not None:
        db.close()
#creating a database with the name app 
def init_db():
    db= get_db() 
    cursor = db.cursor()
    with current_app.open_resource('schema.sql') as f:
        cursor.execute(f.read().decode('utf8'))
    
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('initilized the database')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

