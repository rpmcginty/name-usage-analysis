from analysis_functions import *
import data





########################################
# Importing data and setting variables #
########################################

name_mapping, rank_count, rank_id = data.import_data(save=False,try_from_csv=True)
m='M';f='F'
# Splitting all gender data into individual dataframes and dictionaries
id2nm = name_mapping['id2str'][m]
id2nf = name_mapping['id2str'][f]
n2idm = name_mapping['str2id'][m]
n2idf = name_mapping['str2id'][f]
rcm = rank_count[m]
rcf = rank_count[f]
ridm = rank_id[m]
ridf = rank_id[f]
years = np.arange(start=1880,stop=1880+rcm.columns.size)
year_cm = np.array([[(years[i]-years.min())/(years.max()-years.min()) for i in range(len(years))],
                    [0]*len(years),
                    [(years.max()-years[i])/(years.max()-years.min()) for i in range(len(years))]])

# Other Variables
verbose = False
cur_fig = 1

#######################
# Analysis Code Below #
#######################


### Starting basic analysis of rankings and count data ###
if verbose:print("\nStarting Analysis...")
if 0: # calculating basic stuff
    if verbose: print("Plotting total births per year and number of Unique names used per year...")
    #plot_the_basics(rcm,rcf)
    cur_fig+=1
    #plot_top_perc_name_stats(rcm,rcf,fignum=cur_fig)
    cur_fig+=1
    plot_rank_count_values(rc=rcm,fignum=cur_fig,use_intervals=False,lim=50)
    cur_fig+=1
    plot_rank_count_values(rc=rcf,fignum=cur_fig,use_intervals=False,lim=50,ismale=False)
    cur_fig+=1
    plot_usage_vs_prop(rc=rcm,fignum=cur_fig,top=50)
    cur_fig+=1
    plot_usage_vs_prop(rc=rcf,fignum=cur_fig,top=50,ismale=False)
    cur_fig+=1

''' Analysis of yearly differences in rankings '''
if 0:
    rcmdi,rcmdc = calc_yearly_diff(rcm,ridm,load_saved=[True,True],save_file=[True,True],verbose = True,
                                   filename=['MaleRankCountDiffIndex.csv','MaleRankCountDiffCount.csv'])
    rcfdi,rcfdc = calc_yearly_diff(rcf,ridf,load_saved=[True,True],save_file=[True,True],verbose = True,
                                   filename=['FemaleRankCountDiffIndex.csv','FemaleRankCountDiffCount.csv'])
    plot_top_N_diff_values(rcmdi=rcmdi,rcfdi=rcfdi,cur_fig=cur_fig,lims=[5,10,20],use_filt=True,window_len=5)
    cur_fig+=1
    plot_top_N_diff_values(rcmdi=rcmdi,rcfdi=rcfdi,cur_fig=cur_fig,lims=[50,100],use_filt=True,window_len=5)
    cur_fig+=1
    plot_top_N_diff_values(rcmdi=rcmdi[list(range(1985,rcmdi.columns[-1]))],
                           rcfdi=rcfdi[list(range(1985,rcmdi.columns[-1]))],
                           cur_fig=cur_fig,lims=[5,10,20],use_filt=True,window_len=5)
    cur_fig+=1

''' Analysis of historical Individual Name Usage '''
if 1:
    numi,numc = calc_name_usage(rid=ridm,rc=rcm,nid=id2nm,load_saved=[True,True],save_file=[True,True],verbose = True,
                                filename=['MaleNameUsageStatsIndex.csv','MaleNameUsageStatsCount.csv'])
    nufi,nufc = calc_name_usage(rid=ridf,rc=rcf,nid=id2nf,load_saved=[True,True],save_file=[True,True],verbose = True,
                                filename=['FemaleNameUsageStatsIndex.csv','FemaleNameUsageStatsCount.csv'])
    if 0:
        plot_top_name_trajectories(rid_df=ridm,name_usage_df=numi,N=20,cur_fig=cur_fig)
        plot_top_name_trajectories(rid_df=ridf,name_usage_df=nufi,N=20,cur_fig=cur_fig)

    N = 50
    topN_stm = ridm[ridm.columns[0]][0:N]
    topN_endm = ridm[ridm.columns[-1]][0:N]
    topN_both = list(set((topN_stm)+(topN_endm)))


    hrm = numi.min(axis=1)
    highestMeanm = numi.mean(axis=1)
    nameCountTotalsm = numc.sum(axis=1)
    id2attrm = calc_name_features(id2nm=id2nm)


    topN_stf = ridm[ridf.columns[0]][0:N]
    topN_endf = ridm[ridf.columns[0]][0:N]
    topN_bothf = list(set((topN_stf)+(topN_endf)))

    highestRankf = nufi.min(axis=1)
    highestMeanf = nufc.mean(axis=1)
    nameCountTotalsf = nufc.sum(axis=1)
    id2attrf = calc_name_features(id2nm=id2nf)

    # Calculate Number of different Names across
    if 0:
        plot_counts_historic_rank(ridm=ridm,ridf=ridf,N=200,cur_fig=cur_fig)
        cur_fig+=1


    ### Histogram Data
    x = np.array(list(map(lambda x: x[0],id2attrm.values()))) # Letter
    y = np.array(list(map(lambda x: x[1],id2attrm.values()))) # Number of Syllables
    z = np.array(list(map(lambda x: x[2],id2attrm.values()))) # Length of Name

    if 0:
        plot_mf_name_histograms(id2attrm=id2attrm,id2attrf=id2attrf,cur_fig=cur_fig)
        cur_fig+=1

    if 1: # Calculate Name length with First Letter of names
        plot_heatmap_len_vs_letter(id2attr=id2attrm,cur_fig=cur_fig,gender='Males')
        cur_fig+=1
        plot_heatmap_len_vs_letter(id2attr=id2attrm,cur_fig=cur_fig,gender='Females')
        cur_fig+=1

    if 0: # Plotting Syllables and Length
        plot_heatmap_len_vs_syllables(id2attr=id2attrm,cur_fig=cur_fig,gender='Males')
        cur_fig+=1
        plot_heatmap_len_vs_syllables(id2attr=id2attrf,cur_fig=cur_fig,gender='Females')
        cur_fig+=1

    if 1: # Compare General Word usage to word usage from
        letter_freqs = data.import_letters()
        mfreqd = letter_freq(id2nm.values())
        mfreqs = pd.Series(data=list(mfreqd.values()),index=list(mfreqd.keys()))
        ffreqd = letter_freq(id2nf.values())
        ffreqs = pd.Series(data=list(ffreqd.values()),index=list(ffreqd.keys()))


