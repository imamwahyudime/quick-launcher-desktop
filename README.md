# Quick Launcher (Python)

A simple, minimalistic GUI application launcher and quick access tool built with Python and Tkinter. This tool allows users to quickly find and launch applications installed on their system.

## Current Features:

* **Minimalistic GUI:** A clean and simple user interface with a single text input field and a listbox for results.
* **Dynamic Application Filtering:** As you type into the input field, the listbox dynamically filters and displays matching application names from a predefined list.
* **Application Launching:**
    * Select an application from the listbox and press `Enter` or `Double-Click` to launch it.
    * Press `Enter` in the search field to launch the top selected application in the list.
* **Keyboard Navigation:**
    * Use `Up` and `Down` arrow keys to navigate the application list.
    * Pressing `Down` arrow in the search input moves focus to the listbox.
* **Basic Styling:** A modern dark theme for better aesthetics.
* **Status Bar:** Provides feedback on actions (e.g., "Launching...", "Error...", "X applications found").
* **Cross-Platform (Basic Support):** Includes example application paths for Windows, Linux, and macOS. Launching logic attempts to be platform-aware.
* **Centered Window:** The application window appears centered on the screen.

## Requirements:

* Python 3.x
* Tkinter (usually included with standard Python installations)

## Usage:

1.  **Save the Code:** Save the Python code (from the `app_launcher_part1` artifact) as a `.py` file (e.g., `quick_launcher.py`).
2.  **Open a Terminal or Command Prompt:** Navigate to the directory where you saved the file.
3.  **Execute the Script:** Run the script using the Python interpreter:
    ```bash
    python quick_launcher.py
    ```
