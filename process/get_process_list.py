# -*- coding: utf-8 -*-
#
# Copyright (c), doudoudzj
# All rights reserved.
#


import os


def get_process_list():
    '''获取进程列表'''
    p = []
    for subdir in os.listdir('/proc'):
        if subdir.isdigit():
            pn = get_process_name(subdir)
            if pn:
                p.append({'pid': int(subdir), 'name': pn})
    return {'process': p, 'total': len(p)}


def get_process_name(pid):
    '''提取进程名字'''
    if not pid:
        return False
    name = None
    comm = '/proc/%s/comm' % pid
    if os.path.exists(comm):
        with open(comm, 'r') as f:
            line = f.readline()
            name = line.strip()
    if not name:
        sched = '/proc/%s/sched' % pid
        if os.path.exists(sched):
            with open(sched, 'r') as f:
                line = f.readline()
                name = line.split()[0]
    if not name:
        status = '/proc/%s/status' % pid
        if os.path.exists(status):
            with open(status, 'r') as f:
                line = f.readline()
                name = line.split()[1]
    if not name:
        stat = '/proc/%s/stat' % pid
        if os.path.exists(stat):
            with open(stat, 'r') as f:
                # name = line.strip()
                # name = line.replace('(','').replace(')','')
                line = f.readline()
                line = line.split()[1]
                if line[0] == '(':
                    line = line[1:]
                if line[-1] == ')':
                    line = line[:-1]
                name = line
    return name


if __name__ == '__main__':
    pids = get_process_list()
    print(pids)
