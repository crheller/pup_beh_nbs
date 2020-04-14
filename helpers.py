"""
helper function to load and process state model results from the 
pupil behavior dump files e.g. d_307_sdexp_pup_fil.csv
"""

import pandas as pd
import numpy as np
import os

def preprocess_stategain_dump(df_name, batch, full_model=None, p0=None, b0=None, shuf_model=None, octave_cutoff=0.5, r0_threshold=0,
                                 path='/auto/users/hellerc/code/nems_db/'):
    
    db_path = path
    cutoff = octave_cutoff
    
    # load model results data
    dMI = pd.read_csv(os.path.join(db_path, str(batch), df_name), index_col=0)
    try:
        dMI['r'] = [np.float(r.strip('[]')) for r in dMI['r'].values]
        dMI['r_se'] = [np.float(r.strip('[]')) for r in dMI['r_se'].values]
    except:
        pass

    # remove AMT cells
    dMI = dMI[~dMI.cellid.str.contains('AMT')]


    # get task model params / MI
    cols = ['cellid', 'state_chan_alt', 'MI', 'g', 'd', 'r', 'r_se']
    file_merge = dMI[(dMI['state_sig']==full_model) & (dMI['state_chan_alt'].str.contains('ACTIVE'))][cols].merge(\
                    dMI[(dMI['state_sig']==b0) & (dMI['state_chan_alt'].str.contains('ACTIVE'))][cols], \
                    on=['cellid', 'state_chan_alt'])

    file_merge['gain_task'] = file_merge['g_x']
    file_merge['MI_task'] = file_merge['MI_x'] - file_merge['MI_y']
    file_merge['dc_task'] = file_merge['d_x']

    # get sig task cells
    file_merge['sig_task'] = [True if ((file_merge.iloc[i]['r_x'] - file_merge.iloc[i]['r_y']) > 
                                            (file_merge.iloc[i]['r_se_x'] + file_merge.iloc[i]['r_se_y'])) else False for i in range(file_merge.shape[0])]

    # strip extraneous columns
    file_merge = file_merge.drop(columns=[c for c in file_merge.columns if ('_x' in c) | ('_y' in c)])

    # get pupil model params / MI
    pupil_merge = dMI[(dMI['state_sig']==full_model) & (dMI['state_chan_alt']=='pupil')][cols].merge(\
                    dMI[(dMI['state_sig']==p0) & (dMI['state_chan_alt']=='pupil')][cols], \
                    on=['cellid', 'state_chan_alt'])

    pupil_merge['gain_pupil'] = pupil_merge['g_x']
    pupil_merge['MI_pupil'] = pupil_merge['MI_x'] - pupil_merge['MI_y']
    pupil_merge['dc_pupil'] = pupil_merge['d_x']

    # get sig pupil cells
    pupil_merge['sig_pupil'] = [True if ((pupil_merge.iloc[i]['r_x'] - pupil_merge.iloc[i]['r_y']) > 
                                            (pupil_merge.iloc[i]['r_se_x'] + pupil_merge.iloc[i]['r_se_y'])) else False for i in range(pupil_merge.shape[0])]

    # strip extraneous columns
    pupil_merge = pupil_merge.drop(columns=[c for c in pupil_merge.columns if ('_x' in c) | ('_y' in c)])
    pupil_merge = pupil_merge.drop(columns=['state_chan_alt'])
    
    # =========================== get sig sensory cells ============================
    psth_cells = dMI[(dMI.state_sig==shuf_model) & (dMI.r > r0_threshold)].cellid.unique()

    # load BF / SNR data
    dBF = pd.read_csv(db_path+'nems_lbhb/pupil_behavior_scripts/d_{}_tuning.csv'.format(batch), index_col=0)
    dBF.index.name = 'cellid'

    # load tar frequencies
    dTF = pd.read_csv(db_path+'nems_lbhb/pupil_behavior_scripts/d_{}_tar_freqs.csv'.format(batch), index_col=0)

    # merge results into single df for 307 and for 309
    df = file_merge.merge(dTF, on=['cellid', 'state_chan_alt'])
    df = df.merge(pupil_merge, on=['cellid'])
    df.index = df.cellid
    df = df.drop(columns=['cellid'])

    df = df.merge(dBF, left_index=True, right_index=True)

    # add column classifying octave sep. from target
    df['oct_diff'] = abs(np.log2(df['tar_freq'] / df['BF']))

    # add column for on cells / off cells
    df['ON_BF'] = [True if df.iloc[i]['oct_diff']<=cutoff else False for i in range(df.shape[0])]
    df['OFF_BF'] = [True if df.iloc[i]['oct_diff']>cutoff else False for i in range(df.shape[0])]
    
    df['sig_psth'] = df.index.isin(psth_cells)
    
    return df
    
    
    
def preprocess_sdexp_dump(df_name, batch, full_model=None, p0=None, b0=None, shuf_model=None, octave_cutoff=0.5, r0_threshold=0,
                                 path='/auto/users/hellerc/code/nems_db/'):
    db_path = path
    cutoff = octave_cutoff
    
    # load model results data
    dMI = pd.read_csv(os.path.join(db_path, str(batch), df_name), index_col=0)

    try:
        dMI['r'] = [np.float(r.strip('[]')) for r in dMI['r'].values]
        dMI['r_se'] = [np.float(r.strip('[]')) for r in dMI['r_se'].values]
    except:
        pass

    # remove AMT cells
    dMI = dMI[~dMI.cellid.str.contains('AMT')]

    # =================== get task model params / MI ===============================
    cols = ['cellid', 'state_chan_alt', 'MI', 'gain_mod', 'dc_mod', 'r', 'r_se']
    file_merge = dMI[(dMI['state_sig']==full_model) & (dMI['state_chan_alt'].str.contains('ACTIVE'))][cols].merge(\
                    dMI[(dMI['state_sig']==b0) & (dMI['state_chan_alt'].str.contains('ACTIVE'))][cols], \
                    on=['cellid', 'state_chan_alt'])

    file_merge['gain_task'] = file_merge['gain_mod_x'] - file_merge['gain_mod_y']
    file_merge['MI_task'] = file_merge['MI_x'] - file_merge['MI_y']
    file_merge['dc_task'] = file_merge['dc_mod_x'] - file_merge['dc_mod_y']

    file_merge['sig_task'] = [True if ((file_merge.iloc[i]['r_x'] - file_merge.iloc[i]['r_y']) > 
                                           (file_merge.iloc[i]['r_se_x'] + file_merge.iloc[i]['r_se_y'])) else False for i in range(file_merge.shape[0])]


    # strip extraneous columns
    file_merge = file_merge.drop(columns=[c for c in file_merge.columns if ('_x' in c) | ('_y' in c)])

    # ======================= get pupil model params / MI =========================
    pupil_merge = dMI[(dMI['state_sig']==full_model) & (dMI['state_chan_alt']=='pupil')][cols].merge(\
                    dMI[(dMI['state_sig']==p0) & (dMI['state_chan_alt']=='pupil')][cols], \
                    on=['cellid', 'state_chan_alt'])

    pupil_merge['gain_pupil'] = pupil_merge['gain_mod_x'] - pupil_merge['gain_mod_y']
    pupil_merge['MI_pupil'] = pupil_merge['MI_x'] - pupil_merge['MI_y']
    pupil_merge['dc_pupil'] = pupil_merge['dc_mod_x'] - pupil_merge['dc_mod_y']

    pupil_merge['sig_pupil'] = [True if ((pupil_merge.iloc[i]['r_x'] - pupil_merge.iloc[i]['r_y']) > 
                                            (pupil_merge.iloc[i]['r_se_x'] + pupil_merge.iloc[i]['r_se_y'])) else False for i in range(pupil_merge.shape[0])]

    # strip extraneous columns
    pupil_merge = pupil_merge.drop(columns=[c for c in pupil_merge.columns if ('_x' in c) | ('_y' in c)])
    pupil_merge = pupil_merge.drop(columns=['state_chan_alt'])

    # =========================== get sig sensory cells ============================
    psth_cells = dMI[(dMI.state_sig==shuf_model) & (dMI.r > r0_threshold)].cellid.unique()

    # load BF / SNR data
    dBF = pd.read_csv(db_path+'nems_lbhb/pupil_behavior_scripts/d_{}_tuning.csv'.format(batch), index_col=0)
    dBF.index.name = 'cellid'

    # load tar frequencies
    dTF = pd.read_csv(db_path+'nems_lbhb/pupil_behavior_scripts/d_{}_tar_freqs.csv'.format(batch), index_col=0)

    # merge results into single df
    df = file_merge.merge(dTF, on=['cellid', 'state_chan_alt'])
    df = df.merge(pupil_merge, on=['cellid'])
    df.index = df.cellid
    df = df.drop(columns=['cellid'])

    df = df.merge(dBF, left_index=True, right_index=True)

    # add column classifying octave sep. from target
    df['oct_diff'] = abs(np.log2(df['tar_freq'] / df['BF']))

    # add column for on cells / off cells
    df['ON_BF'] = [True if df.iloc[i]['oct_diff']<=cutoff else False for i in range(df.shape[0])]
    df['OFF_BF'] = [True if df.iloc[i]['oct_diff']>cutoff else False for i in range(df.shape[0])]

    df['sig_psth'] = df.index.isin(psth_cells)
    
    return df