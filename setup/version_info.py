#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import src.info as info

app_version = info.__version__
app_version_sep = app_version.split('.')

if len(app_version_sep) < 4:
    app_version_sep.append('0')

prod_vers_final = '({0})'.format(', '.join(app_version_sep))

mask = '0x17'
flags = '0x0'
OS = '0x4'
fileType = '0x1'
subType = '0x0'
date = '(0, 0)'
string_table = '2C0A04B0'
company_name = info.__org_name__
file_description = info.__app_name__
file_version = app_version
int_name = info.__app_name__
legal_copyright = info.__copyright__
original_filename = 'ia.exe'
product_name = info.__app_name__
product_version = app_version
translation = '[11274, 1200]'

version_info_str = """VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={0},
    prodvers={1},
    mask={2},
    flags={3},
    OS={4},
    fileType={5},
    subtype={6},
    date={7}
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '{8}',
        [StringStruct('CompanyName', '{9}'),
        StringStruct('FileDescription', '{10}'),
        StringStruct('FileVersion', '{11}'),
        StringStruct('InternalName', '{12}'),
        StringStruct('LegalCopyright', '{13}'),
        StringStruct('OriginalFilename', '{14}'),
        StringStruct('ProductName', '{15}'),
        StringStruct('ProductVersion', '{16}')])
      ]),
    VarFileInfo([VarStruct('Translation', {17})])
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
    print 'Version Info has been generated.'
