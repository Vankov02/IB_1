import os
import logic
import tkinter as tk
import subprocess
import sys
from PIL import ImageTk, Image
import tkinter.messagebox as mb


def open_file(file_name):
    try:
        opener = 'notepad' if sys.platform == 'win32' else 'xdg-open'
        subprocess.call([opener, file_name])
    except FileNotFoundError:
        mb.showerror("Ошибка", "Невозможно открыть файл")


def open_text():
    try:
        # Получаем текущую директорию
        current_directory = os.getcwd()
        # Формируем путь к файлу 'source.txt' в текущей директории
        source_path = os.path.join(current_directory, "source.txt")

        # Запускаем программу Notepad для открытия файла source.bin
        subprocess.Popen(["start", "notepad", source_path], shell=True)
    except FileNotFoundError:
        mb.showerror("Ошибка", "Невозможно открыть файл")


def open_cipher():
    try:
        # Получаем текущую директорию
        current_directory = os.getcwd()
        # Формируем путь к файлу 'source.txt' в текущей директории
        source_path = os.path.join(current_directory, "ResultCipher.txt")

        # Запускаем программу Notepad для открытия файла source.bin
        subprocess.Popen(["start", "notepad", source_path], shell=True)

    except FileNotFoundError:
        mb.showerror("Ошибка", "Невозможно открыть файл")


def print_error(code):
    msg = ""
    if code == 1:
        msg = "Проблемы с файлом"
    elif code == 2:
        msg = "Операция невозможна"
    mb.showerror("Ошибка", msg)


def gamming_button(source):
    input = open(source, 'r')
    message = input.read()
    input.close()
    result_cipher, cipher_key = logic.gamming_message(message)

    output = open('ResultGamming.txt', 'w+')
    for part in result_cipher:
        output.write(str(part))
        # output.write(' ')
    output.close()

    output = open('key.txt', 'w+')
    for bit in cipher_key:
        output.write(str(bit))
    output.close()

    opener = 'notepad' if sys.platform == 'win32' else 'xdg-open'
    subprocess.call([opener, 'ResultGamming.txt'])
    subprocess.call([opener, 'key.txt'])


def decipher_gamm_button():
    input = open('key.txt', 'r')
    key = input.read()
    input.close()
    input = open('ResultGamming.txt', 'r')
    cipher_text = input.read()
    input.close()
    message = logic.decipher(cipher_text, key)

    output = open('decipherText.txt', 'w+')
    output.write(message)
    output.close()

    # opener = 'open' if sys.platform == 'drawin' else 'xdg-open'
    # subprocess.call([opener, 'decipherText.txt'])

    opener = 'notepad' if sys.platform == 'win32' else 'xdg-open'
    subprocess.call([opener, 'decipherText.txt'])


def decipher_scram_button():
    input = open('keyScram.txt', 'r')
    key = input.read()
    input.close()
    input = open('ResultScrambler.txt', 'r')
    cipher_text = input.read()
    input.close()
    message = logic.decipher(cipher_text, key)

    output = open('decipherText.txt', 'w+')
    output.write(message)
    output.close()

    opener = 'notepad' if sys.platform == 'win32' else 'xdg-open'
    subprocess.call([opener, 'decipherText.txt'])


def scrambler_button(source):
    input = open(source, 'r')
    message = input.read()
    input.close()
    input = open('polinom.txt', 'r')
    polinom = input.read()
    input.close()
    input = open('startVector.txt', 'r')
    startVector = input.read()
    input.close()
    result_cipher, cipher_key = logic.scrambler(polinom, startVector, message)

    output = open('ResultScrambler.txt', 'w+')
    for part in result_cipher:
        output.write(str(part))
        # output.write(' ')
    output.close()

    output = open('keyScram.txt', 'w+')
    for bit in cipher_key:
        output.write(str(bit))
    output.close()

    opener = 'notepad' if sys.platform == 'win32' else 'xdg-open'
    subprocess.call([opener, 'ResultScrambler.txt'])
    subprocess.call([opener, 'keyScram.txt'])


def alias_decipher():
    input = open('polinom.txt', 'r')
    polinom = input.read()
    input.close()
    input = open('startVector.txt', 'r')
    startVector = input.read()
    input.close()
    real_message = 'Do svyazi!'
    result_cipher, cipher_key = logic.scrambler(polinom, startVector, real_message)
    alias_cipher = []
    part_cipher = []
    for i in range(0, 16):
        alias_cipher.append(result_cipher[i])
    print(alias_cipher)
    alias_message = logic.str2bits('Na')
    print('ABOBA ', cipher_key)
    new_part = logic.xor_bits_str(alias_message, alias_cipher)
    for i in range(0, 16):
        cipher_key[i] = new_part[i]
    print('ABOBA ', cipher_key)
    print(real_message, logic.decipher(result_cipher, cipher_key))


def initialization(source):
    root = tk.Tk()
    root.title("ИБ Лабораторная работа 1")
    img = Image.open('bg9try.jpg')
    width = 500
    ratio = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(ratio)))
    imag = img.resize((width, height), Image.LANCZOS)
    image = ImageTk.PhotoImage(imag)
    tk.Label(root, image=image).pack(side="top", fill="both", expand="no")

    p_entry = tk.Entry(root, bd=5)
    p_entry.pack()
    # , p_entry.get()
    tk.Button(root, text='Открыть файл', command=lambda: open_file(p_entry.get()),
              activebackground='black').place(x=75, y=50)
    tk.Button(root, text='Расшифровать\nгаммирование', command=lambda: decipher_gamm_button(),
              activebackground='black').place(x=75, y=90)
    tk.Button(root, text='Расшифровать\nскремблер', command=lambda: decipher_scram_button(),
              activebackground='black').place(x=280, y=90)
    tk.Button(root, text='Шифровать при\nпомощи скремблера', command=lambda: scrambler_button(source),
              activebackground='black').place(x=270, y=150)
    tk.Button(root, text='Выполнить\nгаммирование', command=lambda: gamming_button(source),
              activebackground='black').place(x=75, y=150)
    tk.Button(root, text='Изменить текст\nдля шифрования', command=open_text,
              activebackground='black').place(x=60, y=220)
    tk.Button(root, text='Посмотреть/Изменить\nзашифрованый текст', command=open_cipher,
              activebackground='black').place(x=255, y=220)
    root.mainloop()


def begin(source):
    initialization(source)
