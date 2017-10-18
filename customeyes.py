from xlrd import open_workbook
import collections
import json
import datetime
import customeyes_plots
import pprint
import re

role_column_name = "Requisition_Title"

role_prefix_blacklist = ["Accommodation Service Executive", "Commercial Owner", "Customer Service Executive", "Graduate Commercial Owner", 
    "Operations Analyst - Translations and Content Agency", "Operations Coordinator - Freelance Recruitment", "Partner Marketing (CRM) (Marketing Database Specialist)",
    "Process Specialist Inbound", "Recruiter - Headquarters", "Seasonal Customer Relations Associate *Internal*", "Sourcer - Global Leadership", 
    "Sr. Specialist Partner Marketing & Partner Activations", "Topic Specialist - Operations *Internal*", "Customer Service Business", "Jr. Commercial Owner", 
    "Sr. Internal Communications Specialist","Global Implementation Specialist - Operational Excellence"]

role_title_map = {
    "Back End Developers (Referrals only)":             "Back End Developer", 
    "Back End Developers / Referrals":                  "Back End Developer",
    "Software Developer (Headhunts only)":              "Back End Developer",
    "Software Developer- Headhunts only":               "Back End Developer",
    "Software Engineer":                                "Back End Developer",
    "Perl Developer":                                   "Back End Developer",
    "Software Developer":                               "Back End Developer",
    "Sr. Software Engineer":                            "Sr. Software Developer",
    "Business Applications Specialist":                 "IT Business Applications Engineer",
    "Enterprise Applications Developer":                "IT Business Applications Engineer",
    "Enterprise Applications Developer (BusApps - ITS)":"IT Business Applications Engineer",
    "Front End Developer (Headhunts only)":             "Front End Developer",
    "Front End Developer *Headhunts*":                  "Front End Developer",
    "IT Business Applications Specialist":              "IT Business Applications Engineer",
    "Data Center Engineer - UK (Netw - CoreInfra)":     "Data Center Engineer - UK",
    "Data Scientist Machine Learning":                  "Data Scientist - Machine Learning",
    "Data Scientist - General (Headhunts only)":        "Data Scientist - General",
    "Data Scientist Online Advertising":                "Data Scientist - Online Advertising",
    "IT Support Desk Technician - Berlin (Support - ITS)": "IT Support Desk Technician - Berlin",
    "Internship User Research":                         "Internship - User Research",
    "Network Engineer (Netw - CoreInfra)":              "Network Engineer",
    "Network Tools Developer (NetOffices - ITS)":       "Network Tools Developer - IT Services",
    "Network Tools and Automation Engineer (NetOffices - ITS)": "Network Tools Developer - IT Services",
    "Product Owner E-commerce (Referrals only)":        "Product Owner E-commerce",
    "Referral Product Owner E-commerce":                "Product Owner E-commerce",
    "Sr. Devops Engineer (Monitoring - ITS)":           "Sr. Devops Engineer",
    "Sr. Software Engineer":                            "Sr. Software Developer",
    "Systems Engineer (Platform - ITS)":                "Systems Engineer",
    "UX Designer (Headhunts only)":                     "UX Designer",
    "UX Designer - Headhunts only":                     "UX Designer",
    "Wireless Network Engineer (NetOffices - ITS)":     "Wireless Network Engineer",
    "(Event - Women in Tech) UX Designer":              "Event - Women in Tech - UX Designer",
    "(Event) Assessment Days Mexico City":              "Event - Assessment Day - Mexico City",
    "(Event) Copywriters - Women in Tech Hackathon":    "Event - Women in Tech - Hackathon - Copywriters",
    "(Event) Hackathon Munich":                         "Event - Hackathon - Munich",
    "(Event) Mexico Hackathon":                         "Event - Hackathon - Mexico",
    "(Event) Taipei Hackathon":                         "Event - Hackathon - Taipei",
    "Taipei Software Developers":                       "Event - Hackathon - Taipei - Software Developer",
    "(Event) Technology Interview Day Guadalajara":     "Event - Technology Interview Day - Guadalajara",
    "(Event) Women in Tech Hackathon":                  "Event - Women in Tech - Hackathon",
    "(Event) Women in Tech: Front End Developer":       "Event - Women in Tech - Front End Developer",
    "Assessment day South Africa":                      "Event - Assessment Day - South Africa",
    "HACK WITH PRIDE":                                  "Event - Hackathon - Hack With Pride",
    "Hack a Holiday - Manila Edition":                  "Event - Hackathon - Manila",
    "Product Owner (Women in Tech)":                    "Event - Women in Tech - Product Owner",
    "B2B Copywriter":                                   "Copywriter - B2B",
    "Software Developer & Team Lead":                   "Team Lead - Software Development",
    "Sr. Data Scientist Online Advertising":            "Sr. Data Scientist - Online Advertising",
    "IT Support Desk Team Lead":                        "Team Lead IT Support Desk",
}

role_groups = [
    {"group_title": "Product Owner", "pattern": re.compile(r"^Product Owner")},
    {"group_title": "Event", "pattern": re.compile(r"^Event -")},
    {"group_title": "Graduates", "pattern": re.compile(r"^Graduate")},
    {"group_title": "Designer", "pattern": re.compile(r"^Designer.*$|^(?!Sr\.|Graduate).*Designer$")},
    {"group_title": "Mobile Developer", "pattern": re.compile(r"^(Android|iOS) Developer")},
    {"group_title": "Copywriter", "pattern": re.compile(r"^Copywriter -")}, 
    {"group_title": "Cyber Security", "pattern": re.compile(r"^Cyber Security")},
    {"group_title": "Data Analyst", "pattern": re.compile(r"^Data Analyst -")},
    {"group_title": "Data Scientist", "pattern": re.compile(r"^Data Scientist -")},
    {"group_title": "Sr. Mobile Developer", "pattern": re.compile(r"^(Sr\. Android|Sr\. iOS) Developer")},
    {"group_title": "Sr. Data Scientist", "pattern": re.compile(r"^Sr\. Data Scientist -")},
    {"group_title": "Sr. Product Owner", "pattern": re.compile(r"^Sr\. Product Owner")},
    {"group_title": "Recruiter", "pattern": re.compile(r".*Recruiter.*")}, 
    {"group_title": "Sr. Designer", "pattern": re.compile(r"^Sr\..*Designer$")},
    {"group_title": "Site Reliability Engineer", "pattern": re.compile(r"^(Site Reliability Engineer|MySQL Database Engineer)")},
]

#loading data from Excel
def load_data():
    wb = open_workbook("report.xlsx")
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
            d["Requisition_Title"] = role_title_map.get(d["Requisition_Title"], d["Requisition_Title"])

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
    text_to_score = {"Very easy":0, "Easy":2.5, "Average":5, "Difficult":7.5, "Very difficult":10}
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
            return float(d[score_column_name].split("-", 1)[0].strip())
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
def dates_setting(d, date_column_name, parse_dashes = False):
    if date_column_name not in d: 
        return None
    if date_column_name in d:
        if isinstance(d[date_column_name], list):
            return datetime.date(d[date_column_name][0], d[date_column_name][1],1)
        try:
            dates = datetime.datetime.strptime(d[date_column_name],"%m/%d/%Y").date()
            return datetime.date(dates.year,dates.month,1)
        except TypeError:
            if parse_dashes:
                parts = d[date_column_name].split("-",3)
                if len(parts) == 3:
                    try:
                        return datetime.date(int(parts[2]),int(parts[1]),1)
                    except TypeError: pass
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
def line_month_averages(data, date_column_name, score_column_names, stats = None, series_name = None, series_names = None, role_title = None, selected_roles = None, start_date = None, end_date = None):   
    if stats is None:
        stats = dict()
    if start_date is None:
        start_date = datetime.date(2016,11,1)

    if selected_roles is not None:
        series_names = set()
        for target_names in selected_roles.values():
            series_names.update(target_names)
        score_column_names = [score_column_names[0]]*len(series_names)

    for d in data:
        if selected_roles is not None:
            if d[role_column_name] not in selected_roles:
                continue
        else:
            if role_title is not None and d[role_column_name] != role_title:
                continue
        
        month = dates_setting(d,date_column_name)

        if month is None or month < start_date or (end_date is not None and month > end_date): 
            continue
        if month not in stats:
            stats[month] = dict()

        for idx, sn in enumerate(series_names):
            if sn not in stats[month]:
                stats[month][sn] = list()

            score_column_name = score_column_names[idx]
            if score_column_name == "Degree difficulty interviews":
                score_parser = score_converter
            else:
                score_parser = score_strip

            score = score_parser(d,score_column_name)    
            if score is not None:    
                if selected_roles is not None:
                    if sn not in selected_roles[d[role_column_name]]:
                        continue         

                stats[month][sn].append(score) 

    average_score_calc(stats)

    for month in stats.keys():
        if series_name is None:
            for sn in series_names:
                if sn not in stats[month]:
                    stats[month][sn] = None
        if series_name not in stats[month]:
            stats[month][series_name] = None
    
    pprint.pprint(stats)

    return stats
 
def draw_lineplot(stats, date_column_name, score_column_name, title):
    if score_column_name == "Degree difficulty interviews":
        ylabels = ("Very Easy", "Very Difficult")
    else:
        ylabels = ("Strongly Disagree", "Strongly Agree")
    
    customeyes_plots.lineplot(stats, "{:}".format(title), ylabel = "From {:} (0) to {:} (10)".format(*ylabels), 
        xlabel = "By {:}".format(date_column_name), bottom = 0, top = 10) 
        
#bar charts               
def hbar_role_averages(data, date_column_name = None, score_column_name = None, stats = None, start_date = None, end_date = None, series_name = None, selected_roles = None): 
    stats = dict()
    
    if start_date is None:
        start_date = datetime.date(2016,11,1)
    
    if selected_roles is not None:
        series_names = set()
        for target_names in selected_roles.values():
            series_names.update(target_names)

    if score_column_name == "Degree difficulty interviews":
        score_parser = score_converter
    else:
        score_parser = score_strip
    
    for d in data:
        if selected_roles is not None and d[role_column_name] not in selected_roles:
            continue
        
        month = dates_setting(d,date_column_name)
        if month is None or month < start_date or (end_date is not None and month > end_date): 
            continue    
        
        for target_name in selected_roles.get(d[role_column_name]):
            if target_name not in stats:
                stats[target_name] = list()
            score = score_parser(d,score_column_name)    
            if score is not None:    
                stats[target_name].append(score) 

    for rt,scores in (stats.items()):
        record_count = len(scores)
        if record_count>0:
            stats[rt] = (sum(scores)/record_count, record_count)
        else:
            del stats[rt]

    #pprint.pprint(stats)

    return stats
            
def draw_hbarplot(stats, score_column_name, title):
    if score_column_name == "Degree difficulty interviews":
        xlabels = ("Very Easy", "Very Difficult")
    else:
        xlabels = ("Strongly Disagree", "Strongly Agree")
    
    customeyes_plots.hbarplot(stats, "{:}".format(title), xlabel = "From {:} (0) to {:} (10)".format(*xlabels), sort_key = lambda (k,(v,c)): v, left = 0, right = 10) 

#TO DO: insert data selection possibility and graphs per role and choice between source and completion status
def barchart_average_scores(data, score_column_name = None, stats = None, start_date = None, end_date = None, roles = "Requisition_Title", series_name = None, x_series = None, role_title = None):    
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
        record_count = len(scores)
        if record_count>0:
            stats[x_serie] = (sum(scores)/record_count,record_count)
        else:
            stats[x_serie] = (0,0)
 
    return stats

def draw_barplot(stats, score_column_name, title):

    if score_column_name == "Degree difficulty interviews":
        ylabels = ("Very Easy", "Very Difficult")
    else:
        ylabels = ("Strongly Disagree", "Strongly Agree")
    
    customeyes_plots.barplot(stats, "{:}".format(title), ylabel = "From {:} (0) to {:} (10)".format(*ylabels), bar_width = 0.75, sort_key = lambda (k,(v,c)): -v) #TO DO: Change the generation of title


#Pie charts per role
def pie_chart_calc(data, score_column_name = None, stats = None, start_date = None, end_date = None,  role = "Requisition_Title", series_name = None, role_title = None):
    
    stats = dict()
    count = 0

    if start_date is None:
        start_date = datetime.date(2016,11,1)

    if series_name is None:
        series_name = role_title or "All Roles"

    for d in data:
        if role_title is not None and d[role] != role_title:
            continue
        
        month = dates_setting(d,"Application Date")
        if month is None or month < start_date or (end_date is not None and month > end_date): 
            continue
           
        if score_column_name in d:
            v = d[score_column_name]
            if v not in stats:
                stats[v] = 0
            stats[v] += 1
            count += 1

    for keys,occ in stats.items():
        stats[keys] = (float(occ)/count)*100

    return stats, count
    
def draw_pieplot(stats, title):
    customeyes_plots.pieplot(stats, title)




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
    score_column_name = "Recruitment process"
    for d in data:
        if score_column_name in d:
            try:
                v = d[score_column_name].split("-", 1)    
                if len(v) == 2:
                    v = (float(v[0].strip()), v[1].strip())
                    stats[v] += 1
                    count += 1
            except KeyError:
                pass
    for keys,occ in sorted(stats.items()):
        stats[keys] = (float(occ)/count)*100
    customeyes_plots.histoplot(stats, "Distribution scores \"Recruitment Process\"",ylabel="%",data_label=lambda k: k[1])




#satisfaction of interview by interview stage - in progress
def hv_av_scores_interview_stage(data):    
    stats = dict()
    stages = [
        "Satisfaction online assessments",
        "Technical phone interview satisfaction",
        "Recruiter phone interview satisfaction",
        "Satisfaction face to face interviews",
    ]
    for d in data:
        if "Requisition_Title" not in stats:
            stats["Requisition_Title"] = dict()
            for stage in stages:
                stats["Requisition_Title"][stage] = list()
        for stage in stages:
            if stage in d:
                try:
                    v = float(d[stage].split("-", 1)[0].strip())
                    stats["Requisition_Title"][stage].append(v)
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
    role = "Requisition_Title"
    stages = [
        "Satisfaction online assessments",
        "Technical phone interview satisfaction",
        "Recruiter phone interview satisfaction",
        "Satisfaction face to face interviews",
    ]
    for d in data:
        if role not in stats:
            stats[role] = dict()
            for stage in stages:
                stats[role][stage] = list()
        for stage in stages:
            if stage in d:
                try:
                    v = float(d[stage].split("-", 1)[0].strip())
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
    data = load_data()
    #data = load_data_json()
    dump_data(data)
    
    #stats = dict()
    #line_month_averages(data, "Application Date", "Recruitment process", stats = stats)
    #line_month_averages(data, "Application Date", "Recruitment process", stats = stats, role_title = "Software Developer")
    #draw_lineplot(stats, "Application Date", "Recruitment process")
    
    #stats = interviewers(data, "Application Date")
    #draw_lineplot(stats, "Application Date", "Feedback on Interviewers")
    
    #stats = booking_values(data)
    #draw_lineplot(stats, "Application Date", "Broken shit")
    
    #stage_satisfaction(data)
    #iv_stage_satisfaction_rej_date(data)    
    #source_overall_scores(data)
    #month_score_dist(data)
    #feedback_recieved(data)
    #completion_status(data)
    #hv_av_scores_interview_stage(data)
        
    #with plt.xkcd():

    #customeyes_plots.plt.show()
   
if __name__ == "__main__":
    main()
