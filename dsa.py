import os
import hashlib
import base64
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
import random
import math
from datetime import datetime
from unidecode import unidecode

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_large_prime():
    while True:
        num = random.randint(10 ** 12, 10 ** 13)
        if is_prime(num):
            return num

def generate_key_pair():
    p = generate_large_prime()
    q = generate_large_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    d = pow(e, -1, phi)
    return (e, n), (d, n)

def encrypt_message(message, key):
    e, n = key
    X = 8
    block_size = 56
    
    normalized_text = unidecode(message)

    blocks = [normalized_text[i:i + X] for i in range(0, len(normalized_text), X)]
    
    decimal_values = [[ord(char) for char in block] for block in blocks]

    binary_values = ''.join(format(value, '08b') for block in decimal_values for value in block)

    binary_blocks = [binary_values[i:i + block_size] for i in range(0, len(binary_values), block_size)]

    decimal_blocks = [int(block, 2) for block in binary_blocks]

    encrypted_message = [pow(block, e, n) for block in decimal_blocks]
    print(encrypted_message)
    
    return encrypted_message


def decrypt_message(encrypted_message, key):
    d, n = key
    X = 8
    block_size = 56

    decrypted_blocks = [pow(block, d, n) for block in encrypted_message]

    binary_blocks = [format(block, f'0{block_size}b') for block in decrypted_blocks]

    binary_string = ''.join(binary_blocks)

    binary_chars = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]

    characters = [chr(int(b, 2)) for b in binary_chars if b.strip('0')]

    decrypted_message = ''.join(characters)

    return decrypted_message

def hash_file(filepath):
    sha3_512 = hashlib.sha3_512()
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            sha3_512.update(chunk)
    return sha3_512.hexdigest()

def save_keys_to_files(public_key, private_key):
    with open("public_key.pub", "w") as pub_file:
        pub_file.write(f"RSA {base64.b64encode(str(public_key).encode()).decode()}")
    with open("private_key.priv", "w") as priv_file:
        priv_file.write(f"RSA {base64.b64encode(str(private_key).encode()).decode()}")

def sign_file(filepath, private_key):
    file_hash = hash_file(filepath)

    encrypted_hash = encrypt_message(file_hash, private_key)
    signature = f"RSA_SHA3-512 {base64.b64encode(str(encrypted_hash).encode()).decode()}"

    with open(filepath + ".sign", "w") as sign_file:
        sign_file.write(signature)
    return signature

def verify_signature(filepath, signature_file, public_key):
    with open(signature_file, "r") as sf:
        signature = sf.read().split(' ', 1)[1]
    
    decrypted_signature = decrypt_message(eval(base64.b64decode(signature).decode()), public_key)


    file_hash = hash_file(filepath)

    return file_hash == decrypted_signature

def export_signed_file(filepath, signature_file):
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    suggested_name = f"{base_name}_signed.zip"

    export_path = filedialog.asksaveasfilename(
        initialfile=suggested_name,
        defaultextension=".zip",
        filetypes=[("ZIP files", "*.zip")]
    )

    if export_path:
        try:
            with zipfile.ZipFile(export_path, 'w') as zipf:
                zipf.write(filepath, os.path.basename(filepath))
                zipf.write(signature_file, os.path.basename(signature_file))
            messagebox.showinfo("Export", "Soubor a podpis byly úspěšně exportovány do ZIP.")
        except Exception as e:
            messagebox.showerror("Chyba", f"Při exportu došlo k chybě: {e}")

def add_public_key_to_zip(zip_path, public_key):
    with zipfile.ZipFile(zip_path, 'a') as zipf:
        with zipf.open("public_key.pub", 'w') as pub_key_file:
            pub_key_file.write(base64.b64encode(str(public_key).encode()))

def generate_keys():
    public_key, private_key = generate_key_pair()
    save_keys_to_files(public_key, private_key)
    messagebox.showinfo("Generování klíčů", "Klíčový pár byl úspěšně vygenerován a uložen.")

def select_file():
    global selected_file_path
    file_path = filedialog.askopenfilename(title="Vyberte soubor", filetypes=[("Všechny soubory", "*.*")])
    if file_path:
        selected_file_path = file_path
        file_info = {
            "Název": os.path.basename(file_path),
            "Cesta": file_path,
            "Velikost": f"{os.path.getsize(file_path)} bytes",
            "Datum úpravy": f"{datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d-%m-%Y %H:%M:%S')}"
        }
        file_details.delete('1.0', tk.END)
        for key, value in file_info.items():
            file_details.insert(tk.END, f"{key}: {value}\n")

def sign_selected_file():
    if selected_file_path:
        private_key_path = filedialog.askopenfilename(title="Vyberte soukromý klíč", filetypes=[("Private Key", "*.priv")])
        if private_key_path:
            with open(private_key_path, "r") as pk_file:
                private_key = eval(base64.b64decode(pk_file.read().split(' ', 1)[1]).decode())
            signature = sign_file(selected_file_path, private_key)

            messagebox.showinfo("Podepisování", "Soubor byl úspěšně podepsán.")

            signature_file = selected_file_path + ".sign"
            export_signed_file(selected_file_path, signature_file)

def verify_selected_file():
    if selected_file_path:
        zip_path = filedialog.askopenfilename(title="Vyberte ZIP soubor", filetypes=[("ZIP soubory", "*.zip")])
        if zip_path:
            try:
                with zipfile.ZipFile(zip_path, 'r') as zipf:
                    zip_file_names = zipf.namelist()
                    
                    text_files = [file for file in zip_file_names if file.endswith('.txt')]
                    sign_files = [file for file in zip_file_names if file.endswith('.sign')]

                    if not text_files or not sign_files:
                        messagebox.showerror("Chyba", "Chybí potřebné soubory (textové soubory nebo soubory s podpisem).")
                        return

                    zipf.extract(text_files[0], path="temp/")
                    zipf.extract(sign_files[0], path="temp/")

                public_key_path = filedialog.askopenfilename(title="Vyberte veřejný klíč", filetypes=[("Public Key", "*.pub")])
                if public_key_path:
                    with open(public_key_path, "r") as pub_file:
                        public_key = eval(base64.b64decode(pub_file.read().split(' ', 1)[1]).decode())

                    signature_file_path = f"temp/{sign_files[0]}"
                    is_valid = verify_signature(f"temp/{text_files[0]}", signature_file_path, public_key)

                    if is_valid:
                        messagebox.showinfo("Ověření", "Podpis je platný.")
                    else:
                        messagebox.showerror("Ověření", "Podpis je neplatný.")
            except Exception as e:
                messagebox.showerror("Chyba", f"Při ověřování souboru došlo k chybě: {e}")

#GUI
root = tk.Tk()
root.title("DSA")

selected_file_path = None

frame = tk.Frame(root)
frame.pack(pady=10)

select_button = tk.Button(frame, text="Vybrat soubor", command=select_file)
select_button.pack(side=tk.LEFT, padx=5)

keygen_button = tk.Button(frame, text="Generovat klíče", command=generate_keys)
keygen_button.pack(side=tk.LEFT, padx=5)

sign_button = tk.Button(frame, text="Podepsat soubor", command=sign_selected_file)
sign_button.pack(side=tk.LEFT, padx=5)

verify_button = tk.Button(frame, text="Ověřit podpis", command=verify_selected_file)
verify_button.pack(side=tk.LEFT, padx=5)

file_details = tk.Text(root, width=60, height=15)
file_details.pack(pady=10)

root.mainloop()
