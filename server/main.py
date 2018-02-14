#! /usr/bin/env python3
# -*- coding: utf8 -*-

from flask import Flask, render_template, request as flask_request
from HostInfo import HostInfo
import json

# Lancement de l'application
app = Flask(__name__)

# Affichage des données
@app.route('/', methods=['GET'])
def index():
  host = HostInfo.getLast()
  return render_template('index.html', name="Raphael", infos=host.getInfo())

# Création d'un enregistrement
@app.route('/api', methods=['POST'])
def create():
  hostInfo = HostInfo(flask_request.json)
  hostInfo.save()
  return 'success'