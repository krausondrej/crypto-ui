import tkinter as tk
from tkinter import ttk
import re
import pyperclip

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def preprocess_text(text):
    text = text.upper()
    text = text.replace("Č", "C").replace("Š", "S").replace("Ř", "R").replace("Ú", "U").replace("Ů", "U")
    text = text.replace("Ž", "Z").replace("Ý", "Y").replace("Á", "A").replace("É", "E").replace("Ť", "T")
    text = text.replace("Í", "I").replace("Ň", "N").replace("0", "ZERO").replace("1", "ONE")
    text = text.replace("2", "TWO").replace("3", "THREE").replace("4", "FOUR").replace("5", "FIVE")
    text = text.replace("6", "SIX").replace("7", "SEVEN").replace("8", "EIGHT").replace("9", "NINE")
    text = re.sub(fr'[^A-Z0-9 {text}]', '', text)
    text = text.replace(" ", "XMEZERAX")
    return text.upper()

def postprocess_text(text):
    text = text.replace("XMEZERAX", " ").replace("ZERO", "0").replace("ONE", "1").replace("TWO", "2")
    text = text.replace("THREE", "3").replace("FOUR", "4").replace("FIVE", "5").replace("SIX", "6")
    text = text.replace("SEVEN", "7").replace("EIGHT", "8").replace("NINE", "9")
    return text.upper()

def affine_encrypt(text, key_a, key_b):
    result = ""
    text = preprocess_text(text)
    char_count = 0

    char_mapping = []

    for char in text:
        if char.isalpha():
            encrypted_char = chr(((ord(char) - 65) * key_a + key_b) % 26 + 65)
            result += encrypted_char
            char_mapping.append((char, encrypted_char))

            char_count += 1
            if char_count % 5 == 0:
                result += ' '
        elif char.isdigit():
            result += char
        elif char.isspace():
            result += char
        else:
            result += char

    mapping_str = ""
 
    for i in range(0, len(char_mapping), 3):
        line = " | ".join([f"{original} -> {encrypted}" for original, encrypted in char_mapping[i:i+3]])
        mapping_str += line + "\n"

    mapping_text.delete('1.0', "end")
    mapping_text.insert('1.0', mapping_str)
    
    return result

def affine_decrypt(ciphertext, key_a, key_b):
    result = ""
    a_inverse = mod_inverse(key_a, 26)
    print(a_inverse)
    if a_inverse is not None:
        ciphertext = preprocess_text(ciphertext)
        char_count = 0

        char_mapping = []

        for char in ciphertext:
            if char.isalpha():
                decrypted_char = chr(((ord(char) - 65 - key_b) * a_inverse) % 26 + 65)
                result += decrypted_char
                char_mapping.append((char, decrypted_char))

                char_count += 1
                if char_count % 6 == 0:
                    char_count += 1

            elif char.isdigit():
                result += char
            elif char.isspace():
                result += char
            else:
                result += char

        mapping_str = ""
        for i in range(0, len(char_mapping), 3):
            line = " | ".join([f"{encrypted} -> {decrypted}" for encrypted, decrypted in char_mapping[i:i+3]])
            mapping_str += line + "\n"

        mapping_text.delete('1.0', "end")
        mapping_text.insert('1.0', mapping_str)

        return postprocess_text(result)
    else:
        return "The provided key is not valid."

encrypted_result = ""
decrypted_result = ""

def encrypt_text():
    global encrypted_result
    key_a_str = key_a_entry.get()
    key_b_str = key_b_entry.get()
    plaintext = plaintext_entry.get()

    if key_a_str.isdigit() and key_b_str.isdigit():
        key_a = int(key_a_str)
        key_b = int(key_b_str)
        encrypted_text = affine_encrypt(plaintext, key_a, key_b)
        encrypted_result = encrypted_text

        encrypted_text_display.delete('1.0',"end")
        encrypted_text_display.insert('1.0',formatted_encrypted_text(encrypted_text))
    else:
        encrypted_text_display.delete('1.0',"end")
        encrypted_text_display.insert('1.0',"Invalid keys (a and b must be integers).")

def decrypt_text():
    global decrypted_result
    key_a_str = key_a_entry.get()
    key_b_str = key_b_entry.get()
    ciphertext = ciphertext_entry.get()
    ciphertext = ciphertext.replace(" ", "")

    if key_a_str.isdigit() and key_b_str.isdigit():
        key_a = int(key_a_str)
        key_b = int(key_b_str)
        decrypted_text = affine_decrypt(ciphertext, key_a, key_b)
        decrypted_result = decrypted_text
        decrypted_text_display.delete('1.0', "end")
        decrypted_text_display.insert('1.0',decrypted_text)
    else:
        decrypted_text_display.insert('1.0',"Invalid keys (a and b must be integers).")

def formatted_encrypted_text(text):
    text = text.replace(" ", "")
    return " ".join([text[i:i+5] for i in range(0, len(text), 5)])

def copy_encrypted_text():
    global encrypted_result
    if encrypted_result:
        encrypted_text_without_gaps = ''.join(encrypted_result.split())
        pyperclip.copy(encrypted_text_without_gaps)

def copy_decrypted_text():
    global decrypted_result
    if decrypted_result:
        pyperclip.copy(decrypted_result)

app = tk.Tk()
app.title("Afinní šifra")
app.resizable(False, False)

nadpis = tk.Label(app, text="Afinní šifra", font=("Helvetica", 16))
nadpis.pack(pady=20)

# Main frame
center_frame = ttk.Frame(app)
center_frame.pack(fill=None, expand=False, padx=10, pady=5)

bottom_frame = ttk.Frame(app)
bottom_frame.pack(fill=None, expand=False, padx=10, pady=5)

# Input frame for keys
key_input_frame = ttk.LabelFrame(center_frame, padding=10, text="Hodnoty")
key_input_frame.pack(padx=10, pady=10)

key_a_label = ttk.Label(key_input_frame, text="Key A:")
key_a_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
key_a_entry = ttk.Entry(key_input_frame)
key_a_entry.grid(row=0, column=1, padx=5, pady=5)

key_b_label = ttk.Label(key_input_frame, text="Key B:")
key_b_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
key_b_entry = ttk.Entry(key_input_frame)
key_b_entry.grid(row=1, column=1, padx=5, pady=5)

encryption_frame = ttk.LabelFrame(center_frame, text="Šifrování", padding=10)
encryption_frame.pack(side="left", fill=None, expand=False)

plaintext_label = ttk.Label(encryption_frame, text="Text k šifrování:")
plaintext_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
plaintext_entry = ttk.Entry(encryption_frame, width=40)
plaintext_entry.grid(row=0, column=1, padx=5, pady=5)

encrypted_text_label = ttk.Label(encryption_frame, text="Zašifrovaný text:")
encrypted_text_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
encrypted_text_display = tk.Text(encryption_frame, height=5, width=52)
encrypted_text_display.grid(row=1, column=1, padx=5, pady=5, sticky="w")

encrypt_button = ttk.Button(encryption_frame, text="Zašifrovat", command=encrypt_text)
encrypt_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

copy_encrypted_button = ttk.Button(encryption_frame, text="Kopírovat zašifrovaný text", command=copy_encrypted_text)
copy_encrypted_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

decryption_frame = ttk.LabelFrame(center_frame, text="Dešifrování", padding=10)
decryption_frame.pack(side="right", fill=None, expand=False)

ciphertext_label = ttk.Label(decryption_frame, text="Text k dešifrování:")
ciphertext_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
ciphertext_entry = ttk.Entry(decryption_frame, width=40)
ciphertext_entry.grid(row=0, column=1, padx=5, pady=5)

decrypted_text_label = ttk.Label(decryption_frame, text="Dešifrovaný text:")
decrypted_text_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
decrypted_text_display = tk.Text(decryption_frame, height=5, width=52)
decrypted_text_display.grid(row=1, column=1, padx=5, pady=5)

decrypt_button = ttk.Button(decryption_frame, text="Dešifrovat", command=decrypt_text)
decrypt_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

copy_decrypted_button = ttk.Button(decryption_frame, text="Kopírovat dešifrovaný text", command=copy_decrypted_text)
copy_decrypted_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Mapping frame
mapping_frame = ttk.LabelFrame(bottom_frame, text="Zdrojová Abeceda", padding=10)
mapping_frame.pack(pady=10)

mapping_text = tk.Text(mapping_frame, width=40, height=10, wrap="none")
mapping_text.grid(row=0, column=0, padx=5, pady=5)

scrollbar = ttk.Scrollbar(mapping_frame, orient="vertical", command=mapping_text.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

mapping_text.config(yscrollcommand=scrollbar.set)


app.mainloop()
