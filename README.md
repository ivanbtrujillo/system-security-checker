# System Security Checker

This Python script uses osquery to check various security aspects of your system, including disk encryption, antivirus protection, and screen lock settings.

## Prerequisites

- Python 3.6 or higher
- osquery installed on your system

## Installation

1. Install osquery:

   - For macOS:

     ```
     brew install osquery
     ```

   - For Windows:
     Download and install from [osquery.io](https://osquery.io/downloads)

   - For Linux:
     Follow the instructions for your distribution at [osquery.io](https://osquery.io/downloads)

2. Clone this repository:

   ```
   git clone https://github.com/yourusername/system-security-checker.git
   cd system-security-checker
   ```

3. Create a virtual environment (optional but recommended):

   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

## Usage

Run the script using:

```
python src/main.py
```

The script will check and report on:

- Disk encryption status
- Antivirus protection
- Screen lock configuration

## Troubleshooting

If you encounter issues with osquery:

1. Ensure osquery is correctly installed and in your system PATH.
2. On macOS, you might need to grant full disk access to osqueryi in System Preferences > Security & Privacy > Privacy > Full Disk Access.
3. On Windows, ensure you're running the script with administrator privileges.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
