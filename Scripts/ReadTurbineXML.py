import numpy as np
import pandas as pd
from lxml import etree

inpath = ("C:\\Users\\JLanini\\OneDrive - DOI\\Documents\\GitHub\\YellowtailOpsModel\\Scripts\\")
if __name__ == '__main__':
    for file in ["YT_U1_2_SmoothCurve.xml", "YT_U_3_4_SmoothCurve.xml", "BuffaloBill_U1_3_SmoothCurve.xml"]:
        data = inpath + file
        tree = etree.parse(data)
        root = tree.getroot()
        # numcurves=int(root[0].attrib['Unit'])
        df_all = pd.DataFrame(columns=['Head', 'Flow', 'Power', 'Efficiency'])
        i = 0
        # add the origin:
        df_all.loc[i] = [0, 0, 0,0]
        i = i + 1
        for curve in tree.iterfind(".//SmoothCurves"):
            for point in curve.iterfind(".//DataPoint"):
                if (float(point.attrib['Power']) == 0):
                    df_all.loc[i] = [float(curve.attrib['Head']), 0, 0, 0]
                else:
                    df_all.loc[i] = [float(curve.attrib['Head']), float(point.attrib['Flow']),
                                     float(point.attrib['Power']), float(point.attrib['Eff'])]
                i = i + 1
        df_all = df_all.apply(pd.to_numeric, errors='coerce')
        fname = file.split('.xml')[0] + ".csv"
        #export data for unit power table method
        df_all.to_csv(inpath + fname)

        ##############################Unit Generator Power Method Tables###############################################
        ################################Best Generator Flow############################################################
        df_best_gen=pd.DataFrame(columns=['Head', 'Flow'])
        for head in df_all['Head'].unique():
            head_table=df_all.loc[df_all['Head'] == head]
            row=head_table['Efficiency'].idxmax()
            df_best_gen.loc[len(df_best_gen)]=head_table.loc[row,['Head', 'Flow']]
        fname = file.split('.xml')[0] + "best_gen.csv"
        # export data for unit power table method
        df_best_gen.to_csv(inpath + fname)
        #################################best generator power###########################################################
        df_best_pow = pd.DataFrame(columns=['Head', 'Power'])
        for head in df_all['Head'].unique():
            head_table = df_all.loc[df_all['Head'] == head]
            row = head_table['Power'].idxmax()
            df_best_pow.loc[len(df_best_pow)] = head_table.loc[row, ['Head', 'Power']]
        fname = file.split('.xml')[0] + "best_pow.csv"
        # export data for unit power table method
        df_best_pow.to_csv(inpath + fname)
        #################################Full Generator Flow###########################################################
        df_full_flow = pd.DataFrame(columns=['Head', 'Flow'])
        for head in df_all['Head'].unique():
            head_table = df_all.loc[df_all['Head'] == head]
            row = head_table['Flow'].idxmax()
            df_full_flow.loc[len(df_full_flow)] = head_table.loc[row, ['Head', 'Flow']]
        fname = file.split('.xml')[0] + "full_flow.csv"
        # export data for unit power table method
        df_full_flow.to_csv(inpath + fname)
        #################################Full Generator Power###########################################################
        df_full_pow = pd.DataFrame(columns=['Head', 'Power'])
        for head in df_all['Head'].unique():
            head_table = df_all.loc[df_all['Head'] == head]
            row = head_table['Power'].idxmax()
            df_full_pow.loc[len(df_full_pow)] = head_table.loc[row, ['Head', 'Power']]
        fname = file.split('.xml')[0] + "full_pow.csv"
        # export data for unit power table method
        df_full_pow.to_csv(inpath + fname)

