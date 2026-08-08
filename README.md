# KeySpace
This branch contains the files for KeySpace Password Manager

CustomTkinter Official Documentation: https://customtkinter.tomschimansky.com/documentation/

## Installation & Usage

You can run KeySpace either by building it into a standalone application or by running the Python script directly.

### Option 1: Build a Standalone Application (Recommended)
You can use the provided build script to compile KeySpace into a standalone application for your operating system. You won't need to install Python on the target machine to run the compiled app.

1. Clone or download the repository.
2. Open a terminal or command prompt in the project directory.
3. Run the cross-platform build script:
   ```bash
   python build.py
   ```
4. The script will automatically install the necessary build dependencies (`pyinstaller`, `customtkinter`, `pillow`), clean up old builds, and compile the app for your operating system.

**Build Outputs (found in the `dist` folder):**
- **Windows:** `KeySpace.exe`
- **macOS:** `KeySpace.app` and `KeySpace.dmg` installer
- **Linux:** `KeySpace` executable binary

### Option 2: Run Directly via Python
If you prefer to run the app directly from the source code without building it:

1. Ensure you have Python installed.
2. Install the required dependencies:
   ```bash
   pip install customtkinter
   ```
3. Run the application:
   ```bash
   python KeySpace.py
   ```