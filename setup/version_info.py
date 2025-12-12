#!/usr/bin/env python

from __future__ import absolute_import

import sys, os

# Agregar paquete info a PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join('..', 'src')))

from info import app_info

app_version = app_info.__version__
app_version_sep = app_version.split('.')

for i in xrange(0, 4 - len(app_version_sep)):
        app_version_sep.append('0')

prod_vers_final = '({})'.format(', '.join(app_version_sep))

mask = '0x17'
flags = '0x0'
OS = '0x4'
fileType = '0x1'
subType = '0x0'
date = '(0, 0)'
string_table = '2C0A04B0'
company_name = app_info.__org_name__
file_description = app_info.__app_name__
file_version = app_version
int_name = app_info.__app_name__
legal_copyright = app_info.__copyright__
original_filename = 'ia.exe'
product_name = app_info.__app_name__
product_version = app_version
translation = '[11274, 1200]'

version_info_str = """VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={},
    prodvers={},
    mask={},
    flags={},
    OS={},
    fileType={},
    subtype={},
    date={}
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '{}',
        [StringStruct('CompanyName', '{}'),
        StringStruct('FileDescription', '{}'),
        StringStruct('FileVersion', '{}'),
        StringStruct('InternalName', '{}'),
        StringStruct('LegalCopyright', '{}'),
        StringStruct('OriginalFilename', '{}'),
        StringStruct('ProductName', '{}'),
        StringStruct('ProductVersion', '{}')])
      ]),
    VarFileInfo([VarStruct('Translation', {})])
  ]
)""".format(prod_vers_final,
            prod_vers_final,
            mask,
            flags,
            OS,
            fileType,
            subType,
            date,
            string_table,
            company_name,
            file_description,
            file_version,
            int_name,
            legal_copyright,
            original_filename,
            product_name,
            product_version,
            translation
            )

with open('version_info.txt', 'w') as vi:
    vi.write(version_info_str)
    print 'Información de versión generada.'
