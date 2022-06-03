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
columnName ="Document Guid Value"

def openCsv():
    global filename
    global fileArray
    filename=''
    fileArray=''
    openFile_text_box.delete("1.0","end")
    filename=filedialog.askopenfilename(initialdir="/" ,title="Select file", filetypes=(("all files",".csv .xlsx"),("csv","*.csv"),("xlsx","*.xlsx")))
    revName=filename[::-1]
    if(revName[0:3] == "vsc"):
        data = pd.read_csv(filename)
        try:
            fileArray = data.loc[:,columnName]
            fileArray= list(fileArray)
        except:
            pass

    elif(revName[0:4] == "xslx"):
        data = pd.read_excel(filename)
        try:
            fileArray = data.loc[:,columnName]
            fileArray= list(fileArray)
        except:
            pass
    else:
        openFile_text_box.insert(1.0,'try again')

    if(len(fileArray)>1):
        openFile_text_box.insert(1.0,filename)
    else:
        print(len(fileArray))
        openFile_text_box.insert(1.0,'column --- "'+columnName+'" --- NOT FOUND')
        error_text_box.insert(1.0,'\n column --- "'+columnName+'" --- NOT FOUND\n')

def sourceSelect():
    global sourceFolder
    sourceFolder=''
    source_text_box.delete("1.0","end")
    sourceFolder=filedialog.askdirectory()
    source_text_box.insert(1.0,sourceFolder)

def targetSelect():
    global targetFolder
    targetFolder=''
    target_text_box.delete("1.0","end")
    targetFolder=filedialog.askdirectory()
    target_text_box.insert(1.0,targetFolder)

def runPrg():
    global src_files
    src_files=''
    error_text_box.delete("1.0","end")
    lenNotFound = 0
    if(sourceFolder == targetFolder):
         error_text_box.insert(1.0,'\n source folder is same as traget folder change one of them \n')
    if (targetFolder=='' or sourceFolder=='' or filename=='' or fileArray==''):
        error_text_box.insert(1.0,'you did not select some file/folder \nTry again after selecting all the files/folder\n')
    else:
        src_files = os.listdir(sourceFolder)
        templen = len(fileArray)
        if(templen > 1):
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
                    saveTxt= open("save.txt","a")
                    lenNotFound = lenNotFound +1
                    saveTxt.write("\n"+i)
                    saveTxt.close()
                    error_text_box.insert(1.0,'file not found  ---  '+i+'\n')
        else:
            error_text_box.insert(1.0,'\nvalue in the column  == '+str(templen)+'\n')
            error_text_box.insert(1.0,'\n name of the column should be =  '+columnName+' \n -----------------------------------\n in which all the name of the files are')

    error_text_box.insert(1.0,'\n   fILE NOT FOUND  '+str(lenNotFound)+'\n')
    error_text_box.insert(1.0,'\n Process done -- look for any warning ---- \n')
    error_text_box.insert(1.0,'---------------------------------------------------------\n')
    error_text_box.insert(1.0,'File name == >  '+ filename+'\n')
    error_text_box.insert(1.0,e.strftime("%x")+'\n')
    saveTxt= open("save.txt","a")
    saveTxt.write('\n date ==  '+e.strftime("%x")+'\n')
    saveTxt.write('File name == >  '+ filename+'\n')
    saveTxt.write('Source == >  '+ sourceFolder+'\n')
    saveTxt.write('target == >  '+ targetFolder+'\n')
    saveTxt.write('\n -------------------------------------- \n')
    saveTxt.write('\n   fILE NOT FOUND  '+str(lenNotFound)+'\n')
    saveTxt.write('\n *************************************************** \n')
    saveTxt.close()

canvas= tk.Canvas(root, height=700, width=700, bg="#263042")
canvas.pack()

frame= tk.Frame(root, bg="salmon")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

source= tk.Button(frame, text="Source", padx=10, pady=10, fg="white", bg="#263042", command=sourceSelect)
source.place(x=30,y=50)

source_text_box= tk.Text(frame, height=1,width=60, padx=8, pady=8, bg="silver")
source_text_box.place(x=30,y=100)

target= tk.Button(frame, text="target", padx=10, pady=10, fg="white", bg="#263042", command=targetSelect)
target.place(x=30,y=150)

target_text_box= tk.Text(frame, height=1,width=60, padx=8, pady=8, bg="silver")
target_text_box.place(x=30,y=200)

openFile=tk.Button(frame, text="CSV/XLSX  File", padx=10, pady=10, fg="white", bg="#263042", command=openCsv)
openFile.place(x=30,y=250)

openFile_text_box= tk.Text(frame, height=1,width=60, padx=8, pady=8, bg="silver")
openFile_text_box.place(x=30,y=300)

errorLabel = Label(frame, text='Progress', bg="green",fg="white")
errorLabel.place(x=30,y=350)

error_text_box= tk.Text(frame, height=9,width=60, padx=8, pady=8, bg="cyan")
error_text_box.place(x=30,y=390)

run= tk.Button(frame, text="Run", height=1,width=20, padx=8, pady=8, fg="white", bg="green", command=runPrg)
run.place(x=210,y=5)

root.mainloop()