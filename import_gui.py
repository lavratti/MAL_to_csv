from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import webbrowser
import xml.etree.ElementTree

def openMAL(event):
    webbrowser.open_new(r"www.myanimelist.net/profile/lavratti")

def openfname():
    fname = filedialog.askopenfilename(initialdir = "/",title = "Chose the xml", filetypes = ((".xml","*.xml"),("all files","*.*")))
    print('open  fname =', fname)
    openPathText.set(fname)
    return fname

def savefname():
    fname = filedialog.asksaveasfilename(initialdir = "/",title = "Save csv as...", filetype = ((".csv","*.csv"),(".csv","*.csv")))
    if not fname.endswith('.csv'):
        print('Fixed \'.csv\'-less save fname')
        fname += '.csv'

    print('save fname =', fname)
    savePathText.set(fname)
    return fname

def closeToplevel(self):
    self.topFrame.destroy()

def convert():
    infile = openPathText.get()
    outfile = savePathText.get()
    print('in:',infile)
    print('out',outfile)
    try:

        tree = xml.etree.ElementTree.parse(infile)
        docroot = tree.getroot()
        a = 1

        try:
            with open(outfile, 'w') as file:
                file.write('Anime Db id;Title;Type;Episodes;My id;'
                           'Watched episodes;My start date;'
                           'My finish date;My Rated;My Score;"Dvd?";'
                           'Storage;Status;Comments;My times watched;'
                           'Rewatch value;Tags;My rewatching;'
                           'Rewatching ep;Update on Import\n');

                while a < len(docroot):
                    b = 0
                    while b < len(docroot[a]):
                        txt = str(docroot[a][b].text)
                        txt = txt.encode('ascii', 'ignore').decode('ascii')
                        txt = txt.replace(';', ':')
                        txt = txt.replace('None', '')
                        txt = txt.replace('0000-00-00', '')

                        print(txt, ';', end="", flush=True)
                        file.write(txt + ';')
                        b += 1
                    print('\n')
                    file.write('\n')

                    a += 1

                messagebox.showinfo('Done',
                                    'File saved at '+outfile+
                                    '\n'
                                    '\nDrop by my MAL page if you liked :)')

        except IOError:
            messagebox.showerror('Error: cannot save file',
                                 'Cannot save file'
                                 '\n[IOError ln:39]'
                                 '\n[except ln:69]'
                                 '\n\nHow to solve this:'
                                 '\n1. Select a valid filename.'
                                 '\n2. Ensure there are no other services using the file'
                                 '\n3. Try running in Admin mode')

    except IOError:
        messagebox.showerror('Error: cannot open file',
                             'Cannot open file'
                             '\n[IOError ln:33]'
                             '\n[except ln:74]'
                             '\n\nHow to solve this:'
                             '\n1. Select a valid filename.'
                             '\n2. Ensure there are no other services using the file'
                             '\n3. Try running in Admin mode')

root = Tk()

bottomFrame = Frame(root, height='80', width='380')
bottomFrame.pack()
footerFrame = Frame(root, height='20', width='380')
footerFrame.pack(side=BOTTOM)

openPathText = StringVar()
savePathText = StringVar()

label1 = Label(bottomFrame, text='Convert your XML export into an cool \'excel CSV\'')
openButton = Button(bottomFrame, text='Open xml...', command=openfname, width='12')
openPath = Entry(bottomFrame, textvariable=openPathText, width='50', state='disabled')
saveButton = Button(bottomFrame, text='Save csv as...', command=savefname, width='12')
savePath = Entry(bottomFrame, textvariable=savePathText, width='50', state='disabled')

label1.grid(columnspan=2)

openButton.grid(row=1, sticky=E)
openPath.grid(row=1, column=1)

saveButton.grid(row=2, sticky=E)
savePath.grid(row=2, column=1)


labelCredito1 = Label(footerFrame, text='By:')
link = Label(footerFrame, text='lavratti', fg='blue', cursor='hand2')
link.bind("<Button-1>", openMAL)
labelCredito2 = Label(footerFrame, text=', leave a comment on my profile :)')

labelCredito1.pack(side=LEFT)
link.pack(side=LEFT)
labelCredito2.pack(side=LEFT)

convertButton = Button(bottomFrame, text='Convert to Excel xml!', command=convert)
convertButton.grid(columnspan=2)

root.minsize(width=400, height=120)
root.maxsize(width=400, height=120)
root.title("MAL xml to csv")
root.mainloop()