from setuptools import setup, find_packages
setup(
    name="tools",
    version="1.0.0",
    description="一个做着玩的游戏工具库",
    long_description=open("README.md",encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author="Li Mo",
    author_email="28009663@qq.com",
    license="MIT",
    url="https://github.com/limo1027/mlib/",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    keywords="game development, gamedev, game tools, graphics, rendering, game math, game physics",
)
