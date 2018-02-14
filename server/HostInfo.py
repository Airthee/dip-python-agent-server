# -*- coding: utf8 -*-
import sqlite3

class HostInfo:
  def __init__(self, infos={}):
    self._infos = infos

  def getInfo(self):
    return self._infos

  ###
  # Save record to database
  ###
  def save(self):
    request = "INSERT INTO `host_info` (os,hostname,uptime,cpu_usage,cpu_number,cpu_frequency, ram_size, ram_used) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    infos = self._infos
    print(infos)
    args = (
      infos['os'],
      infos['hostname'],
      infos['uptime'],
      infos['cpu_usage'],
      infos['cpu_number'],
      infos['cpu_frequency'],
      infos['ram_size'],
      infos['ram_used']
    )
    connection = HostInfo.getConnection()    
    c = connection.cursor()
    c.execute(request, args)
    newId = c.lastrowid

    # Partitions
    args = []
    request = "INSERT INTO host_info_partition (host_info_id,device,mountpoint,type,size,used) VALUES(?, ?, ?, ?, ?, ?)"
    for p in infos['partitions']:
      args.append((
        newId,
        p['device'],
        p['mountpoint'],
        p['type'],
        p['size'],
        p['used'],
      ))
    c.executemany(request, args)
    
    # Exécution de la requête
    connection.commit()

  ###
  # Return last record
  ###
  @staticmethod
  def getLast():
    connection = HostInfo.getConnection()
    c=connection.cursor()
    c.execute("SELECT rowId, * FROM host_info ORDER BY rowId DESC LIMIT 1")
    row = c.fetchone()
    print(row)
    if(row != None):
      host = HostInfo()
      
      # Récupération des informations principales
      columns = ['os','hostname','uptime','cpu_usage','cpu_number','cpu_frequency','ram_size','ram_used']
      infos = {}
      for column in columns:
        infos[column] = row[column]

      # Récupération des infos des partitions
      c.execute("SELECT * FROM host_info_partition WHERE host_info_id = ?", [row['rowId']])
      infos['partitions'] = []
      columns = ['device','mountpoint','type','size','used']
      for rowInfoPartition in c.fetchall():
        obj = {}
        for column in columns:
          obj[column] = rowInfoPartition[column]
        infos['partitions'].append(obj)

      # Attribut les infos à l'objet courant
      host._infos = infos
      return host

  ###
  # Return connection to database
  ###
  @staticmethod
  def getConnection(createTables=True):
    # Create tables
    if(createTables):
      HostInfo._createTableIfNotExists()    

    # Return connection
    conn = sqlite3.connect('hosts_infos.db')
    conn.row_factory = sqlite3.Row
    return conn

  ###
  # Créate tables if does'nt exist
  ###
  @staticmethod
  def _createTableIfNotExists():
    connection = HostInfo.getConnection(False)
    c = connection.cursor()

    # Table principale
    c.execute('''
      CREATE TABLE IF NOT EXISTS `host_info` (
        `os` TEXT DEFAULT NULL,
        `hostname` TEXT DEFAULT NULL,
        `uptime` TEXT DEFAULT NULL,
        `cpu_usage` NUMERIC DEFAULT 0,
        `cpu_number` INTEGER DEFAULT 0,
        `cpu_frequency` INTEGER DEFAULT 0,
        `ram_size` INTEGER DEFAULT 0,
        `ram_used` INTEGER DEFAULT 0
      )
    ''')

    # Table de liaison
    c.execute('''
      CREATE TABLE IF NOT EXISTS `host_info_partition` (
        `host_info_id` INTEGER NOT NULL,
        `device` TEXT DEFAULT NULL,
        `mountpoint` TEXT DEFAULT NULL,
        `type` TEXT DEFAULT NULL,
        `size` INTEGER DEFAULT 0,
        `used` NUMERIC DEFAULT 0,
        FOREIGN KEY (`host_info_id`) REFERENCES `host_info`(`id`) ON DELETE CASCADE ON UPDATE CASCADE
      )
    ''')
    connection.commit()
