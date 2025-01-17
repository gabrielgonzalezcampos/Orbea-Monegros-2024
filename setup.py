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
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'orbea-analysis=main:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['data/*.csv', 'img/*.png'],
    },
)

