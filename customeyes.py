from xlrd import open_workbook
import collections
import json
import datetime
import customeyes_plots
import pprint

role_prefix_blacklist = ["Accommodation Service Executive", "Commercial Owner", "Customer Service Executive", "Graduate Commercial Owner", "Account Executive",
    "Operations Analyst - Translations and Content Agency", "Operations Coordinator - Freelance Recruitment", "Partner Marketing (CRM) (Marketing Database Specialist)",
    "Process Specialist Inbound", "Recruiter - Headquarters", "Seasonal Customer Relations Associate *Internal*", "Sourcer - Global Leadership", 
    "Sr. Specialist Partner Marketing & Partner Activations", "Topic Specialist - Operations *Internal*", "Customer Service Business", "Booking Home Support", "Market Manager", 
    "Sr. Specialist Partner Marketing", "Regional Manager EMEA - Experiences", "Reporting Analyst", "Sr. Business Analyst - BookingSuite *INTERNAL*", "Booking Home Support Executive"]

#loading data from Excel
def load_data():
    wb = open_workbook("report.xlsx")
    s = wb.sheets()[0]
    
    header_col_map = dict()
    headers = collections.defaultdict(int)
    data = list()
    
    for col in range(s.ncols):
        if s.cell(0,col).value != u"":
            hdr = s.cell(0,col).value
            headers[hdr] += 1
            
            if headers[hdr] > 1:
                hdr = "{:}_{:}".format(hdr, headers[hdr])
            
            header_col_map[col] = hdr
    for idx,row in enumerate(range(1,s.nrows)):
        d = dict()
        for col in range(s.ncols):
            if s.cell(row,col).value != u"":
                d[header_col_map[col]] = s.cell(row,col).value
        for prefix in role_prefix_blacklist:
            if d["Requisition_Title"].startswith(prefix):
                d = None
                break
        
        if d is not None:
            app_date = dates_setting(d,"Application Date", parse_dashes = idx <= 158)
            if app_date is None:
                d["Application Date"] = None
            else:
                d["Application Date"] = [app_date.year, app_date.month, app_date.day]
        if d is not None:
            rej_date = dates_setting(d, "Rejection Date", parse_dashes = idx <= 158)
            if rej_date is None:
                d["Rejection Date"] = None
            else:
                d["Rejection Date"] = [rej_date.year, rej_date.month, rej_date.day]
        
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
def line_month_averages(data, date_column_name, score_column_name, stats = None, series_name = None, roles = "Requisition_Title", role_title = None, start_date = None, end_date = None):   
    if stats is None:
        stats = dict()
    if start_date is None:
        start_date = datetime.date(2016,11,1)
    if series_name is None:
        series_name = "All Roles"

    if score_column_name == "Degree difficulty interviews":
        score_parser = score_converter
    else:
        score_parser = score_strip
    
    for d in data:
        month = dates_setting(d,"Application Date")

        if month is None or month < start_date or (end_date is not None and month > end_date): 
            continue
        if month not in stats:
            stats[month] = dict()
        if series_name not in stats[month]:
            stats[month][series_name] = list()
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
    
    customeyes_plots.lineplot(stats, "{:}".format(title), ylabel = "From {:} (0) to {:} (10)".format(*ylabels), 
        xlabel = "By {:}".format(date_column_name), bottom = 0, top = 10) 
        
            
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
    
    customeyes_plots.barplot(stats, "{:}".format(title), ylabel = "From {:} (0) to {:} (10)".format(*ylabels), bar_width = 0.75, sort_key = lambda (k,(v,c)): -v)


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
def histo_score_dist(data, score_column_name = None, stats = None, start_date = None, end_date = None, roles = "Requisition_Title", series_name = None, role_title = None):       
    if stats is None:
        stats = dict()
    
    count = 0

    if start_date is None:
        start_date = datetime.date(2016,11,1)

    if series_name is None:
        series_name = role_title or "All Roles"
        
    for d in data:
        if role_title is not None and d[roles] != role_title:
            continue
        
        month = dates_setting(d,"Application Date")
        if month is None or month < start_date or (end_date is not None and month > end_date): 
            continue    
 
        if score_column_name in d:
            key = d[score_column_name].replace(u"\u2019", "'")
            if score_column_name != "Degree difficulty interviews":
                key = key.split("-", 1)[-1].strip()
            if key not in stats:
                stats[key] = 0
            stats[key] += 1
            count += 1

    for keys,occ in stats.items():
        stats[keys] = ((float(occ)/count)*100, occ)

    return stats, count    
  
def draw_histoplot(stats, title, order):
    customeyes_plots.histoplot(stats, title, ylabel = "%", sort_key = lambda k:order[k[0]])

def NPS_score_calc(data, score_column_name = None, stats = None, start_date = None, end_date = None, roles = "Requisition_Title", series_name = None, role_title = None):       
    if stats is None:
        stats = dict()
    
    count = 0

    if start_date is None:
        start_date = datetime.date(2016,11,1)

    if series_name is None:
        series_name = role_title or "All Roles"

    for d in data:
        if role_title is not None and d[roles] != role_title:
            continue
        if score_column_name not in d:
            continue
        score_label = (d[score_column_name].split("-", 1)[1].strip())
        
        month = dates_setting(d,"Application Date")
        if month is None or month < start_date or (end_date is not None and month > end_date): 
            continue    

        if score_column_name in d:
            key = score_label
            if key not in stats:
                stats[key] = 0
            stats[key] += 1
            count += 1

    for keys,occ in stats.items():
        stats[keys] = ((float(occ)/count)*100)

    nps_score = int(stats["Promoter"] - stats["Criticaster"])

    return stats, count, nps_score  


def main():
    data = load_data()
    #data = load_data_json()
    dump_data(data)
    
   
if __name__ == "__main__":
    main()
