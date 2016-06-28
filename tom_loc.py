import sys
import json
from psychopy import visual, gui, event, core
import random
import numpy as np

from utils import flicker

class Stimuli:
	def __init__(self, win, timing):
		self.win = win
		self.timing = timing
		self.keymap = {'left': 1, 'right': 0} #1 is True, 0 is False
		
	def show_story(self, trial):
		story_start = core.getTime()
		text = self.text(trial)
		self.win.flip()
		offset = flicker(self.win, 1)
		core.wait(self.timing['story'] - offset)
		text.autoDraw = False
		self.win.flip()
		self.win.flip()
		return story_start
		
	def show_question(self, trial):
		text = self.text(trial)
		quest_start = core.getTime()
		self.win.flip()
		offset = flicker(self.win, 4)
		key = event.waitKeys(
					maxWait=self.timing['question'] - offset, keyList=self.keymap.keys() + ['escape'])
		if key is None:
			text.autoDraw = False
			self.win.flip()
			self.win.flip()
			return(quest_start, 'timeout', 'timeout')
		elif key == 'escape':
			flicker(self.win, 0)
			core.quit()
		else:
			text.autoDraw = False
			self.win.flip()
			self.win.flip()
			time_of_resp = core.getTime()
			offset = flicker(self.win, 16)
			return (quest_start, self.keymap[key[0]], time_of_resp)		
		
	def text_and_stim_keypress(self, text, stim=None):
		if stim is not None:
			if type(stim) == list:
				map(lambda x: x.draw(), stim)
			else:
				stim.draw()
		display_text = visual.TextStim(self.win, text=text,
										font='Helvetica', alignHoriz='center',
										alignVert='center', units='norm',
										pos=(0, 0), height=0.1,
										color=[255, 255, 255], colorSpace='rgb255',
										wrapWidth=2)
		display_text.draw()
		self.win.flip()
		key = event.waitKeys()
		if key[0] == 'escape':
			flicker(self.win, 0)
			core.quit()
			self.win.flip()
		self.win.flip()
		
	def text(self, text):
		display_text = visual.TextStim(self.win, text=text,
                                       font='Helvetica', alignHoriz='center',
                                       alignVert='center', units='norm',
                                       pos=(0, 0), height=0.1,
                                       color=[255, 255, 255], colorSpace='rgb255',
                                       wrapWidth=2)
		display_text.autoDraw=True
                                       
		return display_text

def get_settings():
    dlg = gui.Dlg(title='Choose Settings')
    dlg.addField('Experiment Name:', 'ToM_Loc')
    dlg.addField('Subject ID:', '0')
    dlg.addField('Speed Factor:', 1.0)
    dlg.addField('Run Number:', 1)
    dlg.show()
    if dlg.OK:
        return dlg.data
    else:
        sys.exit()

def get_window():
    return visual.Window(
        winType='pyglet', monitor="testMonitor", units="pix", screen=1,
        fullscr=True, colorSpace='rgb255', color=(0, 0, 0))

def run():
	(expname, sid, speed, run_num) = get_settings()
	
	if run_num == 1:
		pass
	else:
		core.quit()
	
	win = get_window()
	timing = {'fixation': 4.,
				'story': (12.*speed),
				'question': (4.*speed),
				'delay': 4.}
	
	win.mouseVisible = False
	
	stim = Stimuli(win, timing)
	
	stim.text_and_stim_keypress('You are going to be reading a number of stories about\n'+
								'different people and places.\n\n'+
								'Afterward, you will be asked a True or False question.\n\n' +
								'(Press any key to continue)')
	stim.text_and_stim_keypress('Press the left arrow key for True and the right arrow key for False.\n\n'+
    							'(Press any key to continue)')
	stim.text_and_stim_keypress('Ready?\n\n'+
    							'Press any key to begin!')
	
	win.flip()
	core.wait(timing['fixation'])
	
	#Sequence through trials
	routes = [[1, 2, 2, 1, 2, 1, 2, 1, 1, 2,
			  2, 1, 2, 1, 1, 2, 2, 1, 2, 1]]
	# Correct answers to each story/question
	answers = [[0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1]]
	# b - Belief, p - Photo
	conditions = ['b', 'p']
	
	design = routes[run_num-1]
	answer = answers[run_num-1]
	
	text_files = []
	counter = np.ones(2)+(5*(run_num-1))
	results = []

	#Construct the trials
	for trial in range(len(design)):
		trial_dict = {}
		trial_type = design[trial]
		condition = conditions[trial_type-1]
		trial_num = str(int(counter[trial_type-1]))
		
		with open('text_files/'+trial_num+condition+'_story.txt', 'r') as f:
			story = f.read()
		with open('text_files/'+trial_num+condition+'_question.txt', 'r') as f:
			question = f.read()
		
		text_files.append([story, question])
		
		trial_dict['trial_num'] = trial+1
		trial_dict['trial_cond'] = condition
		trial_dict['story'] = int(trial_num)
		if answer[trial] == 1:
			trial_dict['answer'] = 'True'
		elif answer[trial] == 0:
			trial_dict['answer'] = 'False'
		results.append(trial_dict)
		
		counter[trial_type-1] = counter[trial_type-1]+1
		
	# Run the trials		
	for trial in range(len(results)):
		
		story_start = stim.show_story(text_files[trial][0])
		results[trial]['story_start'] = story_start
		
		quest_start, resp, time_of_resp = stim.show_question(text_files[trial][1])
		results[trial]['quest_start'] = quest_start
		
		if resp == 1:
			results[trial]['response'] = 'True'
		elif resp == 0:
			results[trial]['response'] = 'False'
		else:
			results[trial]['response'] = 'Invalid'
				
		results[trial]['time_of_resp'] = time_of_resp
		corr_resp = (results[trial]['response'] == results[trial]['answer'])
		results[trial]['corr_resp'] = corr_resp
		
		if time_of_resp != 'timeout':
			results[trial]['resp_time'] = time_of_resp - quest_start
		else:
			results[trial]['resp_time'] = time_of_resp

		core.wait(timing['delay'])
		
		if not os.path.exists('behavioral/'):
			os.makedirs('behavioral')
	
		with open('behavioral/' + expname + '_' + str(sid)+ '.json', 'a') as f:
			f.write(json.dumps(results[trial]))
			f.write('\n')
		if trial == (len(results)-1):
			text = stim.text('Congratulations! You\'ve finished!')
			win.flip()
			core.wait(timing['delay'])
			flicker(win, 0)
			core.quit()
	
if __name__ == '__main__':
	run()