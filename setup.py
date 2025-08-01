import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="ktb-py310",
    version="0.1.0",
    author="Nikolas lamb (original), Enhanced for Python 3.10+",
    author_email="nikolas.lamb@gmail.com",
    description="Python 3.10+ compatible Kinect v2 wrapper built on pylibfreenect2-py310",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cerealkiller2527/kinect-toolbox-py310",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11", 
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Topic :: Multimedia :: Video :: Capture",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development"
    ],
    python_requires='>=3.10',
)
