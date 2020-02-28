import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
        name="quat",
        version="0.0.1",
        author="John Stechschulte",
        author_email="john.l.stechschulte@gmail.com",
        description="Simple, pure-Python quaternions",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="http://github.com/JStech/quat",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        python_requires='>=3.6',
        )

