#####################################################################################
#                                                                                   #
#           +++CIBiSt - Computerized Image Binary Stenography+++                    #
#                                                                                   #
#   by bastART                                                                      #
#   2015        Python 2.7.10                                                       #
#   Facebook Page:      https://www.facebook.com/bastartcottbus                     #
#   YouTube Channel:    https://www.youtube.com/channel/UChBq4swt76NsV_BdXUgltBg    #
#                                                                                   #
#   You are allowed to copy, share, derivate and use (commercial and                #
#   non-commercial) the software and source code under the condition                #
#   that you give me credits!                                                       #
#                                                                                   #
#   Thank you and have fun =)                                                       #
#                     Fight For Your Digital Rights!                                #
#                                                                                   #
#####################################################################################

#imports
import Tkinter
import PIL
from Tkinter import *
import ttk
import tkMessageBox
from PIL import ImageTk, Image, ImageChops
import operator
from operator import xor
import os
import binascii
import random
from random import randint
import math
import rsa


main=Tkinter.Tk()           #start
main.wm_title("CIBiSt")            #window title



#display image class
class display(Frame): #http://tinyurl.com/ndwqmdo

    def __init__(self, parent,img):
        Frame.__init__(self, parent)
        self.parent = parent
        self._init_ui(img)


    def _init_ui(self,img):
        img_w=int(ent_img_w.get())/2
        img_h=int(ent_img_h.get())/2
        # Load an image
        img=img.resize((img_w, img_h), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img)
        #Define a canvas in a frame
        frame = Frame(self)
        c = Canvas(frame, bg='#2980B9', height=355, width=635, scrollregion=(0,0,img_w,img_h))
        # Display the image in the canvas
        c.create_image(0, 0, image=self.img, anchor=NW)
        # Y-scrollbar
        yscrollbar = Scrollbar(frame, command=c.yview)
        c.config(yscrollcommand=yscrollbar.set)
        # X-scrollbar
        xscrollbar = Scrollbar(frame, orient=HORIZONTAL, command=c.xview)
        c.config(xscrollcommand=xscrollbar.set)
        # Display widgets using grid layout.
        frame.grid(row=0, column=0)
        yscrollbar.grid(row=0, column=2, sticky=S+N)
        xscrollbar.grid(row=2, column=0, sticky=W+E)
        c.grid(row=0, column=0)
        self.pack(fill=BOTH, expand=1)
        self.place(x=900, y=200)



def add_black_sqr(pixels,a,b,c):          #adding black square=1Bit high
    s=a             #start point x
    t=b             #start point y
    c1=0            #line counter
    c2=0            #row counter
    pix_siz=c

    while c1<(pix_siz):
        while c2<(pix_siz):
            pixels[s,t] = (0, 0, 0)             #pixel color black
            s=s+1           #next pixel in row
            c2=c2+1             #counter c2 up
        t=t+1           #next line
        s=a             #reset row start point
        c1=c1+1             #counter c1 up
        c2=0            #reset row counter

####
####
####algorithm for encrypting a message
def encryption():

    if (ent_img_w.get()==""):          #when no image width input
        tkMessageBox.showerror("Error: 66-B", "Error: 66-B: \nPlease enter an image width!")           #error if msg longer than 162 chars
        return None           #stop exec
    if (ent_img_h.get()==""):          #when no image height input
        tkMessageBox.showerror("Error: 67-C", "Error: 67-C: \nPlease enter an image height!")           #error if msg longer than 162 chars
        return None           #stop exec
    if (ent_msg.get()==""):          #when message input
        tkMessageBox.showerror("Error: 68-D", "Error: 68-D: \nPlease enter your message!")           #error if msg longer than 162 chars
        return None           #stop exec
    if (ent_out_path.get()==""):          #when no output path input
        tkMessageBox.showerror("Error: 69-E", "Error: 69-E: \nPlease enter the path for your image!")           #error if msg longer than 162 chars
        return None           #stop exec

    img_w=int(ent_img_w.get())
    img_h=int(ent_img_h.get())

    img_enc_msg = Image.new("RGB", (img_w, img_h), "#ffffff")             #new white image
    pixels=img_enc_msg.load()           #load pixel map

    or_msg=ent_msg.get()            #extract message from entry box
    or_msg=or_msg.replace(" ","X")              #replace space with X

    PubKey=rsa.PublicKey

    if (var_rsaE.get()==1):
        if (ent_PubK_path.get()==""):          #when no public key path
            tkMessageBox.showerror("Error: 72-H", "Error: 72-H: \nPlease enter a path to the RSA Public Key or disable the RSA option!")           #error if PubK path empty
            return None           #stop exec
        if (os.path.isfile(ent_PubK_path.get())==False):          #when public key file not exists
            tkMessageBox.showerror("Error: 73-I", "Error: 73-I: \nThis RSA Public Key file doesn't exist!")           #error if PubK path empty
            return None           #stop exec

        PubK_path=ent_PubK_path.get()
        f=open(PubK_path, 'r')
        keydata=f.read()
        PubKey=PubKey.load_pkcs1(keydata)
        f.close()
        or_msg=rsa.encrypt(or_msg, PubKey)

    bin_msg=bin(int(binascii.hexlify(or_msg),16))           #convert the message into binary
    bin_msg=bin_msg.replace("b","")                     #remove the 'b'
    cx=0            #counter x
    cy=0            #counter y
    cz=0            #iteration counter
    cc=0            #digit counter
    rand=''
    res=img_w*img_h

    if (var_auto.get()== 0):
        if (pix_siz.get()==""):          #when no bit size input
            tkMessageBox.showerror("Error: 65-A", "Error: 65-A: \nPlease enter the size of a bit!")           #error if msg longer than 162 chars
            return None           #stop exec
        ps=int(pix_siz.get())
    else:
        pix_siz.insert(INSERT, "")
        ps=int(math.sqrt((img_w*img_h)/(int(len(bin_msg))+32)))
        pix_siz.insert(INSERT, "")
        pix_siz.insert(INSERT, str(ps))

    ps_sqr=ps*ps
    bits=res/ps_sqr

    if (int(len(str(bin_msg)))>bits):          #when too many bits
        tkMessageBox.showerror("Error: 70-F", "Error: 70-F: \nPlease enter a message with "+str(bits/8)+" characters ("+str(bits)+" Bits) max!")           #error if msg longer than 162 chars
        return None           #stop exec


    if (int(len(str(bin_msg)))<=bits):          #when not all bits used: generate random bits
        length=int(len(str(bin_msg)))           #length of the message
        while (length<bits):            #if length not max
            rand=rand+str(randint(0,1))             #generate random bits with the length of the remaining free bits
            length=length+1             #counter up/remaining free bits down
    bin_msg=bin_msg+rand            #join the message with the random bits

    while (cz<int(len(str(bin_msg)))):          #when iteration under number of digits

        if (bin_msg[cc]=='1'):          #when value of a bit is 1
            add_black_sqr(pixels,cx,cy,ps)          #add 40x40 black square=1Bit high
        cx=cx+ps            #next image bit
        cc=cc+1             #next digit
        cz=cz+1             #next iteration
        if (cx>(img_w-ps)):           #when last image bit is reached/end of line
            cy=cy+ps            #next line
            cx=0            #reset x/jump to beginning of line
        if (cy>(img_h-ps)):
            break

    if (ent_out_path.get()!=''):
        img_enc_msg.save(ent_out_path.get())

    display(main,img_enc_msg)          #display image using class UI


####
####
#### algorithm for decrypting the message from the message image
def decryption():

    if (ent_img_w.get()==""):          #when no image width input
        tkMessageBox.showerror("Error: 66-B", "Error: 66-B: \nPlease enter an image width!")           #error if msg longer than 162 chars
        return None           #stop exec
    if (ent_img_h.get()==""):          #when no image height input
        tkMessageBox.showerror("Error: 67-C", "Error: 67-C: \nPlease enter an image height!")           #error if msg longer than 162 chars
        return None           #stop exec
    if (ent_path.get()==""):          #when no output path input
        tkMessageBox.showerror("Error: 69-E", "Error: 69-E: \nPlease enter the path for your image!")           #error if msg longer than 162 chars
        return None           #stop exec
    if (pix_siz.get()==""):          #when no bit size input
        tkMessageBox.showerror("Error: 65-A", "Error: 65-A: \nPlease enter the size of a bit!")           #error if msg longer than 162 chars
        return None           #stop exec
    if (os.path.isfile(ent_path.get())==False):
        tkMessageBox.showerror("Error: 71-G", "Error: 71-G: \nThis file doesn't exist!")           #error if msg longer than 162 chars
        return None           #stop exec
    list_out.delete(0, END)
    txt_msg.delete('1.0', END)

    img_w=int(ent_img_w.get())
    img_h=int(ent_img_h.get())
    ps=int(pix_siz.get())

    res=img_w*img_h
    ps_sqr=ps*ps
    bits=res/ps_sqr

#open image
    path=ent_path.get()             #read the path
    img=Image.open(path)            #open image for displaying it

#display image
    display(main,img)           #display image using class UI

#variables
    rgb_img = img.convert('RGB')            #extract rgb values
    x=0             #counter for 1bit/40pixels horizontal for rgb function
    y=0             #counter for lines/vertical for rgb function
    red_value=0             #sum of al values of the red channel of 40px of 1bit
    i1=0            #counter for 40px for condition (somewhat senseless =) because of x)
    i2=0            #counter for horizontal bits
    i3=0            #line counter
    i4=0            #counting 8bits
    z=0             #counter for adressing msg_bin array slots
    j=0             #counter for 8bit characters... merge in one string
    g=0             #list_out line counter
    msg=""          #message in characters without XOR
    or_msg_clr=""           #XOR decrypted message in characters
    msg_bin=[""]            #message in binary without XOR/array for single characters
    or_msg=[""]             #XOR decrypted message in binary

#main reading, converting and decrypting algorithm
    while (i3<img_h/ps):          #vertical
        while (i2<img_w/ps):          #horizontal
            while (i1<ps):          #checking 40pixels=1bit
                r= rgb_img.getpixel((x, y))             #extracting rgb from pixel with position x and y
                red_value=red_value+r[0]            #adding the red value of current pixel to the red value sum
                x=x+1           #counter x up
                i1=i1+1             #counter i1 up
            i2=i2+1             #counter i2 up
            i1=0            #reset counter i1
            if (red_value>0):           #1bit not black
                msg_bin[z]=msg_bin[z]+"0"           #black=0; to msg_bin slot
            else:
                msg_bin[z]=msg_bin[z]+"1"           #white=1; to msg_bin slot
            i4=i4+1             #counter i4 up
            if (i4==8):             #when 8bit are reached
                i4=0            #reset counter i4
                list_out.insert(END, str(g)+": "+msg_bin[z])            #insert line number g and the (undecrypted) 8bit binary for ascii char into list_out

                g=g+1           #counter g up
                z=z+1           #counter z up
                msg_bin.extend([""])            #new slot for msg_bin
            red_value=0             #reset the red value sum
        i2=0            #reset counter i2
        y=y+ps          #move on to the next vertical line for rgb extraction
        x=0             #jump to beginning of line
        i3=i3+1             #counter i3 up
    list_out.insert(END,"END")          #END as separator in case of reruns or similar


#message in characters into text box
    while (j<(len(msg_bin))-1):             #162 maximum numbers of characters
        msg=msg+(chr(int(msg_bin[j], 2)))           #convert binary into ascii character and merge it into msg
        j=j+1           #counter j up

    if (var_rsaD.get()==1):
        if (ent_PriK_path.get()==""):          #when no public key path
            tkMessageBox.showerror("Error: 72-H", "Error: 72-H: \nPlease enter a path to the RSA Public Key or disable the RSA option!")           #error if PubK path empty
            return None           #stop exec
        if (os.path.isfile(ent_PriK_path.get())==False):          #when public key file not exists
            tkMessageBox.showerror("Error: 73-I", "Error: 73-I: \nThis RSA Public Key file doesn't exist!")           #error if PubK path empty
            return None           #stop exec
        PriKey=rsa.PrivateKey
        PriK_path=ent_PriK_path.get()
        f=open(PriK_path, 'r')
        keydata=f.read()
        PriKey=PriKey.load_pkcs1(keydata)
        f.close()
        print(msg)
        print(rsa.decrypt(msg,PriKey))

    txt_msg.insert(END, msg.replace("X"," "))           #replace X with space and enter msg into text box

####
####
#### algorithm for generating rsa keys
def KeyGen():
    if (ent_key_len.get()==""):          #when no key length
        tkMessageBox.showerror("Error: 74-J", "Error: 74-J: \nPlease enter the Length of the RSA Key!")           #error if key length empty
        return None           #stop exec
    if (ent_key_num.get()==""):          #when no key number
        tkMessageBox.showerror("Error: 75-K", "Error: 75-K: \nPlease enter the number of keys which should be generated!")           #error if key number empty
        return None           #stop exec
    if (ent_path_PubK.get()==""):          #when no key path for public key
        tkMessageBox.showerror("Error: 76-L", "Error: 76-L: \nPlease enter a path for the Public Key!")           #error if public key path empty
        return None           #stop exec
    if (ent_path_PriK.get()==""):          #when no key path for private key
        tkMessageBox.showerror("Error: 77-M", "Error: 77-M: \nPlease enter a path for the Private Key!")           #error if private key path empty
        return None           #stop exec

    key_len=int(ent_key_len.get())
    key_num=int(ent_key_num.get())
    path_PubK=ent_path_PubK.get()
    path_PriK=ent_path_PriK.get()
    p=0

    while(p<key_num):
        p=p+1
        (PubK, PriK)=rsa.newkeys(key_len)
        f = open(path_PriK + '_PrivateKey_' + str(p) + '.pem','w')
        f.write(rsa.PrivateKey.save_pkcs1(PriK,'PEM'))
        f.close()
        f = open(path_PubK +  '_PublicKey_' + str(p) + '.pem','w')
        f.write(rsa.PublicKey.save_pkcs1(PubK,'PEM'))
        f.close()



#GUI show and hide algorithms

def show_hide():            #show hide widgets depending on program mode
    if (var_rbtn.get()==2):             #when decrypt mode
        btn_dec_start.place(x=1400,y=800)           #show widgets/start button
        ent_path.place(x=200,y=400)             #entry path for image
        lab_path.place(x=50,y=400)          #label path for image
        list_out.place(x=600,y=400)          #list_out
        txt_msg.place(x=900,y=600)          #text box
        check_rsaD.place(x=200,y=250)            #RSA checkbox
        pix_siz.place(x=500, y=250)
        lab_bit_siz.place(x=400,y=250)
        ent_img_w.place(x=200, y=300)
        ent_img_h.place(x=200, y=330)
        lab_img_w.place(x=50,y=300)
        lab_img_h.place(x=50,y=330)
        if (var_rsaD.get()==1):
            ent_PriK_path.place(x=200,y=550)             #entry box for PubK path
            lab_PriK_path.place(x=50,y=550)          #label PubK path

        else:
            ent_PriK_path.place_forget()
            lab_PriK_path.place_forget()

    else:
        btn_dec_start.place_forget()            #hide widgets
        ent_path.place_forget()
        lab_path.place_forget()
        list_out.place_forget()
        txt_msg.place_forget()
        check_rsaD.place_forget()
        ent_PriK_path.place_forget()
        lab_PriK_path.place_forget()

    if (var_rbtn.get()==1):
        btn_enc_start.place(x=1400,y=800)           #show widgets/start button
        ent_msg.place(x=200,y=400)             #entry box for message
        lab_msg.place(x=50,y=400)          #label message entry
        ent_out_path.place(x=200,y=450)             #entry box for output path
        lab_out_path.place(x=50,y=450)          #label output path
        check_rsaE.place(x=200,y=250)            #rsa checkbox
        pix_siz.place(x=500, y=250)
        lab_bit_siz.place(x=400,y=250)
        ent_img_w.place(x=200, y=300)
        ent_img_h.place(x=200, y=330)
        lab_img_w.place(x=50,y=300)
        lab_img_h.place(x=50,y=330)
        check_auto.place(x=475,y=275)
        if (var_rsaE.get()==1):
            ent_PubK_path.place(x=200,y=550)             #entry box for PubK path
            lab_PubK_path.place(x=50,y=550)          #label PubK path

        else:
            ent_PubK_path.place_forget()
            lab_PubK_path.place_forget()


    else:
        btn_enc_start.place_forget()
        ent_msg.place_forget()
        lab_msg.place_forget()
        ent_out_path.place_forget()
        lab_out_path.place_forget()
        check_auto.place_forget()
        ent_PubK_path.place_forget()
        lab_PubK_path.place_forget()
        check_rsaE.place_forget()

    if (var_rbtn.get()==3):
        pix_siz.place_forget()
        lab_bit_siz.place_forget()
        ent_img_w.place_forget()
        ent_img_h.place_forget()
        lab_img_w.place_forget()
        lab_img_h.place_forget()

        lab_key_len.place(x=30,y=250)
        ent_key_len.place(x=200,y=250)
        lab_key_num.place(x=30,y=280)
        ent_key_num.place(x=200,y=280)
        lab_path_PubK.place(x=30,y=340)
        ent_path_PubK.place(x=200,y=340)
        lab_PubK.place(x=460,y=340)
        lab_path_PriK.place(x=30,y=370)
        ent_path_PriK.place(x=200,y=370)
        lab_PriK.place(x=460,y=370)
        btn_keygen.place(x=460,y=430)

    else:
        lab_key_len.place_forget()
        ent_key_len.place_forget()
        lab_key_num.place_forget()
        ent_key_num.place_forget()
        lab_path_PubK.place_forget()
        ent_path_PubK.place_forget()
        lab_PubK.place_forget()
        lab_path_PriK.place_forget()
        ent_path_PriK.place_forget()
        lab_PriK.place_forget()
        btn_keygen.place_forget()



###############
###GUI elements MAIN
main.geometry('1600x900+50+50')           #window size and position
main.resizable(width=False, height=False)
lab_title_1=Label(main,text="CIBiSt",font="Arial 30 bold")             #title 1: CIXBiSt
lab_title_1.place(x=700,y=10)
lab_title_2=Label(main,text="Computerized Image Binary Steganography",font="Arial 15")            #title 2: Computerized Image XOR Binary Stenography
lab_title_2.place(x=550,y=60)
lab_mode=Label(main,text="Choose your Mode:")           #label modes
lab_mode.place(x=50,y=150)

img_ffydr=Image.open('digital_rights.png')           #fight for your digital rights path
img_ffydr=img_ffydr.resize((125, 105), Image.ANTIALIAS)          #resizing

var_rsaE= IntVar()           #variable for RSA checkbox
check_rsaE = ttk.Checkbutton(main, text="RSA", variable=var_rsaE,command=show_hide)           #RSA checkbox
lab_PubK_path=Label(main,text="Public Key Path (.pem):")
ent_PubK_path = Entry(main,width=60)

var_rsaD= IntVar()           #variable for RSA checkbox
check_rsaD = ttk.Checkbutton(main, text="RSA", variable=var_rsaD,command=show_hide)           #RSA checkbox
lab_PriK_path=Label(main,text="Private Key Path (.pem):")
ent_PriK_path = Entry(main,width=60)

#encryption mode
btn_enc_start = ttk.Button(main, text="Encrypt", command=encryption, width=10)            #encypher start button
ent_msg = Entry(main,width=60)             #entry box for message
lab_msg=Label(main,text="Message:")             #label for entry message
ent_out_path = Entry(main,width=60)             #entry box for output path
pix_siz = Entry(main,width=10)
lab_out_path=Label(main,text="Path for Message Image:")             #label for output path
lab_bit_siz=Label(main,text="Size of a Bit:")
ent_img_w = Entry(main,width=15)
ent_img_h = Entry(main,width=15)
lab_img_w=Label(main,text="Image Width:")
lab_img_h=Label(main,text="Image Height:")

var_auto = IntVar()
check_auto = ttk.Checkbutton(main, text="Auto Bit Size", variable=var_auto)
check_auto.place_forget()


#decryption mode
btn_dec_start = ttk.Button(main, text="Decrypt", command=decryption, width=10)            #decypher start button
ent_path = Entry(main,width=60)             #entry path for image
lab_path=Label(main,text="Path for Message-Image:")             #label for entry box for image path

list_out = Listbox(main,width=20, height=28)            #list box for binary without XOR
txt_msg=Text(main,height=10,width=80)           #text box for clear message

ent_rsa_key = Entry(main,width=31)          #entry box for XOR key

#rsa key gen mode
lab_key_len=Label(main,text="Key Length (Bytes):")
ent_key_len = Entry(main,width=15)
lab_key_num=Label(main,text="Number of Keys:")
ent_key_num = Entry(main,width=15)
lab_path_PubK=Label(main,text="Public Key Path and Name:")
ent_path_PubK = Entry(main,width=50)
lab_PubK=Label(main,text="_PublicKey_#.pem")
lab_path_PriK=Label(main,text="Private Key Path and Name:")
ent_path_PriK = Entry(main,width=50)
lab_PriK=Label(main,text="_PrivateKey_#.pem")
btn_keygen = Button(main, text="Generate",command=KeyGen, height=1, width=10)


#radiobuttons for program mode
var_rbtn = IntVar()             #variable for rbtn/mode
rbtn_enc=ttk.Radiobutton(main, text="Encrypt Message", variable=var_rbtn, value=1,command=show_hide,width=20)          #encryption mode
rbtn_enc.place(x=200, y=150)
rbtn_dec=ttk.Radiobutton(main, text="Decrypt Message", variable=var_rbtn, value=2,command=show_hide,width=20)          #decryption mode
rbtn_dec.place(x=380,y=150)
rbtn_rsa=ttk.Radiobutton(main, text="RSA Key Generator", variable=var_rbtn, value=3,command=show_hide,width=20)          #rsa keygen mode
rbtn_rsa.place(x=560,y=150)

#colors
bg_col='#2980B9'
ttk.Style().configure('blue.TRadiobutton', background='#2980B9')
ttk.Style().configure('blue.TButton', background='#2980B9')
ttk.Style().configure('blue.TCheckbutton', background='#2980B9')

main.configure(background=bg_col)
lab_title_1.configure(background=bg_col)
lab_title_2.configure(background=bg_col)
lab_path.configure(background=bg_col)
lab_mode.configure(background=bg_col)
lab_msg.configure(background=bg_col)
lab_out_path.configure(background=bg_col)
lab_bit_siz.configure(background=bg_col)
lab_img_w.configure(background=bg_col)
lab_img_h.configure(background=bg_col)
lab_PubK_path.configure(background=bg_col)
lab_PriK_path.configure(background=bg_col)
rbtn_enc.configure(style="blue.TRadiobutton")
rbtn_dec.configure(style="blue.TRadiobutton")
rbtn_rsa.configure(style="blue.TRadiobutton")
btn_enc_start.configure(style="blue.TButton")
btn_dec_start.configure(style="blue.TButton")
check_auto.configure(style="blue.TCheckbutton")
check_rsaE.configure(style="blue.TCheckbutton")
check_rsaD.configure(style="blue.TCheckbutton")

lab_key_len.configure(background=bg_col)
lab_key_num.configure(background=bg_col)
lab_path_PubK.configure(background=bg_col)
lab_path_PriK.configure(background=bg_col)
lab_PubK.configure(background=bg_col)
lab_PriK.configure(background=bg_col)


###
main.mainloop()
