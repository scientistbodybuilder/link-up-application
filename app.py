from flask import Flask, render_template

app = Flask(__name__)


ORGS = [
    {
        'id': 1,
        'name': 'Google',
        'cards': 3,
        'reviews gained': 50
    },
    {
        'id':2,
        'name': 'Netflix',
        'cards': 5,
        'reviews gained': 72
    },
    {
        'id': 3,
        'name': 'Indigo',
        'cards': 3,
        'reviews gained': 60
    }
]

@app.route("/")
def home_page():
    return render_template('home.html', orgs=ORGS)

@app.route("/contact")
def contact_page():
    return render_template('contact.html')

@app.route("/login")
def login_page():
    return render_template('login.html')

@app.route("/signup")
def signup_page():
    return render_template('signup.html')



#{% for org in orgs %}
#            <div>
#                <h4>{{orgs['name']}}</h4>
#                <div>
#                    Activated Cards: {{orgs['cards']}}
#                    <br>
#                    <b>Reviews Added: {{orgs['reviews gained']}}</b>
#                </div>
#                
#            </div>
#        {% endfor %}





if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
    print("Server is Running....")

