#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 14:46:23 2018

@author: zhanglemei
"""
try:
    from contextlib import nested  # Python 2
except ImportError:
    from contextlib import ExitStack, contextmanager
import json
import os
output_fname1 = 'dataset1.data'
output_fname2 = 'dataset2.data'

input_file = os.path.expanduser(r"C:\Users\kimme\Git\web-int\src\test.data")

input_fname = 'one-week'+os.sep+'20170101'
rootPath = os.path.abspath('.')
#input_file = rootPath + os.sep + input_fname
counter = 0
print ('>>>Start reading file...')
with open(output_fname1, 'a') as f1:
        with open(output_fname2, 'a') as f2:
            for line in open(input_file):
                counter += 1
                if counter == 100000:
                    break
                obj = json.loads(line.strip())
                try:
                    uid, iid = obj['userId'], obj['id']
                    keywords = obj['keywords'] if 'keywords' in obj else 'None'
                    active_time = str(obj['activeTime']) if 'activeTime' in obj else '0'
                except Exception:
                    continue
                if not keywords=='None':
                    print(",".join([uid, iid, keywords]).encode('utf8'), file=f2)
                if not active_time=='0':
                    #print(",".join([uid, iid, active_time]).encode('utf8'), file=f1)
                    print(uid+","+ iid+","+ str(active_time), file=f1)
print ('>>>Done!')
