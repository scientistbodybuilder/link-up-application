from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from .model import Cards, db
from sqlalchemy import desc
from .auth import session
from datetime import date, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, os
from dotenv import load_dotenv
from jinja2 import Template

views=Blueprint('views', __name__)
m = "card"

#Email Configs
load_dotenv()
# HOST = "smtp.office365.com"
# PORT = 587
# FROM_EMAIL = "linkup.canada@outlook.com"
# PASSWORD = os.getenv('LINKUP_EMAIL_PASSWORD')
# TO_EMAIL = "linkup.canada@outlook.com"

class CardButton():
    def __init__(self,name,card_num,date):
        self.name = name
        self.card_num = card_num
        self.date = date

def orderOrg(m):
    # cur = mysql.connection.cursor()
    l=[]
    try:
        if m=="card":
            cards = Cards.query.filter(
                Cards.org_name.isnot(None),
                Cards.first_order_date.isnot(None)
            ).order_by(
                (Cards.direct_card + Cards.link_tree_card).desc()
            ).all()
            print(cards)

    
            # cur.execute("SELECT * FROM cards WHERE org_name IS NOT NULL AND first_order_date IS NOT NULL ORDER BY (direct_card + link_tree_card) DESC")
            # result = cur.fetchall()
            for org in cards:
                if isinstance(org.first_order_date, (date, datetime)):
                    date_str = org.first_order_date.strftime('%Y-%m-%d')
                else:
                    date_str = org.first_order_date
                card = CardButton(org.org_name, org.link_tree_card + org.direct_card, date_str)
                l.append(card)
            return l
        else:
            # cur.execute("SELECT * FROM cards WHERE org_name IS NOT NULL AND first_order_date IS NOT NULL ORDER BY first_order_date DESC")
            # result = cur.fetchall()
            cards = Cards.query.filter(
                Cards.org_name.isnot(None),
                Cards.first_order_date.isnot(None)
            ).order_by(
                (Cards.first_order_date).desc()
            ).all()
            print(cards)
            for org in cards:
                if isinstance(org.first_order_date, (date, datetime)):
                    date_str = org.first_order_date.strftime('%Y-%m-%d')
                else:
                    date_str = org.first_order_date
                card = CardButton(org.org_name, org.link_tree_card + org.direct_card, date_str)
                l.append(card)
            print(l)
            return l
    except Exception as e:
        print(f"Error: {e}")
        return l

@views.route('/')
# @login_required
def home_page():
    list = orderOrg(m)
    print(list)
    if "user" not in session:
        return render_template('home.html', prompt2 = "Sign in")
    return render_template('home.html', prompt2 = "Sign out")

@views.route("/contact")
def contact_page():
    if "user" not in session:
        return render_template('contact.html', prompt2 = "Sign in")
    return render_template('contact.html', prompt2 = "Sign out")

# @views.route("/contact-message", methods=['POST'])
# def send_message():
#     data = request.get_json()
#     msg = data['msg']

#     message = MIMEMultipart()
#     message["From"] = FROM_EMAIL
#     message["To"] = TO_EMAIL
#     message["Subject"] = f"Inquiry from {session["user"]}"

#     html_content = """
#         <html>
#         <body>
#             <p>{{ msg }}</p>
#         </body>
#         </html>
#         """
#     template = Template(html_content)
#     html = template.render(msg=msg)
#     try:
#         server = smtplib.SMTP(HOST,PORT)
#         message.attach(MIMEText(html, 'html'))
#         server.starttls()
#         server.login(FROM_EMAIL,PASSWORD)
#         server.sendmail(FROM_EMAIL,TO_EMAIL,message.as_string())
#         server.quit()

#         # signal to user that order completed successfully
#         return jsonify({'status': 'success'})
#     except Exception as e:
#         print(f"Sending Order Email:{e}")
#         # signal that the order did not go through successfully
#         return jsonify({'status': 'error'})

@views.route("/fetch_order_change", methods=["POST"])
# @login_required
def fetch_home():
    global m
    data = request.get_json()
    if 'm' in data:
        m = data['m']
        print(f"request to change card ordering: {m}")
        new_list = orderOrg(m)
        print(new_list)
        print("done list")
        print(Cards.query.all())
        result = [{'name': card.name, 'card_num': card.card_num, 'date':card.date} for card in new_list]
        print("returning json list")
        return jsonify(result)
    return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

@views.route("/view_signout", methods=["POST"])
def fetch_signout():
    session.pop("user", None)
    data = request.get_json()
    if 'm' in data:
        page = data['m']
        if page == "home":
            return jsonify({'status': 'success', 'redirect': url_for('views.home_page')})
        else:
            return jsonify({'status': 'success', 'redirect': url_for('views.contact_page')})
    return jsonify({'status': 'error', 'message': 'm not found in data'})