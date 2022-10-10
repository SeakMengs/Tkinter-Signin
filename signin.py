import csv
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from ctypes import windll

#* Constatnt
FRAMEBG='#005D85'
FONTFG='#FFFFFF'
BOXBG='#3A96BD'
is_ticked = False
is_tickedSignup = False
inLogin = True
inSignup = False
# Some WindowsOS styles, required for task bar integration
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
#*

#*----------------------------------------------------------------------------------------------------------------------------------------
class tittle():
    def __init__(self):
        self.root = root
# ? these functions copy from https://stackoverflow.com/questions/63217105/tkinter-overridedirect-minimizing-and-windows-task-bar-issues
    def SaveLastClickPos(self, event):
        global lastClickX, lastClickY
        lastClickX = event.x
        lastClickY = event.y

    def Dragging(self, event):
        # ? current window x - last click + current window x
        # print('event x=', event.x, 'lastClick x=', lastClickX , 'root.winfo x=', root.winfo_x())
        self.x, self.y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
        root.geometry("+%s+%s" % (self.x , self.y))

    def minimizeGUI(self):
        global z
        root.state('withdrawn')
        root.overrideredirect(False)
        root.state('iconic')
        z = 1

    def set_appwindow(self, mainWindow):
        # Honestly forgot what most of this stuff does. I think it's so that you can see
        # the program in the task bar while using overridedirect. Most of it is taken
        # from a post I found on stackoverflow.
        self.hwnd = windll.user32.GetParent(mainWindow.winfo_id())
        self.stylew = windll.user32.GetWindowLongW(self.hwnd, GWL_EXSTYLE)
        self.stylew = self.stylew & ~WS_EX_TOOLWINDOW
        self.stylew = self.stylew | WS_EX_APPWINDOW
        self.res = windll.user32.SetWindowLongW(self.hwnd, GWL_EXSTYLE, self.stylew)
        # re-assert the new window style
        mainWindow.wm_withdraw()
        mainWindow.after(10, lambda: mainWindow.wm_deiconify())

    def frameMapped(self,event=None):
        global z
        root.overrideredirect(True)
        # root.iconbitmap("ANAL_OG.ico")
        if z == 1:
            self.set_appwindow(root)
            z = 0
    #*----------------------------------------------------------------------------------------------------------------------------------------

    def fullScreen(self):
        self.is_fullScreen = BooleanVar

        self.current_width = root.winfo_width()
        self.current_height = root.winfo_height()
        # print(self.current_width)

        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        
        x2 = int((screenWidth/2) - (self.current_width/2))
        y2 = int((screenHeight/2) - (self.current_height/2))

        if (root.winfo_width() == root.winfo_screenwidth() or root.winfo_height() == root.winfo_screenheight()):
            self.is_fullScreen = True
        else:
            self.is_fullScreen = False

        if self.is_fullScreen == True:
            # root.attributes('-fullscreen', True)
            # root.geometry(f"{current_width}x{self.current_height}")
            root.state('normal')
            # root.geometry('1280x720')
            # print("fullscreen")
        elif self.is_fullScreen == False:
            # root.geometry(f"{screenWidth}x{screenHeight}")
            # root.geometry("%dx%d" % (screenWidth, screenHeight))
            root.state('zoomed')
            # print("minimized")

    def titleBar(self):
        # ? create my own titlebar
        root.overrideredirect(True)
        root.after(10, lambda: self.set_appwindow(root))
        self.titlebar = Frame(root, background=FRAMEBG, bd=0)

        #*----------------------------------------------------------------------------------------------------------------------------------------
        # ? these functions copy from https://stackoverflow.com/questions/63217105/tkinter-overridedirect-minimizing-and-windows-task-bar-issues
        self.titlebar.bind('<Button-1>', self.SaveLastClickPos)
        self.titlebar.bind('<B1-Motion>', self.Dragging)
        self.titlebar.bind("<Map>", self.frameMapped) # This brings back the window
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
        Button(self.titlebar, image=self.maximizeIcon, command=self.fullScreen, background=FRAMEBG, bd=0, activebackground=FRAMEBG).pack(side=RIGHT, pady=10, padx=10)

        self.minimizeIcon = Image.open("asset\\minus.png")
        self.minimizeIcon = self.minimizeIcon.resize((24, 24))
        self.minimizeIcon = ImageTk.PhotoImage(self.minimizeIcon)
        Button(self.titlebar, image=self.minimizeIcon, command=self.minimizeGUI, background=FRAMEBG, bd=0, activebackground=FRAMEBG).pack(side=RIGHT, pady=10, padx=10)

            # make the frame in the middle
        self.titlebar.pack(expand=0, fill=BOTH)

#*----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#* Sign in page
class loginPage():
    def __init__(self):
    # def signIn(self):

        self.root = root
        self.form = Frame(root, background=FRAMEBG)

        global inLogin, inSignup
        inSignup = False
        inLogin = True
        self.uiLogo()

        # ? create frame of the form
        # self.form = Frame(root, background=FRAMEBG)

        self.entryBox = PhotoImage(file='asset\entrybox.png')
        Label(self.form, text='Sign in', font=('Lexend', 64), bg=FRAMEBG, fg=FONTFG).grid(row=0)
        Label(self.form, text='sign in to start managing your bank account', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG).grid(row=1, pady=20)

        Label(self.form, text='Username', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG,).grid(row=2, sticky=W, padx=(50))
        Label(self.form, image=self.entryBox, bg=FRAMEBG, compound=BOTTOM).grid(row=3, pady=(0,20))
        self.username = Entry(self.form, font=('Lexend Deca', 16), background=BOXBG, foreground=FONTFG,bd=0, insertbackground='white')
        self.username.grid(row=3, pady=(0, 20))
    
        Label(self.form, text='Password', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG,).grid(row=4, sticky=W, padx=(50))
        Label(self.form, image=self.entryBox, bg=FRAMEBG).grid(row=5, pady=(0,20))
        self.pw = Entry(self.form, font=('Lexend Deca', 16), background=BOXBG, foreground=FONTFG,bd=0,show='*', exportselection=0, insertbackground='white')
        self.pw.grid(row=5, pady=(0,20))

        self.checkIcon = PhotoImage(file="asset\\checkbox.png")
        self.checkbox = Button(self.form, text='remember me', font=('Lexend Deca', 10), bg=FRAMEBG, fg=FONTFG, image=self.checkIcon, compound=LEFT, bd=0, activebackground=FRAMEBG, activeforeground=FONTFG, command=self.ticked, cursor='hand2')
        self.checkbox.grid(row=6, column=0,sticky=W, padx=(55))

        Button(self.form, text='forgot password?', font=('Lexend Deca', 10), bg=FRAMEBG, fg=FONTFG, bd=0, activebackground=FRAMEBG, activeforeground=FONTFG, cursor='hand2').grid(row=6, column=0, sticky=E, padx=(0, 50))

        self.Login = Button(self.form,text='Login',font=('Lexend Deca', 16), image=self.entryBox, background=FRAMEBG, foreground=FONTFG,bd=0,
        compound='center', activebackground=FRAMEBG, activeforeground=FRAMEBG, command=self.checkExist, cursor='hand2')
        self.Login.grid(row=7, pady=31)
        # ? bind click Enter key to login button
        self.root.bind("<Return>", lambda e: self.checkExist())

        Label(self.form, text='Need an account?', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG,).grid(row=8, sticky=W, padx=(68))
        Button(self.form, text='SIGN UP', font=('Lexend Deca', 16, 'bold'), bg=FRAMEBG, fg=FONTFG, bd=0, activebackground=FRAMEBG, activeforeground=FONTFG, command=self.changeToSignup, cursor='hand2').grid(row=8, sticky=E, padx=(0, 70))
        
        self.form.pack(expand=1)


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
            # ? read all data after reading first row, convert it into list
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
            messagebox.showinfo(title="Yato Bank", message="Logging in")
        elif (self.exist == False):
            messagebox.showerror(title="Yato Bank", message="Account doesn't exist")

        
    def uiLogo(self):
        #* Thank to this post https://stackoverflow.com/questions/33046790/how-to-horizontally-center-a-widget-using-grid
        #* i learn relx and rely :)
        global inLogin, inSignup
        if (inLogin == True):
            self.loginLogo = Image.open('asset\\login.png')  
            self.loginLogo = self.loginLogo.resize((360,360))
            self.loginLogo = ImageTk.PhotoImage(self.loginLogo)

            self.loginBG = Label(self.root, image=self.loginLogo, bg=FRAMEBG)
            self.loginBG.place(anchor=E, relx = 0.94, rely = .57)

    #* switch frame
    def startLogin(self):
        global inLogin, inSignup
        inSignup = False
        inLogin = True

        self.form.pack(expand=1)
    
    def changeToSignup(self):
        self.form.pack_forget()
        signupPage().startSignup()

#*----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#* Sign up page
class signupPage():
    #* Sign up function
    # def signUp(self):
    def __init__(self):
        self.root = root
        self.signupFrame = Frame(root, background=FRAMEBG)

        global inLogin, inSignup
        inSignup = True
        inLogin = False
        self.signupLogo()

        # ? create frame of the signup
        # self.signupFrame = Frame(root, background=FRAMEBG)

        self.entryBox = PhotoImage(file='asset\entrybox.png')
        Label(self.signupFrame, text='Sign up', font=('Lexend', 64), bg=FRAMEBG, fg=FONTFG).grid(row=0)
        Label(self.signupFrame, text='Signup to start managing your bank account', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG).grid(row=1, pady=20)

        Label(self.signupFrame, text='Username', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG,).grid(row=2, sticky=W, padx=(50))
        Label(self.signupFrame, image=self.entryBox, bg=FRAMEBG, compound=BOTTOM).grid(row=3, pady=(0,20))
        self.username = Entry(self.signupFrame, font=('Lexend Deca', 16), background=BOXBG, foreground=FONTFG,bd=0, insertbackground='white')
        self.username.grid(row=3, pady=(0, 20))
    
        Label(self.signupFrame, text='Password', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG,).grid(row=4, sticky=W, padx=(50))
        Label(self.signupFrame, image=self.entryBox, bg=FRAMEBG).grid(row=5, pady=(0,20))
        self.pw = Entry(self.signupFrame, font=('Lexend Deca', 16), background=BOXBG, foreground=FONTFG,bd=0,show='*', exportselection=0, insertbackground='white')
        self.pw.grid(row=5, pady=(0,20))

        Label(self.signupFrame, text='Pin-Code', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG,).grid(row=6, sticky=W, padx=(50))
        Label(self.signupFrame, image=self.entryBox, bg=FRAMEBG).grid(row=7, pady=(0,20))
        self.pw = Entry(self.signupFrame, font=('Lexend Deca', 16), background=BOXBG, foreground=FONTFG,bd=0,show='*', exportselection=0, insertbackground='white')
        self.pw.grid(row=7, pady=(0,20))

        self.checkIcon = PhotoImage(file="asset\\checkbox.png")
        self.checkbox = Button(self.signupFrame, text='Terms and Conditions agreement', font=('Lexend Deca', 10), bg=FRAMEBG, fg=FONTFG, image=self.checkIcon, compound=LEFT, bd=0, activebackground=FRAMEBG, activeforeground=FONTFG, cursor='hand2', command=self.signupTicked)
        self.checkbox.grid(row=8, column=0,sticky=W, padx=(55))

        self.signupBtn = Button(self.signupFrame,text='Sign up',font=('Lexend Deca', 16), image=self.entryBox, background=FRAMEBG, foreground=FONTFG,bd=0,
        compound='center', activebackground=FRAMEBG, activeforeground=FRAMEBG, cursor='hand2')
        self.signupBtn.grid(row=9, pady=31)
        # ? bind click Enter key to login button
        # self.root.bind("<Return>", lambda e: self.checkExist())

        Label(self.signupFrame, text='Already have an account?', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG,).grid(row=10, sticky=W, padx=(40))
        Button(self.signupFrame, text='SIGN IN', font=('Lexend Deca', 16, 'bold'), bg=FRAMEBG, fg=FONTFG, bd=0, activebackground=FRAMEBG, activeforeground=FONTFG, command=self.changeToLogin, cursor='hand2').grid(row=10, sticky=E, padx=(0, 35))
        
        self.signupFrame.pack(expand=1)

    def signupLogo(self):
        global inLogin, inSignup
        if (inSignup == True):
            self.signUpLogo = Image.open('asset\\signup.png')  
            self.signUpLogo = self.signUpLogo.resize((400,400))
            self.signUpLogo = ImageTk.PhotoImage(self.signUpLogo)

            self.signUpBG = Label(self.root, image=self.signUpLogo, bg=FRAMEBG)
            self.signUpBG.place(anchor=E, relx = 0.94, rely = .57)

    def signupTicked(self):
        global is_tickedSignup
        
        self.checkedIcon = PhotoImage(file="asset\\check.png")

        if (is_tickedSignup == False):
            self.checkbox.config(image=self.checkedIcon)
            #* this line is from the help of https://stackoverflow.com/questions/57388865/tkinter-button-doesnt-work-when-i-add-an-image-on-this-button
            self.checkbox.image = self.checkedIcon
            # *----------------------------------------------------------------------------------------------------------------------------------------
            is_tickedSignup = True
        elif (is_tickedSignup == True):
            self.checkbox.config(image=self.checkIcon)
            self.checkbox.image = self.checkIcon
            is_tickedSignup = False

    #* switch frame
    def startSignup(self):
        global inLogin, inSignup
        inSignup = True
        inLogin = False
        self.signupFrame.pack(expand=1)

    def changeToLogin(self):
        self.signupFrame.pack_forget()
        loginPage().startLogin()


def main():
    global root, z
    z = 0
    root = Tk()
    icon = PhotoImage('asset\\icon.ico')
    root.iconbitmap(True, icon)
    root.title("Yato Bank")
    root.geometry('1280x720')

    tittle().titleBar()
    # app.uiLogo()
    loginPage()
    # signupPage()
    root.config(background='#005D85')

    # makes sure everything is up-to-date
    root.update_idletasks() 

    # ? make the window appear in the middle of the screen everytime
    height = root.winfo_height()
    width = root.winfo_width()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # print(width, height)
    x = int((screen_width/2) - (width/2))
    y = int((screen_height/2) - (height/2))

    root.geometry(f"{width}x{height}+{x}+{y}")
    # root.minsize(width, height)

    #*---------------------------- window opacity 
    root.attributes('-alpha',0.80)
    #*-------------------------------------------

    root.mainloop()

#? to prevent duplicate variables
if __name__ == "__main__":
    main()