import sys

MORSE_CODE_DICT = {
    'A': '.-',     'B': '-...',   'C': '-.-.',   'D': '-..',    'E': '.',
    'F': '..-.',   'G': '--.',    'H': '....',   'I': '..',     'J': '.---',
    'K': '-.-',    'L': '.-..',   'M': '--',     'N': '-.',     'O': '---',
    'P': '.--.',   'Q': '--.-',   'R': '.-.',    'S': '...',    'T': '-',
    'U': '..-',    'V': '...-',   'W': '.--',    'X': '-..-',   'Y': '-.--',
    'Z': '--..',   '0': '-----',  '1': '.----',  '2': '..---',  '3': '...--',
    '4': '....-',  '5': '.....',  '6': '-....',  '7': '--...',  '8': '---..',
    '9': '----.',  '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
    '!': '-.-.--', '/': '-..-.',  '(': '-.--.',  ')': '-.--.-', '&': '.-...',
    ':': '---...', ';': '-.-.-.', '=': '-...-',  '+': '.-.-.',  '-': '-....-',
    '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
}

def text_to_morse(text: str) -> str:
    morse_output = []
    
    words = text.upper().split(' ')
    
    for word in words:
        word_morse = []
        for char in word:
            if char in MORSE_CODE_DICT:
                word_morse.append(MORSE_CODE_DICT[char])
            else:
                word_morse.append('[?]')
        morse_output.append(' '.join(word_morse))
        
    return ' / '.join(morse_output)

def print_banner():
    print("=" * 60)
    print("      📡 PYTHON TEXT TO MORSE CODE CONVERTER 📡      ")
    print("=" * 60)

def main():
    print_banner()
    print("Type your message to convert it to Morse Code.")
    print("Type 'exit' or 'q' at any time to quit.\n")

    while True:
        user_input = input("Enter text: ").strip()

        if not user_input:
            print("⚠️ Please enter a non-empty string.\n")
            continue

        if user_input.lower() in ['exit', 'q', 'quit']:
            print("\nThank you for using Morse Code Converter. Goodbye! 👋")
            sys.exit()

        converted_code = text_to_morse(user_input)
        
        print("\n" + "-" * 60)
        print("RESULT (Morse Code):")
        print(converted_code)
        print("-" * 60 + "\n")

if __name__ == '__main__':
    main()