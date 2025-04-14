import secrets
import string
import math
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

def calculate_entropy(password: str) -> float:
    """Calculate Shannon entropy (in bits) for a given password."""
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
    """Calculate total search space size given the length and character set."""
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
    """Generate a random password with the specified character types."""
    if length < 1:
        raise ValueError("Password length must be at least 1.")

    # Build list of possible character pools
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
        raise ValueError("No character types selected. At least one must be chosen.")

    if require_each and length < len(pools):
        raise ValueError(
            f"Password length ({length}) is too short to include at least one "
            f"character from each of the {len(pools)} selected categories."
        )

    all_chars = "".join(pools)

    # Build password
    password_chars = []
    if require_each:
        # Ensure at least one from each pool
        for pool in pools:
            password_chars.append(secrets.choice(pool))

    while len(password_chars) < length:
        new_char = secrets.choice(all_chars)
        # Optional small check to avoid repeating same char consecutively
        if not password_chars or new_char != password_chars[-1]:
            password_chars.append(new_char)

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)

class PasswordGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ClatShield Password Generator v1.00")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Title Frame
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=10)

        title_label = ttk.Label(
            title_frame,
            text="ClatShield Password Generator",
            font=("Helvetica", 18, "bold"),
            foreground="#333333"
        )
        title_label.pack()

        version_label = ttk.Label(
            title_frame,
            text="Version 1.0.1",
            font=("Helvetica", 11),
            foreground="#555555"
        )
        version_label.pack()

        author_label = ttk.Label(
            self.root,
            text="By Joshua M Clatney (Clats97) - Ethical Pentesting Enthusiast",
            font=("Helvetica", 9),
            foreground="#555555"
        )
        author_label.pack(pady=5)

        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', padx=20, pady=10)

        # Input Frame
        input_frame = ttk.Frame(self.root)
        input_frame.pack(padx=20, pady=10, fill='x')

        # Password Length
        length_label = ttk.Label(input_frame, text="Password Length (at least 12 characters):", font=("Helvetica", 10))
        length_label.grid(row=0, column=0, sticky='w', pady=5)

        self.length_var = tk.IntVar(value=12)
        length_spinbox = ttk.Spinbox(
            input_frame,
            from_=8,
            to=64,
            textvariable=self.length_var,
            width=5
        )
        length_spinbox.grid(row=0, column=1, sticky='w', pady=5, padx=10)

        # Character Type Checkboxes
        self.lower_var = tk.BooleanVar(value=True)
        lower_check = ttk.Checkbutton(
            input_frame,
            text="Include Lowercase (a-z)",
            variable=self.lower_var
        )
        lower_check.grid(row=1, column=0, columnspan=2, sticky='w', pady=2)

        self.upper_var = tk.BooleanVar(value=True)
        upper_check = ttk.Checkbutton(
            input_frame,
            text="Include Uppercase (A-Z)",
            variable=self.upper_var
        )
        upper_check.grid(row=2, column=0, columnspan=2, sticky='w', pady=2)

        self.digits_var = tk.BooleanVar(value=True)
        digits_check = ttk.Checkbutton(
            input_frame,
            text="Include Digits (0-9)",
            variable=self.digits_var
        )
        digits_check.grid(row=3, column=0, columnspan=2, sticky='w', pady=2)

        self.special_var = tk.BooleanVar(value=True)
        special_check = ttk.Checkbutton(
            input_frame,
            text="Include Special Characters (!@#$...)",
            variable=self.special_var
        )
        special_check.grid(row=4, column=0, columnspan=2, sticky='w', pady=2)

        self.require_each_var = tk.BooleanVar(value=False)
        require_each_check = ttk.Checkbutton(
            input_frame,
            text="Require at least one of each selected type",
            variable=self.require_each_var
        )
        require_each_check.grid(row=5, column=0, columnspan=2, sticky='w', pady=5)

        # Generate Button
        generate_button = ttk.Button(
            self.root,
            text="Generate Password",
            command=self.generate_password
        )
        generate_button.pack(pady=10)

        # Output Frame
        output_frame = ttk.Frame(self.root)
        output_frame.pack(fill='x', padx=20, pady=10)

        # --- Password Field ---
        password_label = ttk.Label(
            output_frame,
            text="Generated Password:",
            font=("Helvetica", 10, "bold")
        )
        password_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky='w')

        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(
            output_frame,
            textvariable=self.password_var,
            font=("Helvetica", 12),
            width=40,
            state='readonly'
        )
        password_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # --- Copy Button (Below the Password Field) ---
        copy_button = ttk.Button(
            output_frame,
            text="Copy",
            command=self.copy_password
        )
        # Placed on next row (row=1) so it appears underneath password_entry
        copy_button.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Entropy
        entropy_label = ttk.Label(output_frame, text="Entropy (bits):", font=("Helvetica", 10, "bold"))
        entropy_label.grid(row=2, column=0, sticky='w', pady=5)

        self.entropy_var = tk.StringVar(value="0.00")
        entropy_value = ttk.Label(output_frame, textvariable=self.entropy_var, font=("Helvetica", 10))
        entropy_value.grid(row=2, column=1, sticky='w', pady=5)

        # Search Space
        search_space_label = ttk.Label(output_frame, text="Search Space Size:", font=("Helvetica", 10, "bold"))
        search_space_label.grid(row=3, column=0, sticky='w', pady=5)

        self.search_space_var = tk.StringVar(value="0")
        search_space_value = ttk.Label(output_frame, textvariable=self.search_space_var, font=("Helvetica", 10))
        search_space_value.grid(row=3, column=1, sticky='w', pady=5)

        # Brute-Force Time
        brute_force_label = ttk.Label(
            output_frame,
            text="Estimated Brute-Force Time:",
            font=("Helvetica", 10, "bold")
        )
        brute_force_label.grid(row=4, column=0, sticky='w', pady=5)

        self.brute_force_var = tk.StringVar(value="0 years")
        brute_force_value = ttk.Label(output_frame, textvariable=self.brute_force_var, font=("Helvetica", 10))
        brute_force_value.grid(row=4, column=1, sticky='w', pady=5)

        # Exit Button
        exit_button = ttk.Button(self.root, text="Exit", command=self.root.quit)
        exit_button.pack(pady=10)

    def generate_password(self):
        try:
            length = self.length_var.get()
            include_lower = self.lower_var.get()
            include_upper = self.upper_var.get()
            include_digits = self.digits_var.get()
            include_special = self.special_var.get()
            require_each = self.require_each_var.get()

            password = generate_random_password(
                length=length,
                use_lower=include_lower,
                use_upper=include_upper,
                use_digits=include_digits,
                use_special=include_special,
                require_each=require_each
            )
            self.password_var.set(password)

            # Determine the combined character set
            all_chars = ""
            if include_lower:
                all_chars += string.ascii_lowercase
            if include_upper:
                all_chars += string.ascii_uppercase
            if include_digits:
                all_chars += string.digits
            if include_special:
                all_chars += "!@#$%^&*()-_=+[]{}|;:,.<>?/\\"

            # Calculate entropy and search space
            entropy = calculate_entropy(password)
            search_space = calculate_search_space_size(length, all_chars)

            self.entropy_var.set(f"{entropy:.2f}")
            self.search_space_var.set(f"{search_space:,}")

            # Estimate brute-force time (assuming 1 trillion guesses/s)
            if search_space > 0:
                guesses_per_second = 1e12
                time_seconds = search_space / guesses_per_second
                time_years = time_seconds / (3600 * 24 * 365)
                self.brute_force_var.set(f"{time_years:,.2f} years")
            else:
                self.brute_force_var.set("N/A")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def copy_password(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showwarning("No Password", "There is no password to copy.")

def main():
    root = tk.Tk()
    # Try a modern theme if available
    try:
        style = ttk.Style()
        style.theme_use('clam')
    except Exception:
        pass

    app = PasswordGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()