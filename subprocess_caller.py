import subprocess

def analyze_image(text):
    # Run the called script with arguments
    filename = "todo"
    slice_id = "1"
    subprocess.run(['python', 'app/analyze_image.py', 1, filename, slice_id])
    return text.upper()