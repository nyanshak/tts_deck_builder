import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tts_deck_builder",
    version="0.0.1",
    description="Tools for building decks of cards for Tabletop Simulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'Pillow',
    ],
    extras_require={
        'dev': [
            'flake8'
        ]
    }
)
