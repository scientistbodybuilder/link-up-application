from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from .model import mysql
from .auth import session
from datetime import date, datetime

views=Blueprint('views', __name__)
m = "card"

class CardButton():
    def __init__(self,name,card_num,date):
        self.name = name
        self.card_num = card_num
        self.date = date

def orderOrg(m):
    cur = mysql.connection.cursor()
    l=[]
    try:
        if m=="card":
            cur.execute("SELECT * FROM cards WHERE org_name IS NOT NULL AND first_order_date IS NOT NULL ORDER BY (direct_card + link_tree_card) DESC")
            result = cur.fetchall()
            for org in result:
                if isinstance(org[5], (date, datetime)):
                    date_str = org[5].strftime('%Y-%m-%d')
                else:
                    date_str = org[5]
                card = CardButton(org[1], org[2] + org[3], date_str)
                l.append(card)
            cur.close()
            return l
        else:
            cur.execute("SELECT * FROM cards WHERE org_name IS NOT NULL AND first_order_date IS NOT NULL ORDER BY first_order_date DESC")
            result = cur.fetchall()
            for org in result:
                if isinstance(org[5], (date, datetime)):
                    date_str = org[5].strftime('%Y-%m-%d')
                else:
                    date_str = org[5]
                card = CardButton(org[1], org[2] + org[3], date_str)
                l.append(card)
            cur.close()
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
        return render_template('home.html', prompt="Sign in to make an order", prompt2 = "Sign in")
    return render_template('home.html', prompt2 = "Sign out")

@views.route("/contact")
def contact_page():
    if "user" not in session:
        return render_template('contact.html', prompt="Sign in to make an order", prompt2 = "Sign in")
    return render_template('contact.html', prompt2 = "Sign out")

@views.route("/fetch_order_change", methods=["POST"])
# @login_required
def fetch_home():
    global m
    data = request.get_json()
    if 'm' in data:
        m = data['m']
        print(f"request to change card ordering: {m}")
        new_list = orderOrg(m)
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