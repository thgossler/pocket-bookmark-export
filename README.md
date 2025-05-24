<!-- SHIELDS -->
<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">Pocket Bookmark Export</h1>

  <p align="center">
    Export your Pocket saved articles to your browser bookmarks with ease.
    <br />
    <a href="https://github.com/thgossler/pocket-bookmark-export/issues">Report Bug</a>
    ·
    <a href="https://github.com/thgossler/pocket-bookmark-export/issues">Request Feature</a>
    ·
    <a href="https://github.com/thgossler/pocket-bookmark-export#contributing">Contribute</a>
  </p>
</div>

# Introduction

Pocket Bookmark Export is a Python command-line tool that seamlessly exports your saved articles from Pocket to your browser bookmarks. The exported bookmarks are organized in a dedicated 'Pocket-Export' folder in your browser, making it easy to access your saved content directly from your browser's bookmark bar.

## Motivation

Mozilla has announced the discontinuation of its Pocket service, effective July 8, 2025. After this date, users will no longer be able to save new content, and the platform will transition into an export-only mode. All user data, including saved articles, highlights, notes, and archives, will be permanently deleted after October 8, 2025.

To preserve your saved content, Mozilla provides two primary export options:
1. CSV Export: Users can request a CSV file containing their saved items. This file will be sent to the email address associated with their Pocket account. Note that the export process may take up to 24 hours, and the download link will remain active for 48 hours.
2. API Access (JSON Format): For those who prefer a more technical approach, Pocket’s API allows users to retrieve their data in JSON format. This method is suitable for developers or users who wish to integrate their Pocket data into other applications or workflows.

To assist with the transition, this script is available that utilizes the API to fetch your saved items in JSON format and converts them into browser bookmarks. This allows for seamless integration of your Pocket content into your preferred web browser, ensuring continued access to your saved articles.

For detailed instructions on exporting your data and to access the export tool, please visit Mozilla’s official support page: [Pocket is saying goodbye - What you need to know](https://support.mozilla.org/en-US/kb/future-of-pocket).

It’s crucial to complete the export of your data before the October 8, 2025 deadline, as all user information will be irreversibly deleted after this date.

## Features

### Authentication and Authorization

- **Interactive OAuth flow** with Pocket API via web browser
- **Secure token management** using Pocket's official OAuth 2.0 implementation
- **Consumer Key setup guidance** with step-by-step instructions

### Export Functionality

- **Complete export** of all saved Pocket articles to browser bookmarks
- **Automatic organization** in a dedicated 'Pocket-Export' folder
- **Intelligent title handling** using resolved titles, given titles, or item IDs as fallback
- **URL resolution** with support for both resolved and given URLs

### Browser Support

- **Microsoft Edge** (Windows, macOS, Linux)
- **Google Chrome** (Windows, macOS, Linux)
- **Mozilla Firefox** (Windows, macOS, Linux)
- **Cross-platform compatibility** with automatic OS detection
- **Smart default browser suggestion** based on operating system

### Data Safety

- **Automatic backup creation** of existing bookmarks before export
- **Non-destructive updates** - existing bookmarks remain untouched
- **Previous export cleanup** - removes old Pocket-Export folders before creating new ones
- **Error handling and recovery** with detailed error messages

### User Experience

- **Interactive setup wizard** for first-time users
- **Clear progress indicators** throughout the export process
- **Comprehensive error messages** with troubleshooting guidance
- **Browser restart reminders** to ensure bookmarks are properly loaded

## Used Technologies

- **Python 3.6+**
- **requests** library for HTTP API calls
- **pathlib** for cross-platform file system operations
- **JSON handling** for bookmark file manipulation
- **webbrowser** module for OAuth flow
- **Pocket API v3** for article retrieval

## Getting Started

### Prerequisites

- Python 3.6 or higher
- A Pocket account with saved articles
- One of the supported browsers installed

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/thgossler/pocket-bookmark-export.git
   cd pocket-bookmark-export
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv .
   source bin/activate  # On macOS/Linux
   # or: .\\Scripts\\activate  # On Windows
   ```

3. **Install required packages**
   ```bash
   pip install requests
   ```

4. **Get your Pocket API Consumer Key**
   - Go to: https://getpocket.com/developer/apps/new
   - Create a new application with 'Retrieve' permissions
   - Copy the Consumer Key (you'll be prompted for it when running the script)

5. **Run the script**
   ```bash
   python main.py
   ```

### Usage

1. **Run the script** and follow the interactive prompts
2. **Enter your Pocket Consumer Key** when prompted
3. **Authorize the application** in your browser when redirected
4. **Select your browser** for bookmark export
5. **Wait for the export** to complete
6. **Restart your browser** to see the new bookmarks

The script will:
- Create a backup of your current bookmarks
- Export all your Pocket items to a new 'Pocket-Export' folder
- Provide clear feedback throughout the process

## Supported Browsers

| Browser | Windows | macOS | Linux |
|---------|---------|-------|-------|
| Microsoft Edge | ✅ | ✅ | ✅ |
| Google Chrome | ✅ | ✅ | ✅ |
| Mozilla Firefox | ✅ | ✅ | ✅ |

## Report Bugs

Please open an issue on the GitHub repository with the tag "bug".

## Donate

If you are using the tool but are unable to contribute technically, please consider promoting it and donating an amount that reflects its value to you. You can do so either via PayPal

[![Donate via PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate/?hosted_button_id=JVG7PFJ8DMW7J)

or via [GitHub Sponsors](https://github.com/sponsors/thgossler).

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/thgossler/pocket-bookmark-export.svg
[contributors-url]: https://github.com/thgossler/pocket-bookmark-export/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/thgossler/pocket-bookmark-export.svg
[forks-url]: https://github.com/thgossler/pocket-bookmark-export/network/members
[stars-shield]: https://img.shields.io/github/stars/thgossler/pocket-bookmark-export.svg
[stars-url]: https://github.com/thgossler/pocket-bookmark-export/stargazers
[issues-shield]: https://img.shields.io/github/issues/thgossler/pocket-bookmark-export.svg
[issues-url]: https://github.com/thgossler/pocket-bookmark-export/issues
[license-shield]: https://img.shields.io/github/license/thgossler/pocket-bookmark-export.svg
[license-url]: https://github.com/thgossler/pocket-bookmark-export/blob/main/LICENSE
