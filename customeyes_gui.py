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
        ]
    },
    2: {
        "series":
            ["Recruitment process","Degree difficulty interviews", "Fast application process"]
    },
    3: {
        "series": 
            ["Source", "Completion status", "Rejection Reason", "Number of interviews", "Degree difficulty interviews"] 
    },
}

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
        
        if len(series) == 1:
            selected_roles = list()
            title = self.GetLabel()
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
                title = "{:} {:}".format(self.GetLabel(), "All Roles")
            else:
                role_title = app.roles[role_idx - 1]
                title = "{:} - {:}".format(self.GetLabel(), role_title)
            
            for s in series:
                customeyes.line_month_averages(app.data, date_column_name, s, start_date = start_date, end_date = end_date, stats = stats, series_name =  s, role_title = role_title)

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
        
        selected_roles = list()
        title = self.GetLabel()
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
  
        if start_date > end_date:
            dlg = wx.MessageDialog(self, "Cannot select End Date before Start Date.", "Alert", wx.OK | wx.ICON_EXCLAMATION)                              
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        title = self.GetLabel()
        role_idx = self.rolelb.GetSelection()
        if role_idx == 0:
            role_title = None
            title = "{:} {:}".format(self.GetLabel(), "All Roles")
        else:
            role_title = app.roles[role_idx]
            title = "{:} - {:}".format(self.GetLabel(), role_title)

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

class Pie_ChartWindow(Base_GraphWindow): #TO DO connect with button ID's to feedback received and completion status

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

        score_column_name =  "Received feedback" #remove when connected to button ID
        stats, count = customeyes.pie_chart_calc(app.data, start_date = start_date, end_date = end_date, score_column_name = score_column_name, role_title = role_title)

        title = self.GetLabel()
        if role_idx == 0:
            title = "{:} - {:} ({:} records)".format(self.GetLabel(), "All Roles", count)
        else:
            title = "{:} - {:} ({:} records)".format(self.GetLabel(), role_title, count)

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
        text_process = wx.StaticText(panel1, -1, "\"My overall experience of the \nprocess was good\"") 
        text_process.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_process.SetSize(text_process.GetBestSize())
        trendbtn = wx.Button(panel1, 101, "Compare average monthly scores by role")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, trendbtn)
        overallbtn = wx.Button(panel1, 201, "Compare roles")
        self.Bind(wx.EVT_BUTTON, self.OnHbarGraph, overallbtn)
        barprocbtn = wx.Button(panel1, 301, "Compare averages and correlations by role")
        self.Bind(wx.EVT_BUTTON, self.OnBarGraph, barprocbtn)
        scoredistbtn = wx.Button(panel1, 501, "Distribution of scores")
        self.Bind(wx.EVT_BUTTON, self.month_score_dist, scoredistbtn)

        #Difficulty interviews analytics
        text_diff = wx.StaticText(panel1, -1, "Degree Difficulty Interviews") #rename text variable
        text_diff.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_diff.SetSize(text_diff.GetBestSize())
        ivdifbtn = wx.Button(panel1, 102, "Compare average monthly scores by role")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, ivdifbtn)
        ivdif2btn = wx.Button(panel1, 202, "Compare roles")
        self.Bind(wx.EVT_BUTTON, self.OnHbarGraph, ivdif2btn)
        bardifbtn = wx.Button(panel1, 302, "Compare averages and correlations by role")
        self.Bind(wx.EVT_BUTTON, self.OnBarGraph, bardifbtn)

        #Speed interviews analytics
        text_fast = wx.StaticText(panel1, -1, "\"I had a fast interview process\"") 
        text_fast.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_fast.SetSize(text_fast.GetBestSize())
        fastivbtn = wx.Button(panel1, 103, "Compare average monthly scores by role")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, fastivbtn)
        fastiv2btn = wx.Button(panel1, 203, "Compare roles")
        self.Bind(wx.EVT_BUTTON, self.OnHbarGraph, fastiv2btn)
        barfstbtn = wx.Button(panel1, 303, "Compare averages and correlations by role")
        self.Bind(wx.EVT_BUTTON, self.OnBarGraph, barfstbtn) 

        #Feedback analytics
        text_fb = wx.StaticText(panel2, -1, "Feedback on Booking.com, \ninterviews and feedback") 
        text_fb.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_fb.SetSize(text_fb.GetBestSize())        
        ivfbbtn = wx.Button(panel2, 104, "Interviewer Feedback")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, ivfbbtn)
        fbvaluesbtn = wx.Button(panel2, 105, "Feedback on Booking.com Values")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, fbvaluesbtn)

        fbqualitybtn = wx.Button(panel2, 106, "Feedback Quality")
        self.Bind(wx.EVT_BUTTON, self.OnLineGraph, fbqualitybtn)
        fbreceivedbtn = wx.Button(panel2, 401, "Feedback recieved?")
        self.Bind(wx.EVT_BUTTON, self.OnPieChart, fbreceivedbtn)

        #standalone graphs new categories
        text_other = wx.StaticText(panel2, -1, "Standalone graphs \n(more graphs to be added)") #need to make per role as well
        text_other.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text_other.SetSize(text_other.GetBestSize())
        statusbtn = wx.Button(panel2, 402, "Distribution Rejected, Offered & Hired")
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
        sizer2.Add(fbvaluesbtn, 0, wx.ALL, 10)
        sizer2.Add(fbqualitybtn, 0, wx.ALL, 10)
        sizer2.Add(fbreceivedbtn, 0, wx.ALL, 10)    

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
         #   print role_title
        
 
app = MyApp(redirect=True)
app.MainLoop()
