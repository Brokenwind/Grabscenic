#!/usr/bin/python
# coding: utf-8

__author__ = 'Brokenwind'

from setuptools import setup, find_packages

setup(
      name="Grabscenic",
      version="0.10",
      description="A simple spider to grab China Tourism Information Website",
      author="Brokenwind",
      author_email="wangkun6536@163.com",
      url="https://github.com/Brokenwind/Grabscenic",
      license="LGPL",
      packages=find_packages(),
      scripts=["scenic/StartGrab.py"],
      install_requires=['selenium', 'beautifulsoup4','MySQLdb'],
      keywords=["spider", "china", "tourism"],
)
