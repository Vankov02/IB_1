import os
import logic
import tkinter as tk
import subprocess
import sys
from PIL import ImageTk, Image
import tkinter.messagebox as mb


# Создание кнопки для открытия файла с указанным именем
def open_file(file_name):
    try:
        opener = 'notepad' if sys.platform == 'win32' else 'xdg-open'
        subprocess.call([opener, file_name])
    except FileNotFoundError:
        mb.showerror("Ошибка", "Невозможно открыть файл")


# изменение текста для шифрования
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


# просмотр и изменение зашифрованного текста
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


# Вывод ошибки
def print_error(code):
    msg = ""
    if code == 1:
        msg = "Проблемы с файлом"
    elif code == 2:
        msg = "Операция невозможна"
    mb.showerror("Ошибка", msg)


# гаммирование текста
def gamming_button(source):
    # Открываем файл для чтения и считываем содержимое
    input = open(source, 'r')
    message = input.read()
    input.close()

    # Шифруем сообщение с помощью функции gamming_message из модуля logic
    result_cipher, cipher_key = logic.gamming_message(message)

    # Записываем зашифрованное сообщение в файл ResultGamming.txt
    output = open('ResultGamming.txt', 'w+')
    for part in result_cipher:
        output.write(str(part))
        # output.write(' ')
    output.close()

    # Записываем ключ шифрования в файл key.txt
    output = open('key.txt', 'w+')
    # проходим по каждому биту в ключе шифрования cipher_key. На каждой итерации бит преобразуем в строку с помощью
    # функции str(), затем записываем в файл key.txt с помощью метода write() объекта output, который представляет
    # открытый файл для записи.
    for bit in cipher_key:
        output.write(str(bit))
    output.close()

    # Определяем команду для открытия текстового редактора в зависимости от операционной системы
    opener = 'notepad' if sys.platform == 'win32' else 'xdg-open'

    # Открываем зашифрованное сообщение и ключ в текстовом редакторе
    subprocess.call([opener, 'ResultGamming.txt'])
    subprocess.call([opener, 'key.txt'])


# расшифровка текста, зашифрованного методом гаммирования
def decipher_gamm_button():
    # Открываем файл с ключом для чтения и считываем его содержимое
    input = open('key.txt', 'r')
    key = input.read()
    input.close()

    # Открываем файл с зашифрованным текстом для чтения и считываем его содержимое
    input = open('ResultGamming.txt', 'r')
    cipher_text = input.read()
    input.close()

    # Расшифровываем зашифрованный текст с помощью функции decipher из модуля logic
    message = logic.decipher(cipher_text, key)

    # Открываем файл для записи расшифрованного текста и записываем в него расшифрованное сообщение
    output = open('decipherText.txt', 'w+')
    output.write(message)
    output.close()

    # Открываем получившийся файл с помощью стандартного текстового редактора в зависимости от операционной системы
    opener = 'notepad' if sys.platform == 'win32' else 'xdg-open'
    subprocess.call([opener, 'decipherText.txt'])


# расшифровка текста, зашифрованного скремблером
def decipher_scram_button():
    # Открываем файл с ключом для чтения и считываем его содержимое
    input = open('keyScram.txt', 'r')
    key = input.read()
    input.close()

    # Открываем файл с зашифрованным текстом для чтения и считываем его содержимое
    input = open('ResultScrambler.txt', 'r')
    cipher_text = input.read()
    input.close()

    # Расшифровываем зашифрованный текст с помощью функции decipher из модуля logic
    message = logic.decipher(cipher_text, key)

    # Открываем файл для записи расшифрованного текста и записываем в него расшифрованное сообщение
    output = open('decipherText.txt', 'w+')
    output.write(message)
    output.close()

    # Открываем получившийся файл с помощью стандартного текстового редактора в зависимости от операционной системы
    opener = 'notepad' if sys.platform == 'win32' else 'xdg-open'
    subprocess.call([opener, 'decipherText.txt'])


# шифрования текста методом скремблера
def scrambler_button(source):
    # Открываем файл с исходным текстом для чтения и считываем его содержимое
    input = open(source, 'r')
    message = input.read()
    input.close()

    # Открываем файл с полиномом для чтения и считываем его содержимое
    input = open('polinom.txt', 'r')
    polinom = input.read()
    input.close()

    # Открываем файл с начальным вектором для чтения и считываем его содержимое
    input = open('startVector.txt', 'r')
    startVector = input.read()
    input.close()

    # Зашифровываем исходный текст с помощью функции scrambler из модуля logic
    result_cipher, cipher_key = logic.scrambler(polinom, startVector, message)

    # Открываем файл для записи зашифрованного текста и записываем в него зашифрованное сообщение
    output = open('ResultScrambler.txt', 'w+')
    for part in result_cipher:
        output.write(str(part))
        # output.write(' ')
    output.close()

    # Открываем файл для записи ключа шифрования и записываем в него ключ
    output = open('keyScram.txt', 'w+')
    for bit in cipher_key:
        output.write(str(bit))
    output.close()

    # Открываем получившиеся файлы с помощью стандартного текстового редактора в зависимости от операционной системы
    opener = 'notepad' if sys.platform == 'win32' else 'xdg-open'
    subprocess.call([opener, 'ResultScrambler.txt'])
    subprocess.call([opener, 'keyScram.txt'])


#  создание псевдосообщения и его дешифровка с использованием алгоритма скремблирования
def alias_decipher():
    # Открываем файл с полиномом для чтения и считываем его содержимое
    input = open('polinom.txt', 'r')
    polinom = input.read()
    input.close()

    # Открываем файл с начальным вектором для чтения и считываем его содержимое
    input = open('startVector.txt', 'r')
    startVector = input.read()
    input.close()

    # Определяем исходное сообщение
    real_message = 'Do svyazi!'

    # Зашифровываем исходное сообщение с помощью функции scrambler из модуля logic
    result_cipher, cipher_key = logic.scrambler(polinom, startVector, real_message)

    # Создаем псевдосообщение для шифрования (в данном случае "Na")
    alias_cipher = []
    part_cipher = []
    for i in range(0, 16):
        alias_cipher.append(result_cipher[i])
    print(alias_cipher)
    alias_message = logic.str2bits('Na')
    print('ABOBA ', cipher_key)

    # Заменяем часть ключа на новую часть, полученную из псевдосообщения
    new_part = logic.xor_bits_str(alias_message, alias_cipher)
    for i in range(0, 16):
        cipher_key[i] = new_part[i]
    print('ABOBA ', cipher_key)

    # Выводим исходное сообщение и дешифрованное сообщение
    print(real_message, logic.decipher(result_cipher, cipher_key))


def initialization(source):
    # Создание главного окна
    root = tk.Tk()
    # Установка заголовка окна
    root.title("ИБ Лабораторная работа 1")
    # Загрузка изображения и его масштабирование
    img = Image.open('bg9try.jpg')
    width = 500
    ratio = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(ratio)))
    imag = img.resize((width, height), Image.LANCZOS)
    image = ImageTk.PhotoImage(imag)
    # Вставка изображения в окно
    tk.Label(root, image=image).pack(side="top", fill="both", expand="no")

    # Создание поля для ввода текста
    p_entry = tk.Entry(root, bd=5)
    p_entry.pack()
    # Создание кнопки для открытия файла с указанным именем
    tk.Button(root, text='Открыть файл', command=lambda: open_file(p_entry.get()),
              activebackground='black').place(x=200, y=50)
    # Создание кнопки для расшифровки текста, зашифрованного методом гаммирования
    tk.Button(root, text='Расшифровать\nгаммирование', command=lambda: decipher_gamm_button(),
              activebackground='black').place(x=75, y=90)
    # Создание кнопки для расшифровки текста, зашифрованного скремблером
    tk.Button(root, text='Расшифровать\nскремблер', command=lambda: decipher_scram_button(),
              activebackground='black').place(x=310, y=90)
    # Создание кнопки для шифрования текста методом скремблера
    tk.Button(root, text='Шифровать при\nпомощи скремблера', command=lambda: scrambler_button(source),
              activebackground='black').place(x=290, y=150)
    # Создание кнопки для выполнения гаммирования текста
    tk.Button(root, text='Выполнить\nгаммирование', command=lambda: gamming_button(source),
              activebackground='black').place(x=75, y=150)
    # Создание кнопки для изменения текста для шифрования
    tk.Button(root, text='Изменить текст\nдля шифрования', command=open_text,
              activebackground='black').place(x=70, y=220)
    # Создание кнопки для просмотра и изменения зашифрованного текста
    tk.Button(root, text='Посмотреть/Изменить\nзашифрованый текст', command=open_cipher,
              activebackground='black').place(x=290, y=220)
    # Запуск главного цикла обработки событий
    root.mainloop()


def begin(source):
    initialization(source)
