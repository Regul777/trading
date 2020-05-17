#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 17:49:57 2020

@author: nishant.gupta
"""

from intrinsic_data import value_investing_data_getter

tickers =  ["NAUKRI.BO",\
            "TATACONSUM.BO",\
            "DIVISLAB.BO",\
            "FEDERALBNK.BO",\
            "BIOCON.BO",\
            "LICHSGFIN.BO",\
            "UBL.BO",\
            "ALKEM.BO",\
            "BALKRISIND.BO",\
            "CUMMINSIND.BO",\
            "NATCOPHARM.BO",\
            "TVSMOTOR.BO",\
            "RBLBANK.BO",\
            "SRTRANSFIN.BO",\
            "BERGEPAINT.BO",\
            "GLAXO.BO",\
            "GLENMARK.BO",\
            "CRISIL.BO",\
            "L&TFH.BO",\
            "PGHH.BO",\
            "GODREJIND.BO",\
            "FRETAIL.BO",\
            "CANBK.BO",\
            "ISEC.BO",\
            "HONAUT.BO",\
            "CROMPTON.BO",\
            "WHIRLPOOL.BO",\
            "NBCC.BO",\
            "IDFCFIRSTB.BO",\
            "M&MFIN.BO",\
            "GMRINFRA.BO",\
            "INDIANB.BO",\
            "ABCAPITAL.BO",\
            "JSWENERGY.BO",\
            "3MINDIA.BO",\
            "BANKINDIA.BO",\
            "PNBHOUSING.BO",\
            "CHOLAHLDNG.BO",\
            "NAM-INDIA.BO",\
            "GODREJAGRO.BO",\
            "COLPAL.BO",\
            "IDBI.BO",\
            "UNIONBANK.BO",\
            "MRF.BO",\
            "VARROC.BO",\
            "NLCINDIA.BO",\
            "GILLETTE.BO",\
            "SJVN.BO",\
            "AUBANK.BO",\
            "KIOCL.BO",\
            "LTI.BO",\
            "MRPL.BO",\
            "SHRIRAMCIT.BO",\
            "CENTRALBK.BO",\
            "ADANIENT.BO",\
            "SUNTV.BO",\
            "AJANTPHARM.BO",\
            "CONCOR.BO",\
            "KANSAINER.BO",\
            "HUDCO.BO",\
            "RAJESHEXPO.BO",\
            "MUTHOOTFIN.BO",\
            "PAGEIND.BO",\
            "BHARATFORG.BO",\
            "MFSL.BO",\
            "ENDURANCE.BO",\
            "CHOLAFIN.BO",\
            "ABFRL.BO",\
            "BAYERCROP.BO",\
            "BAJAJHLDNG.BO",\
            "OFSS.BO",\
            "SUPREMEIND.BO",\
            "MOTILALOFS*.BO",\
            "OIL.BO",\
            "HAL.BO",\
            "EDELWEISS.BO",\
            "VOLTAS.BO",\
            "INDHOTEL.BO",\
            "EMAMILTD*.BO",\
            "AMARAJABAT.BO",\
            "EXIDEIND.BO",\
            "TORNTPHARM.BO",\
            "RAMCOCEM.BO",\
            "MPHASIS.BO",\
            "BEL.BO",\
            "APOLLOHOSP.BO"]

intersting_data_dict, tickers_collated_data, df_mid_cap = value_investing_data_getter.get_interesting_data(tickers)
df_mid_cap.to_excel("mid_cap.xls")
