#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import sqlite3, copy, datetime

from pathlib import Path

class CalibrationStore():

    def __init__(self):
        
        self.root_path = '../databases'
        self.dbfile = 'call_calibrations.db'
        self.agentdb = Path(self.root_path,self.dbfile)

    def agent_values(self):

        con = sqlite3.connect(self.agentdb)
        with con:
            cur = con.cursor()
            cur.execute('SELECT name FROM agent_names')
            rows = cur.fetchall()
        output_list = []
        for row in rows:
            output_list.append(row[0])
        return output_list
        #return self.reorder(rows)

    def pos_values(self):

        con = sqlite3.connect(self.agentdb)
        with con:
            cur = con.cursor()
            cur.execute('SELECT country FROM point_of_sale')
            rows = cur.fetchall()
        output_list = []
        for row in rows:
            output_list.append(row[0])
        return output_list
    
    def calibration_values(self):

        con = sqlite3.connect(self.agentdb)
        with con:
            cur = con.cursor()
            query = (f"SELECT "
                     #f"STRFTIME('%W', cc.date_calibrated), "
                     #f"STRFTIME('%m', cc.date_calibrated), "
                     #f"STRFTIME('%Y', cc.date_calibrated), "
                     f"cc.date_calibrated, "
                     f"agn.name, agn.site, pos.country, CAST(cc.score AS text), "
                     f"CAST(cc.InteractionFlow AS text), "
                     f"CAST(cc.firstcontactresolution AS text), "
                     f"CAST(cc.Communication AS text), "
                     f"CAST(cc.CustomerFocus AS text), "
                     f"CAST(cc.Demeanor AS text), "
                     f"cc.Feedback, cc.ManagerReview, cc.ReviewedwithManager, "
                     f"cc.Coachingdate, cc.Reviewdate, cc.Flight, "
                     f"cc.Hotel, cc.Rail, cc.Car "
                     f"FROM call_calibrations AS cc "
                     f"INNER JOIN agent_names AS agn ON cc.agent = agn.ROWID "
                     f"INNER JOIN point_of_sale AS pos ON cc.point_of_sale = pos.ROWID "
                    )
            cur.execute(query)
            rows = cur.fetchall()
        return rows
    
    def calibration_filter(self, filter_agent, filter_site, filter_year,
                            filter_month, filter_week):

        if filter_site == 'Any':
            filter_site = "'UK', 'SA', 'NK'"
        else:
            filter_site = f"'{filter_site}'"
        if filter_year == 'Any':
            filter_year = "'2018', '2019'"
        else:
            filter_year = f"'{filter_year}'"
        if filter_month == 0:
            filter_month_start = "01"
            filter_month_end = "12"
        else:
            filter_month_start = f"{filter_month:02d}"
            filter_month_end = f"{filter_month:02d}"
        if filter_week == 0:
            filter_week_start = 0 #"00"
            filter_week_end = 53 #"53"
        else:
            filter_week_start = filter_week #f"{filter_week:02d}"
            filter_week_end = filter_week #f"{filter_week:02d}"
        filter_person_output = ""
        if filter_agent == 'Any':
            for person in self.agent_values():
                if "\'" in person:
                    person = person.replace("\'", "\'\'")
                filter_person_output += f"'{person}',"
            filter_person_output = filter_person_output[:-1]
        else:
            if "\'" in filter_agent:
                    filter_agent = filter_agent.replace("\'", "\'\'")
            filter_person_output = f"'{filter_agent}'"
        con = sqlite3.connect(self.agentdb)
        with con:
            cur = con.cursor()
            query = (f"SELECT "
                     f"cc.date_calibrated, "
                     f"agn.name, agn.site, pos.country, CAST(cc.score AS text), "
                     f"CAST(cc.InteractionFlow AS text), "
                     f"CAST(cc.firstcontactresolution AS text), "
                     f"CAST(cc.Communication AS text), "
                     f"CAST(cc.CustomerFocus AS text), "
                     f"CAST(cc.Demeanor AS text), "
                     f"cc.Feedback, cc.ManagerReview, cc.ReviewedwithManager, "
                     f"cc.Coachingdate, cc.Reviewdate, cc.Flight, "
                     f"cc.Hotel, cc.Rail, cc.Car,  "
                     f"CAST(cc.rowid AS text) "
                     f"FROM call_calibrations AS cc "
                     f"INNER JOIN agent_names AS agn ON cc.agent = agn.ROWID "
                     f"INNER JOIN point_of_sale AS pos ON cc.point_of_sale = pos.ROWID "
                     f"WHERE agn.site IN ({filter_site}) AND "
                     f"agn.name IN ({filter_person_output}) AND "
                     f"strftime('%m', cc.date_calibrated) >= '{filter_month_start}' AND "
                     f"strftime('%m', cc.date_calibrated) <= '{filter_month_end}' AND "
                     f"strftime('%Y', cc.date_calibrated) IN ({filter_year}) AND "
                     f"cc.week >= {filter_week_start} AND "
                     f"cc.week <= {filter_week_end} "
                     #f"strftime('%W', cc.date_calibrated) >= '{filter_week_start}' AND "
                     #f"strftime('%W', cc.date_calibrated) <= '{filter_week_end}' "
                    )
            cur.execute(query)
            rows = cur.fetchall()
        return rows

    def insert_pos(self, new_pos) -> None:

        con = sqlite3.connect(self.agentdb)
        with con:
            cur = con.cursor()
            cur.execute('INSERT OR IGNORE INTO point_of_sale (country) VALUES (?)', (new_pos,))
            con.commit()
    
    def insert_agent(self, new_name:str) -> None:

        con = sqlite3.connect(self.agentdb)
        with con:
            cur = con.cursor()
            cur.execute('INSERT OR IGNORE INTO agent_names (name, site) VALUES (?,?)', 
                        (new_name, 'NK'))
            con.commit()

    def set_site(self, agent_name:str, new_site:str):
        con = sqlite3.connect(self.agentdb)
        with con:
            cur = con.cursor()
            cur.execute(f"UPDATE agent_names SET site='{new_site}' WHERE name = '{agent_name}'")
            #answer = cur.fetchone()
            con.commit()

    def get_agent_details(self, agent_name:str) -> tuple:
        con = sqlite3.connect(self.agentdb)
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT rowid, name, site FROM agent_names WHERE name = '{agent_name}'")
            answer = cur.fetchone()
            con.commit()
        return answer

    def get_pos_details(self, pos_name:str) -> tuple:
        con = sqlite3.connect(self.agentdb)
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT rowid, country FROM point_of_sale WHERE country = '{pos_name}'")
            answer = cur.fetchone()
            con.commit()
        return answer

    def export_weekly_score(self, year_in:str='2019', week_in:int=3):
        con = sqlite3.connect(self.agentdb)
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT AVG(cc.score), AVG(cc.InteractionFlow), "
                        f"AVG(cc.FirstcontactResolution), AVG(cc.Communication), "
                        f"AVG(cc.CustomerFocus), AVG(cc.Demeanor) "
                        f"FROM call_calibrations AS cc "
                        f"WHERE cc.week = {week_in} AND "
                        f"strftime('%Y', cc.date_calibrated) = '{year_in}'")
            answer = cur.fetchone()
            #rows = cur.fetchall()
            con.commit()
        return answer

    def insert_calibration(self, in_cal) -> None:
        con = sqlite3.connect(self.agentdb)
        new_cal = copy.deepcopy(in_cal)
        cal_date = datetime.datetime.strptime(new_cal['date'],'%d/%m/%Y')
        new_cal['week'] = cal_date.strftime('%V')
        new_cal['out_date'] = cal_date.date()
        try:
            new_cal['agentid'] = self.get_agent_details(new_cal['agent'])[0]
        except:
            new_cal['agentid'] = -1
        try:
            new_cal['pos'] = self.get_pos_details(new_cal['pointofsale'])[0]
        except:
            new_cal['pos'] = -1
        if new_cal['flight'] == 2:
            new_cal['flight'] = 'Flight'
        else:
            new_cal['flight'] = None
        if new_cal['hotel'] == 2:
            new_cal['hotel'] = 'Hotel'
        else:
            new_cal['hotel'] = None
        if new_cal['rail'] == 2:
            new_cal['rail'] = 'Rail'
        else:
            new_cal['rail'] = None
        if new_cal['car'] == 2:
            new_cal['car'] = 'Car'
        else:
            new_cal['car'] = None
        with con:
            cur = con.cursor()
            table_listing = ('date_calibrated','week','agent','AgentName','point_of_sale','Flight','Hotel','Rail','Car','Score','FirstcontactResolution','InteractionFlow',
                            'Communication','CustomerFocus','Demeanor','Feedback','ManagerReview','ReviewedwithManager','Coachingdate','Reviewdate')
            cur.execute(f'INSERT OR IGNORE INTO call_calibrations {table_listing} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', 
                            (new_cal['out_date'],new_cal['week'],new_cal['agentid'],new_cal['agent'],new_cal['pos'],new_cal['flight'],new_cal['hotel'],new_cal['rail'],
                             new_cal['car'],new_cal['score'],new_cal['firstcontact'],new_cal['interactionflow'],new_cal['communication'],new_cal['customerfocus'],
                             new_cal['demeanor'],new_cal['feedback'],new_cal['managerreview'],new_cal['reviewedwithmanager'],new_cal['coaching'],new_cal['reviewdate']))
            con.commit()

    #def weekly_breakdown(self):

        #con = sqlite3.connect(self.agentdb)
        #with con:
            #cur = con.cursor()
            #cur.execute('SELECT country FROM point_of_sale')
            #rows = cur.fetchall()
        #output_list = []
        #for row in rows:
            #output_list.append(row[0])
        #return output_list

    #def monthly_breakdown(self):

        #con = sqlite3.connect(self.agentdb)
        #with con:
            #cur = con.cursor()
            #cur.execute('SELECT country FROM point_of_sale')
            #rows = cur.fetchall()
        #output_list = []
        #for row in rows:
            #output_list.append(row[0])
        #return output_list
