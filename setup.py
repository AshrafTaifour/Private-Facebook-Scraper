import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FacebookChat-Automated-Social-Media-Spear-Phisher", 
    version="0.0.1",
    author="Ashraf Taifour, Abdullah Arif, Abdullah Chattha, Abdullah Chattha, Steve Pham",
    description="A bot to read and write to Facebook via selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AshrafTaifour/fbLoginAndScrape",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)