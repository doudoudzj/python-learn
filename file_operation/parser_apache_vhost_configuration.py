#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - 2018, doudoudzj
# All rights reserved.
#

"""Package for parser Apache VirtualHost configuration.
"""

import os.path
import re
import string
import sys

DIRECTIVES = {
    'Directory': '',
    'Files': '',
    'Limit': '',
    'Location': '',
    'VirtualHost': ''
}

OPTIONS = {
    'ServerAdmin': 'admin@localhost',
    'ServerName': 'www',
    'DocumentRoot': '/var/www',
    'Indexs': '',
    'Options': '',
    'ServerAlias': '',
    'Location': '',
    'SuexecUserGroup': '',
}

DIRECTORY = {
    'Options': 'Indexes FollowSymLinks MultiViews',
    'AllowOverride': 'None',
    'Order': 'allow,deny',
    'Allow': 'from all',
}


def _load_virtualhost(conf=''):
    '''parser VirtualHost config to object (array)
    '''
    try:
        if not conf:
            sys.exit('need conf file')
        if not os.path.isfile(conf):
            sys.exit('Unknown file %s' % conf)
    except OSError:
        pass

    with open(conf, 'r') as f:
        lines = f.readlines()
        data = filter(lambda i: re.search('^((?!#).)*$', i), lines)

    id_v = 0
    enable = False
    virtualHosts = []
    vhost = []
    result = {}
    id_d = 0
    enable_d = False
    v_dirs = {}
    result_d = {}
    directorys = {}  # 附加信息
    line_disabled = False
    gen_by_vpsmate = False
    match_start = re.compile(r'<VirtualHost(\s+)(\S+)>')
    match_end = re.compile(r'</VirtualHost>')
    match_start_d = re.compile(r'<Directory(\s+)(\S+)>')
    match_end_d = re.compile(r'</Directory>')
    while len(data) > 0:
        out = data.pop(0)

        # start of VirtualHost
        match = match_start.search(out)
        if match:  # if '<VirtualHost' in out:
            id_d = 0
            v_dirs = {}
            result_d[id_v] = []
            directorys[id_v] = []
            name_port = match.groups()[1].strip(' ').strip('"').strip('\'')
            ip, port = name_port.split(':')
            vhost.append(ip)
            vhost.append(port)
            enable = True
            enable_d = False
            continue

        # start of Directory
        match_d = match_start_d.search(out)
        if enable is True and match_d:
            v_dirs = {}
            path = match_d.groups()[1].strip()
            v_dirs[id_d] = []
            v_dirs[id_d].append(path)
            enable_d = True
            continue

        # end of Directory
        if enable_d is True and match_end_d.search(
                out):  # if '</Directory>' in out:
            result_d[id_v].append(v_dirs[id_d])
            id_d += 1
            enable_d = False
            v_dirs = {}
            continue

        # merge of Directory
        if enable_d:
            v_dirs[id_d].append(out)
            continue

        # end of VirtualHost
        if match_end.search(out):
            enable_d = False

            result[id_v] = vhost
            if id_v in result_d:
                d = _append_directory(result_d[id_v])
                directorys[id_v] = d
            else:
                directorys[id_v] = []
            id_v += 1
            enable = False
            vhost = []
            continue

        if enable:
            vhost.append(out)
            continue
    # print('directorys', directorys)
    for i in result:
        server = {
            'IP': result[i][0],  # IP
            'Port': result[i][1],  # Port
            'Directory': directorys[i]
        }
        for line in result[i]:
            for i in OPTIONS:
                if i in line:
                    if i in ['ServerAlias', 'DirectoryIndex']:
                        server[i] = ' '.join(str(n) for n in line.split()[1:])
                    else:
                        server[i] = line.split()[1].strip(string.punctuation)
                    continue
        virtualHosts.append(server)

    return virtualHosts


def _append_directory(res):
    directorys = []
    for r in res:
        directory = {'Path': r[0]}
        for line in r:
            for i in DIRECTORY:
                if i in line:
                    if i in ['Order']:
                        directory[i] = ','.join(
                            str(n) for n in line.split()[1:])
                    elif i in ['Options', 'Allow']:
                        directory[i] = ' '.join(
                            str(n) for n in line.split()[1:])
                    else:
                        directory[i] = line.split()[1].strip(
                            string.punctuation)
                    continue
        directorys.append(directory)

    return directorys


if __name__ == '__main__':
    aaa = '/Users/doudoudzj/Projects/test/aaa.com.conf'
    bbb = '/Users/doudoudzj/Projects/test/httpd.conf'
    print _load_virtualhost(aaa)
    # _load_virtualhost(aaa)

    # for key in OPTIONS:
    #     # print(key)
    #     if key in ['ServerName', 'DocumentRoot']:
    #         print key

    # _load_directory(aaa)
    # print _load_directory(aaa)
