import os
import subprocess

# Set current directory as working directory
current_dir = os.getcwd()

# Automatically install dependencies
subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

# Run main.py
main_script_path = os.path.join(current_dir, "main.py")
subprocess.run(["python", main_script_path], check=True)