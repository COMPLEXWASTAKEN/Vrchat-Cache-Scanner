from core import *

class logger:
    def __init__(self, prefix: str = "Vrc"):
        self.WHITE: str = "\u001b[37m"
        self.MAGENTA: str = "\033[38;5;97m"
        self.RED: str = "\033[38;5;196m"
        self.GREEN: str = "\033[38;5;40m"
        self.YELLOW: str = "\033[38;5;220m"
        self.BLUE: str = "\033[38;5;21m"
        self.PINK: str = "\033[38;5;176m"
        self.CYAN: str = "\033[96m"
        self.DARKBLUE = "\033[38;5;18m"
        self.LIGHTRED: str = "\033[38;5;203m"
        self.prefix: str = f"{self.LIGHTRED}[{self.RED}{prefix}{self.LIGHTRED}]"
    def message(self, level: str, message: str) -> str:
        return f"  {self.prefix}  {self.WHITE}| {self.LIGHTRED}[{level}{self.LIGHTRED}]  {self.WHITE}->  {self.RED}[{self.RED}{message}{self.RED}]"

    def success(self, message: str, level: str = "Success"):
        print(self.message(f"{self.GREEN}{level}", f"{self.GREEN}{message}"))

    def warning(self, message: str, level: str = "Warning"):
        print(self.message(f"{self.YELLOW}{level}", f"{self.YELLOW}{message}"))

    def info(self, message: str, level: str = "Info"):
        print(self.message(f"{self.RED}{level}", f"{self.RED}{message}"))

    def failure(self, message: str, level: str = "Failure"):
        print(self.message(f"{self.RED}{level}", f"{self.RED}{message}"))

    def debug(self, message: str, level: str = "Debug"):
        print(self.message(f"{self.MAGENTA}{level}", f"{self.MAGENTA}{message}"))

    def scraper(self, message: str, level: str = "Scraper"):
        print(self.message(f"{self.BLUE}{level}", f"{self.BLUE}{message}"), end="\r", flush=True,)
    
    def captcha(self, message: str, level: str = "Captcha"):
        print(self.message(f"{self.CYAN}{level}", f"{self.CYAN}{message}"))

    def PETC(self):
        input(f"  {self.LIGHTRED}[{self.RED}Press Enter To Continue{self.LIGHTRED}]")
    def ask(self, message: str, level: str = "Ask"):
            ask = input(f"  {self.LIGHTRED}[{self.RED}{message}{self.LIGHTRED}]{self.RED} -> ")
            return ask


  

log = logger()