# Author: TuanTran
# Github: https://github.com/quoctuan-iot
# Email: quoctuan.iot@gmail.com

from __future__ import barry_as_FLUFL
from posixpath import split
from tkinter import *
import os
from tkinter.font import BOLD
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showwarning, showinfo, showerror

# Hide console when using with tkinter
# import win32gui
# import win32con
# hide = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(hide, win32con.SW_HIDE)

class FileProcessor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.windowWidth = 700
        self.windowHeight = 280
        self.radioVar = IntVar()
        self.checkVar = IntVar()
        self.selectedFolder = True 
        self.selectedFileOrFolder = False

        self.flagTxt = False
        self.flagWxt = False
        self.flagAddText = True

        self.listFileTxt = []
        self.listFileWxt = []
        self.folderSelection = ''
        self.fileSelection = ''
        self.title('File Processor - Generator')
        self.resizable(False, False)
        self.showScreenCenter()

        # Creating a frames
        self.frame1 = Frame(self)
        self.frame1.grid(column=0,row=0)

        self.frame2 = Frame(
            self, highlightbackground='black', highlightthickness=2)
        self.frame2.grid(column=0,row=1)

        self.frame3 = Frame(self)
        self.frame3.grid(column=0,row=2)

        self.frame4 = Frame(self)
        self.frame4.grid(column=0,row=3)

        # Creating a title
        self.labelTitle = Label(
            self.frame1, text='File Processor/Generator', font=('Arial', 30, BOLD))
        self.labelTitle.grid(column=0,row=0,pady=20)

        # Crateing a label chose radioButton
        # self.labelChose = Label(
        #     self.frame2, text='Chose:', font=('Arial', 15))
        # self.labelChose.grid(column=0, row=1)

        self.radioFolder = Radiobutton(self.frame2, text='Folder',
                                       variable=self.radioVar, value=1, command=self.callRadioChose, font=('Arial', 15))
        self.radioFolder.select()
        self.radioFolder.grid(column=2,row=0)

        self.radioFile = Radiobutton(self.frame2, text='File', variable=self.radioVar,
                                     value=0, command=self.callRadioChose, font=('Arial', 15))
        self.radioFile.grid(column=1,row=0)

        # Creating a label status
        self.labelStatus = Label(self.frame3, font=(
            'Arial', 9), width=80, height=2, bg='white', anchor=W)
        self.labelStatus.grid(column=0, row=0,padx=10,pady=10)

        # Creating a button
        self.buttonSelection = Button(self.frame3, text='Browse', font=(
            'Arial', 15), command=self.callButtonBrowse)
        self.buttonSelection.grid(column=1,row=0,padx=10)

        self.buttonStart = Button(self.frame4, text='Start', font=(
            'Arial', 15), command=self.callButtonStart,width = 60)
        self.buttonStart.pack(pady=20)

        # Creating a check butoon
        self.checkVar.set(1)
        checkbtnAddText = Checkbutton(self.frame2,variable=self.checkVar,onvalue=1,offvalue=0,
            text='Add Text',font=('Arial', 14),command=self.callCheckAddText)
        checkbtnAddText.grid(column=0,row=0,padx=80)

    def showScreenCenter(self):
        # Getting screen width and height
        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()

        x = int((self.screenWidth / 2) - (self.windowWidth / 2))
        y = int((self.screenHeight / 2) - self.windowHeight / 2)

        self.geometry('{}x{}+{}+{}'.format(self.windowWidth, self.windowHeight, x, y))

    def getNumberOfName(self,fileTxtName):
        tmp = fileTxtName.split('.')[0]
        numL = tmp[1]
        numB = tmp[3]
        if tmp[5] == '0':
            numS = tmp[6]
        else:
            numS = tmp[6:7]
        return [numL,numB,numS]
        
    def callCheckAddText(self):
        if (self.checkVar.get() == 1):
            self.flagAddText = True
        else:
            self.flagAddText = False

    def callRadioChose(self):
        radioSelection = self.radioVar.get()

        # Checking selection folder
        if radioSelection:
            self.selectedFolder = True
        else:
            self.selectedFolder = False

    def callButtonStart(self):
        # checking the folder or the file is selected
        if (self.selectedFileOrFolder):

            # Call generate file
            self.generateFileRxt()
            self.generateFileSxt()

            # Clean label status
            self.labelStatus.config(text='')

            # Rename
            self.renameFileOutput()

            showinfo(title='Infor', message='The file is generated completely')

        else:
            showwarning(title='Warning',
                        message='Please select folder of file')

        # Reset flag selection file or folder
        self.selectedFileOrFolder = False

    def callButtonBrowse(self):
        # Reset list file
        self.listFileTxt = []
        self.listFileWxt = []
        self.folderSelection = ''
        self.labelStatus.config(text='')

        if (self.selectedFolder):
            self.folderSelection = fd.askdirectory()

            if (self.folderSelection == ''):
                showwarning(title='Warning', message='Please chose folder')
            else:
                # Update flag selection file or folder
                self.selectedFileOrFolder = True

                if (self.checkFileInputExist()):
                    self.labelStatus.config(text=self.folderSelection)
                else:
                    self.selectedFileOrFolder = False

        else:
            self.folderSelection = ''
            self.filetypes = (('All files', '*.*'), ('Text files', '*.txt'),
                              ('Write files', '*.wxt'))

            self.fileSelection = fd.askopenfilenames(
                title='Open files', initialdir='/',
                filetypes=self.filetypes)

            if (self.fileSelection == ''):
                showwarning(title='Warning', message='Please chose files')

            else:
                # Update flag selection file or folder
                self.selectedFileOrFolder = True
                for item in self.fileSelection[0].split('/')[:-1]:
                        self.folderSelection = self.folderSelection + item + '/'
                
                if (self.checkFileWxtExist()):
                    self.labelStatus.config(text='{},{}'.format(
                        self.listFileTxt, self.listFileWxt))
                    
                else:
                    self.selectedFileOrFolder = False

                self.folderSelection = self.folderSelection[:-1]

    def checkFileBakExist(self):
        for file in self.listFileTxt:
            pathFileBak = self.folderSelection + "/"+ file.split('.')[0]+('.bak')
            if os.path.exists(pathFileBak):
                pathFiletxt = self.folderSelection + "/"+ file.split('.')[0]+('.txt')
                if os.path.exists(pathFiletxt):
                    os.remove(pathFiletxt)
                pathFileSrt = self.folderSelection + "/"+ file.split('.')[0]+('.srt')
                if os.path.exists(pathFileSrt):
                    os.remove(pathFileSrt)
                pathFileBak = self.folderSelection + "/"+ file.split('.')[0]+('.bak')
                pathFileTxt = self.folderSelection + "/"+ file.split('.')[0]+('.txt')
                if os.path.exists(pathFileBak):
                    os.rename(pathFileBak,pathFileTxt)

    def checkFileWxtExist(self):
        if (self.selectedFolder == False):
            for file in self.fileSelection:
                fileNameTxt = file.split('/')[-1]
                if (fileNameTxt.endswith(('.txt'))):
                    self.listFileTxt.append(fileNameTxt)
                else:
                    showwarning(title='Warning', message='Please chose correct file *.txt')
                    return False
                    
                pathFileWxt = file.split('.')[0] + ('.wxt')
                fileNameWxt = fileNameTxt.split('.')[0] + ('.wxt')

                if (os.path.exists(pathFileWxt)):
                    self.listFileWxt.append(fileNameWxt)
                else:
                    showwarning(
                        title='Warning',
                        message="Files {} don't exist".format(fileNameWxt))

                    return False

            self.checkFileBakExist()

            return True


    def checkFileInputExist(self):
        if (self.selectedFolder):
            for file in os.listdir(self.folderSelection):
                if (file.endswith(('.txt'))):
                    self.listFileTxt.append(file)
                    self.flagTxt = True

                if (file.endswith(('.wxt'))):
                    self.listFileWxt.append(file)
                    self.flagWxt = True

            self.checkFileBakExist()
        if (self.flagTxt == False and self.flagWxt == True):
            showwarning(
                title='Warning',
                message="Files *.txt don't exist")

            return False

        elif (self.flagWxt == False and self.flagTxt == True):
            showwarning(
                title='Warning',
                message="Files * .wxt don't exist")
            return False

        elif (self.flagWxt == False and self.flagTxt == False):
            showwarning(
                title='Warning',
                message="Files *.txt and *.wxt don't exist")
            return False

        else:
            return True

    def generateFileRxt(self):
        try:
            # Loop all files in the list file Txt
            for fileName in self.listFileTxt:
                # Creating file paths
                pathFileTxt = self.folderSelection + '/' + fileName
                pathFileRxt = self.folderSelection + \
                    '/' + fileName.split('.')[0] + '.rxt'

                # Creating object read and write
                readLinesTxt = open(pathFileTxt, encoding="utf8").readlines()
                fileRxt = open(pathFileRxt, mode = 'w',encoding="utf8")

                # Declare local variable
                characterAddition = ''
                characterIndex = -1
                characterNumber = 1
                # Loop file to get data line by line
                for cnt, line in enumerate(readLinesTxt):
                    # Tool only add two characters: Example 'zz'
                    # If cnt > 701 lines, break writing file
                    if cnt > 701:
                        showwarning(
                            title='Warning',
                            message="File *.txt contains multiple lines (more than 701 lines), So wrong format file *.rxt ")
                        break

                    # Checking lines need to add character
                    if (cnt % 26 == 0 and cnt != 0):
                        characterNumber = cnt // 26 + 1
                        characterIndex = 0
                    else:
                        characterIndex = characterIndex + 1
                        characterNumber = cnt // 26 + 1

                    # Checking character number need to add
                    if characterNumber == 1:
                        characterAddition = chr(97 + characterIndex)
                    elif characterNumber >= 2:
                        characterAddition = chr(
                            97 + characterNumber - 2) + chr(97 + characterIndex)

                    # Formating output data
                    out_line = line.replace(
                        '\n', '') + characterAddition + '\n'

                    # Writing a file Rxt
                    fileRxt.write(out_line)

                # Close a file
                fileRxt.close()

        except Exception as bug:
            showerror(title='Error',
                      message='Please check the input file structure')

    def generateFileSxt(self):
        try:
            # Loop all files in the list file Txt
            for fileName in self.listFileTxt:
                # Creating file paths
                pathFileTxt = self.folderSelection + '/' + fileName
                pathFileWxt = self.folderSelection + \
                    '/' + fileName.split('.')[0] + '.wxt'
                pathFileSxt = self.folderSelection + \
                    '/' + fileName.split('.')[0] + '.srt'

                # Creating object read and write
                readLinesTxt = open(pathFileTxt,encoding="utf8").readlines()
                readLineWxt = open(pathFileWxt,encoding="utf8").readlines()
                fileSxt = open(pathFileSxt,mode = 'w',encoding="utf8")

                # Loop file to get data line by line
                for cnt, line in enumerate(readLinesTxt):
                    tmp = line.replace('\n', '').split('\t')[0]

                    # Getting integral part and fractional part
                    integralPart = tmp.split('.')[0]
                    fractionalPart = tmp.split('.')[1]

                    # Converting seconds to hours:minutes:seconds
                    conversionResult = ('{},{}'.format(
                        self.convertSecond2FormatTime(int(integralPart)), fractionalPart[0:3]))

                    # Only getting data of the first line, don't write
                    if cnt == 0:
                        previousConversionResult = conversionResult
                        continue

                    # Formating output data
                    lineOutput = '{} --> {}\n'.format(
                        previousConversionResult, conversionResult)

                    # Writing a file Sxt
                    fileSxt.write('{}\n'.format(cnt))
                    fileSxt.write(lineOutput)

                    if (self.flagAddText):
                        if ((cnt-1) == 0):
                            fileSxt.write("KORABC Books\n")
                            fileSxt.write("EASY KOREAN READING\n")
                            tmp = self.getNumberOfName(fileName)
                            fileSxt.write("Level {} - Book {} - Story {}\n\n".format(tmp[0],tmp[1],tmp[2]))
                        elif (cnt == len(readLinesTxt)-1):
                            fileSxt.write("Get KORABC books at Amazon! ^^\n")
                        else:
                            fileSxt.write('{}\n\n'.format(readLineWxt[cnt-1].replace('\n','')))
                            
                    else:
                        if (cnt == len(readLinesTxt)-1):
                            fileSxt.write('{}\n'.format(readLineWxt[cnt-1].replace('\n','')))
                        else:
                            fileSxt.write('{}\n\n'.format(readLineWxt[cnt-1].replace('\n','')))

                    # Updating a conversion result
                    previousConversionResult = conversionResult

                # Close file
                fileSxt.close()

        except Exception as bug:
            showerror(title='Error',
                      message='Please check the input file structure')

    def renameFileOutput(self):
        for fileName in self.listFileTxt:
            pathFileTxt = self.folderSelection + '/' + fileName
            pathFileBak = self.folderSelection + \
                '/' + fileName.split('.')[0] + '.bak'
            if os.path.exists(pathFileTxt):
                os.rename(pathFileTxt, pathFileBak)

            pathFileRxt = self.folderSelection + \
                '/' + fileName.split('.')[0] + '.rxt'
            pathFileRxt2Txt = self.folderSelection + \
                '/' + fileName.split('.')[0] + '.txt'
            if os.path.exists(pathFileRxt):
                os.rename(pathFileRxt, pathFileRxt2Txt)

    def convertSecond2FormatTime(self, seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        result = '{}:{}:{}'.format(str(hour).zfill(2), str(
            minutes).zfill(2), str(seconds).zfill(2))
        return result


def main():
    fileProcessor = FileProcessor()
    fileProcessor.mainloop()

if __name__ == '__main__':
    main()