from django.shortcuts import render
from django.http import JsonResponse
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from .lsb import LSB
from .aes import AESCipher
import cv2
import numpy as np
import base64
import tkinter as tk
from PIL import Image, ImageTk

def aeslsb(request):
    if request.method == 'GET':
        return render(request, 'aeslsb.html')

    # POST request handling
    if request.method == 'POST':
        # Your existing Activity class logic here
        activity = Activity()
        activity.startLoop()
        return JsonResponse({'message': 'Process started'})

class Activity:
    def __init__(self):
        self.master = tk.Tk()
        self.image = np.zeros(shape=[100, 100, 3], dtype=np.uint8)
        self.imgPanel = None
        self.keyInput = None
        self.messageInput = None
        self.path = "./dst.png"

    def startLoop(self):
        self.master.title('AES + Steganography')
        self.updateImage()
        openBtn = tk.Button(self.master, text='Open', command=self.openImage)
        openBtn.pack()
        btnFrame = tk.Frame(self.master)
        btnFrame.pack()
        encodeBtn = tk.Button(btnFrame, text='Encode', command=self.encode)
        encodeBtn.pack(side=tk.LEFT)
        decodeBtn = tk.Button(btnFrame, text='Decode', command=self.decode)
        decodeBtn.pack(side=tk.LEFT)
        savebtnFrame = tk.Frame(self.master)
        savebtnFrame.pack()
        saveBtn = tk.Button(savebtnFrame, text='Save Image', command=self.saveImage)
        saveBtn.pack(side=tk.LEFT)
        saveValueBtn = tk.Button(savebtnFrame, text='Save Value', command=self.saveValue)
        saveValueBtn.pack(side=tk.LEFT)
        tk.Label(self.master, text='Key').pack()
        self.keyInput = tk.Entry(self.master)
        self.keyInput.pack()
        tk.Label(self.master, text='Secret Message').pack()
        self.messageInput = tk.Text(self.master, height=10, width=60)
        self.messageInput.pack()
        self.master.mainloop()

    def updateImage(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        if self.imgPanel == None:
            self.imgPanel = tk.Label(image=image)
            self.imgPanel.image = image
            self.imgPanel.pack(side="top", padx=10, pady=10)
        else:
            self.imgPanel.configure(image=image)
            self.imgPanel.image = image

    def cipher(self):
        key = self.keyInput.get()
        if len(key) != 16:
            messagebox.showwarning("Warning", "Key must be 16 characters")
            return

        return AESCipher(self.keyInput.get())

    def encode(self):
        message = self.messageInput.get("1.0", 'end-1c')
        if len(message) % 16 != 0:
            message += (" " * (16 - len(message) % 16))

        cipher = self.cipher()
        if cipher == None:
            return
        cipherText = cipher.encrypt(message)

        obj = LSB(self.image)
        obj.embed(cipherText)
        self.messageInput.delete(1.0, tk.END)
        self.image = obj.image

        self.updateImage()
        messagebox.showinfo("Info", "Encoded")

    def decode(self):
        cipher = self.cipher()
        if cipher == None:
            return

        obj = LSB(self.image)

        cipherText = obj.extract()
        msg = cipher.decrypt(cipherText)

        self.messageInput.delete(1.0, tk.END)
        self.messageInput.insert(tk.INSERT, msg)

    def openImage(self):
        path = askopenfilename()
        if not isinstance(path, str):
            return

        self.image = cv2.imread(path)
        self.updateImage()

    def saveValue(self):
        path = asksaveasfilename(title="Select file")
        if path == '':
            return

        np.savetxt(path + '_blue.csv', self.image[:, :, 0], delimiter=',', fmt='%d')
        np.savetxt(path + '_green.csv', self.image[:, :, 1], delimiter=',', fmt='%d')
        np.savetxt(path + '_red.csv', self.image[:, :, 2], delimiter=',', fmt='%d')

        messagebox.showinfo("Info", "Saved")

    def saveImage(self):
        path = asksaveasfilename(title="Select file", filetypes=[("png files", "*.png")])
        if path == '':
            return

        if ".png" not in path:
            path = path + ".png"

        obj = LSB(self.image)
        obj.save(path)

        messagebox.showinfo("Info", "Saved")
