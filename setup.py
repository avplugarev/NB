import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="NB_realisation",
    version="1.0.0",
    author="Александр Плугарев",
    author_email="nightgust@gmail.com",
    description="API клиент по запросу классифицирующий товары",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avplugarev/NB.git", # Адрес сайта моего пакета.
    packages=setuptools.find_packages(), #автоматически соберем список всех пакретов необходимых для работы.
    classifiers=[ "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", ],
    python_requires='>=3.8',)