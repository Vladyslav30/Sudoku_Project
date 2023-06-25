import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Define a list of packages that you want to install
packages = ['pygame', 'numpy']

for package in packages:
    try:
        dist = __import__(package)
        print('{} ({}) is already installed'.format(package, dist.__version__))
    except ImportError:
        print('{} is NOT installed'.format(package))
        print('Installing...')
        install(package)
        print('{} has been installed successfully'.format(package))

# For the modules "test", make sure you have the python file in your current directory or the PYTHONPATH
# If "test.py" is not found, you may want to handle this manually




