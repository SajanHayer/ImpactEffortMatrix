
This file is to explain how to run the python file templateReport.py and install any required softwares 

Installing the Required Software:
  (Follow these steps if you do not have Python and Matplotlib installed otherwise you can skip to Step D)
  Step A) 
    Click on the Windows Start button in the bottom-left corner of your screen.
    Type 'Software Center' in the search box select the Software center application from the search results.
  Step B)  
    Once Software Center is open click the search bar and type 'Python' and hit search 
    Scroll through the results til you find the one that has the newest version of python (Python 3.8.8 at this time)
    Install this Software
  Step C)
    Once python is finished installing -> Click on the Windows Start button in the bottom-left corner of your screen
    Type 'Command Prompt' in the search box, open the Command Prompt application from the search results (looks like a black box)
    Once opened type or copy/paste this command: 'pip install matplotlib' and hit enter to run the command
    Now you have all the required software to run the program!
  Step D)
    Extract the TemplateReport.zip folder
    Double click the templateReport.py file to run the application (or right-click and press run with->python)
    Now you can run the program! Feel free to make changes to the code to test different things!


Running the Software:
Different Buttons:
Add row -> To add an empty row to the table 
Remove Row -> Removes the last row of the table
Create Matrix-> Will preview the matrix you have created you can press the save button and save the image to any location you want!
Copy text-> Copy the table entered to your clipboard so you can use it again 
Create CSV-> Creates a csv of the table you have created this will be saved in the same folder you ran the templateReport.py file in 


Additonal Notes (to be looked at if you want to change the code):
To be able to have your table "saved" or appear again when you open the application click the Copy Text button before ending your session 
and replace the MAIN_TABLE line with the copied table you have on your clipboard! (Ctrl+v or Windows Key+v)
Change MAX variable if you want to increase the score of the matrix 
The variables LOWERRANGE, UPPERRANGE, and DECIMALCHANGE affect the spacing of the labels on the point changing these will affect the spacing
The variable GRAPHSIZE affects the padding on the size of the graph changing this will increase or decrease how much space should be past the MAX and MIN values


