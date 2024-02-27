from flask import Flask, redirect, render_template, request, session
import dotenv
from zenora import APIClient
import os

# ну очень важная вещь
dotenv.load_dotenv(dotenv.find_dotenv())

# обозначаю ооп обьекты
app = Flask(__name__)
client = APIClient(str(os.environ["TOKEN"]), client_secret=str(os.environ["CLIENTSECRET"]))
app.config["SECRET_KEY"] = "verysecret"

# код страницы
@app.route("/")
def home():
    if 'token' in session:
        bearer_client = APIClient(session.get("token"), bearer=True)
        current_user = bearer_client.users.get_current_user()
        return render_template("index.html", current_user=current_user)
    return render_template("index.html", redirect_uri=str(os.environ["URL"]))

@app.route("/api/discord/")
def callback():
    code = request.args["code"]
    access_token = client.oauth.get_access_token(code, str(os.environ["REDIRECT"])).access_token
    session["token"] = access_token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)