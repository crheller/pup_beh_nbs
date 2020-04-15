"""
Various different models. Need to decide which gives the cleanest, most interpretable 
results for the on / off gain/mi analysis.

    models: for both stategain and sdexp
        fil
        afl
        afl + pxf

    (so we have 6 total models, two batches)

as of making this file (04 / 14 / 2020). The cleanest task results have been 
observed using stategain per file. However, using perfile seems to underestimate
the influence of pupil bc the passive file epochs can take care of a lot of
this.
"""

import helpers as helper
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from nems import get_setting
path = get_setting('NEMS_RESULTS_DIR')

fig_path = '/auto/users/hellerc/results/pup_beh_ms/'

batch = 309
r0_threshold = 0
octave_cutoff = 0.5
use_sig_from = None #'d_pup_afl_pxf_stategain.csv'  # model fit to determine significance
first_passive = False               # models fit on data with first passive only + actives
group_files = False

sg_fns = ['d_pup_fil_stategain.csv',
          'd_pup_afl_stategain.csv',
          'd_pup_afl_pxf_stategain.csv']
sd_fns = ['d_pup_fil_sdexp.csv',
          'd_pup_afl_sdexp.csv',
          'd_pup_afl_pxf_sdexp.csv']
model_strings = ['st.pup.fil',
                 'st.pup.afl',
                 'st.pup.afl.pxf']
p0_models = ['st.pup0.fil',
             'st.pup0.afl',
             'st.pup0.afl.pxf0']
b0_models = ['st.pup.fil0',
             'st.pup.afl0',
             'st.pup.afl0.pxf0']
shuf_models = ['st.pup0.fil0',
               'st.pup0.afl0',
               'st.pup0.afl0.pxf0']

if first_passive:
    sg_fns = [s.replace('.csv', '_ap1.csv') for s in sg_fns]
    sd_fns = [s.replace('.csv', '_ap1.csv') for s in sd_fns]

iter_obj = zip(sg_fns, sd_fns, model_strings, p0_models, b0_models, shuf_models)
all_results = {}
for i, (sg_fn, sd_fn, model_string, p0_model, b0_model, shuf_model) in enumerate(iter_obj):

    sg1 = helper.preprocess_stategain_dump(sg_fn, 
                                        batch=batch,
                                        full_model=model_string,
                                        p0=p0_model,
                                        b0=b0_model,
                                        shuf_model=shuf_model,
                                        r0_threshold=r0_threshold,
                                        octave_cutoff=octave_cutoff,
                                        path=path)

    sd1 = helper.preprocess_sdexp_dump(sd_fn, 
                                        batch=batch,
                                        full_model=model_string,
                                        p0=p0_model,
                                        b0=b0_model,
                                        shuf_model=shuf_model,
                                        r0_threshold=r0_threshold,
                                        octave_cutoff=octave_cutoff,
                                        path=path)

    if use_sig_from is not None:
        if 'sdexp' in use_sig_from:
            sig_df = helper.preprocess_sdexp_dump(use_sig_from, 
                                                batch=batch,
                                                full_model=model_strings[np.argwhere(np.array(sd_fns)==use_sig_from)[0][0]],
                                                p0=p0_models[np.argwhere(np.array(sd_fns)==use_sig_from)[0][0]],
                                                b0=b0_models[np.argwhere(np.array(sd_fns)==use_sig_from)[0][0]],
                                                shuf_model=shuf_models[np.argwhere(np.array(sd_fns)==use_sig_from)[0][0]],
                                                r0_threshold=r0_threshold,
                                                octave_cutoff=octave_cutoff,
                                                path=path)
        elif 'stategain' in use_sig_from:
            sig_df = helper.preprocess_stategain_dump(use_sig_from, 
                                                batch=batch,
                                                full_model=model_strings[np.argwhere(np.array(sg_fns)==use_sig_from)[0][0]],
                                                p0=p0_models[np.argwhere(np.array(sg_fns)==use_sig_from)[0][0]],
                                                b0=b0_models[np.argwhere(np.array(sg_fns)==use_sig_from)[0][0]],
                                                shuf_model=shuf_models[np.argwhere(np.array(sg_fns)==use_sig_from)[0][0]],
                                                r0_threshold=r0_threshold,
                                                octave_cutoff=octave_cutoff,
                                                path=path)
        task_cells = sig_df.index[sig_df['sig_task']].unique()
        pupil_cells = sig_df.index[sig_df['sig_pupil']].unique()
        sg1['sig_task'] = [True if c in task_cells else False for c in sg1.index]
        sd1['sig_task'] = [True if c in task_cells else False for c in sd1.index]
        sg1['sig_pupil'] = [True if c in pupil_cells else False for c in sg1.index]
        sd1['sig_pupil'] = [True if c in pupil_cells else False for c in sd1.index]


    # save results to dictionary to prevent reloading
    all_results[sg_fn.replace('.csv', '')] = sg1
    all_results[sd_fn.replace('.csv', '')] = sd1

    # plot individual model results
    f, ax = helper.stripplot_df(sg1, group_files=group_files)
    f.canvas.set_window_title(sg_fn)
    f, ax = helper.stripplot_df(sd1, group_files=group_files)
    f.canvas.set_window_title(sd_fn)


# compare significant cells between model fits
task_sig = np.zeros((len(sg_fns) * 2, len(sg1.index.unique())))
pup_sig = np.zeros((len(sg_fns) * 2, len(sg1.index.unique())))
for i, m in enumerate(all_results.keys()):
    task_sig[i, :] = all_results[m]['sig_task'].groupby(by='cellid').mean().values
    pup_sig[i, :] = all_results[m]['sig_pupil'].groupby(by='cellid').mean().values

f, ax = plt.subplots(2, 1, figsize=(12, 4))

ax[0].set_title('Task sig. units')
ax[0].imshow(task_sig, aspect='auto')
ax[0].set_yticks(np.arange(0, task_sig.shape[0]))
ax[0].set_yticklabels(all_results.keys(), fontsize=8)

ax[1].set_title('Pupil sig. units')
ax[1].imshow(pup_sig, aspect='auto')
ax[1].set_xlabel('cellid')
ax[1].set_yticks(np.arange(0, task_sig.shape[0]))
ax[1].set_yticklabels(all_results.keys(), fontsize=8)

f.tight_layout()

# compare phi / MI between stategain and sdexp



plt.show()
