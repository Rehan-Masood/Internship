# Caesar Cipher

A simple, interactive command-line interface (CLI) Python tool to encrypt (encode) and decrypt (decode) messages using the classic Caesar Cipher algorithm.

# Caesar Cipher
  ![Caesar Cipher.](./Caesar%20Cipher.jpg)

## Features

- **Encryption (Encode):** Shift characters in a message forward by a user-specified key to encrypt.
- **Decryption (Decode):** Shift characters in an encrypted message backward to decrypt.
- **Non-Alphabetic Character Preservation:** Spaces, numbers, and punctuation marks are left unchanged.
- **Continuous Loop:** Run multiple encryption/decryption operations in a single session.
- **ASCII Art Logo:** Sleek, retro command-line header.

## How It Works

The Caesar Cipher is a type of substitution cipher in which each letter in the plaintext is replaced by a letter some fixed number of positions down the alphabet. For example, with a left shift of 3, `D` would be replaced by `A`, `E` would become `B`, and so on.

This script implements:
\[ \text{New Position} = (\text{Current Position} \pm \text{Shift}) \pmod{26} \]

## Prerequisites

- [Python 3.x](https://www.python.org/downloads/) installed on your machine.

## How to Run

1. Clone or download this repository.
2. Open your terminal or command prompt.
3. Navigate to the project directory:
   ```bash
   cd "Caesar Cipher"
   ```
4. Run the script:
   ```bash
   python Caesar_Cipher.py
   ```

## Example Usage

```text
 ,adPPYba, ,adPPYYba,  ,adPPYba, ,adPPYba, ,adPPYYba, 8b,dPPYba,  
a8"     "" ""     `Y8 a8P_____88 I8[    "" ""     `Y8 88P'   "Y8  
8b         ,adPPPPP88 8PP"""""""  `"Y8ba,  ,adPPPPP88 88          
"8a,   ,aa 88,    ,88 "8b,   ,aa aa    ]8I 88,    ,88 88          
 `"Ybbd8"' `"8bbdP"Y8  `"Ybbd8"' `"YbbdP"' `"8bbdP"Y8 88          
             88             88                                 
            88             88                                 

Type 'encode' to encrypt, type 'decode' to decrypt:
encode
Type your message:
hello world!
Type the shift number:
5
Here's the encoded result: mjqqt btwqi!
Type 'yes' if you want to go again. Otherwise type 'no'.
yes
Type 'encode' to encrypt, type 'decode' to decrypt:
decode
Type your message:
mjqqt btwqi!
Type the shift number:
5
Here's the decoded result: hello world!
Type 'yes' if you want to go again. Otherwise type 'no'.
no
Goodbye!
```

## File Structure

- [Caesar_Cipher.py](file:///d:/Future/Internship/Projects/Caesar%20Cipher/Caesar_Cipher.py) - Main application containing the Caesar cipher logic and CLI interface.
