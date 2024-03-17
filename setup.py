from setuptools import setup, find_packages

setup(
    name="ana",
    version="0.1",
    packages=find_packages(),
    description="Funciones para analisis descriptivo y utilitarios usados en el Aprendizaje Automatico",
    author="Freddy Alvarado",
    author_email="freddy.alvarado.b1@gmail.com",
    url="https://github.com/FreddyAlvarado/analib",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'pandas==2.1.3',
        'numpy==1.26.2',
        'matplotlib==3.8.2',
        'seaborn==0.13.0',
        'scipy==1.11.4'
    ],
)
