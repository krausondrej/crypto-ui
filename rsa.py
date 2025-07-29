import random
import math
import tkinter as tk
from unidecode import unidecode

app = tk.Tk()
app.title("RSA")

encryption_frame = tk.Frame(app)
matrix_frame = tk.Frame(app)
decryption_frame = tk.Frame(app)
keysectorOne = tk.Frame(app)
keysectorTwo = tk.Frame(app)
keysectorThree = tk.Frame(app)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

keysectorOne.grid(row=1, column=0, padx=10, pady=30, sticky="nsew")
keysectorTwo.grid(row=1, column=1, padx=10, pady=30, sticky="nsew")
keysectorThree.grid(row=1, column=2, padx=10, pady=30, sticky="nsew")
encryption_frame.grid(row=2, column=0, padx=10, pady=30, sticky="nsew")
matrix_frame.grid(row=2, column=1, padx=50, pady=(130, 0), sticky="nsew")
decryption_frame.grid(row=2, column=2, padx=10, pady=30, sticky="nsew")

key_label = tk.Label(matrix_frame, text="p:")
key_label.grid(row=0, column=0, sticky=tk.W)
outputdecrypt_labelMsgP = tk.Text(matrix_frame, height=1, width=22)
outputdecrypt_labelMsgP.grid(row=0, column=1, sticky="nsew", pady=10)

key_label = tk.Label(matrix_frame, text="q:")
key_label.grid(row=1, column=0, sticky=tk.W)
outputdecrypt_labelMsgQ = tk.Text(matrix_frame, height=1, width=22)
outputdecrypt_labelMsgQ.grid(row=1, column=1, sticky="nsew", pady=10)

key_label = tk.Label(matrix_frame, text="e:")
key_label.grid(row=2, column=0, sticky=tk.W)
outputdecrypt_labelMsgE = tk.Text(matrix_frame, height=1, width=22)
outputdecrypt_labelMsgE.grid(row=2, column=1, sticky="nsew", pady=10)

key_label = tk.Label(matrix_frame, text="n:")
key_label.grid(row=3, column=0, sticky=tk.W)
outputdecrypt_labelMsgN = tk.Text(matrix_frame, height=1, width=22)
outputdecrypt_labelMsgN.grid(row=3, column=1, sticky="nsew", pady=10)

key_label = tk.Label(matrix_frame, text="φ(n):")
key_label.grid(row=4, column=0, sticky=tk.W)
outputdecrypt_labelMsgPhi = tk.Text(matrix_frame, height=1, width=22)
outputdecrypt_labelMsgPhi.grid(row=4, column=1, sticky="nsew", pady=10)

key_label = tk.Label(matrix_frame, text="d:")
key_label.grid(row=5, column=0, sticky=tk.W)
outputdecrypt_labelMsgD = tk.Text(matrix_frame, height=1, width=22)
outputdecrypt_labelMsgD.grid(row=5, column=1, sticky="nsew", pady=10)


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
    gcd = math.gcd(e, phi)
    while gcd != 1:
        e = random.randint(2, phi - 1)
        gcd = math.gcd(e, phi)
    d = pow(e, -1, phi)

    outputdecrypt_labelMsgP.delete('1.0', "end")
    outputdecrypt_labelMsgP.insert('1.0', str(p))

    outputdecrypt_labelMsgQ.delete('1.0', "end")
    outputdecrypt_labelMsgQ.insert('1.0', str(q))

    outputdecrypt_labelMsgE.delete('1.0', "end")
    outputdecrypt_labelMsgE.insert('1.0', str(e))

    outputdecrypt_labelMsgN.delete('1.0', "end")
    outputdecrypt_labelMsgN.insert('1.0', str(n))

    outputdecrypt_labelMsgPhi.delete('1.0', "end")
    outputdecrypt_labelMsgPhi.insert('1.0', str(phi))

    outputdecrypt_labelMsgD.delete('1.0', "end")
    outputdecrypt_labelMsgD.insert('1.0', str(d))


key_label = tk.Label(keysectorOne, text="Zašifrovat", font=('Arial', 25, 'bold'))
key_label.pack()

input_text_label = tk.Label(encryption_frame, text="Zadejte text k zašifrování:")
input_text_label.grid(row=0, column=0, sticky=tk.W)

input_text_displayText = tk.Text(encryption_frame, width=60, height=10)
input_text_displayText.grid(row=1, column=0, sticky="nsew", pady=(0, 30))

input_text_label = tk.Label(encryption_frame, text="Číselná reprezentace textu:")
input_text_label.grid(row=2, column=0, sticky=tk.W)

input_text_labelCislo = tk.Text(encryption_frame, width=60, height=10)
input_text_labelCislo.grid(row=3, column=0, sticky="nsew", pady=(0, 30))

input_text_label = tk.Label(encryption_frame, text="Zašifrovaný text:")
input_text_label.grid(row=4, column=0, sticky=tk.W)

input_text_displayFinal = tk.Text(encryption_frame, width=60, height=10)
input_text_displayFinal.grid(row=5, column=0, sticky="nsew", pady=(0, 30))


def encrypt():
    msg = input_text_displayText.get("1.0", "end-1c")
    e = outputdecrypt_labelMsgE.get("1.0", "end-1c")
    n = outputdecrypt_labelMsgN.get("1.0", "end-1c")
    X = 8
    block_size = 56

    normalized_text = unidecode(msg)

    Rozdeleni_Bloku = [normalized_text[i:i + X] for i in range(0, len(normalized_text), X)]
    print("rozdeleni ",Rozdeleni_Bloku)
    Decimalni_hodnoty = [[ord(char) for char in block] for block in Rozdeleni_Bloku]
    print("decimal ",Decimalni_hodnoty)
    Binarni_hodnoty = ''.join(format(value, '08b') for value in [item for sublist in Decimalni_hodnoty for item in sublist])
    print("binar ",Binarni_hodnoty)
    Binary_list = [Binarni_hodnoty[i:i + block_size] for i in range(0, len(Binarni_hodnoty), block_size)]
    print("blist ",Binary_list)
    decimal_values_list = []
    for block in Binary_list:
        decimal_value = int(block, 2)
        print(decimal_value)
        padded_decimal_value = str(decimal_value).zfill(len(str(2 ** block_size)))
        decimal_values_list.append(padded_decimal_value)
    upravenyDecimal_values = ' '.join(map(str, decimal_values_list))
    input_text_labelCislo.delete('1.0', "end")
    input_text_labelCislo.insert('1.0', str(upravenyDecimal_values))
    print(decimal_values_list)
    encrypted_blocks = [pow(int(block), int(e), int(n)) for block in decimal_values_list]

    upravenyEncrypted_blocks = ' '.join(map(str, encrypted_blocks))
    input_text_displayFinal.delete('1.0', "end")
    input_text_displayFinal.insert('1.0', str(upravenyEncrypted_blocks))


encrypt_button = tk.Button(encryption_frame, text="Šifruj", height=2, width=13, command=encrypt)
encrypt_button.grid(row=6, column=0)

key_label = tk.Label(keysectorTwo, text="Generování klíče", font=('Arial', 25, 'bold'))
key_label.pack()

generate_button = tk.Button(matrix_frame, text="Generuj", height=2, width=13, command=generate_key_pair)
generate_button.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=20)

key_label = tk.Label(keysectorThree, text="Dešifrovat", font=('Arial', 25, 'bold'))
key_label.pack()

input_text_label = tk.Label(decryption_frame, text="Zadejte text k dešifrování:")
input_text_label.grid(row=0, column=0, sticky=tk.W)

input_text_displayDesifruj = tk.Text(decryption_frame, width=60, height=10)
input_text_displayDesifruj.grid(row=1, column=0, sticky="nsew", pady=(0, 30))

input_text_label = tk.Label(decryption_frame, text="Číselná reprezentace textu:")
input_text_label.grid(row=2, column=0, sticky=tk.W)

input_text_displayCisloD = tk.Text(decryption_frame, width=60, height=10)
input_text_displayCisloD.grid(row=3, column=0, sticky="nsew", pady=(0, 30))

input_text_label = tk.Label(decryption_frame, text="Dešifrovaný text:")
input_text_label.grid(row=4, column=0, sticky=tk.W)

input_text_displayFinalD = tk.Text(decryption_frame, width=60, height=10)
input_text_displayFinalD.grid(row=5, column=0, sticky="nsew", pady=(0, 30))


def decrypt():
    msg = input_text_displayDesifruj.get("1.0", "end-1c")
    d = outputdecrypt_labelMsgD.get("1.0", "end-1c")
    n = outputdecrypt_labelMsgN.get("1.0", "end-1c")
    X = 8

    number_list = list(map(int, msg.split()))

    decrypted_blocks = [pow(int(block), int(d), int(n)) for block in number_list]
    print('dec ', decrypted_blocks)
    max_digits = max(len(str(num)) for num in decrypted_blocks)

    formatted_numbers = [str(num).zfill(max_digits) for num in decrypted_blocks]

    upravenyFormatted_numbers = ' '.join(map(str, formatted_numbers))
    input_text_displayCisloD.delete('1.0', "end")
    input_text_displayCisloD.insert('1.0', str(upravenyFormatted_numbers))

    binary_numbers = [bin(int(num))[2:] for num in formatted_numbers]

    modified_list = ['0' + item for item in binary_numbers]

    combined_variable = ''.join(modified_list)

    decrypted_text_decimal_values = [int(combined_variable[i:i + X], 2) for i in range(0, len(combined_variable), X)]

    decrypted_text = ''.join([chr(value) for value in decrypted_text_decimal_values])

    input_text_displayFinalD.delete('1.0', "end")
    input_text_displayFinalD.insert('1.0', str(decrypted_text))


decrypt_button = tk.Button(decryption_frame, text="Dešifruj", height=2, width=13, command=decrypt)
decrypt_button.grid(row=6, column=0)

app.mainloop()
