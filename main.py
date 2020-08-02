from tkinter.filedialog import askopenfilenames, askopenfilename
import gzip
from datetime import datetime
from tkinter import *
import sys

#############################################################
rxPlayerJoin = '{}\[[^\]]+\] logged in with entity id'
rxPlayerLeave = '{} lost connection'
rxServerStop = r'Closing Server'

blueColor = '\033[94m'
greenColor = '\033[92m'
redColor = '\033[91m'
orangeColor = '\033[93m'
boldColor = '\033[1m'
headerColor = '\033[95m'
resetColor = '\033[0m'
#############################################################


def get_name_files():
    global searchNamesReturn
    searchNamesReturn = []
    temp_name_file = askopenfilename()
    for line in open(temp_name_file):
        searchNamesReturn.append(line.strip())


def print_name_files():
    global searchNamesReturn
    print(searchNamesReturn)


def get_search_files():
    global filenameReturn
    filenameReturn = askopenfilenames()


def print_search_files():
    global filenameReturn
    print(filenameReturn)


def search():
    global searchNamesReturn
    if len(searchNamesReturn) <= 0 or len(filenameReturn) <= 0:
        sys.exit()

    temp_time_total = ''
    player_results = []
    player_time_results = []
    for i in range(len(searchNamesReturn)):
        player_results.append([])
        player_time_results.append([])

    for file in filenameReturn:
        file_date = str.split(file, sep='/')[-1]
        with gzip.open(file, 'rt', encoding='utf8') as foundFile:
            for line in foundFile:
                for playerIndex in range(len(searchNamesReturn)):
                    if re.search(rxPlayerJoin.format(searchNamesReturn[playerIndex]), line):
                        player_results[playerIndex].append('[' + file_date[0:10] + ']' + line[0:10])
                        continue
                    elif re.search(rxPlayerLeave.format(searchNamesReturn[playerIndex]), line):
                        if len(player_results[playerIndex]) != 0:
                            player_results[playerIndex].append('[' + file_date[0:10] + ']' + line[0:10])

    for resultPlayerIndex in range(len(searchNamesReturn)):
        if len(player_results[resultPlayerIndex]) == 0:
            print(searchNamesReturn[resultPlayerIndex] + ' = 0' + resetColor)
        else:
            if len(player_results[resultPlayerIndex]) % 2 != 0:
                del player_results[resultPlayerIndex][-1]
            print('\n' + headerColor + searchNamesReturn[resultPlayerIndex] + resetColor)
            for index, element in enumerate(player_results[resultPlayerIndex]):
                print((greenColor, redColor)[index % 2 == 0] + element + resetColor)
                if index % 2 == 1:
                    start_datetime = datetime.strptime(
                        player_results[resultPlayerIndex][index - 1][0:22], '[%Y-%m-%d][%H:%M:%S]')
                    end_datetime = datetime.strptime(
                        player_results[resultPlayerIndex][index][0:22], '[%Y-%m-%d][%H:%M:%S]')
                    player_time_results[resultPlayerIndex].append(end_datetime - start_datetime)
                    print(end_datetime - start_datetime)
            for index, element in enumerate(player_time_results[resultPlayerIndex]):
                if index == 0:
                    temp_time_total = element
                else:
                    temp_time_total += element
            print(boldColor + 'Total: ' + str(temp_time_total) + resetColor + '\n')
            temp_label_text = searchNamesReturn[resultPlayerIndex] + ": " + str(temp_time_total)
            Button(root, text=temp_label_text).grid(row=resultPlayerIndex, column=2)


filenameReturn = []
searchNamesReturn = []
root = Tk()

btn1 = Button(root, text='Select Names File', bd='5', command=get_name_files).grid(row=0, column=0)
btn2 = Button(root, text='Print Names', bd='5', command=print_name_files).grid(row=0, column=1)
btn3 = Button(root, text='Select Search Files', bd='5', command=get_search_files).grid(row=1, column=0)
btn4 = Button(root, text='Print Search Files', bd='5', command=print_search_files).grid(row=1, column=1)
btn5 = Button(root, text='Search', bd='5', command=search).grid(row=2, column=0)

root.mainloop()
