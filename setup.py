import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="can_parser",
    version="0.1.0",
    author="WURacing",
    author_email="wuracing@gmail.com",
    description="Package to parse CAN Packets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WURacing/CANParser",
    packages=['can_parser'],
    install_requires=['cantools']
)