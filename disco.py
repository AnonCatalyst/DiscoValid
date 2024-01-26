import os
import random
import time
import logging
from colorama import Fore, init, Style
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import requests
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
import string
import threading
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import os
import subprocess

def clear_screen():
    try:
        # Attempt to clear the screen using subprocess
        subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)

    except Exception as e:
        print(f"Error clearing the screen: {e}")

# Call the function to clear the screen
clear_screen()

init(autoreset=True)

# Configure logging
logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
# Information text about the tool
descriptinfotext = f"""
{Fore.LIGHTBLACK_EX}🌟 Welcome to DiscordValid! 🌟{Style.RESET_ALL}

{Fore.LIGHTBLACK_EX}DiscordValid{Style.RESET_ALL} is a tool developed by {Fore.LIGHTBLACK_EX}AnonCatalyst{Style.RESET_ALL}. It generates random Discord invite links and performs various validation steps on them, including basic validation and advanced criteria.

- {Fore.LIGHTBLACK_EX}Basic Validation:{Style.RESET_ALL}
  - Sends a request to the invite link.
  - Checks for a successful response (status code {Fore.LIGHTBLACK_EX}200-299{Style.RESET_ALL}).
  - Validates the content length.

- {Fore.LIGHTBLACK_EX}Advanced Criteria:{Style.RESET_ALL}
  - Searches for specific keywords in the response content, such as {Fore.LIGHTBLACK_EX}'community,' 'active members,' 'gaming,' 'chat.'{Style.RESET_ALL}

- {Fore.LIGHTBLACK_EX}Extended Validation:{Style.RESET_ALL}
  - {Fore.LIGHTBLACK_EX}Header Validation:{Style.RESET_ALL} Checks for essential headers ({Fore.LIGHTBLACK_EX}content-type, server{Style.RESET_ALL}).
  - {Fore.LIGHTBLACK_EX}HTML Element Validation:{Style.RESET_ALL} Ensures specific HTML elements ({Fore.LIGHTBLACK_EX}title, h1, div with class 'content'{Style.RESET_ALL}) are present.
  - {Fore.LIGHTBLACK_EX}Cookie Validation:{Style.RESET_ALL} Verifies the existence of certain cookies ({Fore.LIGHTBLACK_EX}session_id, user_token{Style.RESET_ALL}).
  - {Fore.LIGHTBLACK_EX}Attribute Validation:{Style.RESET_ALL} Checks for specified attributes in HTML elements ({Fore.LIGHTBLACK_EX}href for 'a' tags, src for 'img' tags{Style.RESET_ALL}).

{Fore.LIGHTBLACK_EX}Please note that the tool may take some time to find valid invites due to the nature of Discord temporary invite links.{Style.RESET_ALL} Thank you for using {Fore.LIGHTBLACK_EX}DiscordValid!{Style.RESET_ALL}
"""

def print_banner():
    banner = f"""
┌{'─' * 60}┐
│{Fore.MAGENTA}{Style.BRIGHT}🎉 DiscordValid 🎉{Style.RESET_ALL}{' ' * 42}│
├{'─' * 60}┤
│{Fore.CYAN}{Style.BRIGHT}👨‍💻 Developer:{Style.RESET_ALL} {Fore.YELLOW}{Style.BRIGHT}AnonCatalyst{Style.RESET_ALL}{' ' * 32}│
│{Fore.CYAN}{Style.BRIGHT}🌐 GitHub:{Style.RESET_ALL} {Fore.BLUE}{Style.BRIGHT}github.com/AnonCatalyst{Style.RESET_ALL}{' ' * 26}│
│{Fore.CYAN}{Style.BRIGHT}📷 Instagram:{Style.RESET_ALL} {Fore.BLUE}{Style.BRIGHT}instagram.com/Istoleyourbutter{Style.RESET_ALL}{' ' * 16}│
└{'─' * 60}┘
    """
    print(banner)

# Fancy separator
def print_separator():
    separator = f"{Fore.CYAN}{'*' * 60}{Style.RESET_ALL}"
    print(separator)
    print(descriptinfotext)
class DiscordValid:
    DEFAULT_THREADS = 50

    def __init__(self, num_threads=DEFAULT_THREADS, delay=10, status_update_interval=100):
        self.delay = delay
        self.num_threads = num_threads
        self.status_update_interval = status_update_interval
        self.total_generated = 0
        self.valid_count = 0
        self.invalid_count = 0
        self.total_errors = 0
        self.processed_invites = set()
        self.processed_invites_lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=self.num_threads)
        self.user_agent = UserAgent()

    def perform_request(self, invite):
        try:
            logger.info(f"{Fore.CYAN}Performing request for invite: {invite}{Style.RESET_ALL}")

            headers = {'User-Agent': self.user_agent.random}
            logger.info(f"{Fore.GREEN}Selected User Agent: {headers['User-Agent']}{Style.RESET_ALL}")

            response = requests.get(invite, headers=headers, timeout=10)
            logger.info(f"{Fore.CYAN}Request completed for invite: {invite}{Style.RESET_ALL}")

            return response
        except requests.RequestException as e:
            logger.warning(f"{Fore.YELLOW}Error performing request for {invite}: {e}{Style.RESET_ALL}")
            return None

    def validate_invite(self, invite):
        try:
            logger.info(f"{Fore.CYAN}Validating invite: {invite}{Style.RESET_ALL}")
            response = self.perform_request(invite)

            if response and 200 <= response.status_code < 300:
                content_length = response.headers.get('Content-Length')

                if content_length and int(content_length) > 0 and self.advanced_validation(invite, response.content):
                    return self.validate_extended(invite, response)

            logger.warning(f"{Fore.YELLOW}Validation failed for invite: {invite}{Style.RESET_ALL}")
            return False
        except Exception as e:
            logger.warning(f"{Fore.YELLOW}Error validating invite {invite}: {e}{Style.RESET_ALL}")
            return False

    def validate_extended(self, invite, response):
        try:
            validations = [
                ('Header Validation', self.header_validation, response.headers),
                ('HTML Element Validation', self.html_element_validation, response.content),
                ('Cookie Validation', self.cookie_validation, response.cookies),
                ('Attribute Validation', self.attribute_validation, response.content)
            ]

            for validation_name, validation_func, validation_data in validations:
                if validation_func(validation_data):
                    logger.info(f"{Fore.GREEN}{validation_name} passed.{Style.RESET_ALL}")
                else:
                    logger.warning(f"{Fore.YELLOW}{validation_name} failed.{Style.RESET_ALL}")
                    return False

            return True  # All validations passed
        except Exception as e:
            logger.error(f"{Fore.RED}Error during extended validation for invite {invite}: {e}{Style.RESET_ALL}")
            return False

    def header_validation(self, response_headers):
        try:
            logger.info(f"{Fore.CYAN}Performing header validation.{Style.RESET_ALL}")
            required_headers = ['content-type', 'server']

            return all(header.lower() in response_headers for header in required_headers)

        except Exception as e:
            logger.error(f"{Fore.RED}Error during header validation: {e}{Style.RESET_ALL}")
            return False

    def html_element_validation(self, response_content):
        try:
            logger.info(f"{Fore.CYAN}Performing HTML element validation.{Style.RESET_ALL}")
            required_elements = ['<title>', '<h1>', '<div class="content">']

            soup = BeautifulSoup(response_content, 'html.parser')

            return all(soup.find_all(string=element) for element in required_elements)

        except Exception as e:
            logger.error(f"{Fore.RED}Error during HTML element validation: {e}{Style.RESET_ALL}")
            return False

    def cookie_validation(self, response_cookies):
        try:
            logger.info(f"{Fore.CYAN}Performing cookie validation.{Style.RESET_ALL}")
            required_cookies = ['session_id', 'user_token']

            return all(cookie in response_cookies for cookie in required_cookies)

        except Exception as e:
            logger.error(f"{Fore.RED}Error during cookie validation: {e}{Style.RESET_ALL}")
            return False

    def attribute_validation(self, response_content):
        try:
            logger.info(f"{Fore.CYAN}Performing attribute validation.{Style.RESET_ALL}")
            required_attributes = {'a': 'href', 'img': 'src'}

            soup = BeautifulSoup(response_content, 'html.parser')

            return all(soup.find_all(tag, {attribute: True}) for tag, attribute in required_attributes.items())

        except Exception as e:
            logger.error(f"{Fore.RED}Error during attribute validation: {e}{Style.RESET_ALL}")
            return False

    def generate_invite(self):
        try:
            logger.info("Generating a random Discord invite.")

            invite_patterns = [
                "https://discord.gg/{code}",
                "https://discord.com/invite/{code}",
                "https://discord.me/{code}",
                "https://discordapp.com/invite/{code}"
            ]

            random_invite_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            invite_pattern = random.choice(invite_patterns)
            random_invite = invite_pattern.format(code=random_invite_code)

            if self.validate_invite(random_invite):
                logger.info(f"Generated invite: {random_invite}")
                return random_invite
            else:
                logger.warning("Failed to generate a valid invite.")
                return None
        except RecursionError:
            logger.error("RecursionError: Unable to generate a valid invite.")
            return None

    def main(self):
        try:
            while True:
                invite = self.generate_invite()

                if invite:
                    self.executor.submit(self.check_invite, invite)

                self.total_generated += 1
                time.sleep(self.delay)

        except KeyboardInterrupt:
            self.display_results()
            print(Fore.YELLOW + "\nDiscordValid terminated by user." + Style.RESET_ALL)
        except Exception as e:
            logger.error(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
        finally:
            if self.executor:
                self.executor.shutdown(wait=False)

    def display_results(self):
        self.print_results_info()
#        print(Fore.YELLOW + "\nDiscordValid terminated by user." + Style.RESET_ALL)

    def print_results_info(self):
        print(f"\n--- Results Information ---")
        print(f"Total Invites Generated: {self.total_generated}")
#        print(f"Valid Invites: {self.valid_count}")
#        print(f"Invalid Invites: {self.invalid_count}")
#        print(f"Total Errors: {self.total_errors}")

    def print_status_update(self):
        print(f"\n--- Status Update ---")
        print(f"Total Invites Generated: {self.total_generated}")
#        print(f"Valid Invites: {self.valid_count}")
#        print(f"Invalid Invites: {self.invalid_count}")
#        print(f"Total Errors: {self.total_errors}")

    def print_valid_invite(self, invite):
        formatted_message = highlight(f"\nValid Invite: {invite}", PythonLexer(), TerminalFormatter())
        print(formatted_message)

    def check_invite(self, invite):
        try:
            with tqdm(total=100, desc=f'Validating {invite}', position=0, leave=True) as pbar1:
                if self.handle_processed_invite(invite):
                    logger.info(f"Invite {invite} is being processed.")
                    pbar1.update(10)

                    logger.info(f"Performing basic validation for invite: {invite}")
                    if self.validate_invite(invite):
                        self.valid_count += 1
                        pbar1.update(30)
                        logger.info(f"Basic validation passed for Invite: {invite}")

                        logger.info(f"Checking advanced criteria for invite: {invite}")
                        pbar1.update(20)

                        self.print_valid_invite(invite)
                    else:
                        self.invalid_count += 1
                        logger.warning(f"Invalid Invite: {invite}")

                    if self.total_generated % self.status_update_interval == 0:
                        self.print_status_update()

                    pbar1.update(40)

                logger.info(f"Invite {invite} has completed all validation steps.")

        except Exception as e:
            logger.error(f"Error validating invite {invite}: {e}")
            self.total_errors += 1
        finally:
            self.processed_invites.discard(invite)
            self.print_results_info()

    def handle_processed_invite(self, invite):
        with self.processed_invites_lock:
            if invite not in self.processed_invites:
                self.processed_invites.add(invite)
                logger.info(f"Invite {invite} is being processed.")
                return True
            else:
                logger.warning(f"Invite {invite} has already been processed.")
                return False

if __name__ == "__main__":
    try:
        print_banner()
        print_separator()
        input(Fore.YELLOW + "Press Enter to launch DiscordValid or Ctrl+C to exit." + Style.RESET_ALL)

        disco_valid = DiscordValid()
        disco_valid.main()

    except KeyboardInterrupt:
        disco_valid.display_results()
        print(Fore.YELLOW + "\nDiscordValid terminated by user." + Style.RESET_ALL)
    except Exception as e:
        logger.error(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
