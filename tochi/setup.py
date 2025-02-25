from setuptools import setup, find_packages

setup(
    name="tochi",
    version="1.0.0",
    description="tochiDB command line",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["psycopg2","argparse", "http","groq"],
    entry_points={
        "console_scripts": ["tochi=tochi.cli:main",],
    },
    python_requires=">=3.9",
)