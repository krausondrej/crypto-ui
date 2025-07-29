import tkinter as tk
from unidecode import unidecode
import pyperclip
import re

def loc_index(c):
    loc = list()
    if var.get() == 1:
        if c == 'J':
            c = 'I'
    elif var.get() == 2:
        if c == 'W':
            c = 'V'
    for i, j in enumerate(my_matrix):
        for k, l in enumerate(j):
            if c == l:
                loc.append(i)
                loc.append(k)
                return loc

def encrypt_normalize_text(text):
    text = text.upper()
    text = unidecode(text)

    number_to_word = {
        "1": "ONE",
        "2": "TWO",
        "3": "THREE",
        "4": "FOUR",
        "5": "FIVE",
        "6": "SIX",
        "7": "SEVEN",
        "8": "EIGHT",
        "9": "NINE",
    }

    for number, word in number_to_word.items():
        text = text.replace(number, word)

    if len(text) % 2 != 0:
        if text[-1] == 'X':
            text += 'Q'
        else:
            text += 'X'

    text = text.replace(" ", "QMEZERAS")
    text = re.sub(r'[^A-Z0-9]', '', text)
    return text


def decrypt_normalize_text(text):
    text = text.upper()
    text = unidecode(text)
    return text.replace(" ", "")


def create_matrix():
    global my_matrix, alphabet, key

    key = key_entry.get()
    key = key.replace(" ", "")
    key = key.upper()

    number_to_word = {
        "1": "ONE",
        "2": "TWO",
        "3": "THREE",
        "4": "FOUR",
        "5": "FIVE",
        "6": "SIX",
        "7": "SEVEN",
        "8": "EIGHT",
        "9": "NINE"
    }
    for number, word in number_to_word.items():
        key = key.replace(number, word)
    key = unidecode(key)
    key = re.sub(r'[^A-Z0-9]', '', key)

    result = []
    
    for c in key:
        if c not in result:
            if var.get() == 1:
                if c == 'J':
                    result.append('I')
                else:
                    result.append(c)
            elif var.get() == 2:
                if c == 'W':
                    result.append('V')
                else:
                    result.append(c)
 
    if var.get() == 1:
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    elif var.get() == 2:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVXYZ"

    for letter in alphabet:
        if letter not in result:
            result.append(letter)

    result = list(dict.fromkeys(result))

    k = 0
    my_matrix = [[0 for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            my_matrix[i][j] = result[k]
            k += 1

    for i in range(5):
        for j in range(5):
            cell = tk.Label(matrix_frame, text=my_matrix[i][j], borderwidth=1, relief="solid", width=5, height=2)
            if i == 0:
                cell.config(bg="blue", fg="white")
            cell.grid(row=i, column=j, sticky="nsew")
            if j == 0:
                cell.config(bg="blue", fg="white")

    for i in range(5):
        matrix_frame.grid_rowconfigure(i, weight=1)
        matrix_frame.grid_columnconfigure(i, weight=1)

def copy_result(result):
    pyperclip.copy(result)

def encrypt():
    global resultencrypt

    create_matrix()
    msg = entry.get()
    msg = encrypt_normalize_text(msg)
    i = 0
    filtered_text = ""

    for s in range(0, len(msg) + 1, 2):
        if s < len(msg) - 1:
            if msg[s] == msg[s + 1]:
                msg = msg[:s + 1] + 'X' + msg[s + 1:]

    if len(msg) % 2 != 0:
        msg = msg[:] + 'X'

    result = ""
    while i < len(msg):
        loc = list()
        loc = loc_index(msg[i])
        loc1 = list()
        loc1 = loc_index(msg[i + 1])
        if loc[1] == loc1[1]:
            result += "{}{}".format(my_matrix[(loc[0] + 1) % 5][loc[1]], my_matrix[(loc1[0] + 1) % 5][loc1[1]])
        elif loc[0] == loc1[0]:
            result += "{}{}".format(my_matrix[loc[0]][(loc[1] + 1) % 5], my_matrix[loc1[0]][(loc1[1] + 1) % 5])
        else:
            result += "{}{}".format(my_matrix[loc[0]][loc1[1]], my_matrix[loc1[0]][loc[1]])
        i = i + 2
        filtered_text += msg[i - 2:i] + ' '

    resultencrypt = ' '.join([result[i:i + 5] for i in range(0, len(result), 5)])

    output_label.delete('1.0', "end")
    output_label.insert('1.0', resultencrypt)

    output_labelFiltered.delete('1.0', "end")
    output_labelFiltered.insert('1.0', filtered_text)

def decrypt():
    global resultdecrypt

    create_matrix()
    msg = entry.get()
    msg = decrypt_normalize_text(msg)
    result = ""
    i = 0

    while i < len(msg):
        loc = list()
        loc = loc_index(msg[i])
        loc1 = list()
        loc1 = loc_index(msg[i + 1])
        if msg[i] == msg[i + 1] and msg[i] == 'X':
            result += 'X'
        else:
            if loc[1] == loc1[1]:
                result += "{}{}".format(my_matrix[(loc[0] - 1) % 5][loc[1]], my_matrix[(loc1[0] - 1) % 5][loc1[1]])
            elif loc[0] == loc1[0]:
                result += "{}{}".format(my_matrix[loc[0]][(loc[1] - 1) % 5], my_matrix[loc1[0]][(loc1[1] - 1) % 5])
            else:
                result += "{}{}".format(my_matrix[loc[0]][loc1[1]], my_matrix[loc1[0]][loc[1]])

        i = i + 2

    replacement_dict = {
        "QMEZERAS": " ",
        "ONE": "1",
        "TVO": "2",
        "THREXE": "3",
        "FOUR": "4",
        "FIVE": "5",
        "SIX": "6",
        "SEVEN": "7",
        "EIGHT": "8",
        "NINE": "9",
        "THREE": "3"
    }

    for key, value in replacement_dict.items():
        result = result.replace(key, value)

    result = result.rstrip('X')
    result = result.rstrip('Q')

    outputdecrypt_label.delete('1.0', "end")
    outputdecrypt_label.insert('1.0', result)

    outputdecrypt_labelMsg.delete('1.0', "end")
    outputdecrypt_labelMsg.insert('1.0', msg)

app = tk.Tk()
app.title("Playfair Cipher")

matrix_visible = False

encryption_frame = tk.Frame(app)
matrix_frame = tk.Frame(app)
decryption_frame = tk.Frame(app)
keysector = tk.Frame(app)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

keysector.grid(row=0, column=1, padx=10, pady=30, sticky="nsew")
encryption_frame.grid(row=1, column=0, padx=10, pady=30, sticky="nsew")
matrix_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
decryption_frame.grid(row=1, column=2, padx=10, pady=30, sticky="nsew")

key_label = tk.Label(keysector, text="Enter key:")
key_label.pack()

key_entry = tk.Entry(keysector)
key_entry.pack()

label = tk.Label(keysector, text="Enter message/cipher:")
label.pack()

entry = tk.Entry(keysector, width=50)
entry.pack()

var = tk.IntVar()
R1 = tk.Radiobutton(keysector, text="CZ", variable=var, value=1, command=create_matrix)
R1.pack(side="left", padx=(10, 5), pady=5)

R2 = tk.Radiobutton(keysector, text="EN", variable=var, value=2, command=create_matrix)
R2.pack(side="right")

encrypt_button = tk.Button(encryption_frame, text="Encrypt", command=encrypt)
encrypt_button.pack(pady=10)

copy_button = tk.Button(encryption_frame, text="Copy Encrypt", command=lambda: copy_result(resultencrypt))
copy_button.pack()

output_label = tk.Text(encryption_frame, height=3, width=40)
output_label.pack(pady=10)

label = tk.Label(encryption_frame, text="Filtrovana cifra:")
label.pack()

output_labelFiltered = tk.Text(encryption_frame, height=3, width=40)
output_labelFiltered.pack(pady=10)

decrypt_button = tk.Button(decryption_frame, text="Decrypt", command=decrypt)
decrypt_button.pack(pady=10)

copy_button = tk.Button(decryption_frame, text="Copy Decrypt", command=lambda: copy_result(resultdecrypt))
copy_button.pack()

outputdecrypt_label = tk.Text(decryption_frame, height=3, width=40)
outputdecrypt_label.pack(pady=10)

label = tk.Label(decryption_frame, text="Filtrovana decifra:")
label.pack()

outputdecrypt_labelMsg = tk.Text(decryption_frame, height=3, width=40)
outputdecrypt_labelMsg.pack(pady=10)

app.mainloop()
