import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

extras_requirements = {
    "dev": [
        "wheel",
        "black",
    ],
}

setuptools.setup(
    name="rounding",
    version="0.2.0",
    author="Ruud van der Ham & Nyggus",
    author_email="nyggus@gmail.com",
    description="A tool for rounding floats in complex structures",
    long_description=long_description,
    long_description_content_type="text/x-md",
    url="https://github.com/nyggus/rounding",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    extras_require=extras_requirements,
)
