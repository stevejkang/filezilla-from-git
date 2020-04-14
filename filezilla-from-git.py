#-*- coding:utf-8 -*-
# filezilla-from-git.py
#
# Author: stevejkang <iam@juneyoung.io>
# Created at: 2020.03.30

import os
import sys
import pathlib
import subprocess
import xml.etree.cElementTree as ET

FTP_HOST = 'localhost'
FTP_PORT = '22220'
FTP_PTCL = '1' # 0: FTP, 1: SFTP
FTP_TYPE = '0' # DEFAULT
FTP_USER = 'root'
FTP_KEYFILE_PATH = '/home/key.ppk' # ONLY FTP_LOGON_TYPE = 5
FTP_LOGON_TYPE = '5' # 2: Ask for password, 5: Key file
FTP_ENCODING_TYPE = 'Auto' # DEFAULT
FTP_BYPASS_PROXY = '0' # DEFAULT
FTP_NAME = 'SERVER' # NOT NECESSARY
FTP_REMOTE_PATH = '/var/www/html/project/' # Ends with slash(/)

def set_error_message(errorCode, errorTitle, errorInfo):
  print('----------\nError(' + errorCode + '): ' + errorTitle + '\n----------\n\nInfo: ' + errorInfo + '\nUsage: python filezilla-from-git.py <githash>')

def get_file_name(path):
  return os.path.basename(path)

def get_filezilla_path(filePath):
  _remote_full_path = FTP_REMOTE_PATH + filePath
  _path_array = _remote_full_path.split('/')
  _path_array_except_file = _path_array[:-1]
  i = 0
  while i < len(_path_array_except_file):
    if _path_array_except_file[i] != "":
      l = len(_path_array_except_file[i])
      _path_array_except_file.insert(i, l)
      i += 2
    else:
      _path_array_except_file[i] = 1
      i += 1
  _path_array_except_file.insert(1, 0)
  return ' '.join(str(e) for e in _path_array_except_file)

if len(sys.argv) != 2:
  set_error_message('0001', 'Only one argument, "git_hash" is required.', '')
  sys.exit(1)

_git_hash = sys.argv[1]

_git_command = subprocess.Popen('git show ' + _git_hash + ' --pretty=\"format:\" --name-only', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
_git_command_stdout, _git_command_stderr = _git_command.communicate()
_git_command_stdout_string = _git_command_stdout.decode('utf-8')

if 'not a git repository' in _git_command_stdout_string:
  set_error_message('0002', 'Cannot find `.git` folder in this directory.', 'This python script must be placed at the same level as `.git` folder.')
  sys.exit(1)
if 'unknown revision' in _git_command_stdout_string:
  set_error_message('0003', 'Invalid commit hash.', 'Use `git log` to get commit hash.')
  sys.exit(1)

_absolute_path = pathlib.Path(__file__).parent.absolute()
_absolute_path_string = str(_absolute_path)

_git_list = _git_command_stdout_string.split('\n')
_git_list_name_only = _git_command_stdout_string.split('\n')

for x in range(len(_git_list) - 1):
  _git_list[x] = ''.join([_absolute_path_string, '/', _git_list[x]])

_xml_root = ET.Element('FileZilla3')
_xml_queue = ET.SubElement(_xml_root, 'Queue')
_xml_server = ET.SubElement(_xml_queue, 'Server')

ET.SubElement(_xml_server, "Host").text = FTP_HOST
ET.SubElement(_xml_server, "Port").text = FTP_PORT
ET.SubElement(_xml_server, "Protocol").text = FTP_PTCL
ET.SubElement(_xml_server, "Type").text = FTP_TYPE
ET.SubElement(_xml_server, "User").text = FTP_USER
ET.SubElement(_xml_server, "Keyfile").text = FTP_KEYFILE_PATH
ET.SubElement(_xml_server, "Logontype").text = FTP_LOGON_TYPE
ET.SubElement(_xml_server, "EncodingType").text = FTP_ENCODING_TYPE
ET.SubElement(_xml_server, "BypassProxy").text = FTP_BYPASS_PROXY

_xml_file = list()
j = 0
while j < len(_git_list) - 1:
  _xml_file = ET.SubElement(_xml_server, 'File')
  ET.SubElement(_xml_file, "LocalFile").text = _git_list[j]
  ET.SubElement(_xml_file, "RemoteFile").text = get_file_name(_git_list[j])
  ET.SubElement(_xml_file, "RemotePath").text = get_filezilla_path(_git_list_name_only[j])
  ET.SubElement(_xml_file, "Download").text = '0'
  j += 1

tree = ET.ElementTree(_xml_root)
tree.write("queue.xml")

print('DONE')
