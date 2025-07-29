import tkinter as tk
import random
import re
import math
import pyperclip
from itertools import cycle
import string

abeceda = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
abecedaADFGVX = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def genAbeceda(moz, jaz):
    znaky = []
    counter = 0
    if moz == 5:
        size = len(abeceda)
        abc = abeceda
    elif moz == 6:
        size = len(abecedaADFGVX)
        abc = abecedaADFGVX
    while counter < size:
        ch = random.choice(abc)
        if ch not in znaky:
            znaky.append(ch)
            counter += 1
    if moz == 5:
        if jaz in ['en', 'cz']:
            znaky.remove('J')

    matrixADF = matrixGen(znaky, moz)
    return matrixADF

def matrixGen(znaky, vyber):
    matica = [[0 for _ in range(vyber)] for _ in range(vyber)]
    k = 0
    for i in range(vyber):
        for j in range(vyber):
            matica[i][j] = znaky[k]
            k += 1
    return matica

def display_matrix(matrix):
    for widget in matrix_frame.winfo_children():
        widget.destroy()

    if mozSelection == 5:
        headers = "ADFGX"
    elif mozSelection == 6:
        headers = "ADFGVX"

    for i, header in enumerate(headers):
        tk.Label(matrix_frame, text=header, font=("Arial", 12, "bold"), relief="ridge",width=3, height=2, bg="lightblue").grid(row=0, column=i+1, sticky="nsew")
        tk.Label(matrix_frame, text=header, font=("Arial", 12, "bold"), relief="ridge",width=4, bg="lightblue").grid(row=i+1, column=0, sticky="nsew")
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            tk.Label(matrix_frame, text=matrix[i][j], font=("Arial", 12), relief="ridge", width=4, height=2).grid(row=i+1, column=j+1, sticky="nsew")

def sanitized_passwd(word):
    letter_count = {}
    result = []

    for letter in word:
        if letter in letter_count:
            letter_count[letter] += 1
            result.append(f"{letter}{letter_count[letter]},")
        else:
            letter_count[letter] = 0
            result.append(f"{letter},")

    if result:
        result[-1] = result[-1].rstrip(',')

    return ''.join(result).upper()

def diacRem(vstupText):
    text = vstupText.upper()
    text = text.replace("Ř", "R").replace("Ě", "E").replace("Š", "S").replace("Ž", "Z").replace("Ý", "Y")
    text = text.replace("Á", "A").replace("Č", "C").replace("Í", "I").replace("É", "E").replace("Ť", "T")
    text = text.replace("Ď", "D").replace("Ň", "N").replace("Ú", "U").replace("Ů", "U").replace(" ", "QAQ")
    text = text.replace("0", "CDAT").replace("1", "BGKL").replace("2", "ASVF").replace("3", "FCYO").replace("4", "TRLC")
    text = text.replace("5", "IPVN").replace("6", "KYIV").replace("7", "IDBP").replace("8", "ZHLS").replace("9", "NCTG")
    text = re.sub('[^A-Za-z0-9]+', '', text)
    return text

def numback(vstupText):
    text = vstupText.upper()
    replacements = {
        "CDAT": "0", "BGKL": "1", "ASVF": "2", "FCYO": "3", "TRLC": "4", "IPVN": "5",
        "KYIV": "6", "IDBP": "7", "ZHLS": "8", "NCTG": "9", "QAQ": " "
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def tableForm(vstupnyText, abeceda, moz, klic, jazyk):
    if moz == 5:
        tabI = 'ADFGX'
    elif moz == 6:
        tabI = 'ADFGVX'
    vstupnyText = diacRem(vstupnyText)
    form = []
    for ch in vstupnyText:
        idx = changeChar(abeceda, ch, moz, jazyk)
        form.append(tabI[idx[0]])
        form.append(tabI[idx[1]])
    form = ''.join(form)
    sizeRad = math.ceil(len(form) / len(klic))
    x = [[form[i * len(klic) + j] if i * len(klic) + j < len(form) else '' for j in range(len(klic))] for i in range(sizeRad)]
    return x

def changeChar(abeceda, ch, moz, jaz):
    if moz == 5:
        if ch == 'J' and jaz in ['en', 'cz']:
            ch = 'I'
    for i, row in enumerate(abeceda):
        if ch in row:
            return [i, row.index(ch)]

def sifrace(vstupnyText, abeceda, klic, moz, jazyk):
    tab = tableForm(vstupnyText, abeceda, moz, klic, jazyk)
    x = [y for x in tab for y in x]
    form = ''.join(x).replace('0', '')

    sifra = {}

    for i, char in zip(cycle(klic), form):
        sifra.setdefault(i, '')
        sifra[i] += char
    return ''.join(sifra[key] for key in sorted(sifra.keys()))

def posun(vstupText, klic):
    tab = {}

    for i in klic:
        tab[i] = []
    counter = 0

    for i in cycle(klic):
        tab[i].append('')
        counter += 1
        if counter == len(vstupText):
            break
    for i in sorted(tab.keys()):
        tab[i] = list(vstupText[:len(tab[i])])
        vstupText = vstupText[len(tab[i]):]
    return tab

def desifrace(vstupText, abeceda, klic, moz):
    global table
    pos = posun(vstupText, klic)
    x = ''
    cnt = 0
    for i in cycle(klic):
        x += pos[i][0]
        del pos[i][0]
        cnt += 1
        if cnt == len(vstupText):
            break
    desif = ''
    if moz == 5:
        table = 'ADFGX'
    if moz == 6:
        table = 'ADFGVX'
    for i in range(0, len(x), 2):
        row = table.index(x[i])
        column = table.index(x[i + 1])
        desif += abeceda[row][column]

    finalText = numback(desif)

    return finalText

def print_selectionJazyk():
    global jazyk
    jazyk = 'cz' if var.get() == 1 else 'en'

def print_selectionMatice():
    global mozSelection
    mozSelection = 5 if varMatice.get() == 1 else 6
    
global matica
matica = None 

def make_sifraceion():
    key = key_entry.get()
    text = input_text.get("1.0", 'end-1c')
    
    global matica
    if matica is None:
        matica = genAbeceda(mozSelection, jazyk)
        display_matrix(matica)

    sanitized_word = sanitized_passwd(key)
    output_labelL.config(text=sanitized_word)

    alphabet = abeceda if mozSelection == 5 else abecedaADFGVX
    output_labelAlphaB.config(text=alphabet)
    sifraceik = sifrace(text, matica, key, mozSelection, jazyk)

    output_text.delete('1.0', "end")
    output_text.insert('1.0', sifraceik)

def make_decryption():
    key = key_entry.get()
    text = input_text.get("1.0", 'end-1c')

    decryptik = desifrace(text, matica, key, mozSelection)

    output_text.delete('1.0', "end")
    output_text.insert('1.0', decryptik)

def copy_result(result):
    pyperclip.copy(result)

def update_matrix_action():
    global matica
    matica = genAbeceda(mozSelection, jazyk)
    display_matrix(matica)
    
root = tk.Tk()
root.title("ADFG(V)X")

keysector = tk.Frame(root)
matrix_frame = tk.Frame(root)
update_frame = tk.Frame(root)

keysector.grid(row=0, column=1, padx=10, pady=30, sticky="nsew")
matrix_frame.grid(row=0, column=2, padx=10)
update_frame.grid(row=1, column=2, padx=10)

input_label = tk.Label(keysector, text="Vloz text k sifraci/desifraci:")
input_label.pack()
input_text = tk.Text(keysector, height=3, width=40)
input_text.pack()

key_label = tk.Label(keysector, text="Heslo:")
key_label.pack()
key_entry = tk.Entry(keysector)
key_entry.pack()

output_labelos = tk.Label(keysector, text="Vyber jazyk:")
output_labelos.pack()

var = tk.IntVar()
R1 = tk.Radiobutton(keysector, text="CZ", variable=var, value=1, command=print_selectionJazyk)
R1.pack()
R2 = tk.Radiobutton(keysector, text="EN", variable=var, value=2, command=print_selectionJazyk)
R2.pack()

output_labelos = tk.Label(keysector, text="Vyber velikost matice:")
output_labelos.pack()

varMatice = tk.IntVar()
R1 = tk.Radiobutton(keysector, text="5x5", variable=varMatice, value=1, command=print_selectionMatice)
R1.pack()
R2 = tk.Radiobutton(keysector, text="6x6", variable=varMatice, value=2, command=print_selectionMatice)
R2.pack()

sifrace_button = tk.Button(keysector, text="Zasifrovat", command=make_sifraceion)
sifrace_button.pack()

desifrace_button = tk.Button(keysector, text="Desifrovat", command=make_decryption)
desifrace_button.pack()

output_label = tk.Label(keysector, text="Upravene heslo:")
output_label.pack()
output_labelL = tk.Label(keysector, text="", font=("Arial", 12))
output_labelL.pack(padx=10, pady=10)

output_label = tk.Label(keysector, text="Alphabet:")
output_label.pack()
output_labelAlphaB = tk.Label(keysector, text="", font=("Arial", 12))
output_labelAlphaB.pack(padx=10, pady=10)

output_label = tk.Label(keysector, text="Vysledek:")
output_label.pack()
output_text = tk.Text(keysector, height=3, width=40)
output_text.pack()

copy_button = tk.Button(keysector, text="Kopirovat vysledek", command=lambda: copy_result(output_text.get("1.0", "end-1c")))
copy_button.pack()

update_matrix = tk.Button(keysector, text="Aktualizace Matice", command=update_matrix_action)
update_matrix.pack(pady=5)

def generate_random_matrix():
    alphabet = list(string.ascii_uppercase.replace('J', ''))
    random.shuffle(alphabet)
    
    matrix = [alphabet[i:i+5] for i in range(0, 25, 5)]
    return matrix

def display_matrixx():
    matrix = generate_random_matrix()

    column_headers = ['A', 'D', 'F', 'G', 'X']
    for i, header in enumerate(column_headers):
        tk.Label(matrix_frame, text=header, font=("Arial", 12, "bold"), relief="ridge", width=3, height=2, bg="lightblue").grid(row=0, column=i+1, sticky="nsew")

    row_headers = ['A', 'D', 'F', 'G', 'X']
    for i, header in enumerate(row_headers):
        tk.Label(matrix_frame, text=header, font=("Arial", 12, "bold"), relief="ridge", width=4, bg="lightblue").grid(row=i+1, column=0, sticky="nsew")

    for i in range(5):
        for j in range(5):
            label = tk.Label(matrix_frame, text=matrix[i][j], font=("Arial", 12), width=4, height=2, relief="ridge", anchor="center")
            label.grid(row=i+1, column=j+1, sticky="nsew")

    for i in range(6):
        matrix_frame.grid_columnconfigure(i, weight=1)
        matrix_frame.grid_rowconfigure(i, weight=1)

display_matrixx()

root.mainloop()

