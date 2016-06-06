# Tom_localizer

Theory of Mind Localizer- Adapted from MATLAB code provided by Saxe Lab at MIT.

1. tom_loc.py runs task/localizer in PsychoPy, saving json file to directory "behavioral"
2. utils.py contains flicker function for photodiode recording of events
3. behav_process_loc converts behavioral data (.json file) to .csv in "data" directory
4. data_analysis_loc imports .csv file, sorts trials by belief and photo condition, correct and incorrect responses and produces boxplots for comparison (saved in "boxplots" directory)
