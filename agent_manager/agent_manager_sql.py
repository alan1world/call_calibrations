#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import sqlite3
from pathlib import Path
#import sys

class AgentDataStore():

    def __init__(self):
        
        self.root_path = '../databases'
        self.dbfile = 'agents.db'
        self.agentdb = Path(self.root_path,self.dbfile)
    
    def site_values(self):

        con = sqlite3.connect(self.agentdb)
        with con:
            cur = con.cursor()
            cur.execute('SELECT ROWID, site FROM sites')
            rows = cur.fetchall()
        return self.reorder(rows)

    def title_values(self):

        con = sqlite3.connect(self.agentdb)
        with con:
            cur = con.cursor()
            cur.execute('SELECT ROWID, title FROM titles')
            rows = cur.fetchall()
        return self.reorder(rows)

    def reorder(self, mylist:list):
        newlist = []
        for list_number, locations in enumerate(mylist,1):
            del locations
            for location in mylist:
                if location[0] == list_number:
                    newlist.append(location[1])
        return newlist

    def agent_values(self,
                    site_list:list=['UK','SA',],
                    status_list:list=['Active', 'Inactive',]):

        con = sqlite3.connect(self.agentdb)
        if not status_list:
            status_list = ['Active',]
        if not site_list:
            site_list = ['UK','SA',]
        with con:
            cur = con.cursor()
            search_status = ','.join('?'*len(status_list))
            search_sites = ','.join('?'*len(site_list))
            searchs = []
            searchs.extend(status_list)
            searchs.extend(site_list)
            query = (f"SELECT agents.display, statuses.status, titles.title, sites.site "
                     f"FROM agents LEFT JOIN statuses ON agents.status = statuses.ROWID "
                     f"LEFT JOIN titles ON agents.title = titles.ROWID "
                     f"LEFT JOIN sites ON agents.site = sites.ROWID "
                     f"WHERE statuses.status IN ({search_status}) "
                     f"AND sites.site IN ({search_sites})")
            cur.execute(query,searchs)
            rows = cur.fetchall()
            #con.commit()
        return rows

