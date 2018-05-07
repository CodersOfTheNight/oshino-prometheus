#!/usr/bin/python
# -*- coding: UTF-8 -*-
from setuptools import setup

from oshino_prometheus.version import get_version


setup(name="oshino_prometheus",
      version=get_version(),
      description="Read metrics from Prometheus",
      author="Šarūnas Navickas",
      author_email="zaibacu@gmail.com",
      packages=["oshino_prometheus"],
      install_requires=["oshino"],
      test_suite="pytest",
      tests_require=["pytest", "pytest-cov", "pytest-asyncio", "prometheus_client"],
      setup_requires=["pytest-runner"]
      )
