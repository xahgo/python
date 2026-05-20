from setuptools import setup, find_packages

setup(
    name='pdfminer_custom',       # 설치될 PyPI 이름
    version='0.1',
    packages=find_packages(include=["pdfminer*"]),  # 실제 import 되는 모듈명
    install_requires=[
        "chardet",
    ],
)