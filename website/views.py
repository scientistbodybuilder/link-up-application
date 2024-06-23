from flask import Blueprint, render_template
from .model import mysql
from .auth import login_required, session

views=Blueprint('views', __name__)

class CardButton():
    def __init__(self,name,card_num,date):
        self.name = name
        self.card_num = card_num
        self.date = date

# def listByCards():
#     cur = mysql.connection.cursor()
#     l=[]
#     try:
#         cur.execute("SELECT * FROM cards WHERE org_name != NULL")
#         result = cur.fetchall()
#         for org in result:
#             card = CardButton(org[1],org[2]+org[3],org[5])
#             l.append(card)
#         cur.close()
#         return l

#     except Exception as e:
#         print(f"Error: {e}")

# def listByDate():
#     cur = mysql.connection.cursor()
#     l=[]
#     try:
#         cur.execute("SELECT * FROM cards WHERE org_name != NULL")
#         result = cur.fetchall()
#         for org in result:
#             card = CardButton(org[1],org[2]+org[3],org[5])
#             l.append(card)
#         cur.close()
#         return l
#     except Exception as e:
#         print(f"Error: {e}")

def getOrgs():
    cur = mysql.connection.cursor()
    l=[]
    try:
        cur.execute("SELECT * FROM cards WHERE org_name != NULL")
        result = cur.fetchall()
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
    list = getOrgs()
    return render_template('home.html', orgs = list)

@views.route("/contact")
@login_required
def contact_page():
    return render_template('contact.html')



# {% for org in list %}
#     <li>
#         <div class="drop-down">
#             <button> 
#                 {% org.name %}
#             </button>
#             <div class="stat">
#                 <p>Cards in use: {% org.card_num %}</p>
#                 <p>Date joined: {% org.date %}</p>
#             </div>
#         </div>
#     </li>
# {% endfor %}