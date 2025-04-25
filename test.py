import pandas as pd
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MaxNLocator
sns.set_theme()
# Sample Data (Dates and Values)
df = pd.read_excel(r'C:\Users\ousma\Downloads\testdata.xlsx')

# Convert 'date' to datetime (if not already)
def acronym(exception):
    if exception == 'Duplicate Expense Same Employee':
        return 'DESE'
    elif exception == 'Duplicate Expense Different Employees':
        return 'DEDE'
    elif exception == 'Duplicate Expense Mileage Submission':
        return 'DEMS'
    elif exception == 'Expense Excessive Out of Pocket':
        return 'EEOP'
    elif exception == 'Expense Excessive Personal':
        return 'EEP'
    elif exception == 'Expense Out of Pocket Unusual':
        return 'EOPU'
    elif exception == 'Expense Excessive Late Submission':
        return 'EELS'
    else:
        return 'No Exception'
    
def get_date(date):
    d = datetime.strptime(date,'%Y-%m-%d %I:%M')
    return d

def get_exceptions_per_day(date_list,df,exception):
    temp = df[df['Exception']==exception]
    count_list = []
    for date in date_list:
        t = temp[temp['Tran Date']==date]
        count = t['Exception'].count()
        count_list.append(count)

    return count_list


df['Exception Acronym'] = df.apply(lambda x: acronym(x['Exception']),axis=1)
df['Tran Date'] = pd.to_datetime(df['Tran Date'], format='%Y-%m-%d', errors='coerce')
df = df.dropna(subset=['Tran Date'])

colors = ['#f7b7a3','#ea5f89','#9b3192','#57167e','#2b0b35','#6050dc','#fff1c9']
dese_count = df[df['Exception Acronym']=='DESE'].count()[0]
dede_count = df[df['Exception Acronym']=='DEDE'].count()[0]
dems_count = df[df['Exception Acronym']=='DEMS'].count()[0]
eeop_count = df[df['Exception Acronym']=='EEOP'].count()[0]
eep_count = df[df['Exception Acronym']=='EEP'].count()[0]
eels_count = df[df['Exception Acronym']=='EELS'].count()[0]
eopu_count = df[df['Exception Acronym']=='EOPU'].count()[0]
no_exception = df[df['Exception Acronym']=='No Exception'].count()[0]

count_categories = [dese_count,dede_count,dems_count,eep_count,eopu_count,eeop_count,eels_count]
labels = ['DESE','DEDE','DEMS','EEP','EOPU','EEOP','EELS']

path = r'C:\Users\ousma\Downloads\summary.pdf'
with PdfPages(path) as pdf:
    # plt.figure(figsize=(10,8))
    # plot 1 bar chart with total count of exceptions type
    print('PLOT 1')
    #data prep
    plot_labels = []
    plot_categories = []
    for l,c in zip(labels,count_categories):
        if c>0:
            plot_categories.append(c)
            plot_labels.append(l)
    plot_colors = colors[:len(plot_categories)]

    #plot
    fig1, ax1 = plt.subplots()
    ax1.bar(plot_labels,height=plot_categories,color=plot_colors,tick_label=plot_labels)
    ax1.set_title("Total Exception Occurances in Feb 2025")
    ax1.set_ylabel('Exception Count')
    ax1.set_xlabel('Exception Types')

    # fig1.tight_layout()
    pdf.savefig()

    # plot 2 pie chart with total percentages of exception type 
    print('PLOT 2')
    pie_categories = plot_categories + [no_exception]
    pie_labels = plot_labels + ['No Exception']
    pie_colors = colors + ['#2b0b28']
    pie_percentages = [100.*x/sum(pie_categories) for x in pie_categories]
    #update labels with percentages
    pie_labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(pie_labels,pie_percentages)]
    
    #plot
    fig2, ax2 = plt.subplots()
    sections = ax2.pie(pie_categories,colors=pie_colors,radius=1)
    ax2.set_title('Total Exception Occurances in Feb 2025 (Percentage)')
    fig2.legend(sections,labels=pie_labels, loc='upper left',fontsize=7,bbox_to_anchor=(0,0.9))
    fig2.tight_layout()
    pdf.savefig()

    #plot 3 a time series chart over the course of the month's transaction dates
    print('PLOT 3')
    #data work - for each exception, create a list of it's amount of occurances per each day of the time series
    dates = sorted(list(set(df['Tran Date'].to_list())))

    dese_ts = get_exceptions_per_day(dates,df,'Duplicate Expense Same Employee')
    dede_ts = get_exceptions_per_day(dates,df,'Duplicate Expense Different Employees')
    dems_ts = get_exceptions_per_day(dates,df,'Duplicate Expense Mileage Submission')
    eeop_ts = get_exceptions_per_day(dates,df,'Expense Excessive Out of Pocket')
    eep_ts = get_exceptions_per_day(dates,df,'Expense Excessive Personal')
    eels_ts = get_exceptions_per_day(dates,df,'Expense Excessive Late Submission')
    eopu_ts = get_exceptions_per_day(dates,df,'Expense Out of Pocket Unusual')

    print(f'We have {len(dates)}')
    print(f'dese ts: {dese_ts}')
    print(f'dates: {dates}')

    #plot
    fig3, ax3 = plt.subplots()
    ax3.set_title('Time Series of Exception Occurances')
    ax3.set_ylabel('Exception Count')
    ax3.set_xlabel('Days')
    ax3.plot(dates,dese_ts,label='DESE',color='#57167e')
    ax3.plot(dates,dede_ts,label='DEDE',color='#9b3192')    
    ax3.plot(dates,eels_ts,label='EELS',color='#57167e')


    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b, %d, %Y'))
    ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
    fig3.autofmt_xdate()
    # fig3.tight_layout()
    fig3.legend(loc='upper right',fontsize=6)

    pdf.savefig()


    #plot 4. Another pie chart of which exceptions are taking up the most expense
