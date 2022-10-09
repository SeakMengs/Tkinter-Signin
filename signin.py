import csv
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from ctypes import windll

#* Constatnt
FRAMEBG='#005D85'
FONTFG='#FFFFFF'
BOXBG='#3A96BD'
global is_ticked 
is_ticked = False
# Some WindowsOS styles, required for task bar integration
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
#*

#*----------------------------------------------------------------------------------------------------------------------------------------
# ? these functions copy from https://stackoverflow.com/questions/63217105/tkinter-overridedirect-minimizing-and-windows-task-bar-issues
def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y

def Dragging(event):
    # ? current window x - last click + current window x
    # print('event x=', event.x, 'lastClick x=', lastClickX , 'root.winfo x=', root.winfo_x())
    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry("+%s+%s" % (x , y))

def minimizeGUI():
    global z
    root.state('withdrawn')
    root.overrideredirect(False)
    root.state('iconic')
    z = 1

def set_appwindow(mainWindow):
    # Honestly forgot what most of this stuff does. I think it's so that you can see
    # the program in the task bar while using overridedirect. Most of it is taken
    # from a post I found on stackoverflow.
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
    # re-assert the new window style
    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())

def frameMapped(event=None):
    global z
    root.overrideredirect(True)
    # root.iconbitmap("ANAL_OG.ico")
    if z == 1:
        set_appwindow(root)
        z = 0
#*----------------------------------------------------------------------------------------------------------------------------------------

def fullScreen():
    is_fullScreen = BooleanVar

    current_width = root.winfo_width()
    current_height = root.winfo_height()
    print(current_width)

    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    
    x2 = int((screenWidth/2) - (current_width/2))
    y2 = int((screenHeight/2) - (current_height/2))

    if (root.winfo_width() == root.winfo_screenwidth() or root.winfo_height() == root.winfo_screenheight()):
        is_fullScreen = True
    else:
        is_fullScreen = False

    if is_fullScreen == True:
        # root.attributes('-fullscreen', True)
        # root.geometry(f"{current_width}x{current_height}")
        root.state('normal')
        # root.geometry('1280x720')
        print("fullscreen")
    elif is_fullScreen == False:
        # root.geometry(f"{screenWidth}x{screenHeight}")
        # root.geometry("%dx%d" % (screenWidth, screenHeight))
        root.state('zoomed')
        print("minimized")

class App():
    def __init__(self):
        self.root = root
        self.userFocus = False
        self.pwFocus = False

    def titleBar(self):
        # ? create my own titlebar
        root.overrideredirect(True)
        root.after(10, lambda: set_appwindow(root))
        self.titlebar = Frame(root, background=FRAMEBG, bd=0)

        #*----------------------------------------------------------------------------------------------------------------------------------------
        # ? these functions copy from https://stackoverflow.com/questions/63217105/tkinter-overridedirect-minimizing-and-windows-task-bar-issues
        self.titlebar.bind('<Button-1>', SaveLastClickPos)
        self.titlebar.bind('<B1-Motion>', Dragging)
        self.titlebar.bind("<Map>", frameMapped) # This brings back the window
        #*----------------------------------------------------------------------------------------------------------------------------------------

        self.icon = Image.open('asset\\bank.png')
        self.icon = self.icon.resize((22, 22))
        self.icon = ImageTk.PhotoImage(self.icon)
        Label(self.titlebar, text='  Yato Bank', font=('Lexend', 16), bg=FRAMEBG, fg=FONTFG, image=self.icon, compound=LEFT).pack(side=LEFT, pady=10, padx=10)

        # ? Open image using pil (for resize purpose)
        self.closeIcon = Image.open("asset\\close.png")
        self.closeIcon = self.closeIcon.resize((24, 24))
        self.closeIcon = ImageTk.PhotoImage(self.closeIcon)
        Button(self.titlebar, image=self.closeIcon, command=root.destroy, background=FRAMEBG, bd=0, activebackground=FRAMEBG).pack(side=RIGHT, pady=10, padx=10)

        self.maximizeIcon = Image.open("asset\\maximize.png")
        self.maximizeIcon = self.maximizeIcon.resize((24, 24))
        self.maximizeIcon = ImageTk.PhotoImage(self.maximizeIcon)
        Button(self.titlebar, image=self.maximizeIcon, command=fullScreen, background=FRAMEBG, bd=0, activebackground=FRAMEBG).pack(side=RIGHT, pady=10, padx=10)

        self.minimizeIcon = Image.open("asset\\minus.png")
        self.minimizeIcon = self.minimizeIcon.resize((24, 24))
        self.minimizeIcon = ImageTk.PhotoImage(self.minimizeIcon)
        Button(self.titlebar, image=self.minimizeIcon, command=minimizeGUI, background=FRAMEBG, bd=0, activebackground=FRAMEBG).pack(side=RIGHT, pady=10, padx=10)

            # make the frame in the middle
        self.titlebar.pack(expand=0, fill=BOTH)
    
    def ticked(self):
        global is_ticked

        self.checkedIcon = PhotoImage(file="asset\\check.png")

        if (is_ticked == False):
            self.checkbox.config(image=self.checkedIcon)
            #* this line is from the help of https://stackoverflow.com/questions/57388865/tkinter-button-doesnt-work-when-i-add-an-image-on-this-button
            self.checkbox.image = self.checkedIcon
            # *----------------------------------------------------------------------------------------------------------------------------------------
            is_ticked = True
        elif (is_ticked == True):
            self.checkbox.config(image=self.checkIcon)
            self.checkbox.image = self.checkIcon
            is_ticked = False

    # ? read from csv into a list
    def fetchAccount(self):
        with open('data\\account.csv', 'r') as file:
            Read = csv.reader(file)
            field = next(Read)
            rows = list(Read)
        file.close()

        return rows

    def checkExist(self):
        self.exist = False
        self.Username = self.username.get()
        self.Password = self.pw.get()

        self.accountDataSet = (self.fetchAccount())
        for users, pws in self.accountDataSet:
            if users == self.Username and pws == self.Password:
                self.exist = True
                break

        if (self.exist == True):
            messagebox.showinfo(title="Account exist", message="Logging in")
        elif (self.exist == False):
            messagebox.showerror(title="Account doesn't exist", message="Account doesn't exist")

    # def Preview(self):
    #     # 1ms
    #     delay = 1000
    #     print("run")
    #     # ? if entry box is not selected
    #     if self.username.focus_get() != None:
    #         self.userFocus = True
    #         self.pwFocus = False
    #         print("userFocus:", self.userFocus)
    #     elif self.userFocus == False:
    #         if self.username.get() == "" and self.username.focus_get() == None:
    #             self.username.insert(0,"Username")
    #             print(self.username.focus_get())

    #     if self.pw.focus_get() != None:
    #         self.userFocus = False
    #         self.pwFocus = True
    #         print("pwFocus:", self.pwFocus)
    #     elif self.pwFocus == False:
    #         if  not self.username.get() and self.username.focus_get() == None:
    #             self.username.insert(0,"Username")
    #             print(self.username.focus_get())
        
    #     # if self.pwFocus == True:
    #     #     self.userFocus = False
    #     # elif self.pwFocus == False:
    #     #     self.userFocus = True

    #     if self.username.focus_get() == None:
    #         self.username.after(delay, self.Preview)
    #     elif self.pw.focus_get == None:
    #         self.pw.after(delay, self.Preview)

    # def removePreview(self, text):
    #     if text.get() == "Password" or text.get() == "Username":
    #         text.delete(0, END)

    #     if self.username.focus_get() != None:
    #         self.username.after(1000, self.Preview)
    #     elif self.pw.focus_get != None:
    #         self.pw.after(1000, self.Preview)

    def signIn(self):
        # ? create frame of the form
        self.form = Frame(root, background=FRAMEBG)
        self.entryBox = PhotoImage(file='asset\entrybox.png')
        Label(self.form, text='Sign in', font=('Lexend', 64), bg=FRAMEBG, fg=FONTFG).grid(row=0)
        Label(self.form, text='sign in to start managing your bank account', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG).grid(row=1, pady=20)

        Label(self.form, text='Username', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG,).grid(row=2, sticky=W, padx=(50))
        Label(self.form, image=self.entryBox, bg=FRAMEBG, compound=BOTTOM).grid(row=3, pady=(0,20))
        self.username = Entry(self.form, font=('Lexend Deca', 16), background=BOXBG, foreground=FONTFG,bd=0, insertbackground='white')
        self.username.grid(row=3, pady=(0, 20))
        # self.username.bind("<Button-1>", lambda e: self.removePreview(self.username))

    
        Label(self.form, text='Password', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG,).grid(row=4, sticky=W, padx=(50))
        Label(self.form, image=self.entryBox, bg=FRAMEBG).grid(row=5, pady=(0,20))
        self.pw = Entry(self.form, font=('Lexend Deca', 16), background=BOXBG, foreground=FONTFG,bd=0,show='*', exportselection=0, insertbackground='white')
        self.pw.grid(row=5, pady=(0,20))
        # self.pw.bind("<Button-1>", lambda e: self.removePreview(self.pw))

        # self.Preview()

        # global checkbox, checkIcon
        self.checkIcon = PhotoImage(file="asset\\checkbox.png")
        self.checkbox = Button(self.form, text='remember me', font=('Lexend Deca', 10), bg=FRAMEBG, fg=FONTFG, image=self.checkIcon, compound=LEFT, bd=0, activebackground=FRAMEBG, activeforeground=FONTFG, command=self.ticked)
        self.checkbox.grid(row=6, column=0,sticky=W, padx=(55))

        Button(self.form, text='forgot password?', font=('Lexend Deca', 10), bg=FRAMEBG, fg=FONTFG, bd=0, activebackground=FRAMEBG, activeforeground=FONTFG).grid(row=6, column=0, sticky=E, padx=(0, 50))

        self.Login = Button(self.form,text='Login',font=('Lexend Deca', 16), image=self.entryBox, background=FRAMEBG, foreground=FONTFG,bd=0,
        compound='center', activebackground=FRAMEBG, activeforeground=FRAMEBG, command=self.checkExist)
        self.Login.grid(row=7, pady=31)
        self.root.bind("<Return>", lambda e: self.checkExist())

        self.form.pack(expand=1)

def main():
    global root, z
    z = 0
    root = Tk()
    icon = PhotoImage('asset\\icon.ico')
    root.iconbitmap(True, icon)
    app = App()
    root.geometry('1280x720')
    app.titleBar()
    app.signIn()
    
    root.config(background='#005D85')

    # makes sure everything is up-to-date
    root.update_idletasks() 

    # ? make the window appear in the middle of the screen everytime
    height = root.winfo_height()
    width = root.winfo_width()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    print(width, height)
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))

    root.geometry(f"{width}x{height}+{x}+{y}")
    root.minsize(width, height)
    root.mainloop()

#? to prevent duplicate variables
if __name__ == "__main__":
    main()