import sys
from PySide2.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout,QLabel,QLineEdit, QFormLayout, QMessageBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys
import random

#Global variable used to distinguish different types of errors
global error
error = 100

class Window(QDialog):
    def __init__(self, parent=None):

        super(Window, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.setWindowTitle('Function Plotter')

#The plot button code, upon pressing it calls plot function
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        layout = QFormLayout()
        self.fn=QLineEdit()
        self.minx=QLineEdit()
        self.maxx = QLineEdit()

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(QLabel('Figure Equation:'))
        layout.addWidget(self.fn)
        layout.addWidget(QLabel('Min x axis value:'))
        layout.addWidget(self.minx)
        layout.addWidget(QLabel('Max x axis value:'))
        layout.addWidget(self.maxx)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
# Clearing the figure to empty the canvas before plotting a new function
        self.figure.clear()
        unary = False
        fn=self.fn.text()
        global error
#Checking if either min x or max x fields are empty
        if(self.minx.text()=='' or self.maxx.text()==''):
            error=5
            errormsg()
            return
#Checking if the input min x is not a number
        try:
            isinstance(int(self.minx.text()),int)
        except:
            error=7
            errormsg()
            return

#Checking if the input max x is not a number
        try:
            isinstance(int(self.maxx.text()),int)
        except:
            error=7
            errormsg()
            return
#Checking if min x value is bigger than or equal to max x value
        if(int(self.minx.text())>=int(self.maxx.text())):
            error = 6
            errormsg()
            return
#Checking if the input function is a constant
        if (fn.isdigit() or (fn[1:].isdigit() and fn[0]=="-")):
            step = abs(int(self.minx.text())) + abs(int(self.maxx.text())) * 10
            x = np.linspace(int(self.minx.text()), int(self.maxx.text()), step)
            y = np.full(step, int(fn))
            plt.plot(x,y)
            unary = True;
            self.canvas.draw()
            return

        # For later easier use, as a preprocessing step, the input expression, any ^ is replaced with ** as in python ^
        # when evaluated is interpretted as xor operator, uppercase x will be changed to lowercase x to accomodate user input
        # mistakes that can be resolved, and all spaces shall be removed.

        fn = fn.replace('^', '**')
        fn = fn.replace('X', 'x')
        fn = fn.replace(' ', '')

        validate(fn)

        # If the input is valid, which is checked by the below implemented function validate(exp), and the input isn't a constant function,
        # both axes will be created for plotting.

        if (validate(fn) == 4 and not unary):
            step = abs(int(self.minx.text())) + abs(int(self.maxx.text())) * 10
            x = np.linspace(int(self.minx.text()), int(self.maxx.text()), step)
        #If the entered input function is validated but syntactically invalid the below try except block will raise an error
            try:
                y = eval(fn)
            except:
                error=3
                errormsg()
                return
            plt.plot(x, y)
        else:
            errormsg()
        # refresh canvas
        self.canvas.draw()

#This function is used to check if the input function valid or not

def validate(exp):
    oper = ['+','-','/','*','^']

    global error
#If the user doesn't enter an input, an eror is raised in this function
    if(len(exp)==0):
        error=0
        return 0

    for i in range(len(exp)):
#If the user attempts to divide by zero, an error is raised in this function
        if(r"/0" in exp):
            error=1
            return 1
#If the character is an alphabetic character, denoting that the user is attempting to enter a multi-variable function, an error is raised in this function
        elif(exp[i].isalpha() and exp[i] != "x"):
            error=2
            return 2
#If the character being looped is a number, an operand, a parenthesis, or x, then its valid input character
        elif ( exp.isdigit or exp[i] in oper or exp[i]=="x" or exp[i]=="(" or exp[i]==")"):
            continue

        else:
            error=3
            return 3
    return 4

#This function is used to differentiate between different types of errors, based on the global variable error
def errormsg():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    print(error)

    if(error==0):
        msg.setText("Empty function")
        msg.setInformativeText('Please do not leave the function blank')
        msg.setWindowTitle("Error")
        msg.exec()

    elif(error==1):
        msg.setText("Dividing by zero?")
        msg.setInformativeText('You cannot divide by zero or use leading zeroes')
        msg.setWindowTitle("Error")
        msg.exec()

    elif(error==2):
        msg.setText("Not a multivariable function plotter")
        msg.setInformativeText('Please only use variable x in the equation')
        msg.setWindowTitle("Error")
        msg.exec()

    elif(error==3):
        msg.setText("Syntax Error")
        msg.setInformativeText('Invalid mathematical syntax for function')
        msg.setWindowTitle("Error")
        msg.exec()

    elif(error==5):
        msg.setText("Empty min x and/or max x values")
        msg.setInformativeText('Please enter both min x and max x values')
        msg.setWindowTitle("Error")
        msg.exec()

    elif(error==6):
        msg.setText("Min x>Max x?")
        msg.setInformativeText('Please make sure that min x is less than max x')
        msg.setWindowTitle("Error")
        msg.exec()

    elif(error==7):
        msg.setText("Invalid x values")
        msg.setInformativeText('Please make sure that min x and max x are numbers')
        msg.setWindowTitle("Error")
        msg.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())