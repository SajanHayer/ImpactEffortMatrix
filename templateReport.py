#--------------------------------IMPORTS-------------------------------------------------------
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import random
import csv
import math
import sys
import os
#----------------------------------------------------------------------------------------------


#--------------------------------SETTINGS---------------------------------------------------
#Original Range -> 0.22, 0.27, 0.17, 5, 0.2

#Global Variables
MAIN_TABLE = [] 
# MAIN_TABLE = [['aw', '1', '4', ''], ['as', '1', '4', ''], ['as', '1', '4', ''], ['as', '1', '4', '']]

#Change values to change spacing of labels on points, lower = less space, higher = more
LOWERRANGE = 0.22
UPPERRANGE = 0.27
DECIMALCHANGE = 0.17

#Max Score
MAX = 5

#Size of Padding on Graph
GRAPHSIZE = 0.3

#main list to keep track of data points for spacing purposes
data_list = {}
#---------------------------------------SETTINGS--------------------------------------------


#---------------------------------------CLASS/FUNCTIONS-------------------------------------
class MainWindow():

  def __init__(self, master):
    """
    Creates Intial Window and adds scroll bar and dynamic windows to seperate buttons and grid

    Args:
    self: this pointer in python, mandatory and defalut 
    master (tk.TK): Master Frame to be used

    Constructor: Creates scroll functionality and calls functions to build application
    """
    #main frame to be used
    self.main_frame = Frame(master)
    self.main_frame.pack(fill=BOTH, expand=1)
    
    #Canvas created for multi-functional purproses (dynamic vs static) 
    self.my_canvas = self.canvas_builder() #-> Function

    #Table Frame for grid to enter table, adding to canavas (Left side) R(C[TF|])
    self.table_frame = Frame(self.my_canvas)
    self.table_frame.pack(fill = BOTH, expand=1, padx=20, pady=20,side=LEFT)

    #Create Window of Table Frame for scrolling purposes and it doesnt affect the buttons
    self.my_canvas.create_window((0,0), window=self.table_frame, anchor=NW)

    #Second Frame for buttons R(C[TF|SF])
    self.second_frame = Frame(self.my_canvas)

    #Create more frames for buttons and interface purposes Root(MainF[Canvas[TableF|Second[TopF/SecTopF/BottomF]]])
    self.top_frame, self.second_top_frame, self.bottom_frame = self.build_frames()

    #Pre Table Setup function to setup Column names and scale on app
    self.pre_table_setup()

    #local class table copy of global main table
    self.main_table = MAIN_TABLE
    # self.secondWindow = None

    #file path to be used later
    self.filePath = None

    #if data in table add to gui 
    if len(self.main_table) > 0:
      self.main_table = self.placeholder_table()

    #add top frame buttons
    self.add_second_top_buttons()

    #add bottom frame buttons 
    self.error_label_text = self.add_bottom_buttons()


  def destroy_window(self):
    """
    Force Close Application when funtion is called
    """
    sys.exit()

  #--------------------------------Building Model Functions ------------------------
  def canvas_builder(self):
    """
    Creates Canvas/Scroll Bar and adds to main frame

    Args: 
      Self: Mandatory this pointer

    Returns:
      tk.Canvas: Appended to mainframe with scroll bar function
    """
    #Add canvas to main frame and configure its position
    my_canvas = Canvas(self.main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    #Creates scroll bar and adds to main frame with movement along the y-axis
    my_scroll_bar = ttk.Scrollbar(self.main_frame, orient=VERTICAL, command= my_canvas.yview)
    my_scroll_bar.pack(side=RIGHT, fill=Y)

    #configure scroll functionality 
    my_canvas.configure(yscrollcommand=my_scroll_bar.set)
    my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    return my_canvas
  
  def build_frames(self):
    """
    Configure Frames for buttons within ride side of main frame (Apperance)
    """
    #Second Frame
    self.second_frame.pack(side=RIGHT, fill=Y)

    #Top Frame, Second Top Frame, Bottom Frame added to second frame (Right of table) these are ontop of one another
    top_frame = Frame(self.second_frame)
    top_frame.pack(side = TOP, fill=Y)

    second_top_frame = Frame(self.second_frame)
    second_top_frame.pack(side=TOP, fill=Y)

    bottom_frame = Frame(self.second_frame)
    bottom_frame.pack(side = TOP, fill=Y)

    #returns frame
    return top_frame, second_top_frame, bottom_frame

  def pre_table_setup(self):
    """
    Pre Table Setup To create Column titles and scale to be displayed within application 
    """

    #Column Title dict to be used in creation, if add more columns increase size of loop to be accurate to size of dict
    columnTitle_dict = {
      0 : 'Name of Item:',
      1 : f'Effort Value (1-{MAX}):',
      2 : f'Impact Value (1-{MAX}):',
      3 : f'(Optional)\nMandatory (M):'
    }

    #Loop to add column titles to app using grid with formatting
    for i in range(4):
      labelString= columnTitle_dict[i]
      columntitle = Label(self.table_frame, text=labelString)
      columntitle.grid(row=0, column=i, padx=5, pady=5)
    
    #scale for values
    diagramLabel = Label(self.top_frame, text="Scale for Effort/Impact:")
    diagramLabel.grid(row=0, column=1, pady=5)
    diagramDict = {
      'Very Low': 1,
      'Intermediate': math.ceil(MAX/2),
      'Very High': MAX
    }
    
    #Loop to add values, Labels to scale
    for row_length in range(2):
      for i in range(3):
        if row_length==0:
          diagramLabel = Label(self.top_frame, text=list(diagramDict.values())[i])
          diagramLabel.grid(row=1, column =i, padx=5, pady=5)
        if row_length==1:    
          diagramLabel = Label(self.top_frame, text=list(diagramDict.keys())[i])
          diagramLabel.grid(row=2, column=i, padx=5, pady=5)

  def add_second_top_buttons(self):
    """
    Function to add "Add/Remove Row" buttons with their functionality
    """


    add_row_button = Button(self.second_top_frame, text="Add Row", command=self.add_row)
    add_row_button.pack(pady=10,padx=7, side=LEFT, expand=True, fill=X)

    remove_row_button = Button(self.second_top_frame, text="Remove Row", command=self.remove_row)
    remove_row_button.pack(pady=10,padx=7,side=RIGHT,expand=True, fill =X)

  def add_bottom_buttons(self):
    """
    Function to add "Create Matrix, Copy Text, Print CSV" buttons and have error label to print errors to app
    """
    create_matrix_button = Button(self.bottom_frame, text="Create Impact-Effort Matrix", command=self.create_impact_effort_matrix)
    create_matrix_button.pack(pady=10,padx=35, fill=X)

    error_label_text = StringVar(value=" ")
    error_label = Label(self.bottom_frame, textvariable=error_label_text)
    error_label.pack()

    copy_button = Button(self.bottom_frame, text="Copy Text", command=self.table_to_string)
    copy_button.pack(pady=5, padx= 10,side=LEFT,expand=True,fill=X)

    csv_button = Button(self.bottom_frame, text="Print CSV", command=self.table_to_csv)
    csv_button.pack(pady=5,padx=10,side=RIGHT,expand=True,fill=X)

    # save_matrix_button = Button(self.bottom_frame, text="Save Matrix", command=self.save_matrix)
    # save_matrix_button.pack(pady=5,padx=10, expand=True, fill=X)
    return error_label_text
  #--------------------------------Building Model Functions ------------------------
  
  #--------------------------------Functionality Functions -------------------------
  def get_dx_dy(self,x, y):
    """
    Function to create custom spacing for points on the graph so labels dont overlap on the same point

    Args:
      Self-Mandatory this pointer
      x (int): X postion of point 
      y (int): Y postion of point
    
    Return:
      dx (int): Spacing for X point
      dy (int): Spacing for Y point
    """

    #Variables to be intialized 
    dx = 0
    dy = 0
    check_y = 1
    check_x = 1
    #to check if point is the Max Value
    if y == MAX:
      check_y = -1 
    if x == MAX:
      check_x = -1
    #Add points with spacing to data list, if they exist change the spacing to another value for no overlap
    if (x,y) not in data_list: 
      dx = random.uniform(LOWERRANGE, UPPERRANGE)
      dy = random.uniform(LOWERRANGE*1.3, UPPERRANGE*1.3)
      data_list[(x, y)] = [dx, dy, 1]
      dx = x + (dx*check_x)
      dy = y + (dy*check_y)
    else:
      dx = data_list[(x, y)][0]
      dy = data_list[(x, y)][1]
      if data_list[(x, y)][2] == 1:
        data_list[(x, y)][2] += 1
        dx,dy = x-DECIMALCHANGE, y+(dy*check_y)
      elif data_list[(x, y)][2] == 2:  
        data_list[(x, y)][2] += 1
        dx, dy = x-DECIMALCHANGE, y-dy
      elif data_list[(x, y)][2] == 3:
        data_list[(x, y)][2] += 1
        dx, dy = x+(dx*check_x), y-DECIMALCHANGE
      elif data_list[(x, y)][2] == 4:  
        data_list[(x, y)][2] += 1
        dx, dy = x-dx, y-DECIMALCHANGE
      elif data_list[(x, y)][2] == 5: 
        data_list[(x, y)][2] += 1
        dx, dy = x-dx, y+dy
      elif data_list[(x, y)][2] == 6: 
        data_list[(x, y)][2] += 1
        dx, dy = x-dx, y-dy
      elif data_list[(x, y)][2] == 7: 
        data_list[(x, y)][2] += 1
        dx, dy = x+dx, y-dy    
    return dx, dy

  def get_impact_effort_matrix(self):
    """
    Function that creates that impact effort matrix using values entered in the grid from the app 
    
    Return:
      fig (matplotlib.plt): plot of impact-effort matrix
    """

    #Clear data list so each time spacing is different, get data from grid 
    data_list.clear()
    data = self.get_table_data()

    #if no data return (error)
    if data == None:
      return
    
    #collect values for each row
    items = [row[0] for row in data]
    effort = [int(row[1]) for row in data]
    impact = [int(row[2]) for row in data]
    mandatory = [row[3] for row in data]

    #Create scatter plots
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(effort, impact, s=100, color= 'b')

    #Setting Limits on plot with spacing so labels dont go off the graph
    if MAX%2==0: #even max volume
      midpoint = (MAX/2) + .5  
    else: #odd max volume
      midpoint = math.ceil(MAX/2)
    
    ax.set_xlim(1-GRAPHSIZE, MAX+GRAPHSIZE)
    ax.set_ylim(1-GRAPHSIZE, MAX+GRAPHSIZE)

    #Loop to add points and labels to graph
    for i, item in enumerate(items):
      x = effort[i]
      y = impact[i]
      label_colour = 'black'
      if mandatory[i] == 'M':
        label_colour = 'red'
      dx, dy = self.get_dx_dy(x,y)
      ax.annotate(item, 
                  (x, y), 
                  xytext=(dx, dy), 
                  arrowprops=dict(arrowstyle="->",
                                  color=label_colour,
                                  connectionstyle="angle3",
                                  clip_on=True),
                                  color = label_colour)
    ax.set_xlabel('Effort', fontdict={'weight': 'bold'})
    ax.set_ylabel('Impact', fontdict={'weight': 'bold'})
    ax.set_title('Impact-Effort Matrix',fontdict={'weight': 'bold'})

    #Set ticks/labels for x/y-axis
    ax.set_xticks([(midpoint+1-GRAPHSIZE)/2, (MAX + midpoint + GRAPHSIZE)/2])
    ax.set_xticklabels(["Low", "High"])
    ax.set_yticks([(midpoint+1-GRAPHSIZE)/2, (MAX + midpoint + GRAPHSIZE)/2])
    ax.set_yticklabels(["Low", "High"])

    #Mid lines
    ax.axvline(x=midpoint, color='black', linestyle='-', alpha = 0.6)
    ax.axhline(y=midpoint, color='black', linestyle='-', alpha = 0.6)

    #Patches to be added to legend
    red_patch = plt.Rectangle((0, 0), 1, 1, color='red', label='Mandatory')
    black_patch = plt.Rectangle((0, 0), 1, 1, color='black', label='Optional')
    blue_patch = plt.Rectangle((0, 0), 1, 1, color='blue', label='Data Point')
    topright_patch = plt.Rectangle((0, 0), 1, 1, color='Orange', alpha = 0.3, label='Major Projects')
    topleft_patch = plt.Rectangle((0, 0), 1, 1, color='Purple', alpha = 0.3, label='Quick Wins')  
    bottomleft_patch = plt.Rectangle((0, 0), 1, 1, color='g', alpha = 0.1, label='Small Revisions')
    bottomright_patch = plt.Rectangle((0, 0), 1, 1, color='Yellow', alpha = 0.1, label='Low Priority')
    ax.legend(handles=[red_patch, black_patch, blue_patch, topright_patch, topleft_patch, bottomleft_patch, bottomright_patch], 
              loc = 'upper left', 
              bbox_to_anchor= (1, 1.05), 
              title='Legend',
              title_fontproperties={'weight':'bold'})

    #colouring graph
    #top right
    ax.add_patch(plt.Rectangle((midpoint, midpoint),midpoint, midpoint, facecolor='Orange', alpha=0.3))
    #top left
    ax.add_patch(plt.Rectangle((0, midpoint),midpoint, midpoint, facecolor='Purple', alpha=0.3))
    #bottom left
    ax.add_patch(plt.Rectangle((0, 0),midpoint, midpoint, facecolor='g', alpha=0.1))
    #bottom right
    ax.add_patch(plt.Rectangle((midpoint, 0),midpoint, midpoint, facecolor='Yellow', alpha=0.1))
    plt.subplots_adjust(right=0.86)
    # plt.tight_layout()
    return fig

  def create_impact_effort_matrix(self):
    """
    Function to show impact effort matrix
    """
    #Get graph, if none return error
    fig = self.get_impact_effort_matrix()
    if fig == None:
      return
    plt.show()
    #if second window needs to be used (testing to be used as an .exe so make it simplier to use)
    # secondWindow = SecondWindow(fig)
    # secondWindow.mainloop()

  def validate_integer(self,value):
    """
    Function to validate whether a value entered into a table is a integer and between
    min and max values stated

    Args:
      Value (int): Value to be checked 

    Return:
      Boolean (True or False)
    """
    try:
      value = int(value)
      if 1 <= value <= MAX:  # Change the range as needed
        return True
      else:
        return False
    except ValueError:
      return value == ""

  def validate_M(self,value):
    """
    Function to validate whether a value entered into a grid was M (for Mandatory)

    Args:
      Value (String): Value to be checked
    
    Return:
      Boolean (True or False)
    """
    if value == "M":
      return True
    else:
      return value==""

  def entry_creation(self, index):
    """
    Function to create entrys into the grid that will pose as the table,
    these have validations to check whether a value is "correct" or not 

    Args:
      index (int): Postion of where entry will be created
    
    Return
      entry (tk.Entry): Input field with validation
    """
    if index==3:
      entry = Entry(self.table_frame, width=5)
      vcmd = (entry.register(self.validate_M), '%P')
      entry.config(validate='all', validatecommand=vcmd)
    else:
      entry = Entry(self.table_frame, width=10)
    if index==1 or index==2:
      vcmd = (entry.register(self.validate_integer), '%P')
      entry.config(validate='all', validatecommand=vcmd)
    return entry

  def placeholder_table(self):
    """
    Function to create the grid with values pre-entered if MAIN_TABLE variable is not filled out
    
    Return:
      temp_table (2D array): Table to be placed in gui keeps track of entries
    """
    row_check = 1
    temp_table = []
    for item in self.main_table:
      row = []
      for i,element in enumerate(item):
        entry = self.entry_creation(i)
        entry.insert(0,element)
        entry.grid(row=row_check, column=i, padx=5, pady=5)
        row.append(entry)
        if i==3:
          row_check+=1
      temp_table.append(row)
    return temp_table

  def add_row(self):
    """
    Function to add row to grid in app
    """
    row = []
    for i in range(4):
      entry = self.entry_creation(i)
      entry.grid(row=len(self.main_table)+2, column=len(row), padx=5, pady=5)
      row.append(entry)
    self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))     
    self.main_table.append(row)

  def remove_row(self):
    """
    Function to remove a row from the grid in the app
    """
    if len(self.main_table)<1:
      return
    for item in self.main_table[-1]:
      item.destroy()
    self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all"))
    self.main_table.pop()

  def get_table_data(self):
    """
    Function to get data that exists witin the grid in the app

    Return:
      data(2D array): Contains values of entries in the grid (shows error if values are missing)
    """
    data = []
    self.error_label_text.set("")
    if len(self.main_table) < 1:
      return 
    for row in self.main_table:
      row_data = []
      i = 0
      for item in row:
        if item.get() == None or item.get()=="" and i != 3:
          self.error_label_text.set("One or more columns have an empty space")
          return
        row_data.append(item.get())
        i+=1
      data.append(row_data)
    return data

  def table_to_string(self):
    """
    Function to turn the table in the grid to the string to be added to Code if application needs to be closed
    Appends string to clipboard of computer
    """
    data = self.get_table_data()
    if data == None:
      return
    root.clipboard_append("MAIN_TABLE = " + str(data)+"\n")

  def table_to_csv(self):
    """
    Function to turn table in grid to a csv file saved to folder where code was ran
    """
    data = self.get_table_data()
    if data == None or len(self.main_table)<1:
      return
    self.filePath = os.path.join("TemplateReport", "output.csv")
    with open(self.filePath, 'w', newline='') as csvfile:
      csv_writer = csv.writer(csvfile, delimiter=',')
      row = ['Name of Item','Effort Value','Impact Value','Mandatory (M):']
      csv_writer.writerow(row)
      for row in data:
          csv_writer.writerow(row)
  #--------------------------------Functionality Functions -------------------------


#---------------TESTING OTHER OPTiONS-----------------------
# class SecondWindow(Tk):
#   def __init__(self, fig):
#     super().__init__()
#     self.title("Impact Effort Matrix")
#     self.canvas = FigureCanvasTkAgg(fig, master=self)
#     self.canvas.draw()
#     self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

#   def get_window_status(self):
#     try:
#       if self.winfo_exists():
#         return True
#     except TclError:
#       return False
#---------------TESTING OTHER OPTiONS-----------------------


#---------------MAIN-----------------------
if __name__ == "__main__":
  root = Tk()
  #creates window, with name, size and shows to user
  main_window = MainWindow(root)
  root.title("Enter Data")
  root.resizable(width=False,height=True)
  root.geometry("700x300")
  root.mainloop()
#---------------MAIN-----------------------
