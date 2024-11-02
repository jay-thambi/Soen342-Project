from setuptools import setup, find_packages
import os

# Define the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))

# Read the contents of the README file
with open(os.path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Soen342Project',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>=2.0',
        'Flask-SQLAlchemy>=2.5'
    ],
    entry_points={
        'console_scripts': [
            'run_app=app:main'  # Make sure 'main' is defined in app.py for this to work
        ],
    },
    author="Alexander Kepekci and Sanjay Thambithurai",
    description="A project for SOEN 342: Software Requirements and Deployment",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/soen342project",  # Replace with the actual URL of your project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
