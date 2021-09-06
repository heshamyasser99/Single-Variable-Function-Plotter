
# Importing PySide2 for application window, matplotlib for plotting the function, numpy for creating the arrays to be plotted.
from PySide2.QtWidgets import QApplication,QWidget,QMainWindow,QDialog,QPushButton,QVBoxLayout
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import sys




#Main plotting function which takes as input a function, and the minimum and maximum values of x from the user

def plot(min,max,fn):

#To avoid errors when evaluating expressions, constant functions are dealt with seperately
    unary = False
    if(len(fn)==1 and 49 <= ord(fn[0]) <= 57):
        step = abs(min)+abs(max)*10
        x = np.linspace(min,max,step)
        y = np.full(step, fn)
        plt.plot(x, y)
        plt.show()
        unary = True;

#For later easier use, as a preprocessing step, the input expression, any ^ is replaced with ** as in python ^
#when evaluated is interpretted as xor operator, uppercase x will be changed to lowercase x to accomodate user input
#mistakes that can be resolved, and all spaces shall be removed.

    fn=fn.replace('^','**')
    fn=fn.replace('X','x')
    fn=fn.replace(' ','')

#If the input is valid, which is checked by the below implemented function validate(exp), and the input isn't a constant function,
#both axes will be created for plotting.

    if(validate(fn)==4 and not unary):
        step = abs(min)+abs(max)*10
        x = np.linspace(min,max,step)
        try:
            y = eval(fn)
        except:
            print("Wrong Syntax")
            return
        plt.plot(x,y)
        plt.show()
    else:
        print(validate(fn))


#This function aims at validating whether the input entered by the user can be plotted as a function or not. That is, it consists
#of a combination between the operands stated in oper list, numbers, and only the argument variable (x) as we're plotting a
# single variable function.

def validate(exp):
    oper = ['+','-','/','*','^']
    if(len(exp)==0): return 0
    for i in range(len(exp)):
        if(r"/0" in exp):
            return 1
        elif ( 49 <= ord(exp[i]) <= 57 or exp[i] in oper or exp[i]=="x" or exp[i]=="(" or exp[i]==")"):
            continue
        elif(exp[i].isalpha()):
            return 2
        else:
            return 3
    return 4

plot(-10,10,"x")


