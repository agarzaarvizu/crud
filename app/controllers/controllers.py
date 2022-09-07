from app import app
from flask import render_template
from app.config.config import urls


@app.route(urls['index'], methods = ['GET'])
def get_index():
    return render_template('index.html')
