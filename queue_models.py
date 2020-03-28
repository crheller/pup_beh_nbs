import nems.db as nd

modellist = [
    'psth.fs20.pup-ld-st.pup.fil-ref-psthfr.s_sdexp.S.snl_jk.nf20-basic.t7',
    'psth.fs20.pup-ld-st.pup0.fil-ref-psthfr.s_sdexp.S.snl_jk.nf20-basic.t7',
    'psth.fs20.pup-ld-st.pup.fil0-ref-psthfr.s_sdexp.S.snl_jk.nf20-basic.t7',
    'psth.fs20.pup-ld-st.pup0.fil0-ref-psthfr.s_sdexp.S.snl_jk.nf20-basic.t7',
]

batch = 309
force_rerun = True
cells = nd.get_batch_cells(batch).cellid.tolist()
script = '/auto/users/hellerc/code/NEMS/scripts/fit_single.py'
executable = '/auto/users/hellerc/anaconda3/envs/crh_nems/bin/python'

nd.enqueue_models(celllist=cells,
                  modellist=modellist,
                  batch=batch,
                  force_rerun=force_rerun,
                  script_path=script,
                  executable_path=executable,
                  reserve_gb=1,
                  user='hellerc')

