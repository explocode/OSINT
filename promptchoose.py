import os

def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def main():
    while True:        
        print_colored("Choose which script to execute:", "33")
        print_colored("1. ApiOsintMail.py", "32")
        print_colored("2. OSINT-COLLECTOR.py", "32")
        print_colored("3. Exit", "31")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            os.system("python ApiOsintMail.py")
        elif choice == "2":
            os.system("python OSINT-COLLECTOR.py")
        elif choice == "3":
            print_colored("Exiting the program...", "31")
            break
        else:
            print_colored("Invalid choice. Please try again.", "31")

if __name__ == "__main__":
    main()
