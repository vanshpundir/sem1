
import speech_recognition as sr
import pyttsx3
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfile
import socket
import base64

def server():
    global var
    global host
    global port

# take the server name and port name
    host = 'local host'
    port = 5000

    # socket at client side
    # using TCP / IP protocol
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)

#number of local comp
    s.connect(('127.0.0.1', port))


    msg = s.recv(1024)
    var = s.recv(1024)

    while msg:
        a=msg.decode()
        var=var.decode()
        text1.insert(1.0,a)
        break
    s.close()

r = sr.Recognizer()


def send():
    global host
    global port

    host = 'local host'
    port = 5000

    #socket at server side
    # using TCP / IP protocol
    s = socket.socket(socket.AF_INET,
               socket.SOCK_STREAM)

    # bind the socket with server
    # and port number
    s.bind(('', port))

    # allow maximum 1 connection to
    # the socket
    s.listen(1)

    # wait till a client accept
    # connection
    c, addr = s.accept()


    msg = text1.get(1.0,END)
    c.send(msg.encode())
    c.send(var.encode())
    c.close()


def decrypt():
    global var2
    var2 = code.get()

    global message
    if var == var2:
        screen2 = Toplevel(screen)
        screen2.title("decryption")
        screen2.geometry("600x600")
        screen2.configure(bg="#00bd56")

        message = text1.get(1.0, END)

        decode_message = message.encode("utf-8")
        base64_bytes = base64.b64decode(decode_message)
        decrypt = base64_bytes.decode("utf-8")

        Label(screen2, text="DECRYPT", font="arial", fg="white", bg="#00bd56").place(x=10, y=0)
        text2 = Text(screen2, font="Rpbote 16", bg="white", relief=GROOVE, wrap=WORD, bd=0)
        text2.place(x=10, y=40, width=580, height=550)

        text2.insert(END, str(decrypt))
    elif var2 != var:
        messagebox.showerror("encryption", "Invalid Password")


def encrypt():

    var2 = code.get()

    global var
    global encode_message
    global encrypt
    var = code.get()
    if var2 == var:
        screen1 = Toplevel(screen)
        screen1.title("encryption")
        screen1.geometry("600x600")
        screen1.configure(bg="#ed3833")

        message = text1.get(1.0, END)
        encode_message = message.encode("utf-8")
        base64_bytes = base64.b64encode(encode_message)
        encrypt = base64_bytes.decode("utf-8")

        Label(screen1, text="ENCRYPT", font="arial", fg="white", bg="#ed3833").place(x=10, y=0)
        text2 = Text(screen1, font="Rpbote 16", bg="white", relief=GROOVE, wrap=WORD, bd=0)
        text2.place(x=10, y=40, width=580, height=550)

        text2.insert(END, str(encrypt))
    elif var2 != var:
        messagebox.showerror("encryption", "Invalid Password")

def speechtotext():
    while (1):
        global MyText

        try:
            with sr.Microphone() as source2:
# wait to set the surrounding ambient noise
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                text1.insert(END, MyText)

                break

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error")


def open_file():
    file = askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
    if file is not None:
        content = file.read()
        text1.insert(END, content)


def file():
    files = [('All Files', '*.*'),
             ('Python Files', '*.py'),
             ('Text Document', '*.txt')]
    file = asksaveasfile(filetypes=files, defaultextension=files)
    filename = file.name

    a = text1.get("1.0", END)
    f = open(filename, 'w')
    f.write(a)
    f.close()


def main_screen():
    global screen
    global code
    global text1
    global textContent

    screen = Tk()
    screen.geometry("800x600")

    # icon
    imageicon = PhotoImage(file="D:\\bla.png")
    screen.iconphoto(False, imageicon)



    def reset():
        code.set("")
        text1.delete(1.0, END)

    screen.title("Encryptor Decryptor")
    img = Image.open("D:\\blaa.png")
    tkimage = ImageTk.PhotoImage(img)
    label = Label(screen, image=tkimage).pack()

    img = Image.open("D:\\save.png")
    image_icon = ImageTk.PhotoImage(img)

    mic = Image.open("D:\\mic.png")
    mic = mic.resize((100,100),Image.ANTIALIAS)
    mic_icon = ImageTk.PhotoImage(mic)

    textContent = StringVar()
    Label(text="Enter text", fg="black", font=("calbiri", 13), bg="#bbbdbc").place(x=10, y=10)
    text1 = Text(font="Robote 20", bg="White", relief=GROOVE, wrap=WORD, bd=3)
    text1.place(x=10, y=50, width=650, height=200)

    Label(text="Enter a password", fg="black", bg="#bbbdbc", font=("calbiri", 13)).place(x=10, y=270)
    code = StringVar()
    Entry(textvariable=code, width=19, bd=3, font=("arial", 25), show="*").place(x=10, y=310, width=650)

    Button(text="ENCRYPT", height='3', width=40, bg="green", fg="white", bd=3, command=encrypt).place(x=30, y=400)
    Button(text="DECRYPT", height='3', width=40, bg="red", fg="white", bd=3, command=decrypt).place(x=340, y=400)
    Button(text="RESET", height='3', width=40, bg="blue", fg="white", bd=3, command=reset).place(x=30, y=470)
    Button(text="FILE", height='3', width=40, bg="grey", fg="white", bd=3, command=open_file).place(x=340, y=470)
    Button(text="SAVE", height='20', width=20, bd=3, image=image_icon, command=file).place(x=630, y=12)
    Button(text="mic", height='80', width=80, bg="grey", fg="white", bd=3,image=mic_icon, command=speechtotext).place(x=690, y=60)
    Button(text="SEND", height='3', width=40, bg="purple", fg="white",command=send, bd=3).place(x=30, y=540)
    Button(text="RECEIVE", height='3', width=40, bg="brown",command=server, fg="white", bd=3).place(x=340, y=540)

    screen.mainloop()


main_screen()


