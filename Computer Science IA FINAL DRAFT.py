#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
import os.path


# In[ ]:


root = Tk()
root.title("Disaster Relief Residence Map")
root.geometry("800x640")

if(not os.path.isfile(r"Comp Sci IA Code CSV.csv")):
    df = pd.DataFrame(columns = ["Number", "Address Number", "Street", "City", "State", 
                             "Zip Code", "Residence State", "Latitude", "Longitude", "Additional Info"])
    df.to_csv(r"Comp Sci IA Code CSV.csv", index = False)
    
dataCSV = pd.read_csv(r"Comp Sci IA Code CSV.csv")
dataList = dataCSV.values.tolist()

buttonList = []
residenceNum = 0

def getCSVList(num, CSV):
    global dataCSV
    CSVNumbers = CSV['Number'].to_numpy().tolist() #Obtain list of numbers that are corresponded to each residence
    rowNum = 0 #Set initially to 0x`
    for i in range(len(CSVNumbers)+1): #Identifies which row in the CSV the desired residence is in
        if CSVNumbers[i] == num:
            rowNum = i
            break
    CSVList = [list(row) for row in CSV.values][rowNum] #Obtains a list containing all the data in that row
    return CSVList #Returns the list of information 

def findCoordinates(street, label, city = "Boulder", state = "CO", zipCode = ""):
    geolocator = Nominatim(user_agent = "Disaster Relief Residence Map")
    addressString = street + " " + city + " " + state + " " + zipCode
    location = geolocator.geocode(addressString)
    if location is None:
        label.config(text = "Residence Not Found")
        raise Exception("Residence Not Found")
    locationInformation = [location.latitude, location.longitude, location.address]
    return locationInformation

def addButton(num, label, CSV):
    global buttonList
    global dataCSV
    CSVList = getCSVList(num, CSV)
    if CSVList[6] == "Destroyed":
        btnImg = Image.open(r"Black Circle.png")
        btnImg = btnImg.resize((10, 10), Image.ANTIALIAS)
        btnImg = ImageTk.PhotoImage(btnImg)
    elif CSVList[6] == "Able to help":
        btnImg = Image.open(r"Blue Circle.png")
        btnImg = btnImg.resize((10, 10), Image.ANTIALIAS)
        btnImg = ImageTk.PhotoImage(btnImg)
    elif CSVList[6] == "Damaged":
        btnImg = Image.open(r"Red Circle.png")
        btnImg = btnImg.resize((10, 10), Image.ANTIALIAS)
        btnImg = ImageTk.PhotoImage(btnImg)
    else:
        btnImg = Image.open(r"Green Circle.png")
        btnImg = btnImg.resize((10, 10), Image.ANTIALIAS)
        btnImg = ImageTk.PhotoImage(btnImg)
    newButton = Button(root, image = btnImg, command = lambda: openResidenceWindow(num))
    lat = (39.986277 - CSVList[7])*((float(600))/(39.986277 - 39.963037)) + 20
    long = (CSVList[8] + 105.270528)*(float(800)/(105.270586 - 105.231186))
    if lat < 20 or lat > 620 or long < 0 or long > 800:
        label.config(text = "Coordinates not in range")
        raise Exception("Coordinates not in range")
    newButton.place(x = long, y = lat)
    buttonList.append([newButton, btnImg, num])

def deleteButton(num, label):
    global dataCSV
    global buttonList
    CSVNumbers = dataCSV['Number'].to_numpy().tolist()
    rowNum = 0
    for i in range(len(CSVNumbers)+1):
        if CSVNumbers[i] == num:
            rowNum = i
            break
    for j in range(len(buttonList)):
        if rowNum == buttonList[j][2]:
            buttonList[j][0].destroy()
            dataCSV = dataCSV.drop(rowNum)
            dataCSV.to_csv(r"Comp Sci IA Code CSV.csv", index = False)
            dataCSV = pd.read_csv(r"Comp Sci IA Code CSV.csv")
            del buttonList[j]
            label.config(text = "Deleted")
            break
            
def changeData(num, residenceState, notes, label):
    global dataCSV
    CSVNumbers = dataCSV['Number'].to_numpy().tolist()
    rowNum = 0
    for i in range(len(CSVNumbers)+1):
        if CSVNumbers[i] == num:
            rowNum = i
            break
    CSVList = getCSVList(num, dataCSV)
    dataCSV.at[rowNum, 'Residence State'] = residenceState
    dataCSV.at[rowNum, 'Additional Info'] = notes
    if residenceState == "Destroyed":
        btnImg = Image.open(r"Black Circle.png")
        btnImg = btnImg.resize((10, 10), Image.ANTIALIAS)
        btnImg = ImageTk.PhotoImage(btnImg)
    elif residenceState == "Able to help":
        btnImg = Image.open(r"Blue Circle.png")
        btnImg = btnImg.resize((10, 10), Image.ANTIALIAS)
        btnImg = ImageTk.PhotoImage(btnImg)
    elif residenceState == "Damaged":
        btnImg = Image.open(r"Red Circle.png")
        btnImg = btnImg.resize((10, 10), Image.ANTIALIAS)
        btnImg = ImageTk.PhotoImage(btnImg)
    else:
        btnImg = Image.open(r"Green Circle.png")
        btnImg = btnImg.resize((10, 10), Image.ANTIALIAS)
        btnImg = ImageTk.PhotoImage(btnImg)
    newButton = Button(root, image = btnImg, command = lambda: openResidenceWindow(num))
    global buttonList
    for i in range(len(buttonList)):
        if buttonList[i][2] == num:
            buttonList[i][0].destroy()
            buttonList[i][0] = newButton
            buttonList[i][1] = btnImg
            lat = (39.986277 - CSVList[7])*((float(600))/(39.986277 - 39.963037)) + 20
            long = (CSVList[8] + 105.270528)*(float(800)/(105.270586 - 105.231186))
            newButton.place(x = long, y = lat)
            break
    dataCSV.to_csv(r"Comp Sci IA Code CSV.csv", index = False)
    dataCSV = pd.read_csv(r"Comp Sci IA Code CSV.csv")
    label.config(text = "Saved")

def openResidenceWindow(num):
    resWin = Toplevel(root)
    resWin.title("Residence Information")
    resWin.geometry("350x230")
    
    global dataCSV
    
    resInfo = getCSVList(num, dataCSV)
    
    streetChangeLabel = Label(resWin, text = "Street and Number: ")
    streetChangeEntry = Label(resWin, text = str(int(resInfo[1])) + " " + resInfo[2])
    
    cityChangeLabel = Label(resWin, text = "City: ")
    cityChangeEntry = Label(resWin, text = resInfo[3])
    
    zipChangeLabel = Label(resWin, text = "Zip Code: ")
    zipChangeEntry = Label(resWin, text = int(resInfo[5]))
    
    residenceStates = ["Able to help", "Normal", "Damaged", "Destroyed"]
    stateOfResidenceChange = StringVar()
    stateOfResidenceChange.set(resInfo[6])
    stateEntryChangeDropdown = OptionMenu(resWin, stateOfResidenceChange, *residenceStates)
    dropDownChangeLabel = Label(resWin, text = resInfo[6])
    
    notesChangeLabel = Label(resWin, text = "Additional Notes: ")
    notesChangeEntry = Entry(resWin, width = 20)
    notesChangeEntry.insert(0, resInfo[9])
    
    saveLabel = Label(resWin, text = "")
    saveButton = Button(resWin, text = "Save", width = 10, command = lambda: changeData(num, stateOfResidenceChange.get(), 
        notesChangeEntry.get(), saveLabel))
    
    deleteButtonButton = Button(resWin, text = "Delete", width = 10, command = lambda: deleteButton(num, saveLabel))
    
    streetChangeLabel.grid(column = 0, row = 0)
    streetChangeEntry.grid(column = 1, row = 0, pady = 5)
    cityChangeLabel.grid(column = 0, row = 1)
    cityChangeEntry.grid(column = 1, row = 1, pady = 5)
    zipChangeLabel.grid(column = 0, row = 2)
    zipChangeEntry.grid(column = 1, row = 2, pady = 5)
    saveButton.grid(column = 1, row = 5, pady = 5)
    saveLabel.grid(column = 1, row = 6)
    stateEntryChangeDropdown.grid(column = 1, row = 3, pady = 5)
    dropDownChangeLabel.grid(column = 0, row = 3)
    notesChangeLabel.grid(column = 0, row = 4)
    notesChangeEntry.grid(column = 1, row = 4, pady = 5)
    deleteButtonButton.grid(column = 0, row = 5)

def addData(street, city, zipCode, residenceState, notes, label, window):
    try:
        coordinates = findCoordinates(street, label, city, "CO", zipCode)
        splitAddress = coordinates[2].split(", ")
        if not splitAddress[0].isdigit():
            del splitAddress[0]
        global residenceNum
        global dataCSV
        tempCSV = dataCSV.copy()
        tempCSV.at[residenceNum, 'Number'] = residenceNum
        tempCSV.at[residenceNum, 'Address Number'] = splitAddress[0]
        tempCSV.at[residenceNum, 'Street'] = splitAddress[1]
        tempCSV.at[residenceNum, 'City'] = city
        tempCSV.at[residenceNum, 'State'] = "Colorado"
        tempCSV.at[residenceNum, 'Zip Code'] = zipCode
        tempCSV.at[residenceNum, 'Residence State'] = residenceState
        tempCSV.at[residenceNum, 'Latitude'] = coordinates[0]
        tempCSV.at[residenceNum, 'Longitude'] = coordinates[1]
        tempCSV.at[residenceNum, 'Additional Info'] = notes
        addButton(residenceNum, label, tempCSV)
        tempCSV.to_csv(r"Comp Sci IA Code CSV.csv", index = False)
        dataCSV = pd.read_csv(r"Comp Sci IA Code CSV.csv")
        residenceNum += 1
        label.config(text = "Saved")
    except:
        pass
    
def openInputWindow():
    inputWindow = Toplevel(root)
    inputWindow.title("Residence Information Input")
    inputWindow.geometry("350x230")
    
    streetEntryLabel = Label(inputWindow, text = "Enter the first line of the address here: ")
    streetEntry = Entry(inputWindow, width = 20)
    streetEntry.insert(0, "Street Address")

    cityEntryLabel = Label(inputWindow, text = "Enter the city here: ")
    cityEntry = Entry(inputWindow, width = 20)
    cityEntry.insert(0, "City Name")

    zipEntryLabel = Label(inputWindow, text = "Enter the zip code here: ")
    zipEntry = Entry(inputWindow, width = 20)
    zipEntry.insert(0, 'Zip Code')
    
    residenceStates = ["Able to help", "Normal", "Damaged", "Destroyed"]
    stateOfResidence = StringVar()
    stateOfResidence.set("Normal")
    stateEntryDropdown = OptionMenu(inputWindow, stateOfResidence, *residenceStates)
    dropDownLabel = Label(inputWindow, text = "Select the state of the residence") 
    
    notesLabel = Label(inputWindow, text = "Enter any additional notes here: ")
    notesEntry = Entry(inputWindow, width = 20)
    notesEntry.insert(0, 'Additional Notes')
    
    confirmationLabel = Label(inputWindow, text = "")
    submitButton = Button(inputWindow, text = "Submit", width = 10, command = lambda: addData(
        streetEntry.get(), cityEntry.get(), zipEntry.get(), stateOfResidence.get(), notesEntry.get(), 
        confirmationLabel, inputWindow))
    
    streetEntryLabel.grid(column = 0, row = 0)
    streetEntry.grid(column = 1, row = 0, pady = 5)
    cityEntryLabel.grid(column = 0, row = 1)
    cityEntry.grid(column = 1, row = 1, pady = 5)
    zipEntryLabel.grid(column = 0, row = 2)
    zipEntry.grid(column = 1, row = 2, pady = 5)
    submitButton.grid(column = 1, row = 5, pady = 5)
    confirmationLabel.grid(column = 1, row = 6)
    stateEntryDropdown.grid(column = 1, row = 3, pady = 5)
    dropDownLabel.grid(column = 0, row = 3)
    notesLabel.grid(column = 0, row = 4)
    notesEntry.grid(column = 1, row = 4, pady = 5)
    
def clearMap():
    try:
        df = pd.DataFrame(columns = ["Number", "Address Number", "Street", "City", "State", 
                             "Zip Code", "Residence State", "Latitude", "Longitude", "Additional Info"])
        df.to_csv(r"Comp Sci IA Code CSV.csv", index = False)
        global buttonList
        for button in buttonList:
            button[0].destroy()
        buttonList = []
    except:
        CSVExceptionWindow = Toplevel(root)
        CSVExceptionWindow.title("CSV Error")
        CSVExceptionWindow.geometry("200x50")
        CSVExceptionLabel = Label(CSVExceptionWindow, text = "CSV cannot be changed at this time.")
        CSVExceptionLabel.grid(column = 0, row = 0)
        closeExceptionWindowButton = Button(CSVExceptionWindow, text="Ok", command=CSVExceptionWindow.destroy)
        closeExceptionWindowButton.grid(column = 0, row = 1)

#Set up map and buttons
frame = LabelFrame(root)
frame.grid(column = 0, row = 0)

openInputWindowButton = Button(frame, text = "Input New Residence", command = openInputWindow)
openInputWindowButton.grid(column = 0, row = 0)

clearMapButton = Button(frame, text = "Clear Map", command = clearMap)
clearMapButton.grid(column = 1, row = 0)

soBoMap = Image.open(r"Google Maps South Boulder.png")
soBoMap = soBoMap.resize((800, 600))
soBoMap = ImageTk.PhotoImage(soBoMap, master = root)
soBoMapLabel = Label(root, image = soBoMap)
soBoMapLabel.grid(column = 0, row = 1)

#Set up prexisting locations
for i in range(len(dataList)):
    if dataList[i][6] == "Destroyed":
        btnImg = Image.open(r"Black Circle.png")
        btnImg = btnImg.resize((10, 10), Image.ANTIALIAS)
        btnImg = ImageTk.PhotoImage(btnImg)
    elif dataList[i][6] == "Able to help":
        btnImg = Image.open(r"Blue Circle.png")
        btnImg = btnImg.resize((10, 10), Image.ANTIALIAS)
        btnImg = ImageTk.PhotoImage(btnImg)
    elif dataList[i][6] == "Damaged":
        btnImg = Image.open(r"Red Circle.png")
        btnImg = btnImg.resize((10, 10), Image.ANTIALIAS)
        btnImg = ImageTk.PhotoImage(btnImg)
    else:
        btnImg = Image.open(r"Green Circle.png")
        btnImg = btnImg.resize((10, 10), Image.ANTIALIAS)
        btnImg = ImageTk.PhotoImage(btnImg)
    newButton = Button(root, image = btnImg, command = lambda: openResidenceWindow(dataList[i][0]))
    buttonList.append([newButton, btnImg, i])
    lat = (39.986277 - dataList[i][7])*((float(600))/(39.986277 - 39.963037)) + 20
    long = (dataList[i][8] + 105.270528)*(float(800)/(105.270586 - 105.231186))
    newButton.place(x = long, y = lat)

root.mainloop()

