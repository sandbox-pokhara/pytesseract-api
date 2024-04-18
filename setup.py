import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytesseract-api",
    version="1.0.2",
    author="Pradish Bijukchhe",
    author_email="pradishbijukchhe@gmail.com",
    description=(
        "Tesseract C-API in python, a faster alternative to pytesseract"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sandbox-pokhara/pytesseract-api",
    project_urls={
        "Bug Tracker": (
            "https://github.com/sandbox-pokhara/pytesseract-api/issues"
        ),
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    include_package_data=True,
    package_dir={"pytesseract_api": "pytesseract_api"},
    python_requires=">=3",
    install_requires=[],
)
