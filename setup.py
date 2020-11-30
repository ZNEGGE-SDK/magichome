#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: zengge
# Mail: cnzengge@gmail.com
# Created Time:  2019-10-16 10:10:08
#############################################

from setuptools import setup, find_packages           

setup(
    name = "magichome",      
    version = "0.1.79", 
    keywords = ("pip", "magichome","Zengge smart Home"),
    description = "Magic Home Smart API",
    long_description = "Magic Home Smart Controller API",
    license = "MIT",
    url = "https://github.com/ZNEGGE-SDK/magichome",     
    author = "zengge",
    author_email = "cnzengge@gmail.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests","uuid"]         
)
