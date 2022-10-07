from email.mime import image
from tkinter import *
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
        root.geometry('1280x720')
        print("fullscreen")
    elif is_fullScreen == False:
        # root.geometry(f"{screenWidth}x{screenHeight}")
        # root.geometry("%dx%d" % (screenWidth, screenHeight))
        root.state('zoomed')
        print("minimized")

def ticked():
    global is_ticked

    checkedIcon = PhotoImage(file="asset\\check.png")

    if (is_ticked == False):
        checkbox.config(image=checkedIcon)
        #* this line is from the help of https://stackoverflow.com/questions/57388865/tkinter-button-doesnt-work-when-i-add-an-image-on-this-button
        checkbox.image = checkedIcon
        # *----------------------------------------------------------------------------------------------------------------------------------------
        is_ticked = True
    elif (is_ticked == True):
        checkbox.config(image=checkIcon)
        checkbox.image = checkIcon
        is_ticked = False

def main():
    global root, z
    z = 0
    root = Tk()
    root.geometry('1280x720')
    root.title("Yato Bank")

    # ? create my own titlebar
    root.overrideredirect(True)
    root.after(10, lambda: set_appwindow(root))
    titlebar = Frame(root, background=FRAMEBG, bd=0)

    #*----------------------------------------------------------------------------------------------------------------------------------------
    # ? these functions copy from https://stackoverflow.com/questions/63217105/tkinter-overridedirect-minimizing-and-windows-task-bar-issues
    titlebar.bind('<Button-1>', SaveLastClickPos)
    titlebar.bind('<B1-Motion>', Dragging)
    titlebar.bind("<Map>", frameMapped) # This brings back the window
    #*----------------------------------------------------------------------------------------------------------------------------------------

    Label(titlebar, text='Yato Bank', font=('Lexend', 16), bg=FRAMEBG, fg=FONTFG).pack(side=LEFT, pady=10, padx=10)

    # ? Open image using pil (for resize purpose)
    closeIcon = Image.open("asset\\close.png")
    closeIcon = closeIcon.resize((24, 24))
    closeIcon = ImageTk.PhotoImage(closeIcon)
    close = Button(titlebar, image=closeIcon, command=root.destroy, background=FRAMEBG, bd=0, activebackground=FRAMEBG).pack(side=RIGHT, pady=10, padx=10)


    maximizeIcon = Image.open("asset\\maximize.png")
    maximizeIcon = maximizeIcon.resize((24, 24))
    maximizeIcon = ImageTk.PhotoImage(maximizeIcon)
    maximize = Button(titlebar, image=maximizeIcon, command=fullScreen, background=FRAMEBG, bd=0, activebackground=FRAMEBG).pack(side=RIGHT, pady=10, padx=10)

    minimizeIcon = Image.open("asset\\minus.png")
    minimizeIcon = minimizeIcon.resize((24, 24))
    minimizeIcon = ImageTk.PhotoImage(minimizeIcon)
    minimize = Button(titlebar, image=minimizeIcon, command=minimizeGUI, background=FRAMEBG, bd=0, activebackground=FRAMEBG).pack(side=RIGHT, pady=10, padx=10)

    # ? create frame of the form
    form = Frame(root, background=FRAMEBG)
    entryBox = PhotoImage(file='asset\entrybox.png')
    Label(form, text='Sign in', font=('Lexend', 64), bg=FRAMEBG, fg=FONTFG).grid(row=0)
    Label(form, text='sign in to start managing your bank account', font=('Lexend Deca', 16), bg=FRAMEBG, fg=FONTFG).grid(row=1)

    Label(form, image=entryBox, bg=FRAMEBG).grid(row=2)
    username = Entry(form, font=('Lexend Deca', 16), background=BOXBG, foreground=FONTFG,bd=0, insertbackground='white')
    # entryPreview(username, "Username")
    username.grid(row=2, pady=31)

    Label(form, image=entryBox, bg=FRAMEBG).grid(row=3)
    pw = Entry(form, font=('Lexend Deca', 16), background=BOXBG, foreground=FONTFG,bd=0,show='*', exportselection=0, insertbackground='white')
    pw.grid(row=3, pady=31)


    global checkbox, checkIcon
    checkIcon = PhotoImage(file="asset\\checkbox.png")
    checkbox = Button(form, text='remember me', font=('Lexend Deca', 10), bg=FRAMEBG, fg=FONTFG, image=checkIcon, compound=LEFT, bd=0, activebackground=FRAMEBG, activeforeground=FONTFG, command=ticked)
    checkbox.grid(row=4, column=0,sticky=W, padx=(55))

    Button(form, text='forgot password?', font=('Lexend Deca', 10), bg=FRAMEBG, fg=FONTFG, bd=0, activebackground=FRAMEBG, activeforeground=FONTFG).grid(row=4, column=0, sticky=E, padx=(0, 50))

    Button(form,text='Login',font=('Lexend Deca', 16), image=entryBox, background=FRAMEBG, foreground=FONTFG,bd=0,
    compound='center', activebackground=FRAMEBG, activeforeground=FRAMEBG).grid(row=5, pady=31)

    # make the frame in the middle
    titlebar.pack(expand=0, fill=BOTH)
    form.pack(expand=1)
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