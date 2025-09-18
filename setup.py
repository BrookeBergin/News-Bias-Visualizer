import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="nbv",
    version='0.0.1',
    author='Brooke Bergin',
    author_email='brookebergin27@gmail.com',
    description='News Bias Visualization Tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    extras_requres={"dev": ["pytest", "flake8", "autopep8"]},
)