#----------------------------------------------------------------------
# A very simple wxPython example.  Just a wx.Frame, wx.Panel,
# wx.StaticText, wx.Button, and a wx.BoxSizer, but it shows the basic
# structure of any wxPython application.
#----------------------------------------------------------------------
import pprint
import datetime
import customeyes
import customeyes_plots
import wx
import wx.dataview


category_info = {
    1: {
        "show_all": True,
        "series": [
            ["Recruitment process"],
            ["Degree difficulty interviews"],
            ["Fast application process"],
            [
                "Interviewers were friendly",
                "Interviewers were professional",
                "Interviewers were interested in my unique skills",
                "Interviewers were interested in my experience",
            ], 
            [
                "Customer oriented",
                "Innovative",
                "Data driven",
                "Getting things done",
                "Humble and open atmosphere",    
            ],
            [
                "Satisfaction feedback",
                "Feedback concrete",
                "Feedback recognizable",
            ],
            [   "I found the content of the blog helpful in my prep...",
                "I thought that the booking.com blog gave me a good...",
            ],
            [   "Satisfaction online assessments",
                "Recruiter phone interview satisfaction",
                "Technical phone interview satisfaction",
                "Satisfaction face to face interviews",
            ],
            [   "Offer accepted (OA): Satisfaction offer",
                "Offer accepted: Satisfaction salary and benefits",
                "Offer accepted: Clarity job letter",
                "Offer declined(OD): Satisfaction offer",
                "Offer declined: Satisfaction salary and benefits",
                "Offer declined: Clarity job letter",
            ],
        ],
        "labels": [
            ["Overall recruitment process"],
            ["Overall degree difficulty interviews"],
            ["Perception speed application process"],
            [
                "...were friendly",
                "...were professional",
                "...were interested in my unique skills",
                "...were interested in my experience",
            ], 
            [
                "...is customer oriented",
                "...is innovative",
                "...is data driven",
                "...is getting things done every day",
                "...has a humble and open atmosphere",    
            ],
            [
                "Overall, I'm satisfied with the feedback I received",
                "The feedback I received was concrete and constructive",
                "The feedback I received was recognizable/fair",
            ],
            [   "I found the blog helpful in my preparation",
                "I thought the blog gave me a good insight in the challenges",
            ],
            [   "Online assessments",
                "Recruiter phone screen",
                "Technical phone interview",
                "Face to face interviews",
            ],
            [   "Offer accepted: Overall, I'm satisfied with the offer I received",
                "Offer accepted: To what extent where you satisfied with the salary and benefits?",
                "Offer accepted: The offer letter was clear to me",
                "Offer declined: Overall, I'm satisfied with the offer I received",
                "Offer declined: To what extent where you satisfied with the salary and benefits?",
                "Offer declined: The offer letter was clear to me",
            ],
        ],
        "questions": [
            "\"Overall, I am satisfied with the recruitment process\"",
            "\"Could you describe the degree of difficulty of the interviews?\"", 
            "\"I have the feeling that Booking.com acts fast\"",
            "\"The interviewers I communicated with...\"", 
            "\"I think Booking.com...\"", 
            "Feedback Quality",
            "Feedback on Booking.com Tech Blog",
            "\"Overal, I am satisfied with the interview(s) I had\"",
            "Feedback on Offers",
        ],
    },
    2: {
        "series":
            ["Recruitment process","Degree difficulty interviews", "Fast application process"],
        "questions": [
            "\"Overall, I am satisfied with the recruitment process\"",
            "\"Could you describe the degree of difficulty of the interviews?\"", 
            "\"I have the feeling that Booking.com acts fast\"",
            ],
    },
    3: {
        "series": 
            ["Source", "Completion status", "Rejection Reason", "Number of interviews", "Degree difficulty interviews"],
        "series_labels":
            ["By Source", "By Completion status", "By Rejection reason", "By Number of interviews", "By degree difficulty interviews"],
        "questions": [
            "\"Overall, I am satisfied with the recruitment process\"",
            "\"Could you describe the degree of difficulty of the interviews?\"", 
            "\"I have the feeling that Booking.com acts fast\"",
            ],
    },
    4: {
        "series":
            ["Received feedback", "Completion status", "Did you read the booking.com technical blog?"],
        "questions": [
            "\"I recieved feedback after/during my application\"", 
            "Distribution rejected, offered and hired",
            "\"Did you read the technical blog?\"",
            ],
    },
    5: {
        "series":
            ["Recruitment process","Degree difficulty interviews", "Fast application process"],
        "questions": [
            "\"Overall, I am satisfied with the recruitment process\"",
            "\"Could you describe the degree of difficulty of the interviews?\"", 
            "\"I have the feeling that Booking.com acts fast\"",
            ],
    },
    6: {
        "series":
            ["Recommend as employer", "Recommend as customer"],
        "questions": [
            "\"I recommend Booking.com as an employer to others\"\nNPS score:",
            "\"Taking your application process into account, I recommend others to book accomodations at Booking.com\"\nNPS score:",
            ],
    },
}

# questions answered:
#    "\"Overall, I am satisfied with the recruitment process\"","\"I think Booking.com is...\"", "\"The interviewers I communicated with...\"", 
#    "\"Could you describe the degree of difficulty of the interviews?\"", "\"I recieved feedback after/during my application\"", 
#    "\"Overall, I'm satisfied with the feedback I recieved\"", "\"I have the feeling that Booking.com acts fast\""]
#    "\"Did you read the technical blog?\"", "\"I found the content of the blog helpful in my preparation\"", 
#    "\"I thought the blog gave me good insight in the technical challenges I would face\"", "\"Overall, I am satisfied with the offer I recieved\"",
#    "\"To what extend where you satisfied with the salary and benefits?\"" 
#    "\"The job offer letter was clear to me\"",

# questions to be answered:
#    "\"Overal, I am satisfied with the interview(s) I had\"" => Made a graph per stage, but there is no column with this actual data.
    
# questions not yet answered in graphs: 
#    "\"It was clear to me what I could expect from the application procedure\"", "\"How many rounds of interviews have you had in total?\"", 
#    "\"Did you have online assessments?\""


#Popup window for parameters (and graph)
class Base_GraphWindow(wx.Frame):

    panel = None

    def __init__(
            self, parent, ID, title, button_id, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
            ):
        
        super(Base_GraphWindow, self).__init__(parent, ID, title, pos, size, style)
        self.button_id = button_id
        self.category = button_id/100
        self.series_idx = button_id - (self.category*100 + 1)

        self.panel = wx.Panel(self, -1)
        instruction = wx.StaticText(self.panel, -1, "Choose parameters for the graph", (15, 8))
        instruction.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))

    def create_date_select(self, base_y):
       
        month_choices = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        wx.StaticText(self.panel, -1, "Select Start Month:", (15, base_y + 5))
        self.startmonthch = wx.Choice(self.panel, -1, (125, base_y), choices = month_choices)
        self.startmonthch.SetSelection(10)
        self.Bind(wx.EVT_CHOICE, self.on_parameter_change, self.startmonthch)
        
        end_date = datetime.date.today()
        
        year_choices = list()
        year = 2016
        while year <= end_date.year:
            year_choices.append(str(year))
            year += 1
            
        self.startyearch = wx.Choice(self.panel, -1, (220, base_y), choices = year_choices)
        self.startyearch.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.on_parameter_change, self.startyearch)
        
        wx.StaticText(self.panel, -1, "Select End Month:", (15, base_y + 40))
        self.endmonthch = wx.Choice(self.panel, -1, (125, base_y + 35), choices = month_choices)
        self.endmonthch.SetSelection(end_date.month -1)
        self.Bind(wx.EVT_CHOICE, self.on_parameter_change, self.endmonthch)
        
        self.endyearch = wx.Choice(self.panel, -1, (220, base_y + 35), choices = year_choices)
        self.endyearch.SetSelection(end_date.year - 2016)
        self.Bind(wx.EVT_CHOICE, self.on_parameter_change, self.endyearch)

#TO DO: to redraw graph
    def on_parameter_change(self, event):
        print "Check!"
 

class Line_Hbar_GraphWindow(Base_GraphWindow):
    #Popup window for parameters (and graph)

    def __init__(self, parent, ID, title, button_id, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        super(Line_Hbar_GraphWindow, self).__init__(parent, ID, title, button_id, pos, size, style)

        choices = ["By Application Date", "By Rejection Date"]
        self.datesch = wx.Choice(self.panel, -1, (15, 35), choices = choices)
        self.datesch.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.on_parameter_change, self.datesch)

        self.create_date_select(70)

        if category_info[self.category].get("show_all", False):
            self.roles = ["All"] + app.roles
        else:
            self.roles = app.roles

        if self.button_id > 200 or len(category_info[self.category]["series"][self.series_idx]) == 1:        
            self.rolelb = wx.CheckListBox(self.panel, -1, (15,140), (450,150), self.roles)
            self.Bind(wx.EVT_CHECKLISTBOX, self.on_role_select, self.rolelb)
            #self.rolelb.SetCheckedItems([0])
        else:
            self.rolelb = wx.ListBox(self.panel, -1, (15,140), (450,150), self.roles, wx.LB_SINGLE)
            self.Bind(wx.EVT_LISTBOX, self.on_parameter_change, self.rolelb)
            self.rolelb.SetSelection(0)
        
        if self.button_id > 200:
            publishbtn = wx.Button(self.panel, -1, "Show Chart", (15,320))
            self.Bind(wx.EVT_BUTTON, self.On_publish_hbar_chart, publishbtn)
        else:
            publishbtn = wx.Button(self.panel, -1, "Show Graph", (15,320))
            self.Bind(wx.EVT_BUTTON, self.on_publish_graph, publishbtn)

    def on_role_select(self,event):
        if self.button_id > 200:
            max_choice = 12
        else:
            max_choice = 6
        
        if len(self.rolelb.GetCheckedItems()) > max_choice:
            self.rolelb.Check(event.GetSelection(),False)
            max_alert = "{:} {:} {:}".format("Cannot select more than", max_choice, "items") 
            dlg = wx.MessageDialog(self, max_alert, "Alert", wx.OK | wx.ICON_EXCLAMATION)                              
            dlg.ShowModal()
            dlg.Destroy()
     
    def on_publish_graph(self,event):
        if self.datesch.GetSelection() == 0:
            date_column_name = "Application Date"
        else:  
            date_column_name = "Rejection Date"
        
        start_year = int(self.startyearch.GetStringSelection())
        start_month = self.startmonthch.GetSelection() + 1
        start_date = datetime.date(start_year, start_month, 1)

        end_year = int(self.endyearch.GetStringSelection())
        end_month = self.endmonthch.GetSelection() + 1
        end_date = datetime.date(end_year, end_month, 1)        
        
        if start_date > end_date:
            dlg = wx.MessageDialog(self, "Cannot select End Date before Start Date.", "Alert", wx.OK | wx.ICON_EXCLAMATION)                              
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        stats = customeyes.create_month_axes(start_date, end_date)
        
        series = category_info[self.category]["series"][self.series_idx]
        labels = category_info[self.category]["labels"][self.series_idx]
        question = category_info[self.category]["questions"][self.series_idx]   
        
        if len(series) == 1:
            selected_roles = list()
            title = question
            for role_idx in self.rolelb.GetCheckedItems():
                if role_idx == 0:
                    selected_roles.append(None)
                else:
                    selected_roles.append(self.roles[role_idx])

            for role_title in selected_roles:
                customeyes.line_month_averages(app.data, date_column_name, series[0], start_date = start_date, end_date = end_date, stats = stats, role_title = role_title)
        else:
            role_idx = self.rolelb.GetSelection()
            if role_idx == 0:
                role_title = None
                title = "{:}\n{:}".format(question, "All Roles")
            else:
                role_title = app.roles[role_idx - 1]
                title = "{:}\n{:}".format(question, role_title)
            
            for idx,s in enumerate(series):
                customeyes.line_month_averages(app.data, date_column_name, s, start_date = start_date, end_date = end_date, stats = stats, series_name = labels[idx], role_title = role_title)

        has_data = False
        
        for s in stats.values():
            for v in s.values():
                if v is not None:
                    has_data = True
                    break
            if has_data is True:
                break
                
        if has_data is True:
            customeyes.draw_lineplot(stats, date_column_name, series[0], title)
            customeyes_plots.plt.show() 
        else:
            dlg = wx.MessageDialog(self, "No data available for this role", "Alert", wx.OK | wx.ICON_EXCLAMATION)                              
            dlg.ShowModal()
            dlg.Destroy()

    def On_publish_hbar_chart(self,event):
             
        start_year = int(self.startyearch.GetStringSelection())
        start_month = self.startmonthch.GetSelection() + 1
        start_date = datetime.date(start_year, start_month, 1)

        end_year = int(self.endyearch.GetStringSelection())
        end_month = self.endmonthch.GetSelection() + 1
        end_date = datetime.date(end_year, end_month, 1)        
        
        if start_date > end_date:
            dlg = wx.MessageDialog(self, "Cannot select End Date before Start Date.", "Alert", wx.OK | wx.ICON_EXCLAMATION)                              
            dlg.ShowModal()
            dlg.Destroy()
            return
 
        question = category_info[self.category]["questions"][self.series_idx]

        selected_roles = list()
        title = question
        for role_idx in self.rolelb.GetCheckedItems():
            selected_roles.append(self.roles[role_idx])

        score_column_name = category_info[self.category]["series"][self.series_idx]
        stats = customeyes.hbar_role_averages(app.data, start_date = start_date, end_date = end_date, score_column_name = score_column_name, role_titles = selected_roles)
        
        has_data = False
        
        if len(stats) > 0:
            customeyes.draw_hbarplot(stats, score_column_name, title)
            customeyes_plots.plt.show() 
        else:
            dlg = wx.MessageDialog(self, "No data available", "Alert", wx.OK | wx.ICON_EXCLAMATION)                              
            dlg.ShowModal()
            dlg.Destroy()

class Bar_GraphWindow(Base_GraphWindow):

    def __init__(self, parent, ID, title, button_id, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        super(Bar_GraphWindow, self).__init__(parent, ID, title, button_id, pos, size, style)

        self.create_date_select(35) 

        if self.button_id == 302:
            choices = ["By Source", "By Completion Status", "By Rejection Reason", "By Number of Interviews"]
        else:
            choices = ["By Source", "By Completion Status", "By Rejection Reason", "By Number of Interviews", "By Difficulty Interviews"]
        
        self.choicech = wx.Choice(self.panel, -1, (15, 105), choices = choices)
        self.choicech.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.on_parameter_change, self.choicech)
      
        self.roles = ["All"] + app.roles

        self.rolelb = wx.ListBox(self.panel, -1, (15,140), (450,150), self.roles, wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.on_parameter_change, self.rolelb)
        self.rolelb.SetSelection(0)
        
        publishbtn = wx.Button(self.panel, -1, "Show Chart", (15,320))
        self.Bind(wx.EVT_BUTTON, self.On_publish_bar_chart, publishbtn)

    def On_publish_bar_chart(self, event): 
            
        date_column_name = "Application Date"
        
        start_year = int(self.startyearch.GetStringSelection())
        start_month = self.startmonthch.GetSelection() + 1
        start_date = datetime.date(start_year, start_month, 1)

        end_year = int(self.endyearch.GetStringSelection())
        end_month = self.endmonthch.GetSelection() + 1
        end_date = datetime.date(end_year, end_month, 1) 

        x_series = category_info[self.category]["series"][self.choicech.GetSelection()]
        question = category_info[self.category]["questions"][self.series_idx]
        series_label = category_info[self.category]["series_labels"][self.choicech.GetSelection()]

  
        if start_date > end_date:
            dlg = wx.MessageDialog(self, "Cannot select End Date before Start Date.", "Alert", wx.OK | wx.ICON_EXCLAMATION)                              
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        title = self.GetLabel()
        role_idx = self.rolelb.GetSelection()
        if role_idx == 0:
            role_title = None
            title = "{:}\n{:} for {:}".format(question, series_label, "All Roles")
        else:
            role_title = app.roles[role_idx - 1]
            title = "{:}\n{:} for {:}".format(question, series_label, role_title)

        score_column_name = category_info[self.category - 1]["series"][self.series_idx]
        stats = customeyes.barchart_average_scores(app.data, start_date = start_date, end_date = end_date, score_column_name = score_column_name, x_series = x_series, role_title = role_title)
        
        has_data = False
        
        if len(stats) > 0:
            customeyes.draw_barplot(stats, score_column_name, title)
            customeyes_plots.plt.show() 
        else:
            dlg = wx.MessageDialog(self, "No data available", "Alert", wx.OK | wx.ICON_EXCLAMATION)                              
            dlg.ShowModal()
            dlg.Destroy()

class Pie_ChartWindow(Base_GraphWindow):

    def __init__(self, parent, ID, title, button_id, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        super(Pie_ChartWindow, self).__init__(parent, ID, title, button_id, pos, size, style)

        self.create_date_select(35) 
      
        self.roles = ["All"] + app.roles

        self.rolelb = wx.ListBox(self.panel, -1, (15,105), (450,150), self.roles, wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.on_parameter_change, self.rolelb)
        self.rolelb.SetSelection(0)
        
        publishbtn = wx.Button(self.panel, -1, "Show Chart", (15,320))
        self.Bind(wx.EVT_BUTTON, self.On_publish_pie_chart, publishbtn)

    def On_publish_pie_chart(self, event):
            
        date_column_name = "Application Date"
        
        start_year = int(self.startyearch.GetStringSelection())
        start_month = self.startmonthch.GetSelection() + 1
        start_date = datetime.date(start_year, start_month, 1)

        end_year = int(self.endyearch.GetStringSelection())
        end_month = self.endmonthch.GetSelection() + 1
        end_date = datetime.date(end_year, end_month, 1) 
  
        if start_date > end_date:
            dlg = wx.MessageDialog(self, "Cannot select End Date before Start Date.", "Alert", wx.OK | wx.ICON_EXCLAMATION)                              
            dlg.ShowModal()
            dlg.Destroy()
            return
 
        role_idx = self.rolelb.GetSelection()
        if role_idx == 0:
            role_title = None
        else:
            role_title = app.roles[role_idx -1]

        score_column_name = category_info[self.category]["series"][self.series_idx]
        if self.category == 6:
            stats, count, nps_score = customeyes.NPS_score_calc(app.data, start_date = start_date, end_date = end_date, score_column_name = score_column_name, role_title = role_title)
        else:
            stats, count = customeyes.pie_chart_calc(app.data, start_date = start_date, end_date = end_date, score_column_name = score_column_name, role_title = role_title)
        question = category_info[self.category]["questions"][self.series_idx]
        
        title = question
        if self.category == 6:
            if role_idx == 0:
                title = "{:} {:}\n{:} ({:} record(s))".format(question, nps_score, "All Roles", count)
            else:
                title = "{:} {:}\n{:} ({:} record(s))".format(question, nps_score, role_title, count)            
        else:
            if role_idx == 0:
                title = "{:}\n{:} ({:} record(s))".format(question, "All Roles", count)
            else:
                title = "{:}\n{:} ({:} record(s))".format(question, role_title, count)

        has_data = False
                  
        if len(stats) > 0:
            customeyes.draw_pieplot(stats, title)
            customeyes_plots.plt.show() 
        else:
            dlg = wx.MessageDialog(self, "No data available", "Alert", wx.OK | wx.ICON_EXCLAMATION)                              
            dlg.ShowModal()
            dlg.Destroy()    

class Histo_Window(Base_GraphWindow):

    def __init__(self, parent, ID, title, button_id, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        super(Histo_Window, self).__init__(parent, ID, title, button_id, pos, size, style)

        self.create_date_select(35) 
      
        self.roles = ["All"] + app.roles

        self.rolelb = wx.ListBox(self.panel, -1, (15,105), (450,150), self.roles, wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.on_parameter_change, self.rolelb)
        self.rolelb.SetSelection(0)
        
        publishbtn = wx.Button(self.panel, -1, "Show Chart", (15,320))
        self.Bind(wx.EVT_BUTTON, self.On_publish_histogram, publishbtn)

    def On_publish_histogram(self, event):
            
        date_column_name = "Application Date"
        
        start_year = int(self.startyearch.GetStringSelection())
        start_month = self.startmonthch.GetSelection() + 1
        start_date = datetime.date(start_year, start_month, 1)

        end_year = int(self.endyearch.GetStringSelection())
        end_month = self.endmonthch.GetSelection() + 1
        end_date = datetime.date(end_year, end_month, 1) 
  
        if start_date > end_date:
            dlg = wx.MessageDialog(self, "Cannot select End Date before Start Date.", "Alert", wx.OK | wx.ICON_EXCLAMATION)                              
            dlg.ShowModal()
            dlg.Destroy()
            return
 
        role_idx = self.rolelb.GetSelection()
        if role_idx == 0:
            role_title = None
        else:
            role_title = app.roles[role_idx -1]

        score_column_name = category_info[self.category]["series"][self.series_idx]
        question = category_info[self.category]["questions"][self.series_idx]

        stats, count = customeyes.histo_score_dist(app.data, start_date = start_date, end_date = end_date, score_column_name = score_column_name, role_title = role_title)
             
        title = question
        if role_idx == 0:
            title = "{:}\n{:}".format(question, "All Roles")
        else:
            title = "{:}\n{:}".format(question, role_title)

        has_data = False
        
        if len(stats) > 0:
            if score_column_name == "Degree difficulty interviews":
                order = {
                    "Very easy": 0.0,
                    "Easy": 2.5,
                    "Average": 5.0,
                    "Difficult": 7.5,
                    "Very difficult": 10.0,
                }
            else:
                order = {
                    "Strongly disagree": 0.0,
                    "Disagree": 2.5,
                    "Neither agree nor disagree":5.0,
                    "Agree": 7.5,
                    "Strongly agree": 10.0,
                    "Don't know/ no experience": 11.0,
                }
            customeyes.draw_histoplot(stats, title, order)
            customeyes_plots.plt.show() 
        else:
            dlg = wx.MessageDialog(self, "No data available", "Alert", wx.OK | wx.ICON_EXCLAMATION)                              
            dlg.ShowModal()
            dlg.Destroy() 



class MyFrame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    def __init__(self, parent, title):

        super(MyFrame, self).__init__(parent, -1, title, pos=(150, 150), size=(750, 750))

        # Create the menubar
        menuBar = wx.MenuBar()
        # and a menu 
        menu1 = wx.Menu()
        
        menu1.Append(101, "&Update Data", "Will load and update a new raw data file")
        menu1.AppendSeparator()
        menu1.Append(110, "E&xit\tAlt-X", "Exit")
        menuBar.Append(menu1, "&File")

        # bind the menu event to an event handler
        #self.Bind(wx.EVT_MENU, self.Menu1, id=101)        
        self.Bind(wx.EVT_MENU, self.OnTimeToClose, id=110)

        # and put the menu on the menubar
        self.SetMenuBar(menuBar)
        self.CreateStatusBar()

        # create panel for controls
        panel1 = wx.Panel(self)
        panel2 = wx.Panel(self)

        #Overal recruitment process scores analytics
        text_process = wx.StaticText(panel1, -1, "Overall satisfaction recruitment process") 
        text_process.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_process.SetSize(text_process.GetBestSize())
        trendbtn = wx.Button(panel1, 101, "Compare monthly averages")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, trendbtn)
        overallbtn = wx.Button(panel1, 201, "Compare roles")
        self.Bind(wx.EVT_BUTTON, self.OnHbarGraph, overallbtn)
        barprocbtn = wx.Button(panel1, 301, "Correlate by role")
        self.Bind(wx.EVT_BUTTON, self.OnBarGraph, barprocbtn)
        scoredistbtn = wx.Button(panel1, 501, "Distribution of scores")
        self.Bind(wx.EVT_BUTTON, self.OnHistogram, scoredistbtn)

        #Difficulty interviews analytics
        text_diff = wx.StaticText(panel1, -1, "Degree of difficulty of interviews") 
        text_diff.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_diff.SetSize(text_diff.GetBestSize())
        ivdifbtn = wx.Button(panel1, 102, "Compare monthly averages")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, ivdifbtn)
        ivdif2btn = wx.Button(panel1, 202, "Compare roles")
        self.Bind(wx.EVT_BUTTON, self.OnHbarGraph, ivdif2btn)
        bardifbtn = wx.Button(panel1, 302, "Correlate by role")
        self.Bind(wx.EVT_BUTTON, self.OnBarGraph, bardifbtn)
        difdistbtn = wx.Button(panel1, 502, "Distribution of scores")
        self.Bind(wx.EVT_BUTTON, self.OnHistogram, difdistbtn)

        #Speed interviews analytics
        text_fast = wx.StaticText(panel1, -1, "Perception speed application process") 
        text_fast.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_fast.SetSize(text_fast.GetBestSize())
        fastivbtn = wx.Button(panel1, 103, "Compare monthly averages")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, fastivbtn)
        fastiv2btn = wx.Button(panel1, 203, "Compare roles")
        self.Bind(wx.EVT_BUTTON, self.OnHbarGraph, fastiv2btn)
        barfstbtn = wx.Button(panel1, 303, "Correlate by role")
        self.Bind(wx.EVT_BUTTON, self.OnBarGraph, barfstbtn)
        speeddistbtn = wx.Button(panel1, 503, "Distribution of scores")
        self.Bind(wx.EVT_BUTTON, self.OnHistogram, speeddistbtn)

        #some testing buttons
        #text_test = wx.StaticText(panel1, -1, "Test buttons") 
        #text_test.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        #text_test.SetSize(text_fast.GetBestSize())
        #treetestbtn = wx.Button(panel1, 103, "Tree test")
        #self.Bind(wx.EVT_BUTTON, self.OnTreeTest, treetestbtn)

        #Feedback analytics
        text_fb = wx.StaticText(panel2, 13, "Feedback on Interviews") 
        text_fb.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_fb.SetSize(text_fb.GetBestSize())        
        ivfbbtn = wx.Button(panel2, 104, "Interviewer Feedback")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, ivfbbtn)
        stagefbbtn = wx.Button(panel2, 108, "Feedback interview stages") 
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, stagefbbtn)
        fbqualitybtn = wx.Button(panel2, 106, "Feedback Quality")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, fbqualitybtn)
        fbreceivedbtn = wx.Button(panel2, 401, "Feedback recieved?")
        self.Bind(wx.EVT_BUTTON, self.OnPieChart, fbreceivedbtn)

        text_fbv = wx.StaticText(panel2, 13, "Feedback on Booking.com") 
        text_fbv.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_fbv.SetSize(text_fb.GetBestSize()) 
        fbvaluesbtn = wx.Button(panel2, 105, "Feedback on Booking.com Values")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, fbvaluesbtn)
        rblogbtn = wx.Button(panel2, 403, "Read the Tech Blog?")
        self.Bind(wx.EVT_BUTTON, self.OnPieChart, rblogbtn)
        fbblogbtn = wx.Button(panel2, 107, "Feedback on Tech Blog")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, fbblogbtn)

        #feedback on offers
        text_fboffer = wx.StaticText(panel2, 13, "Feedback on Offers") 
        text_fboffer.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_fboffer.SetSize(text_fb.GetBestSize()) 
        statusbtn = wx.Button(panel2, 402, "Distribution Rejected, Offered and Hired")
        self.Bind(wx.EVT_BUTTON, self.OnPieChart, statusbtn)
        fbofferbtn = wx.Button(panel2, 109, "Satisfaction Offer")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, fbofferbtn)

        text_nps = wx.StaticText(panel2, 14, "NPS") 
        text_nps.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_nps.SetSize(text_nps.GetBestSize())
        npsemplbtn = wx.Button(panel2, 601, "Recommend as Employer")
        self.Bind(wx.EVT_BUTTON, self.OnPieChart, npsemplbtn)
        npscustbtn = wx.Button(panel2, 602, "Recommend as Customer")
        self.Bind(wx.EVT_BUTTON, self.OnPieChart, npscustbtn)

        #standalone graphs new categories
        text_other = wx.StaticText(panel2, 14, "Other") 
        text_other.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_other.SetSize(text_other.GetBestSize())        


        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each. Order of buttons to be determined here

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        
        sizer1.Add(text_process, 0, wx.ALL, 10)
        sizer1.Add(trendbtn, 0, wx.ALL, 10)
        sizer1.Add(overallbtn, 0, wx.ALL, 10)       
        sizer1.Add(barprocbtn, 0, wx.ALL, 10) 
        sizer1.Add(scoredistbtn, 0, wx.ALL, 10)

        sizer1.Add(text_diff, 0, wx.ALL, 10)
        sizer1.Add(ivdifbtn, 0, wx.ALL, 10)
        sizer1.Add(ivdif2btn, 0, wx.ALL, 10)      
        sizer1.Add(bardifbtn, 0, wx.ALL, 10) 
        sizer1.Add(difdistbtn, 0, wx.ALL, 10)

        sizer1.Add(text_fast, 0, wx.ALL, 10)
        sizer1.Add(fastivbtn, 0, wx.ALL, 10)
        sizer1.Add(fastiv2btn,0,wx.ALL,10)        
        sizer1.Add(barfstbtn, 0, wx.ALL, 10) 
        sizer1.Add(speeddistbtn, 0, wx.ALL, 10)

        #sizer1.Add(text_test, 0, wx.ALL, 10)
        #sizer1.Add(treetestbtn, 0, wx.ALL, 10) 

        panel1.SetSizer(sizer1)
        panel1.Layout()
        sizer2 = wx.BoxSizer(wx.VERTICAL)
        
        sizer2.Add(text_fb, 0, wx.ALL, 10)
        sizer2.Add(ivfbbtn, 0, wx.ALL, 10)
        sizer2.Add(stagefbbtn, 0, wx.ALL, 10)
        sizer2.Add(fbqualitybtn, 0, wx.ALL, 10)
        sizer2.Add(fbreceivedbtn, 0, wx.ALL, 10)  

        sizer2.Add(text_fbv, 0, wx.ALL, 10)
        sizer2.Add(fbvaluesbtn, 0, wx.ALL, 10) 
        sizer2.Add(rblogbtn, 0, wx.ALL, 10)
        sizer2.Add(fbblogbtn, 0, wx.ALL, 10) 

        sizer2.Add(text_fboffer, 0, wx.ALL, 10)
        sizer2.Add(statusbtn, 0, wx.ALL, 10)
        sizer2.Add(fbofferbtn, 0, wx.ALL, 10)

        sizer2.Add(text_nps, 0, wx.ALL, 10)
        sizer2.Add(npsemplbtn, 0, wx.ALL, 10)
        sizer2.Add(npscustbtn, 0, wx.ALL, 10)

        sizer2.Add(text_other, 0, wx.ALL, 10)

        panel2.SetSizer(sizer2)
        panel2.Layout()

        # And also use a sizer to manage the size of the panel such
        # that it fills the frame
        sizer = wx.BoxSizer()
        sizer.Add(panel1, 1, wx.EXPAND)
        sizer.Add(panel2, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def OnLineGraph(self,evt):
        win =  Line_Hbar_GraphWindow(self, -1, evt.GetEventObject().GetLabel(), evt.GetId(), size=(500, 400), style = wx.DEFAULT_FRAME_STYLE)
        win.Show(True)
        
    def OnHbarGraph(self,evt):
        win = Line_Hbar_GraphWindow(self, -1, evt.GetEventObject().GetLabel(), evt.GetId(), size=(500, 400), style = wx.DEFAULT_FRAME_STYLE)
        win.Show(True)
      
    def OnBarGraph (self, evt):
        win = Bar_GraphWindow(self, -1, evt.GetEventObject().GetLabel(), evt.GetId(), size=(500, 400), style = wx.DEFAULT_FRAME_STYLE)
        win.Show(True)       

    def OnPieChart (self, evt):
        win = Pie_ChartWindow(self, -1, evt.GetEventObject().GetLabel(), evt.GetId(), size=(500, 400), style = wx.DEFAULT_FRAME_STYLE)
        win.Show(True)

    def OnHistogram (self, evt):
        win = Histo_Window(self, -1, evt.GetEventObject().GetLabel(), evt.GetId(), size=(500, 400), style = wx.DEFAULT_FRAME_STYLE)
        win.Show(True)

    def month_score_dist(self, evt):
        data = customeyes.load_data_json()
        customeyes.month_score_dist(data)
        customeyes_plots.plt.show() 

 

#    def OnTreeTest (self, log):
#        win = TestPanel(self, log)
#        win.Show(True)

    def OnTimeToClose(self, evt):
        """Event handler for the button click."""
        self.Close()      

class MyApp(wx.App):
    def OnInit(self):
        self.data = customeyes.load_data_json() 
        self.init_roles()

        frame = MyFrame(None, "Customeyes Analytics")
        self.SetTopWindow(frame)
        print "Print statements go to this stdout window by default."

        frame.Show(True)
        return True
     
    def init_roles(self):
        role_column_name = "Requisition_Title"
        role_set = set()
        for d in self.data:
            role_set.add(d[role_column_name])
        self.roles = sorted(role_set)

        #for role_title in self.roles:
        #    print role_title
        
 
app = MyApp(redirect=True)
app.MainLoop()
