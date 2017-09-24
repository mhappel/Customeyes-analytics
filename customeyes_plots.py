import pprint
import collections
import matplotlib.dates as mdates
import numpy as np
import matplotlib.pyplot as plt
styles = [
    "b.-",
    "r.-",
    "y.-",
    "g.-",
    "m.-",
    "c.-",
]

def pieplot(stats, title, data_label=None):
    labels = list()
    sizes = list()

    for k,v in stats.items():
        if data_label is not None:
            labels.append(data_label(k))
        else:    
            labels.append(k)
        sizes.append(v)
        
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct="%1.1f%%",
        shadow=False, startangle=180)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.set_title(title)
    
  
def hbarplot(stats, title, sort_key=None, data_label=None, xlabel=None, ylabel=None, right=None, left=None):
    plt.rcdefaults()
    fig, ax = plt.subplots()

    labels = list()
    buckets = list()
    
    for k,(v,c) in sorted(stats.items(), key = sort_key):
        if data_label is not None:
            k = data_label(k)
        labels.append("{:} ({:} record(s))".format(k,c))
        buckets.append(v)

    y_pos = np.arange(len(labels))
    
    if left is None:
        left = min(buckets)*0.90
    if right is None:
        right = max(buckets)*1.11
    ax.set_xlim(left=left, right=right, emit=True, auto=False)
    
    ax.barh(y_pos, buckets, align="center", color="blue", ecolor="black")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, ha = "right", va = "center", wrap = True )
    #ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel(xlabel)
    ax.set_title(title)
           
#TO DO: build stats differently in customeyes.py
def multibarplot(stats, title, xlabel=None, ylabel=None, data_label=None, bar_width=0.75, sort_key=None, bottom=None, top=None):
    labels = list()
    buckets = list()

    roles = ["Back End Developer", "Front End developer", "Site Reliability Engineer"]

    for k,(v,c) in sorted(stats.items(), key = sort_key):
        labels.append(list())
        buckets.append(list())

        for role in roles:
            if data_label is not None:
                k = data_label(k)
            labels[-1].append(k)
            buckets[-1].append(v)

    fig, ax = plt.subplots()
    index = np.arange(len(roles))
    opacity = 0.6
    bar_width = bar_width/len(buckets)

    x_ticks = ax.get_xticklabels()
    for x_tick in x_ticks:
        x_tick.set_rotation(45)
        x_tick.set_horizontalalignment("right")

    
    for idx,subbucket in enumerate(buckets):

        rects1 = plt.bar(index + idx*bar_width, subbucket, bar_width,
                     alpha = opacity,
                     color = styles[idx % len(styles)][0],
                     label = labels[idx][0])
    
    if bottom is None:
        bottom = min(map(min, buckets))*0.90
    if top is None:
        top = max(map(max, buckets))*1.11
    ax.set_ylim(bottom=bottom, top=top, emit=True, auto=False)
                     
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(index, roles)
    plt.legend()

    plt.tight_layout()
    #plt.savefig("test.png")

def barplot(stats, title, xlabel=None, ylabel=None, data_label=None, bar_width=None, sort_key=None, bottom=None, top=None):
    labels = list()
    buckets = list()

    for k,(v,c) in sorted(stats.items(), key = sort_key):
        if data_label is not None:
            k = data_label(k)
        labels.append("{:}\n({:} record(s))".format(k,c))
        buckets.append(v)

    fig, ax = plt.subplots()
    index = np.arange(len(buckets))
    opacity = 0.6

    x_ticks = ax.get_xticklabels()
    for x_tick in x_ticks:
        x_tick.set_rotation(45)
        x_tick.set_horizontalalignment("right")

    rects1 = plt.bar(index, buckets, bar_width,
                     alpha=opacity,
                     color="b",
                     label="series 1 label")
    
    if bottom is None:
        bottom = min(buckets)*0.90
    if top is None:
        top = max(buckets)*1.11
    ax.set_ylim(bottom=bottom, top=top, emit=True, auto=False)
                     
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(index, labels)
    #plt.legend()

    plt.tight_layout()
    #plt.savefig("test.png")

def histoplot(stats, title, xlabel=None, ylabel=None, data_label=None, bar_width=1, sort_key=None, bottom=0, top=None):
    labels = list()
    buckets = list()

    for k,(v,c) in sorted(stats.items(), key = sort_key):
        if data_label is not None:
            k = data_label(k)
        labels.append("{:}\n({:} record(s))".format(k,c))
        buckets.append(v)

    fig, ax = plt.subplots()
    index = np.arange(len(buckets))
    opacity = 0.6

    x_ticks = ax.get_xticklabels()
    for x_tick in x_ticks:
        x_tick.set_rotation(45)
        x_tick.set_horizontalalignment("right")

    rects1 = plt.bar(index, buckets, bar_width,
                     alpha=opacity,
                     color="b",
                     label="series 1 label")
 
    ax.set_ylim(bottom=bottom, top=top, emit=True, auto=False)
                     
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(index, labels)
    #plt.legend()

    plt.tight_layout()
    #plt.savefig("test.png")


def lineplot(stats, title, xlabel=None, ylabel=None, data_label=None, bottom=None, top=None):
    month = mdates.MonthLocator()  #every month
    monthsFmt = mdates.DateFormatter("%b, %Y")
       
    x_date = list()
    series = collections.defaultdict(list)
    for date,v in sorted(stats.items()):
        if data_label is not None:
            x_date.append(data_label(date))
        else:    
            x_date.append(date)
            
        if v is None or isinstance(v, (int, long, float)):
            series[title].append(v)
        else:
            for key,value in v.items():
                series[key].append(value)
    
    #Create plots with pre-defined labels.
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(month)
    ax.xaxis.set_major_formatter(monthsFmt)
    #ax.yaxis.set_major_formatter()
    for idx,(label,data) in enumerate(sorted(series.items())):
        ax.plot(x_date, data, styles[idx % len(styles)], label=label)

    ax.set_ylim(bottom=bottom, top=top, emit=True, auto=False)
                     
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    plt.title(title)     
    
    legend = ax.legend(loc="lower center", shadow=False, fontsize="medium")
    legend.get_frame().set_facecolor("#FFFFFF")

    fig.autofmt_xdate()
    #plt.savefig("test.png")
    
    return fig