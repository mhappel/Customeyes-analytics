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
                "...getting things done every day",
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
        ],
        "questions": [
            "\"Overall, I am satisfied with the recruitment process\"",
            "\"Could you describe the degree of difficulty of the interviews?\"", 
            "\"I have the feeling that Booking.com acts fast\"",
            "\"The interviewers I communicated with...\"", 
            "\"I think Booking.com is...\"", 
            "Feedback Quality",
            "Feedback on Booking.com Tech Blog",
            "\"Overal, I am satisfied with the interview(s) I had\"",
        ],
    },
    2: {
        "show_all": True,
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
}

# questions answered:
#    "\"Overall, I am satisfied with the recruitment process\"","\"I think Booking.com is...\"", "\"The interviewers I communicated with...\"", 
#    "\"Could you describe the degree of difficulty of the interviews?\"", "\"I recieved feedback after/during my application\"", 
#    "\"Overall, I'm satisfied with the feedback I recieved\"", "\"I have the feeling that Booking.com acts fast\""]
#    "\"Did you read the technical blog?\"", "\"I found the content of the blog helpful in my preparation\"", 
#    "\"I thought the blog gave me good insight in the technical challenges I would face\"", 

# questions to be answered:
#    "\"Overal, I am satisfied with the interview(s) I had\"" => Made a graph per stage, but there is no column with this actual data.
    
# questions not yet answered in graphs: 
#    "\"It was clear to me what I could expect from the application procedure\"", "\"How many rounds of interviews have you had in total?\"", 
#    "\"Did you have online assessments?\"", "\"Overall, I am satisfied with the offer I recieved\"",
#    "\"To what extend where you satisfied with the salary and benefits?\"", "\"It is clear what tasks belong to the job I accepted\"", 
#    "\"The job offer letter was clear to me\"", "\"I recommend Booking.com as an Employer to others\"", "\"I recommend others to book accomodations at Booking.com\""


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

        if self.button_id > 200 or len(category_info[self.category]["series"][self.series_idx]) == 1: 
            self.tree = wx.dataview.TreeListCtrl(self.panel, -1, (15,140), (450,150), style = wx.dataview.TL_CHECKBOX)       
        else:
            self.tree = wx.dataview.TreeListCtrl(self.panel, -1, (15,140), (450,150), style = wx.dataview.TL_SINGLE)  

        # create some columns
        self.tree.AppendColumn("Technology")
        self.tree.SetColumnWidth(0, 420)
        self.roles = app.roles
        self.role_groups = app.role_groups

        if category_info[self.category].get("show_all", False):
            self.root = self.tree.InsertItem(self.tree.GetRootItem(), wx.dataview.TLI_FIRST, "All Roles")
        else:
            self.root = self.tree.GetRootItem()
        
        for role_group in self.role_groups:
            branch = self.tree.AppendItem(self.root, role_group["group_title"])
            if "roles" in role_group:
                for role in role_group["roles"]:
                    self.tree.AppendItem(branch, role)
            self.tree.Expand(branch)
        self.tree.Expand(self.root)

        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate)
        
        if self.button_id > 200:
            publishbtn = wx.Button(self.panel, -1, "Show Chart", (15,320))
            self.Bind(wx.EVT_BUTTON, self.On_publish_hbar_chart, publishbtn)
        else:
            publishbtn = wx.Button(self.panel, -1, "Show Graph", (15,320))
            self.Bind(wx.EVT_BUTTON, self.on_publish_graph, publishbtn)

    def OnActivate(self, event):
        self.log.write('OnActivate: %s' % self.tree.GetItemText(event.GetItem()))

    def on_role_select(self,event): #need to make this working with trees
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

            item = self.tree.GetFirstItem()
            selected_roles = dict()
            title = question

            while item.IsOk():
                if self.tree.GetCheckedState(item) == 1:
                    child = self.tree.GetFirstChild(item)
                    if not child.IsOk():
                        if self.tree.GetItemText(item) not in selected_roles:
                            selected_roles[self.tree.GetItemText(item)] = list()
                        selected_roles[self.tree.GetItemText(item)].append(self.tree.GetItemText(item))
                    else:
                        stack = list()
                        while child.IsOk():
                            grandchild = self.tree.GetFirstChild(child)
                            if not grandchild.IsOk():
                                if self.tree.GetItemText(child) not in selected_roles:
                                    selected_roles[self.tree.GetItemText(child)] = list()
                                selected_roles[self.tree.GetItemText(child)].append(self.tree.GetItemText(item))
                                
                                
                                
                                child = self.tree.GetNextSibling(child)
                                while not child.IsOk() and len(stack) > 0:
                                    child = self.tree.GetNextSibling(stack.pop())
                            else:
                                stack.append(child)
                                child = grandchild
                item = self.tree.GetNextItem(item) 
            
            customeyes.line_month_averages(app.data, date_column_name, series, start_date = start_date, end_date = end_date, stats = stats, selected_roles = selected_roles)
    
    # TO DO: set group to None if date exceeds data file (=None in dictionary)

        else:
            item = self.tree.GetSelection()
            role_name = self.tree.GetItemText(item)
            selected_roles = dict()
            title = question

            if item.IsOk():
                if self.tree.IsSelected(item) is True:
                    child = self.tree.GetFirstChild(item)
                    if child.IsOk():

                        stack = list()
                        while child.IsOk():
                            grandchild = self.tree.GetFirstChild(child)
                            
                            if not grandchild.IsOk():
                                if self.tree.GetItemText(child) not in selected_roles:
                                    selected_roles[self.tree.GetItemText(child)] = list()
                                selected_roles[self.tree.GetItemText(child)].append(self.tree.GetItemText(item))
                                child = self.tree.GetNextSibling(child)                               

                                while not child.IsOk() and len(stack) > 0:
                                    child = self.tree.GetNextSibling(stack.pop())
                            else:
                                stack.append(child)
                                child = grandchild

                item = self.tree.GetNextItem(item)

            role_group = set(selected_roles.keys())
            print role_group

            if role_name == "All Roles":
                role_title = None
                title = "{:}\n{:}".format(question, "All Roles")
            else:
                role_title = role_name
                title = "{:}\n{:}".format(question, role_title)

            customeyes.line_month_averages(app.data, date_column_name, series, start_date = start_date, end_date = end_date, stats = stats, series_names = labels, role_group = role_group, role_title = role_title)

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
 
        question = category_info[self.category]["questions"][self.series_idx]
        score_column_name = category_info[self.category]["series"][self.series_idx]
        title = question
        

        item = self.tree.GetFirstItem()
        selected_roles = dict()
        title = question

        while item.IsOk():
            if self.tree.GetCheckedState(item) == 1:
                child = self.tree.GetFirstChild(item)
                if not child.IsOk():
                    if self.tree.GetItemText(item) not in selected_roles:
                        selected_roles[self.tree.GetItemText(item)] = list()
                    selected_roles[self.tree.GetItemText(item)].append(self.tree.GetItemText(item))
                else:
                    stack = list()
                    while child.IsOk():
                        grandchild = self.tree.GetFirstChild(child)
                        if not grandchild.IsOk():
                            if self.tree.GetItemText(child) not in selected_roles:
                                selected_roles[self.tree.GetItemText(child)] = list()
                            selected_roles[self.tree.GetItemText(child)].append(self.tree.GetItemText(item))
                            child = self.tree.GetNextSibling(child)
                            while not child.IsOk() and len(stack) > 0:
                                child = self.tree.GetNextSibling(stack.pop())
                        else:
                            stack.append(child)
                            child = grandchild
            item = self.tree.GetNextItem(item) 

        pprint.pprint(selected_roles)
        stats = customeyes.hbar_role_averages(app.data, start_date = start_date, end_date = end_date, date_column_name = date_column_name, score_column_name = score_column_name, selected_roles = selected_roles)
        
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

    def On_publish_bar_chart(self, event): #TO DO: Fix titles
            
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
        stats, count = customeyes.pie_chart_calc(app.data, start_date = start_date, end_date = end_date, score_column_name = score_column_name, role_title = role_title)
        question = category_info[self.category]["questions"][self.series_idx]
        
        title = question
        if role_idx == 0:
            title = "{:}\n{:} ({:} records)".format(question, "All Roles", count)
        else:
            title = "{:}\n{:} ({:} records)".format(question, role_title, count)

        has_data = False
        
        if len(stats) > 0:
            customeyes.draw_pieplot(stats, title)
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
        self.Bind(wx.EVT_BUTTON, self.month_score_dist, scoredistbtn)

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

        #standalone graphs new categories
        text_other = wx.StaticText(panel2, 14, "Other") #need to make per role as well
        text_other.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_other.SetSize(text_other.GetBestSize())
        statusbtn = wx.Button(panel2, 402, "Distribution Rejected, Offered and Hired")
        self.Bind(wx.EVT_BUTTON, self.OnPieChart, statusbtn)

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

        sizer1.Add(text_fast, 0, wx.ALL, 10)
        sizer1.Add(fastivbtn, 0, wx.ALL, 10)
        sizer1.Add(fastiv2btn,0,wx.ALL,10)        
        sizer1.Add(barfstbtn, 0, wx.ALL, 10) 

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

        sizer2.Add(text_other, 0, wx.ALL, 10)
        sizer2.Add(statusbtn, 0, wx.ALL, 10)

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

    def month_score_dist(self, evt):
        data = customeyes.load_data_json()
        customeyes.month_score_dist(data)
        customeyes_plots.plt.show() 

    def feedback_recieved(self, evt):
        data = customeyes.load_data_json()
        customeyes.pie_chart_calc(data)
        customeyes_plots.plt.show() 

    def completion_status(self, evt):
        data = customeyes.load_data_json()
        customeyes.completion_status(data)
        customeyes_plots.plt.show() 

    def OnTreeTest (self, log):
        win = TestPanel(self, log)
        win.Show(True)

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

        self.role_groups = list()

        for role_group in customeyes.role_groups:
            self.role_groups.append({
                "group_title": role_group["group_title"],
                "roles": list(),
            })
            for role in list(role_set):
                m = role_group["pattern"].match(role)
                if m is not None:
                    self.role_groups[-1]["roles"].append(role)
                    role_set.remove(role)
            self.role_groups[-1]["roles"] = sorted(self.role_groups[-1]["roles"])

        for role in role_set:
            self.role_groups.append({"group_title": role}) 
        self.role_groups = sorted(self.role_groups, key = lambda rg: rg["group_title"])

    #    pprint.pprint(self.role_groups)
    #    for role_title in self.roles:
    #        print role_title
        
 
app = MyApp(redirect=True)
app.MainLoop()
