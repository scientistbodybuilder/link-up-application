from flask import Blueprint, render_template, jsonify,redirect, url_for, request, flash
from .model import mysql
from .auth import login_required, session
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from jinja2 import Template

#Email Configs
HOST = "smtp.gmail.com"
PORT = 587
FROM_EMAIL = "linkup.tech.canada@gmail.com"
PASSWORD = "yhls avny ciai wrca"
TO_EMAIL = "linkup.tech.canada@gmail.com"

# price of the cards
price_LT = 10
price_D = 5

order=Blueprint('order', __name__)

# def validOrder(num_l_card,num_d_card,d_card_url,num_lt_link,l_card_url_list):
#     if (num_d_card and num_d_card.isdigit()) or (num_l_card and num_l_card.isdigit()):
#         if num_d_card and num_d_card.isdigit():
#             numd = int(num_d_card)
#             if numd > 0: # atleasrt one direct card
#             # check whether a direct url was added or not
#                 if d_card_url == '':
#                     return 2
#         if num_l_card and num_l_card.isdigit():
#             numl = int(num_l_card)
#             if numl > 0: #atleast one link card
#                 # check whether the link tree url is atleast one
#                 if num_lt_link < 1:
#                     return 3
#                 # check whether all the urls are valid
#                 for url in l_card_url_list:
#                     if not url or url == "":
#                         return 4
#         # the submission is valid
#         return 1
#     else:
#         return 0


def calcPrice(num_direct_card,num_linktree_card):
    return num_direct_card*price_D + num_linktree_card*price_LT

# def orderSuccess():
#     pass

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
    cur = mysql.connection.cursor()
    try:
        date = datetime.today().strftime('%Y-%m-%d')
        cur.execute("INSERT INTO orders (user_id,amount,order_date,LT_card,D_card) VALUES (%s,%s,%s,%s,%s)",(session["id"],calcPrice(DC_amount,LC_amount),date,LC_amount,DC_amount))
        cur.commit()
        cur.close()
    except Exception as e:
        print(f"Reading order to database: {e}")

    #prepare an email
    message = MIMEMultipart()
    message["From"] = FROM_EMAIL
    message["To"] = TO_EMAIL
    message["Subject"] = f"New Order from {session["user"]}"

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


