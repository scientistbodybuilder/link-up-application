from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from .model import mysql
from .auth import login_required, session

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
            cur.execute("SELECT * FROM cards WHERE org_name IS NOT NULL ORDER BY (direct_card + link_tree_card) DESC")
            result = cur.fetchall()
            print(result)
            for org in result:
                card = CardButton(org[1],org[2]+org[3],org[5])
                l.append(card)
            cur.close()
            return l
        else:
            cur.execute("SELECT * FROM cards WHERE org_name IS NOT NULL ORDER BY first_order_date DESC")
            result = cur.fetchall()
            print(result)
            for org in result:
                card = CardButton(org[1],org[2]+org[3],org[5])
                l.append(card)
            cur.close()
            return l
    except Exception as e:
        print(f"Error: {e}")
        return l
    
def getOrgs():
    cur = mysql.connection.cursor()
    l=[]
    try:
        cur.execute("SELECT * FROM cards WHERE org_name IS NOT NULL")
        result = cur.fetchall()
        print(result)
        for org in result:
            card = CardButton(org[1],org[2]+org[3],org[5])
            l.append(card)
        cur.close()
        return l
    except Exception as e:
        print(f"Error: {e}")
        return l

@views.route('/home')
@login_required
def home_page():
    list = orderOrg(m)
    print(list)
    return render_template('home.html', orgs = list)

@views.route("/contact")
@login_required
def contact_page():
    return render_template('contact.html')

@views.route("/fetch_order_change", methods=["POST"])
@login_required
def fetch_home():
    global m
    m = request.get_json()
    return redirect(url_for('views.home_page'))