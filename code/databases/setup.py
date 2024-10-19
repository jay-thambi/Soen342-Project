from setuptools import setup, find_packages
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

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
            'run_app=app:main'
        ],
    },
    author="Your Name",
    description="SOEN 342 Project",
    long_description=open(os.path.join(current_dir, '../README.md')).read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/soen342project",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
