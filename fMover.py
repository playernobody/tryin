from array import array
from ctypes import sizeof
from fileinput import filename
import imp
import tkinter as tk
from tkinter import *
from tkinter import filedialog, Text, Widget, Label
import pandas as pd
import shutil
import os
import fnmatch
import datetime

root= tk.Tk()
filename=''
fileArray=''
src_files=''
sourceFolder=''
targetFolder=''
e = datetime.datetime.now()

def openCsv():
    global filename
    global fileArray
    openFile_text_box.delete("1.0","end")
    filename=filedialog.askopenfilename(initialdir="/" ,title="Select file", filetypes=(("all files",".csv .xlsx"),("csv","*.csv"),("xlsx","*.xlsx")))
    revName=filename[::-1]
    if(revName[0:3] == "vsc"):
        data = pd.read_csv(filename)
        fileArray = data.loc[:,'Document Guild Value']
        fileArray= list(fileArray)
    elif(revName[0:4] == "xslx"):
        data = pd.read_excel(filename)
        fileArray = data.loc[:,'Document Guild Value']
        fileArray= list(fileArray)
    else:
        openFile_text_box.insert(1.0,'try again')
    openFile_text_box.insert(1.0,filename)

def sourceSelect():
    global sourceFolder
    source_text_box.delete("1.0","end")
    sourceFolder=filedialog.askdirectory()
    source_text_box.insert(1.0,sourceFolder)

def targetSelect():
    global targetFolder
    target_text_box.delete("1.0","end")
    targetFolder=filedialog.askdirectory()
    target_text_box.insert(1.0,targetFolder)

def runPrg():
    global src_files
    error_text_box.delete("1.0","end")
    if(sourceFolder == targetFolder):
         error_text_box.insert(1.0,'\n source folder is same as traget folder change one of them \n')
    if (targetFolder=='' or sourceFolder=='' or filename==''):
        error_text_box.insert(1.0,'you did not select some file/folder \nTry again after selecting all the files/folder\n')
    else:
        src_files = os.listdir(sourceFolder)
        Array = [x for x in fileArray if x == x]
        for i in Array:
            tempi= '*'+i+'.pdf'
            tempa =[]
            for file in src_files:
                if fnmatch.fnmatch(file, tempi)== True:
                    tempa.append(1)
                else:
                    tempa.append(0)
            if(sum(tempa)>0):
                shutil.copy(sourceFolder+'/'+i+'.pdf', targetFolder+'/'+i+'.pdf')
            else:
                saveTxt= open("Desktop/save.txt","a")
                saveTxt.write("\n file not found   ---   "+i)
                saveTxt.close()
                error_text_box.insert(1.0,'file not found  ---  '+i+'\n')
    error_text_box.insert(1.0,'\n Process done -- look for any warning ---- \n\n\n')
    error_text_box.insert(1.0,'---------------------------------------------------------\n')
    error_text_box.insert(1.0,'File name == >  '+ filename+'\n')
    error_text_box.insert(1.0,e.strftime("%x")+'\n')
    saveTxt= open("Desktop/save.txt","a")
    saveTxt.write('\n date ==  '+e.strftime("%x")+'\n')
    saveTxt.write('File name == >  '+ filename+'\n')
    saveTxt.write('\n -------------------------------------- \n')
    saveTxt.close()

canvas= tk.Canvas(root, height=700, width=700, bg="#263042")
canvas.pack()

frame= tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

source= tk.Button(frame, text="Source", padx=10, pady=10, fg="white", bg="#263042", command=sourceSelect)
source.place(x=30,y=30)

source_text_box= tk.Text(frame, height=1,width=60, padx=8, pady=8, bg="grey")
source_text_box.place(x=30,y=90)

target= tk.Button(frame, text="target", padx=10, pady=10, fg="white", bg="#263042", command=targetSelect)
target.place(x=30,y=140)

target_text_box= tk.Text(frame, height=1,width=60, padx=8, pady=8, bg="grey")
target_text_box.place(x=30,y=200)

openFile=tk.Button(frame, text="CSV/XLSX  File", padx=10, pady=10, fg="white", bg="#263042", command=openCsv)
openFile.place(x=30,y=250)

openFile_text_box= tk.Text(frame, height=1,width=60, padx=8, pady=8, bg="grey")
openFile_text_box.place(x=30,y=310)

errorLabel = Label(frame, text='Progress', bg="green",fg="white")
errorLabel.place(x=30,y=360)

error_text_box= tk.Text(frame, height=9,width=60, padx=8, pady=8, bg="cyan")
error_text_box.place(x=30,y=400)

run= tk.Button(root, text="Run", padx=100, pady=10, fg="white", bg="green", command=runPrg)
run.pack()

root.mainloop()
