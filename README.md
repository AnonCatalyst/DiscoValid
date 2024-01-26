# **DiscoValid** 🕵️‍♂️🎉

Welcome to **DiscoValid**, a powerful tool crafted by [AnonCatalyst](https://github.com/AnonCatalyst) for exploring and validating Discord invite links! 🚀 This Open Source Intelligence (OSINT) tool is designed to help you discover and verify Discord servers with ease.

## Features 🛠️

- **Random Invite Generation:** DiscoValid generates random Discord invite links to explore a diverse range of servers.

- **Basic Validation:**
  - Sends a request to the invite link.
  - Checks for a successful response (status code 200-299).
  - Validates content length.

- **Advanced Criteria:**
  - Searches for specific keywords in the response content (e.g., 'community,' 'active members,' 'gaming,' 'chat').

- **Extended Validation:**
  - Header Validation: Checks for essential headers (content-type, server).
  - HTML Element Validation: Ensures specific HTML elements (title, h1, div with class 'content') are present.
  - Cookie Validation: Verifies the existence of certain cookies (session_id, user_token).
  - Attribute Validation: Checks for specified attributes in HTML elements (href for 'a' tags, src for 'img' tags).

- **User-Agent Rotation:** DiscoValid uses a variety of user agents to mimic different browsers and devices during requests.

## Why DiscoValid? 🤔

- **OSINT Exploration:** DiscoValid is your companion for Open Source Intelligence, making it easy to discover and validate Discord servers.

- **Validation Process:** DiscoValid employs a multi-step validation process, ensuring generated invites meet specific criteria.

- **Advanced Validation:** Beyond basic checks, DiscoValid performs in-depth validation, including header, HTML element, cookie, and attribute checks.

- **Use Cases:**
  - Discovering vibrant Discord communities.
  - Analyzing servers for specific keywords or themes.
  - Verifying the legitimacy of Discord invites during investigations.

## Note 📝

- **Time Consideration:** DiscoValid may take some time to find valid invites due to the nature of Discord temporary invite links.

- **Community Contribution:** We welcome contributions! Feel free to submit issues, feature requests, or pull requests.

## Getting Started 🚀

### Option 1: Quick Install with `install.py`

1. **Clone the repository:** `git clone https://github.com/AnonCatalyst/DiscoValid.git`
2. **Navigate to the directory:** `cd DiscoValid`
3. **Run the install script:** `python3 install.py`

### Option 2: Manual Installation

#### Prerequisites

- Python 3.x
- Install required dependencies individually:
  - `pip install colorama`
  - `pip install tqdm`
  - `pip install requests`
  - `pip install pygments`
  - `pip install fake_useragent`
  - `pip install beautifulsoup4`

#### Usage

1. **Clone the repository:** `git clone https://github.com/AnonCatalyst/DiscoValid.git`
2. **Navigate to the directory:** `cd DiscoValid`
3. **Run DiscoValid:** `python3 discovalid.py`

For more detailed instructions and options, check out the [Wiki](link-to-your-wiki).

## Acknowledgments 🙌

- Special thanks to the [contributors](https://github.com/AnonCatalyst/DiscoValid/graphs/contributors) of this project.

## Developer 🧑‍💻

- [AnonCatalyst](https://github.com/AnonCatalyst)
  - Instagram: [istoleyourbutter](https://instagram.com/istoleyourbutter)

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
