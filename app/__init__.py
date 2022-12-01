from flask import Flask, render_template, request
from flask_login import LoginManager

app = Flask(__name__, template_folder="views")
app.secret_key = "75fc78df8vhj92gv92yvhz"




app.secret_key = "75fc78df8vhj92gv92yvhz"


from app.controllers import *

if __name__ == "__main__":
    app.run(debug=True)
