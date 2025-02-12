from flask import Blueprint, render_template, jsonify,redirect, url_for, request, flash
from .model import Users
from .auth import login_required, session
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from matplotlib.backends.backend_pdf import PdfPages
import os
from pathlib import Path
plt.style.use("seaborn-v0_8-whitegrid")
from dotenv import load_dotenv

load_dotenv()

def maxDateRange(df_list):
    length = 0
    d = None
    for data in df_list:
        if len(data['df']['Date'].to_list()) > length:
            length = len(data['df']['Date'].to_list())
            d = data['df']['Date'].to_list()

    return d

def reviewRange(df_list):
    l = []
    for data in df_list:
        reviews = data['df']['Review Count'].to_list()
        l = l + reviews

    l =  list(set(l))
    return [min(l), max(l)]


analytic=Blueprint('analytic', __name__)
@analytic.route('/analytic')
@login_required
def dashboard():
    return render_template('analytic.html')

@analytic.route('/analytic_report', methods=['POST'])
@login_required
def genReport():
    if "report_data" in session:
        pass
    else:
        email = session["user"]
        print(email)
        user = Users.query.filter_by(email=email).first()
        org_name = user.org_name
        print(org_name)
        try:

            download_dir = str(Path.home() / "Downloads")
            pdf_path = os.path.join(download_dir, f"{org_name} Review Analytics.pdf")
            df = pd.read_excel(r'C:\Users\ousma\Downloads\Projects\Python\link-up-application\data\linkup_data.xlsx',sheet_name=org_name)

            locations = list(set(df['Location'].to_list()))
            print(f'locations: {locations}')
            df_list = []
            for location in locations:
                df_list.append({'df':df[df['Location']==location],'location':location})

            print(f'df list: {df_list}')
            date_axis = maxDateRange(df_list)
            date_axis = [datetime.strptime(x,'%m/%d/%Y') for x in date_axis]

            review_range = reviewRange(df_list)

            with PdfPages(pdf_path) as pdf:
                # create individual figures
                for location in locations:
                    fig, ax = plt.subplots()
                
                    temp = df[df['Location']==location]
                    y_axis = temp['Review Count'].to_list()
                    y_axis = [int(x) for x in y_axis]

                    # x_axis = temp['Date'].to_list()
                    # x_axis = [datetime.strptime(x,'%m/%d/%Y') for x in x_axis]

                    ax.plot(date_axis,y_axis,label=location)
                    ax.set_ylim(review_range)
                    ax.set_title(f"{org_name} - {location} Review Growth")
                    ax.set_ylabel('Review Count')
                    ax.set_xlabel('Date')
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b, %d, %Y'))
                    fig.autofmt_xdate()
                    fig.tight_layout()

                    pdf.savefig()
        
                #Create the multi plot figure
                # need to get the longest date range
                print(date_axis)
                fig1, ax1 = plt.subplots()
                for data in df_list:
                    ax1.plot(date_axis,data['df']['Review Count'], label=data['location'])

                ax1.set_title(f"{org_name} - {location} Review Growth")
                ax1.set_ylabel('Review Count')
                ax1.set_xlabel('Date')
                ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b, %d, %Y'))
                fig1.autofmt_xdate()
                # fig.tight_layout()

                # Adjust layout
                plt.legend()
                plt.tight_layout()

                pdf.savefig()

            flash('Report Generated Successfully!')
        except Exception as e:
            print(f'Error: {e}')
            flash('Report Generation Failed')




