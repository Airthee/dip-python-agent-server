# -*- coding: utf8 -*-

import psutil, datetime, platform

class HostInfo:
  def _partitions(self):
    partitions = []
    for p in psutil.disk_partitions():
      usage = psutil.disk_usage(p.mountpoint)
      partitions.append({
        'device': p.device,
        'mountpoint' : p.mountpoint,
        'type': p.fstype,
        'size': usage.total,
        'used': usage.percent
      })
    return partitions

  def getInfo(self):
    # Récupération des infos
    cpuPercent = psutil.cpu_percent(interval=1, percpu=True)
    frequencies = []
    for cpu in psutil.cpu_freq(percpu=True):
      frequencies.append(cpu.current)
    virtualMemory = psutil.virtual_memory()

    # Création de l'objet de retour
    infos = {
      'os': "{} - {}".format(platform.system(), platform.release()),
      'hostname': psutil.users()[0].name,
      'uptime': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
      'cpu_usage' : mean(cpuPercent),
      'cpu_number': psutil.cpu_count(),
      'cpu_frequency': mean(frequencies),
      'ram_size': virtualMemory.total,
      'ram_used': virtualMemory.used,
      'partitions': self._partitions()
    }

    return infos

def mean(list):
  try:
    return float(sum(list) / len(list))
  except ZeroDivisionError:
    return 0
