# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 19:27:31 2022

@author: Matt
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from itertools import compress


sns.set_style('white')


np.random.seed(2)

p_up = 0.8

N_steps = 101

confidence_threshold = np.linspace(0, 1, N_steps)

step_size = 1/(N_steps-1)

recall = [0]
precision = [1]

current_recall = 0
current_precision = 1

step = 0
step_bias = 10 

while current_recall <1:
    step += 1
    x = np.random.uniform()
    
    if x < p_up:
        current_precision += 1/(step+step_bias) * (1-current_precision)
        current_recall += 0.01
    else:
        current_precision -= 1/(step+step_bias) * (current_precision)
        
    recall.append(current_recall)
    precision.append(current_precision)

recall = np.around(recall, decimals=2)    

max_index = len(recall)-1
crop_indices = np.array([max_index//3, max_index*2//3, max_index])
crop_confidence = np.around(crop_indices/max_index, decimals = 2)


fig, axes = plt.subplots(1, 3, sharex=True, sharey=True, figsize = (18,5))

ax_fontsize = 18
axes[0].set_ylabel('Precision', size=ax_fontsize+4)
axes[1].set_xlabel('Recall', size=ax_fontsize+4)
for i in range(3):
    crop_index = crop_indices[i]
    axes[i].plot(recall[:crop_index], precision[:crop_index], color='black')
    if i != 2: axes[i].plot(recall[crop_index], precision[crop_index], 'ko', )
    axes[i].annotate('Confidence threshold: '+str(crop_confidence[i]),
                        xy=(1, 1),
                        xycoords='data',
                        size=18, ha='right', va='top',
                        bbox=dict(boxstyle='round', fc='w'))
    axes[i].tick_params(labelsize = ax_fontsize-4)
    
    
interp_points = np.linspace(0, 1, 11)

interp_precision = [max(list(compress(precision, recall>=x))) for x in interp_points]

axes[2].step(interp_points, interp_precision, 'o:', where='pre', color='red')  
axes[2].legend(['Original','11 point \n interpolated'], fontsize = ax_fontsize-4, loc = (0.55,0.64))
    
    
    



