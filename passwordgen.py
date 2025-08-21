import random

def let_sel():
    let = "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
    letter = random.choice(let)
    return letter

def num_sel():
    num = "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
    number = random.choice(num)
    return number

def sym_sel():
    sym = ("!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", "|", "\\", ";", ":", "'", '"', "<", ">", ",", ".", "/", "?")
    symbol = random.choice(sym)
    return symbol

def main():

    while True:
        print("Welcome to the password generator!")
        print("Please select the type of password you would like to generate:")
        print("1. Password with letters, numbers, and symbols")
        print("2. Password with letters and numbers")
        print("3. Password with only letters")
        print("4. Password with only numbers")
        print("5. Password with only symbols")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            try:
                length = int(input("How long does your password need to be? "))
                check_three = input("Can there be more than 3 of the same type of character in a row? (Yes or No): ").lower()
                
                password = ""
                while len(password) < length:
                    char_type = random.randint(1, 3)
                    new_char = ""
                    if char_type == 1:
                        new_char = str(let_sel())
                    elif char_type == 2:
                        new_char = str(num_sel())
                    else:
                        new_char = str(sym_sel())
                    
                    if check_three == 'no' and len(password) >= 2:
                        if new_char != password[-1] or new_char != password[-2]:
                            password += new_char
                    else:
                        password += new_char
                
                print("Your password is:", password[:length])
                
            except ValueError:
                print("Please enter a valid number for length")

        elif choice == '2':
            try:
                length = int(input("How long does your password need to be? "))
                check_three = input("Can there be more than 3 of the same type of character in a row? (Yes or No): ").lower()
                
                password = ""
                while len(password) < length:
                    char_type = random.randint(1, 3)
                    new_char = ""
                    if char_type == 1:
                        new_char = str(let_sel())
                    elif char_type == 2:
                        new_char = str(num_sel())
                    
                    if check_three == 'no' and len(password) >= 2:
                        if new_char != password[-1] or new_char != password[-2]:
                            password += new_char
                    else:
                        password += new_char
                
                print("Your password is:", password[:length])
                
            except ValueError:
                print("Please enter a valid number for length")
                
        elif choice == '3':
            try:
                password = ""
                length = int(input("How long does your password need to be?"))
                for i in range(length):
                    password += str(let_sel())
                print("Your password is:", password)
            
            except ValueError:
                print("Please enter a valid number for length")

        elif choice == '4':
            try:
                password = ""
                length = int(input("How long does your password need to be?"))
                for i in range(length):
                    password += str(num_sel())
                print("Your password is:", password)

            except ValueError:
                print("Please enter a valid number for length")

        elif choice == '5':
            try:
                password = ""
                length = int(input("How long does your password need to be?"))
                for i in range(length):
                    password += str(sym_sel())
                print("Your password is:", password)

            except ValueError:
                print("Please enter a valid number for length")

        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
