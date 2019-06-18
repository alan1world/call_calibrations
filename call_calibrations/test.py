#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import sqlite3, copy, datetime

from pathlib import Path

root_path = '../databases'
dbfile = 'call_calibrations.db'
agentdb = Path(root_path,dbfile)

def get_details(func):
    def wrapper(_search_name):
        con = sqlite3.connect(agentdb)
        with con:
            cur = con.cursor()
            ret_cur = func(cur,_search_name)
            answer = ret_cur.fetchall()
            con.commit()
            return answer
    return wrapper


@get_details
def get_agent_details(cur,agent_name:str):
        cur.execute(f"SELECT rowid, name, site FROM agent_names WHERE name = '{agent_name}'")
        return cur

def fetch_query(func):
    def wrapper(_query,_returns=None):
        con = sqlite3.connect(agentdb)
        with con:
            cur = con.cursor()
            answer = func(cur,_query,_returns)
            con.commit()
            return answer
    return wrapper

@fetch_query
def get_query_details(_cur,_query,_returns=None):
    _cur.execute(_query)
    if _returns == 'one':
        answer = _cur.fetchone()
    elif _returns == 'many':
        answer = _cur.fetchmany()
    elif _returns == 'all':
        answer = _cur.fetchall()
    else:
        answer = True
    return answer

def get_agent_details2(agent_name:str):
    query = f"SELECT rowid, name, site FROM agent_names WHERE name = '{agent_name}'"
    return get_query_details(query,'one')

def get_pos_details2(pos_name:str):
    query = f"SELECT rowid, country FROM point_of_sale WHERE country = '{pos_name}'"
    return get_query_details(query,'one')

@fetch_query
def get_agent_details3(_cur,agent_name,_returns=None):
    _cur.execute(f"SELECT rowid, name, site FROM agent_names WHERE name = '{agent_name}'")
    return _cur.fetchone()

def fetch_query5(func):
    def wrapper(*args,**kwargs):
        arg = list(args)
        #kwarg = 
        con = sqlite3.connect(agentdb)
        with con:
            cur = con.cursor()
            kwargs['cur'] = cur
            arg.insert(0,cur)
            print(arg)
            answer = func(*arg,**kwargs)
            con.commit()
            return answer
    return wrapper

@fetch_query5
def get_agent_details5(*args,**kwargs):
    _cur = kwargs['cur']
    agent_name = kwargs['agent_name']
    print(args)
    print(args[1])
    _cur.execute(f"SELECT rowid, name, site FROM agent_names WHERE name = '{agent_name}'")
    return _cur.fetchone()

@fetch_query5
def get_agent_details5a(*args,**kwargs):
    kwargs['cur'].execute(f"SELECT rowid, name, site FROM agent_names WHERE name = '{kwargs['agent_name']}'")
    return kwargs['cur'].fetchone()

result = get_agent_details("DK")
print(result)
print(get_agent_details2("DK"))
print(get_pos_details2("Australia"))
print(get_agent_details3("DK"))
print(get_agent_details5("DK",agent_name="DK"))
print(get_agent_details5a("DK",agent_name="DK"))