import nems.db as nd

batch = 307
first_passive = False
sdexp = True
stategain = False
force_rerun = False

if stategain == sdexp:
    raise ValueError
# sdexp models
if sdexp:
    modellist = [
        'psth.fs20.pup-ld-st.pup.afl-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.afl-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.afl0-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.afl0-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.afl.pxf-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.afl.pxf-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.afl0.pxf-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.afl.pxf0-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.afl0.pxf-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.afl0.pxf0-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.afl.pxf0-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.afl0.pxf0-ref-psthfr.s_sdexp.S_jk.nf20-basic',    
        'psth.fs20.pup-ld-st.pup.fil-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.fil-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.fil0-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.fil0-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.fil.pxf-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.fil.pxf-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.fil0.pxf-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.fil.pxf0-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.fil0.pxf-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.fil0.pxf0-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.fil.pxf0-ref-psthfr.s_sdexp.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.fil0.pxf0-ref-psthfr.s_sdexp.S_jk.nf20-basic'  
    ]

if stategain:
    # stategain models
    modellist = [
        'psth.fs20.pup-ld-st.pup.afl-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.afl-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.afl0-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.afl0-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.afl.pxf-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.afl.pxf-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.afl0.pxf-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.afl.pxf0-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.afl0.pxf-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.afl0.pxf0-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.afl.pxf0-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.afl0.pxf0-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.fil-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.fil-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.fil0-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.fil0-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.fil.pxf-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.fil.pxf-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.fil0.pxf-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.fil.pxf0-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.fil0.pxf-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup.fil0.pxf0-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.fil.pxf0-ref-psthfr.s_stategain.S_jk.nf20-basic',
        'psth.fs20.pup-ld-st.pup0.fil0.pxf0-ref-psthfr.s_stategain.S_jk.nf20-basic',
    ]

if first_passive:
    modellist = [m.replace('-ld-st', '-ld-ap1-st') for m in modellist]
    
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

