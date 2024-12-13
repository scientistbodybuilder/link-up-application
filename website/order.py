from flask import Blueprint, render_template, jsonify,redirect, url_for, request, flash
from .model import Orders, Users, Cards, db
from .auth import login_required, session
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, os
from dotenv import load_dotenv
from jinja2 import Template

#Email Configs
load_dotenv()
HOST = "smtp.gmail.com"
PORT = 587
FROM_EMAIL = "linkup.tech.canada@gmail.com"
PASSWORD = os.getenv('LINKUP_EMAIL_PASSWORD')
TO_EMAIL = "linkup.tech.canada@gmail.com"

# price of the cards
price_LT = int(os.getenv('LINKTREE_CARD_PRICE'))
price_D = int(os.getenv('DIRECT_CARD_PRICE'))

order=Blueprint('order', __name__)

def calcPrice(num_direct_card,num_linktree_card):
    return num_direct_card*price_D + num_linktree_card*price_LT

@order.route('/order')
@login_required
def order_page():
    return render_template('order.html')

@order.route('/submit-order', methods=['POST'])
@login_required
def submit_order():
    data = request.get_json()
    DC_amount = data['direct-card-qty']
    LC_amount = data['link-card-qty']
    DC_link = data['direct-card-url']
    link_list = data['link-tree-url']

    #Update the database
    # cur = mysql.connection.cursor()
    try:
        date = datetime.today().strftime('%Y-%m-%d')
        # cur.execute("INSERT INTO orders (user_id,amount,order_date,LT_card,D_card) VALUES (%s,%s,%s,%s,%s)",(session["id"],calcPrice(DC_amount,LC_amount),date,LC_amount,DC_amount))
        # cur.commit()
        # cur.close()
        order = Orders(user_id=session["id"],amount=calcPrice(DC_amount,LC_amount),order_date=date,LT_card=LC_amount,D_card=DC_amount)
        db.session.add(order)
        db.session.commit()

        # update the cards
        cards = Cards.query.filter_by(user_id=session["id"]).first()
        if cards:
            cards.link_tree_card  = cards.link_tree_card + LC_amount
            cards.direct_card = cards.direct_card + DC_amount
            if cards.first_order_date == None:
                cards.first_order_date = datetime.today()
        db.session.commit()
    except Exception as e:
        print(f"Reading order to database: {e}")

    #prepare an email
    message = MIMEMultipart()
    message["From"] = FROM_EMAIL
    message["To"] = TO_EMAIL
    message["Subject"] = f"Order from {session["user"]}"

    if LC_amount == 0:  # ordering only direct cards           
        html_content = """
        <html>
        <body>
            <p>Quantity of Linktreee cards: {{ l_amount }}</p>
            <br>
            <p>Quantity of Direct cards: {{ d_amount }}</p>
            <br>
            <p>Direct Card URL: {{ link }}</p>
        </body>
        </html>
        """
        template = Template(html_content)
        html = template.render(d_amount = DC_amount, l_amount = LC_amount, link = DC_link )
        
    elif DC_amount==0:  # ordering only link tree cards
        html_content = """
        <html>
        <body>
            <p>Quantity of Linktreee cards: {{ l_amount }}</p>
            <br>
            <p>Quantity of Direct cards: {{ d_amount }}</p>
            <br>
            <ul>
                {% for url in url_list%}
                        <li>{{ url }}</li>
                    {% endfor %}                  
            </ul>
        </body>
        </html>
        """
        template = Template(html_content)
        html = template.render(url_list = link_list, d_amount = DC_amount, l_amount = LC_amount)
    else:  # ordering direct and link tree cards
        html_content = """
        <html>
        <body>
            <p>Quantity of Linktreee cards: {{ l_amount }}</p>
            <br>
            <p>Quantity of Direct cards: {{ d_amount }}</p>
            <br>
            <p>Direct Card URL: {{ link }} </p>                      
            <br>
            <ul>
                {% for url in url_list %}
                        <li>{{ url }}</li>
                    {% endfor %}                  
            </ul>
        </body>
        </html>
        """
        template = Template(html_content)
        html = template.render(url_list = link_list, d_amount = DC_amount, l_amount = LC_amount, link=DC_link)                    
    # send the email
    try:
        server = smtplib.SMTP(HOST,PORT)
        message.attach(MIMEText(html, 'html'))
        server.starttls()
        server.login(FROM_EMAIL,PASSWORD)
        server.sendmail(FROM_EMAIL,TO_EMAIL,message.as_string())
        server.quit()

        # signal to user that order completed successfully
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Sending Order Email:{e}")
        # signal that the order did not go through successfully
        return jsonify({'status': 'error'})
    

@order.route("/order_signout")
@login_required
def signout():
    session.pop("user", None)
    return redirect(url_for('views.home_page'))


