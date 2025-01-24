# ClatShield Password Tool
A simple Python script that generates cryptographically secure passwords of a variable length and variable characters.

![clatshield](https://github.com/user-attachments/assets/40665e3f-459a-4f54-b6d1-b3c779a8ed72)

## Overview

This Python script is a command-line tool that generates cryptographically secure passwords and provides basic metrics (Shannon entropy and brute-force estimates). It is designed to demonstrate best practices for password generation, including:
- Ensuring no two consecutive characters are identical
- Allowing customization of character sets (lowercase, uppercase, digits, special characters)
- Requiring at least one character from each selected category (if desired)
- Calculating password entropy
- Estimating brute-force times based on a configurable guess rate

It prints a stylized banner, prompts the user for settings, generates a password, and calculates important metrics to help you evaluate password strength.

## Features

1. **Cryptographically Secure Password Generation**  
   Utilizes the built-in `secrets` module to ensure randomness suitable for security applications.

2. **Character Set Selection**  
   Allows including or excluding four categories: lowercase letters, uppercase letters, digits, and special characters.

3. **Require-Each Option**  
   Ensures the generated password has at least one character from each selected category if `require_each=True`.

4. **Consecutive Character Prevention**  
   Ensures no two consecutive characters are the same, reducing the risk of predictable sequences.

5. **Entropy Calculation**  
   Implements Shannon entropy calculation (in bits) to gauge password complexity.

6. **Search Space Size Calculation**  
   Calculates the total possible combinations for a password, given its length and chosen character sets.

7. **Brute-Force Time Estimation**  
   Estimates how long it might take to brute-force the generated password at a specified guess rate (default: 1 trillion guesses per second).

8. **Loop for Multiple Generations**  
   Continues generating passwords until the user chooses to exit.

## Requirements

- **Python 3.7+** (tested up to Python 3.11)
- Uses only standard libraries:
  - `secrets`
  - `string`
  - `math`

No additional external libraries are required.

## How It Works

### 1. Script Banner and Setup
When the script starts, it displays a stylized banner followed by an author note. This is simply a visual introduction.

### 2. User Prompts
The script prompts the user for:
1. **Password Length** (an integer). If the user provides invalid input (e.g., not an integer), it defaults to 12.
2. **Character Set Options**:
   - Lowercase letters (a-z)
   - Uppercase letters (A-Z)
   - Digits (0-9)
   - Special Characters (e.g., `!@#$%^&*()-_=+[]{}|;:,.<>?/\`)
3. **Require Each** (yes/no): Whether to mandate at least one character from each selected category.

### 3. Password Generation

**Function: `generate_random_password()`**  
- Takes parameters `length`, `use_lower`, `use_upper`, `use_digits`, `use_special`, and `require_each`.  
- Builds one or more character pools (e.g., lowercase letters, uppercase letters, etc.) based on user choices.  
- If `require_each=True`, it ensures that each chosen pool contributes at least one character.  
- Randomly selects characters using `secrets.choice()` to ensure cryptographic security.  
- Prevents two consecutive characters from being identical.  
- Returns the generated password as a string.

### 4. Password Entropy Calculation

**Function: `calculate_entropy()`**  
- Uses Shannon entropy (in bits) to measure unpredictability of the password.  
- Returns the entropy value as a floating-point number.

### 5. Search Space Size Calculation

**Function: `calculate_search_space_size()`**  
- Returns the number of possible combinations.

### 6. Brute-Force Time Estimation

After generating the password, the script:
- Calculates the approximate time to brute force the password by dividing the search space by a guess rate (assumed to be \(10^{12}\) guesses per second).
- Converts the resulting seconds into years for a more relatable timeframe.

### 7. Loop or Exit
The script prompts the user to either generate a new password (press Enter) or type "exit" to end the program. On each iteration, new inputs are collected, and a new password is generated with the updated preferences.

## Usage

1. **Clone or download** this repository.
2. **Run the script**:
3. Follow the on-screen prompts. For instance:
   
   Enter the password length (12-16 characters minimum is recommended): 16
   Include lowercase letters (a-z)? (y/n): y
   Include uppercase letters (A-Z)? (y/n): y
   Include numbers (0-9)? (y/n): y
   Include special characters? (y/n): y
   Require at least one of each chosen category? (y/n): n
  
4. View the generated password, its calculated entropy, and the estimated brute-force time.
5. Press Enter to generate another password, or type "exit" to quit.

## Limitations and Considerations

- **Assumed Guess Rate**: The guess rate of \(10^{12}\) guesses per second is for demonstration and may differ in real-world scenarios. Attack speeds vary greatly.
- **Entropy Calculation**: Shannon entropy of the generated password itself is a rough measure of complexity, not a definitive guarantee against real-world attacks.
- **Character Pool Limitations**: Although the special characters string is reasonably broad, you can modify it to include (or exclude) custom characters.
- **Minimum Length**: While the script suggests a minimum length of 12, longer passwords typically provide more security.

## License

Distributed under the Apache 2.0 License. 

**Author**
Joshua M Clatney (Clats97)
Ethical Pentesting Enthusiast

Copyright 2025 Joshua M Clatney (Clats97)
