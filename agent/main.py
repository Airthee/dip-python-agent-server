#! /usr/bin/env python3
# -*- coding: utf8 -*-

import requests, json

from HostInfo import HostInfo

def main():
  host = HostInfo()
  # Toutes les 5 minutes
  # Lister les caracteristiques du pc
  r = requests.post('http://127.0.0.1:5000/api', json=host.getInfo())

main()