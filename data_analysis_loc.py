import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

import argparse

def import_dataframe(filename):
    df = pd.read_csv(filename)
    df = df.drop('Unnamed: 0', axis = 1)
    df = df[['trial_num','story','trial_cond','answer','response','corr_resp','story_start',
         'quest_start','time_of_resp','resp_time']]
    return df

def fix_resp_times(df):
    for trial in range(len(df)):
        if (df.loc[trial, 'resp_time']=='timeout') == True:
            df.loc[trial, 'resp_time'] = np.nan
    df.resp_time = pd.to_numeric(df.resp_time)

    return df
    
def split_trials_cond(df):
    belief = []
    photo = []
    timeout_count = 0
    
    for trial in range(len(df)):
        if df.time_of_resp[trial] != 'timeout':
            if df.trial_cond[trial] == 'b':
                belief.append(df.resp_time[trial])
            else:
                photo.append(df.resp_time[trial])
        else:
            timeout_count += 1
    
    return belief, photo, timeout_count

def split_trials_corr(df):
    correct = []
    incorrect = []
    timeout_count = 0
    
    for trial in range(len(df)):
        if df.time_of_resp[trial] != 'timeout':    
            if df.corr_resp[trial] == True:
                correct.append(df.resp_time[trial])
            else:
                incorrect.append(df.resp_time[trial])
        else:
            timeout_count += 1
            
    return correct, incorrect, timeout_count
    
def split_trials_corr_cond(df):
    belief_corr = []
    photo_corr = []
    timeout_count = 0
    
    for trial in range(len(df)):
        if df.time_of_resp[trial] != 'timeout':
            if df.corr_resp[trial] == True:
                if df.trial_cond[trial] == 'b':
                    belief_corr.append(df.resp_time[trial])
                else:
                    photo_corr.append(df.resp_time[trial])
        else:
            timeout_count += 1
    return belief_corr, photo_corr, timeout_count

        
def plot_boxplot(belief, photo, correct, incorrect, belief_corr, photo_corr, timeout_count, filename):
    fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(10,10))
    
    mean = np.nanmean(df.resp_time)
    std = np.nanstd(df.resp_time)
    
    ax[0, 0].boxplot(belief, 0, 'gD')
    ax[0, 0].set_ylim(mean-2*std, mean+2*std)
    ax[0, 0].set_xticks([])
    ax[0, 0].set_title('Belief Stories')

    ax[0, 1].boxplot(photo, 0, 'gD')
    ax[0, 1].set_ylim(mean-2*std, mean+2*std)
    ax[0, 1].set_xticks([])
    ax[0, 1].set_title('Photo Stories')
    
    if len(incorrect) != 0:
        ax[1, 0].boxplot(correct, 0, 'gD')
        ax[1, 0].set_ylim(mean-2*std, mean+2*std)
        ax[1, 0].set_xticks([])
        ax[1, 0].set_title('Correct Responses')

        ax[1, 1].boxplot(incorrect, 0, 'gD')
        ax[1, 1].set_ylim(mean-2*std, mean+2*std)
        ax[1, 1].set_xticks([])
        ax[1, 1].set_title('Incorrect Responses')
    else:
        ax[1, 0].boxplot(correct, 0, 'gD')
        ax[1, 0].set_ylim(mean-2*std, mean+2*std)
        ax[1, 0].set_xticks([])
        ax[1, 0].set_title('Correct Responses')

        ax[1,1].text(0.1, 0.5, "There were no incorrect responses.")
   
    ax[2, 0].boxplot(belief_corr, 0, 'gD')
    ax[2, 0].set_ylim(mean-2*std, mean+2*std)
    ax[2, 0].set_xticks([])
    ax[2, 0].set_title('Correct Belief Stories')

    ax[2, 1].boxplot(photo_corr, 0, 'gD')
    ax[2, 1].set_ylim(mean-2*std, mean+2*std)
    ax[2, 1].set_xticks([])
    ax[2, 1].set_title('Correct Photo Stories')
    ax[2, 1].text(0.7, -0.1, "Timeouts = " + str(timeout_count), 
                   size = 12, transform=ax[2, 1].transAxes)
    ax[2, 1].text(0.7, -0.2, "Trials = " + str(len(belief+photo)+timeout_count), 
                   size = 12, transform=ax[2, 1].transAxes)

    fig.suptitle("Response Times for Trials", fontsize=12)

    image_0 = filename.replace("data/ToM_Loc", "data/boxplots/Image")
    image = image_0.replace(".csv", "_bxplt.png")
    plt.savefig(image)
        
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "Make boxplots of ToM task: RT")
	parser.add_argument(nargs='+', dest='files',
						help="Files from which to produce boxplots"
						)

	args = parser.parse_args()
	
	for file in args.files:
		df = import_dataframe(file)
		df = fix_resp_times(df)
		belief, photo, timeout_count = split_trials_cond(df)
		correct, incorrect, timeout_count = split_trials_corr(df)
		belief_corr, photo_corr, timeout_count = split_trials_corr_cond(df)
		plot_boxplot(belief, photo, correct, incorrect, belief_corr,
					 photo_corr, timeout_count, file)		