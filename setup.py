from setuptools import setup, find_packages

setup(
    name="VirtualMouseControl",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "mediapipe",
        "pyautogui",
        "keyboard"
    ],
    entry_points={
        "console_scripts": [
            "virtualmouse=src.mouse_control:main"
        ]
    },
)
