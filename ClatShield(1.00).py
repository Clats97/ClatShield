import secrets
import string
import math

def get_bool_input(prompt: str, default: bool = False) -> bool:
    """
    Prompt the user for a yes/no answer; return True/False accordingly.
    If input is invalid, return the default.
    """
    answer = input(prompt).strip().lower()
    if answer in ["y", "yes"]:
        return True
    elif answer in ["n", "no"]:
        return False
    else:
        return default

def calculate_entropy(password: str) -> float:
    """
    Calculate the Shannon entropy of the given password in bits.
    """
    if not password:
        return 0.0
    length = len(password)
    freq = {}
    for char in password:
        freq[char] = freq.get(char, 0) + 1
    entropy = 0.0
    for char, count in freq.items():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy

def calculate_search_space_size(length: int, all_chars: str) -> int:
    """
    Calculate the total possible search space for a password
    of given length using the provided character set.
    """
    if not all_chars or length <= 0:
        return 0
    return len(all_chars) ** length

def generate_random_password(
    length: int,
    use_lower: bool = True,
    use_upper: bool = True,
    use_digits: bool = True,
    use_special: bool = True,
    require_each: bool = False
) -> str:
    """
    Generate a random password using cryptographically secure methods.
    Ensures no two consecutive characters are identical.
    """
    if length < 1:
        raise ValueError("Password length must be at least 1.")

    pools = []
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_special:
        pools.append("!@#$%^&*()-_=+[]{}|;:,.<>?/\\")
    
    if not pools:
        raise ValueError("No character types selected. At least one type must be chosen.")

    if require_each and length < len(pools):
        raise ValueError(
            f"Password length ({length}) is too short to include at least one "
            f"char from each of the {len(pools)} selected categories."
        )

    all_chars = "".join(pools)

    password_chars = []
    if require_each:
        for pool in pools:
            password_chars.append(secrets.choice(pool))

    while len(password_chars) < length:
        new_char = secrets.choice(all_chars)
        if not password_chars or new_char != password_chars[-1]:
            password_chars.append(new_char)

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)

def main():
    print("\033[1;31m██████╗    ██╗          █████╗     ████████╗    ███████╗    ██╗  ██╗    ██╗    ███████╗    ██╗         ██████╗")
    print("██╔════╝    ██║         ██╔══██╗    ╚══██╔══╝    ██╔════╝    ██║  ██║    ██║    ██╔════╝    ██║         ██╔══██╗")
    print("██║         ██║         ███████║       ██║       ███████╗    ███████║    ██║    █████╗      ██║         ██║  ██║")
    print("██║         ██║         ██╔══██║       ██║       ╚════██║    ██╔══██║    ██║    ██╔══╝      ██║         ██║  ██║")
    print("╚██████╗    ███████╗    ██║  ██║       ██║       ███████║    ██║  ██║    ██║    ███████╗    ███████╗    ██████╔╝")
    print(" ╚═════╝    ╚══════╝    ╚═╝  ╚═╝       ╚═╝       ╚══════╝    ╚═╝  ╚═╝    ╚═╝    ╚══════╝    ╚══════╝    ╚═════╝\033[0m")
    print("\033[1;34mC   L   A   T   S   H   I   E   L   D       P   A   S   S   W   O   R   D      T   O   O   L\033[0m   \033[1;31m(Version 1.00)\033[0m")
    author = "🛡️ By Joshua M Clatney (Clats97) - Ethical Pentesting Enthusiast 🛡️"
    print(author + "\n[Password Generator]\nDigital Defense, One Password At A Time\n")

    while True:
        try:
            length = int(input("Enter the password length (12-16 characters minimum is recommended): "))
        except ValueError:
            print("Invalid length. Using a default value of 12.")
            length = 12

        include_lower = get_bool_input("Include lowercase letters (a-z)? (y/n): ", default=True)
        include_upper = get_bool_input("Include uppercase letters (A-Z)? (y/n): ", default=True)
        include_digits = get_bool_input("Include numbers (0-9)? (y/n): ", default=True)
        include_special = get_bool_input("Include special characters? (y/n): ", default=True)
        require_each = get_bool_input("Require at least one of each chosen category? (y/n): ", default=False)

        try:
            password = generate_random_password(
                length=length,
                use_lower=include_lower,
                use_upper=include_upper,
                use_digits=include_digits,
                use_special=include_special,
                require_each=require_each
            )
            print("\nGenerated Password:", password)

            all_chars = ""
            if include_lower:
                all_chars += string.ascii_lowercase
            if include_upper:
                all_chars += string.ascii_uppercase
            if include_digits:
                all_chars += string.digits
            if include_special:
                all_chars += "!@#$%^&*()-_=+[]{}|;:,.<>?/\\"

            entropy = calculate_entropy(password)
            search_space = calculate_search_space_size(length, all_chars)

            print(f"Entropy: {entropy:.2f} bits")
            print(f"Search Space Size: {search_space}")

            if search_space > 0:
                # Assumed brute-force speed: 1 trillion guesses per second (1e12)
                guesses_per_second = 1e12
                time_seconds = search_space / guesses_per_second
                time_years = time_seconds / (3600 * 24 * 365)

                print(f"Approx. time to brute force at 1 trillion guesses/s:")
                # Display with commas for thousands separators, two decimals
                print(f" - {time_years:,.2f} years")

        except ValueError as e:
            print("\nError:", str(e))

        user_choice = input("\nPress enter to generate a new password or type 'exit' to close the program: ")
        if user_choice.lower() == "exit":
            break

if __name__ == "__main__":
    main()