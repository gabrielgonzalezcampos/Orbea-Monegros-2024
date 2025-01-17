from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="orbea-monegros-analysis",
    version="0.1.0",
    author="Gabriel Gonzalez",
    author_email="ggonzalezcamp@uoc.edu",
    description="A data analysis project for Orbea Monegros 2024 cycling event",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/orbea-monegros-analysis",
    packages=find_packages(include=['src', 'src.*']),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Data Visualization",
    ],
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'orbea-analysis=main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'src': ['data/*.csv'],
    },
    data_files=[
        ('data', ['data/dataset.csv']),
    ],
)