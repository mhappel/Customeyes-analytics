from xlrd import open_workbook
import collections
import json
import datetime
import customeyes_plots
import pprint

role_prefix_blacklist = ["Accommodation Service Executive", "Commercial Owner", "Customer Service Executive"]

#loading data from Excel
def load_data():
    wb = open_workbook('report.xlsx')
    s = wb.sheets()[0]
    
    header_col_map = dict()
    headers = collections.defaultdict(int)
    data = list()
    
    for col in range(s.ncols):
        if s.cell(4,col).value != u"":
            hdr = s.cell(4,col).value
            headers[hdr] += 1
            
            if headers[hdr] > 1:
                hdr = "{:}_{:}".format(hdr, headers[hdr])
            
            header_col_map[col] = hdr
    for row in range(5,s.nrows):
        d = dict()
        for col in range(s.ncols):
            if s.cell(row,col).value != u"":
                d[header_col_map[col]] = s.cell(row,col).value
        for prefix in role_prefix_blacklist:
            if d["Requisition_Title"].startswith(prefix):
                d = None
                break
        if d is not None and len(d)>0:
            data.append(d)
    return data
 
#creating and dumping data in json 
def load_data_json():
    with open("report.json", "r") as fp:
        data = json.load(fp)
    return data
    
def dump_data(data):
    with open("report.json", "w") as fp:
        json.dump(data, fp)

        
#score calculations functions
def score_converter(d,score_column_name):    
    text_to_score = {'Very easy':0, 'Easy':2.5, 'Average':5, 'Difficult':7.5, 'Very difficult':10}
    if score_column_name in d:
        try:
            v = d[score_column_name].strip()
            return text_to_score[v]
        except KeyError: pass
    return None

def score_strip(d,score_column_name):
    if score_column_name in d:
        if isinstance(d[score_column_name], float):
            return d[score_column_name]
        try:
            return float(d[score_column_name].split('-', 1)[0].strip())
        except ValueError: pass
    return None
    
def average_score_calc(stats): 
    for month,series in stats.items():
        for series_name, scores in series.items():
            if scores is not None and isinstance(scores, list):
                if len(scores)>0:
                    stats[month][series_name] = sum(scores)/len(scores)
                else:
                    stats[month][series_name] = None
              
#date calculators       
def dates_setting(d,date_column_name):
    if date_column_name not in d: 
        return None
    if date_column_name in d:
        day_month_format = date_column_name == 'Rejection Date'
        date_column = d[date_column_name]
        try:
            dates = datetime.datetime.strptime(d[date_column_name],'%m/%d/%Y').date()
            return datetime.date(dates.year,dates.month,1)
        except ValueError:
           return None 

def create_month_axes(start_date, end_date):
    if end_date < start_date:
        raise ValueError("Cannot choose End Date before Start Date")
    stats = dict()
    month = start_date.replace(day = 1)
    while month <= end_date:
        stats[month] = dict()
        if month.month == 12:
            month = month.replace(year = month.year + 1, month = 1)
        else:
            month = month.replace(month = month.month + 1)
    return stats
 
#single and multi line
def line_month_averages(data, date_column_name, score_column_name, stats = None, series_name = None, roles = 'Requisition_Title', role_title = None, start_date = None, end_date = None):   
    if stats is None:
        stats = dict()
    if start_date is None:
        start_date = datetime.date(2016,11,1)
    if series_name is None:
        series_name = role_title or "All Roles"
    if score_column_name == "Degree difficulty interviews":
        score_parser = score_converter
    else:
        score_parser = score_strip
    
    for d in data:
        if role_title is not None and d[roles] != role_title:
            continue
        month = dates_setting(d,date_column_name)

        if month is None or month < start_date or (end_date is not None and month > end_date): 
            continue
        if month not in stats:
            stats[month] = dict()
        if series_name not in stats[month]:
            stats[month][series_name] = list()
        #print score_column_name, repr(d[score_column_name])
        score = score_parser(d,score_column_name)    
        if score is not None:    
            stats[month][series_name].append(score) 
    average_score_calc(stats)
    
    for month in stats.keys():
        if series_name not in stats[month]:
            stats[month][series_name] = None
    
    return stats
 
def draw_lineplot(stats, date_column_name, score_column_name, title):
    if score_column_name == "Degree difficulty interviews":
        ylabels = ("Very Easy", "Very Difficult")
    else:
        ylabels = ("Strongly Disagree", "Strongly Agree")
    
    customeyes_plots.lineplot(stats, "{:} {:}".format("Average score", title), 
        ylabel = "From {:} (0) to {:} (10)".format(*ylabels), xlabel = "By {:}".format(date_column_name), bottom = 0, top = 10) 
        
#bar charts               
def hbar_role_averages(data, score_column_name = None, stats = None, start_date = None, end_date = None, series_name = None, role = 'Requisition_Title', role_titles = None): 
    stats = dict()
    
    if start_date is None:
        start_date = datetime.date(2016,11,1)

    if series_name is None:
        series_name = role_titles or "All Roles"
    if score_column_name == "Degree difficulty interviews":
        score_parser = score_converter
    else:
        score_parser = score_strip
    
    for d in data:
        if role_titles is not None and d[role] not in role_titles:
            continue
        
        month = dates_setting(d,"Application Date")
        if month is None or month < start_date or (end_date is not None and month > end_date): 
            continue    
        
        if d[role] not in stats:
            stats[d[role]] = list()
        score = score_parser(d,score_column_name)    
        if score is not None:    
            stats[d[role]].append(score) 
    
    for rt,scores in (stats.items()):
        if len(scores)>0:
            stats[rt] = sum(scores)/len(scores)
        else:
            del stats[rt]

    return stats
            
def draw_hbarplot(stats, score_column_name, title):
    if score_column_name == "Degree difficulty interviews":
        xlabels = ("Very Easy", "Very Difficult")
    else:
        xlabels = ("Strongly Disagree", "Strongly Agree")
    
    customeyes_plots.hbarplot(stats, "{:} {:}".format("Average score per role", title), 
        xlabel = "From {:} (0) to {:} (10)".format(*xlabels), sort_key = lambda (k,v): v, left = 0, right = 10) 

#TO DO: insert data selection possibility and graphs per role and choice between source and completion status
def barchart_average_scores(data, score_column_name = None, stats = None, start_date = None, end_date = None,  roles = "Requisition_Title", series_name = None, x_series = None, role_title = None):    
    stats = dict()

    if start_date is None:
        start_date = datetime.date(2016,11,1)

    score_column_name = "Recruitment process"  
    x_series = "Source"

    if series_name is None:
        series_name = role_title or "All Roles"
    if score_column_name == "Degree difficulty interviews":
        score_parser = score_converter
    else:
        score_parser = score_strip

    for d in data:
        if role_title is not None and d[roles] != role_title:
            continue
        
        month = dates_setting(d,"Application Date")
        if month is None or month < start_date or (end_date is not None and month > end_date): 
            continue

        if x_series not in d:
            continue
        if d[x_series] not in stats:
            stats[d[x_series]] = list()
        score = score_parser(d,score_column_name) 
        if score is not None:    
            stats[d[x_series]].append(score)

    for x_serie,scores in stats.items():
        if len(scores)>0:
            stats[x_serie] = sum(scores)/len(scores)
        else:
            stats[x_serie] = 0
 
    return stats

def draw_barplot(stats, score_column_name, title):
    customeyes_plots.barplot(stats, "Sources",ylabel="Average Score", bar_width = 0.75, sort_key = lambda (k,v): -v)


#Average overall interview process scores by source

#TO DO: make generic and per role
def source_overall_scores2(data):    
    stats = dict()
    score_column_name = 'Recruitment process'
    for d in data:
        if 'Source' not in d:
            continue
        if d['Source'] not in stats:
            stats[d['Source']] = list()
        if score_column_name in d:
            try:
                v = float(d[score_column_name].split('-', 1)[0].strip())
                stats[d['Source']].append(v)
            except: pass
    for source,scores in stats.items():
        if len(scores)>0:
            stats[source] = sum(scores)/len(scores)
        else:
            stats[source] = 0
 
#def draw_barplot(stats, score_column_name, title)
    customeyes_plots.barplot(stats, "Sources",ylabel="Average Score", bar_width = 0.75, sort_key = lambda (k,v): -v)
    
#Histogram scores overall recruitment process
#TO DO: make it per role
def month_score_dist(data):    
    stats = {
        (0.0,"Strongly disagree"):0,
        (2.5,"Disagree"):0,
        (5.0,"Neither agree nor disagree"):0,
        (7.5,"Agree"):0,
        (10.0,"Strongly agree"):0
        }
    count = 0
    score_column_name = 'Recruitment process'
    for d in data:
        if score_column_name in d:
            try:
                v = d[score_column_name].split('-', 1)    
                if len(v) == 2:
                    v = (float(v[0].strip()), v[1].strip())
                    stats[v] += 1
                    count += 1
            except KeyError:
                pass
    for keys,occ in sorted(stats.items()):
        stats[keys] = (float(occ)/count)*100
    customeyes_plots.barplot(stats, "Distribution scores \"Recruitment Process\"",
        ylabel="%",data_label=lambda k: k[1], bar_width = 1, bottom = 0)
 
def feedback_recieved(data):
    stats = {"Yes":0, "No":0}
    count = 0
    for d in data:
        if "Received feedback" in d:
            v = d["Received feedback"]
            stats[v] += 1
            count += 1
    
    for keys,occ in stats.items():
        stats[keys] = (float(occ)/count)*100
    
    customeyes_plots.pieplot(stats, "Feedback Received?")


def completion_status(data):
    stats = {"Rejected":0, "Offer accepted":0, "Offer declined":0}
    count = 0
    for d in data:
        if "Completion status" in d:
            v = d["Completion status"]
            stats[v] += 1
            count += 1
    
    for keys,occ in stats.items():
        stats[keys] = (float(occ)/count)*100
    
    customeyes_plots.pieplot(stats, "Completion status")    

#satisfaction of interview by interview stage - in progress
def hv_av_scores_interview_stage(data):    
    stats = dict()
    stages = [
        'Satisfaction online assessments',
        'Technical phone interview satisfaction',
        'Recruiter phone interview satisfaction',
        'Satisfaction face to face interviews',
    ]
    for d in data:
        if 'Requisition_Title' not in stats:
            stats['Requisition_Title'] = dict()
            for stage in stages:
                stats['Requisition_Title'][stage] = list()
        for stage in stages:
            if stage in d:
                try:
                    v = float(d[stage].split('-', 1)[0].strip())
                    stats['Requisition_Title'][stage].append(v)
                except: pass
    for Requisition_Title,stages_stats in stats.items():
        for stage,scores in stages_stats.items():
            if len(scores)>10:
                stats[Requisition_Title][stage] = sum(scores)/len(scores)
            else:
                del stats[Requisition_Title][stage]
    
    customeyes_plots.hbarplot(stats, "Average scores per stage per role (High Volume)", 
        xlabel = "Average Score", sort_key = lambda (k,v): v, left = 0, right = 10)      
    
#satisfaction of interview by interview stage  RETHINK GRAPH, NOT WORKING  
def hv_av_scores_interview_stage(data):    
    stats = dict()
    role = 'Requisition_Title'
    stages = [
        'Satisfaction online assessments',
        'Technical phone interview satisfaction',
        'Recruiter phone interview satisfaction',
        'Satisfaction face to face interviews',
    ]
    for d in data:
        if role not in stats:
            stats[role] = dict()
            for stage in stages:
                stats[role][stage] = list()
        for stage in stages:
            if stage in d:
                try:
                    v = float(d[stage].split('-', 1)[0].strip())
                    stats[role][stage].append(v)
                except: pass
    for Requisition_Title,stages_stats in stats.items():
        for stage,scores in stages_stats.items():
            if len(scores)>10:
                stats[Requisition_Title][stage] = sum(scores)/len(scores)
            else:
                del stats[Requisition_Title][stage]
    
    customeyes_plots.hbarplot(stats, "Average scores per stage per role (High Volume)", 
        xlabel = "Average Score", sort_key = lambda (k,v): v, left = 0, right = 10)  

 
def main():
    #data = load_data()
    data = load_data_json()
    #dump_data(data)
    
    #stats = dict()
    #line_month_averages(data, "Application Date", "Recruitment process", stats = stats)
    #line_month_averages(data, "Application Date", "Recruitment process", stats = stats, role_title = "Software Developer")
    #draw_lineplot(stats, "Application Date", "Recruitment process")
    
    #stats = interviewers(data, "Application Date")
    #draw_lineplot(stats, "Application Date", "Feedback on Interviewers")
    
    #stats = booking_values(data)
    #draw_lineplot(stats, "Application Date", "Broken shit")
    
    stage_satisfaction(data)
    #iv_stage_satisfaction_rej_date(data)    
    #source_overall_scores(data)
    #month_score_dist(data)
    #feedback_recieved(data)
    #completion_status(data)
    #hv_av_scores_interview_stage(data)
        
    #with plt.xkcd():

    customeyes_plots.plt.show()
   
if __name__ == "__main__":
    main()