import argparse
from go import *
import numpy as np
import matplotlib.pyplot as plt
import os
import re

AXIS_FONTSIZE = 44
TICK_FONTSIZE = 40
INPUTS_FONTSIZE = 32

width = 0.90
num_apps = 5
num_inputs = len(inputs["bfs"])
ind = np.arange(1, 6)
llamas = {"bfs": "6", "sssp": "9", "pagerank": "11", "ewsd": "21", "graph_projections": "9"}
approach = "FAST-LLAMAs Pair"

def create_scaling_axis(ax1, ind, yticks, ylabel):
  N = 9
  input_inds = []
  seps = []
  for i in ind:
    input_inds = input_inds + [i-4.5*width/N, i-3.25*width/N, i-2.25*width/N, i-width/N, i, i+1.25*width/N, i+2.25*width/N, i+3.5*width/N, i+4.5*width/N]
    if i == ind[len(ind)-1]:
      continue
    else:
      seps = seps + [i + 0.5]

  ax2 = ax1.twiny()
  ax3 = ax1.twiny()
  ax4 = ax1.twinx()

  input_labels = ['1 InO', '2 Par', '1 FLPs', '4 Par', '2 FLPs', '8 Par', '4 FLPs', '16 Par', '8 FLPs']
  input_labels = input_labels*num_apps
  xticks = ('EWSD', 'GP', 'BFS', 'SSSP', 'PR')

  ax1.set_xlim([0.5, num_apps+0.5])
  ax1.set_xticks(input_inds)
  ax1.set_xticklabels(input_labels, rotation=270, fontsize=INPUTS_FONTSIZE)
  ax1.set_ylim([0, yticks[len(yticks)-1]])
  ax1.set_yticks(yticks)
  ax1.set_yticklabels(yticks, fontsize=TICK_FONTSIZE)
  ax1.set_ylabel(ylabel, fontsize=AXIS_FONTSIZE)
  ax1.tick_params(direction='inout', length=20, width=1)

  ax2.set_xlim([0.5, num_apps+0.5])
  ax2.xaxis.set_ticks_position("bottom")
  ax2.xaxis.set_label_position("bottom")
  ax2.spines["bottom"].set_position(("axes", -0.2))
  ax2.spines["bottom"].set_visible(False)
  ax2.set_xticks(ind)
  ax2.set_xticklabels(xticks, fontsize=AXIS_FONTSIZE)
  ax2.tick_params(length=0)

  ax3.set_xlim([0.5, num_apps+0.5])
  ax3.xaxis.set_ticks_position("bottom")
  ax3.set_xticks(seps)
  ax3.set_xticklabels([])
  ax3.tick_params(direction='inout', length=40, width=1)

  ax4.set_ylim([0, yticks[len(yticks)-1]])
  ax4.set_yticks(yticks)
  ax4.set_yticklabels([])
  ax4.tick_params(direction='inout', length=20, width=1, labelleft=False, labelright=True)

def create_x_axis(ax1, ind, yticks, ylabel):
  input_inds = []
  seps = []
  for i in ind:
    input_inds = input_inds + [i-1.5*width/num_inputs, i-0.5*width/num_inputs, i+0.5*width/num_inputs, i+1.5*width/num_inputs]
    if i == ind[len(ind)-1]:
      continue
    else:
      seps = seps + [i + 0.5]

  ax2 = ax1.twiny()
  ax3 = ax1.twiny()
  ax4 = ax1.twinx()

  scale = 1.25
  input_labels = ['kr', 'sh', 'am', 'yt', 'po', 'db', 'am', 'yt', 'kr', 'tw', 'wp', 'wb', 'kr', 'tw', 'wp', 'wb', 'kr', 'tw', 'wp', 'wb']
  xticks = ('EWSD', 'GP', 'BFS', 'SSSP', 'PR')

  ax1.set_xlim([0.5, num_apps+0.5])
  ax1.set_xticks(input_inds)
  ax1.set_xticklabels(input_labels, fontsize=scale*INPUTS_FONTSIZE)
  ax1.set_ylim([0, yticks[len(yticks)-1]])
  ax1.set_yticks(yticks)
  ax1.set_yticklabels(yticks, fontsize=scale*TICK_FONTSIZE)
  ax1.set_ylabel(ylabel, fontsize=scale*AXIS_FONTSIZE)
  ax1.tick_params(direction='inout', length=20, width=1)

  ax2.set_xlim([0.5, num_apps+0.5])
  ax2.xaxis.set_ticks_position("bottom")
  ax2.xaxis.set_label_position("bottom")
  ax2.spines["bottom"].set_position(("axes", -0.07))
  ax2.spines["bottom"].set_visible(False)
  ax2.set_xticks(ind)
  ax2.set_xticklabels(xticks, fontsize=scale*AXIS_FONTSIZE)
  ax2.tick_params(length=0)

  ax3.set_xlim([0.5, num_apps+0.5])
  ax3.xaxis.set_ticks_position("bottom")
  ax3.set_xticks(seps)
  ax3.set_xticklabels([])
  ax3.tick_params(direction='inout', length=40, width=1)

  ax4.set_ylim([0, yticks[len(yticks)-1]])
  ax4.set_yticks(yticks)
  ax4.set_yticklabels([])
  ax4.tick_params(direction='inout', length=20, width=1, labelleft=False, labelright=True)

def create_x_axis_avg(ax1, ind, yticks, ylabel, avg):
  num_inputs = 5
  input_inds = []
  seps = []
  for i in ind:
    input_inds = input_inds + [i-2*width/num_inputs, i-width/num_inputs, i, i+width/num_inputs, i+2*width/num_inputs]
    if i == ind[len(ind)-1]:
      continue
    else:
      seps = seps + [i + 0.5]

  ax2 = ax1.twiny()
  ax3 = ax1.twiny()
  ax4 = ax1.twinx()

  scale = 1.25
  if (avg):
    input_labels = ['kr', 'sh', 'am', 'yt', 'avg', 'po', 'db', 'am', 'yt', 'avg', 'kr', 'tw', 'wp', 'wb', 'avg', 'kr', 'tw', 'wp', 'wb', 'avg', 'kr', 'tw', 'wp', 'wb', 'avg']
  else:
    input_labels = ['kr', 'sh', 'am', 'yt', 'gm', 'po', 'db', 'am', 'yt', 'gm', 'kr', 'tw', 'wp', 'wb', 'gm', 'kr', 'tw', 'wp', 'wb', 'gm', 'kr', 'tw', 'wp', 'wb', 'gm']
  xticks = ('EWSD', 'GP', 'BFS', 'SSSP', 'PR')

  ax1.set_xlim([0.5, num_apps+0.5])
  ax1.set_xticks(input_inds)
  ax1.set_xticklabels(input_labels, fontsize=scale*INPUTS_FONTSIZE)
  ax1.set_ylim([0, yticks[len(yticks)-1]])
  ax1.set_yticks(yticks)
  ax1.set_yticklabels(yticks, fontsize=scale*TICK_FONTSIZE)
  ax1.set_ylabel(ylabel, fontsize=scale*AXIS_FONTSIZE)
  ax1.tick_params(direction='inout', length=20, width=1)

  ax2.set_xlim([0.5, num_apps+0.5])
  ax2.xaxis.set_ticks_position("bottom")
  ax2.xaxis.set_label_position("bottom")
  ax2.spines["bottom"].set_position(("axes", -0.07))
  ax2.spines["bottom"].set_visible(False)
  ax2.set_xticks(ind)
  ax2.set_xticklabels(xticks, fontsize=scale*AXIS_FONTSIZE)
  ax2.tick_params(length=0)

  ax3.set_xlim([0.5, num_apps+0.5])
  ax3.xaxis.set_ticks_position("bottom")
  ax3.set_xticks(seps)
  ax3.set_xticklabels([])
  ax3.tick_params(direction='inout', length=40, width=1)

  ax4.set_yticks(yticks)
  ax4.set_ylim([0, yticks[len(yticks)-1]])
  ax4.set_yticklabels([])
  ax4.tick_params(direction='inout', length=20, width=1, labelleft=False, labelright=True)

def create_x_axis_avg_simple(ax1, ind, yticks, ylabel, avg):
  ax2 = ax1.twinx()

  scale = 1
  xticks = ('EWSD', 'GP', 'BFS', 'SSSP', 'PR')

  ax1.set_xlim([0.5, num_apps+0.5])
  ax1.set_ylim([0, yticks[len(yticks)-1]])
  ax1.set_xticks(ind)
  ax1.set_xticklabels(xticks, fontsize=scale*AXIS_FONTSIZE)
  ax1.set_yticks(yticks)
  ax1.set_yticklabels(yticks, fontsize=scale*TICK_FONTSIZE)
  ax1.set_ylabel(ylabel, fontsize=scale*AXIS_FONTSIZE)
  ax1.tick_params(direction='inout', length=20, width=1)

  ax2.set_yticks(yticks)
  ax2.set_ylim([0, yticks[len(yticks)-1]])
  ax2.set_yticklabels([])
  ax2.tick_params(direction='inout', length=20, width=1, labelleft=False, labelright=True)

#Total latency breakdown
def latency_breakdown(ys, averages):
  N = num_inputs + 1

  fig = plt.figure(figsize=(35.0, 15.0))
  fig.subplots_adjust(bottom=0.1)
  ax1 = fig.add_subplot(111)

  y = [100.0, 100.0, 100.0, 100.0, 100.0]

  colors = ['tab:orange', 'gold', 'royalblue']
  num_bars = len(colors)
  scale = 0.9
  sym = '.'
  bars = []

  for n in range(N):
    if N % 2 == 0:
      pos = n-N/2+0.5
    else:
      pos = n-(N-1)/2

    bars.append(ax1.bar(ind+pos*width/N, y[n], scale*width/N, color=colors[0], linewidth=1, edgecolor=['black']))
    
    if n != N-1:
      bars.append(ax1.bar(ind+pos*width/N, ys[n][0], scale*width/N, color=colors[1], linewidth=1, edgecolor=['black']))
      bars.append(ax1.bar(ind+pos*width/N, ys[n][1], scale*width/N, color=colors[2], linewidth=1, edgecolor=['black']))
    else:
      bars.append(ax1.bar(ind+pos*width/N, averages[0], scale*width/N, color=colors[1], linewidth=1, edgecolor=['black']))
      bars.append(ax1.bar(ind+pos*width/N, averages[1], scale*width/N, color=colors[2], hatch=sym, linewidth=1, edgecolor=['black']))

  yticks  = np.arange(0, 101, 10)
  ylabel = 'Percentage of Total Runtime'
  create_x_axis_avg(ax1, ind, yticks, ylabel, True)

  legend = ('LLAMAs', 'LLAMAs (Avg)', 'Rest of Memory Accesses', 'Compute')
  chartBox = ax1.get_position()
  ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height*0.8])
  ax1.legend((bars[2][0], bars[len(bars)-1][0], bars[1][0], bars[0][0]), legend, bbox_to_anchor=(0.,1.01,1.,0.101), ncol=len(legend), mode="expand", fontsize=1.25*INPUTS_FONTSIZE)
  #plt.show()
  plt.savefig("../results/motivation_llama.pdf", bbox_inches='tight')

def latency_breakdown_simple(averages):
  N = 1

  fig = plt.figure(figsize=(16.0, 15.0))
  fig.subplots_adjust(bottom=0.1)
  ax1 = fig.add_subplot(111)

  y = [100.0, 100.0, 100.0, 100.0, 100.0]

  colors = ['tab:orange', 'gold', 'royalblue']
  num_bars = len(colors)
  scale = 0.85
  bars = []

  for n in range(N):
    if N % 2 == 0:
      pos = n-N/2+0.5
    else:
      pos = n-(N-1)/2

    bars.append(ax1.bar(ind+pos*width/N, y[n], scale*width/N, color=colors[0], linewidth=1, edgecolor=['black']))
    bars.append(ax1.bar(ind+pos*width/N, averages[0], scale*width/N, color=colors[1], linewidth=1, edgecolor=['black']))
    bars.append(ax1.bar(ind+pos*width/N, averages[1], scale*width/N, color=colors[2], linewidth=1, edgecolor=['black']))

  yticks  = np.arange(0, 101, 10)
  ylabel = 'Percentage of Total Runtime'
  create_x_axis_avg_simple(ax1, ind, yticks, ylabel, True)

  legend = ('LLAMAs', 'Other Accesses', 'Compute')
  chartBox = ax1.get_position()
  ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height*0.8])
  ax1.legend((bars[2][0], bars[1][0], bars[0][0]), legend, bbox_to_anchor=(0.,1.01,1.,0.101), ncol=len(legend), mode="expand", fontsize=INPUTS_FONTSIZE)
  #plt.show()
  plt.savefig("../results/motivation_llama_simple.pdf", bbox_inches='tight')

# Time spent going to main memory
def mm(ys, averages):
  N = num_inputs + 1

  fig = plt.figure(figsize=(35.0, 15.0))
  fig.subplots_adjust(bottom=0.1)
  ax1 = fig.add_subplot(111)

  colors = ['royalblue']
  scale = 0.9
  sym = '.'
  bars = []

  for n in range(N):
    if N % 2 == 0:
      pos = n-N/2+0.5
    else:
      pos = n-(N-1)/2

    if n != N-1:
      bars.append(ax1.bar(ind+pos*width/N, ys[n][2], scale*width/N, color=colors[0], linewidth=1, edgecolor=['black']))
    else:
      bars.append(ax1.bar(ind+pos*width/N, averages[2], scale*width/N, color=colors[0], hatch=sym, linewidth=1, edgecolor=['black']))

  yticks  = np.round(np.arange(0, 1.1, 0.1),1)
  ylabel = 'LLC Miss Rate'
  create_x_axis_avg(ax1, ind, yticks, ylabel, True)

  legend = ('LLC Miss Rate', 'LLC Miss Rate (Avg)')
  chartBox = ax1.get_position()
  ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height*0.8])
  #plt.legend((bars[0][0], bars[num_inputs][0]), legend, ncol=2, fontsize=1.5*INPUTS_FONTSIZE)
  #plt.show()
  plt.savefig("../results/motivation_dram.pdf", bbox_inches='tight')

def mm_simple(averages):
  N = 1

  fig = plt.figure(figsize=(15.0, 15.0))
  fig.subplots_adjust(bottom=0.1)
  ax1 = fig.add_subplot(111)

  colors = ['royalblue']
  scale = 0.85
  bars = []

  for n in range(N):
    if N % 2 == 0:
      pos = n-N/2+0.5
    else:
      pos = n-(N-1)/2

    bars.append(ax1.bar(ind+pos*width/N, averages[2], scale*width/N, color=colors[0], linewidth=1, edgecolor=['black']))

  yticks  = np.round(np.arange(0, 1.1, 0.1),1)
  ylabel = 'LLC Miss Rate'
  create_x_axis_avg_simple(ax1, ind, yticks, ylabel, True)

  chartBox = ax1.get_position()
  ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height*0.8])
  #plt.legend((bars[0][0], bars[num_inputs][0]), legend, ncol=2, fontsize=1.5*INPUTS_FONTSIZE)
  #plt.show()
  plt.savefig("../results/motivation_dram_simple.pdf", bbox_inches='tight')

def autolabel(ax, rects):
  index = 0
  for rect in rects:
    scale = 1.01
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2., scale*height, '%0.2f' % height, ha='center', va='bottom', size=0.9*INPUTS_FONTSIZE)
    index += 1

def simple(speedups, averages):
  N = 20

  fig = plt.figure(figsize=(65.0,15.0))
  fig.subplots_adjust(bottom=0.1)
  ax1 = fig.add_subplot(111)

  colors = ['black', 'royalblue', 'gold', 'tab:orange']
  num_bars = len(colors)
  sym = '.'
  bars = []

  for n in range(N):
    if N % 2 == 0:
      pos = n-N/2+0.5
    else:
      pos = n-(N-1)/2
    if n % num_bars == 0:
      c = 2
    elif n % num_bars == 1:
      c = 10
    elif n % num_bars == 2:
      c = 8
    else:
     c = 6
    i = int(n/num_bars)
    
    if n < N-num_bars:
      bars.append(ax1.bar(ind+pos*width/N, speedups[i][c], width/N, color=colors[n % num_bars], linewidth=1, edgecolor=['black']))
    else:
      bars.append(ax1.bar(ind+pos*width/N, averages[c], width/N, color=colors[n % num_bars], hatch=sym, linewidth=1, edgecolor=['black']))
  dummy = ax1.plot([0], [0], color="w")

  yticks = np.arange(11)
  ylabel = 'Speedup'
  create_x_axis_avg(ax1, ind, yticks, ylabel, False)

  legend = ('1 In-Order Core', '2 Parallel', '1 ' + approach, '1 In-Order w/ Perfect Cache', '', '2 Parallel (GeoMean)', '1 ' + approach + ' (GeoMean)', '1 In-Order w/ Perfect Cache (Geomean)')
  chartBox = ax1.get_position()
  ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height*0.8])
  #ax1.legend((psb1a[0], dummy[0], psb1b[0], psb4b[0], psb1c[0], psb4c[0], psb1d[0], psb4d[0]), legend, bbox_to_anchor=(0.,1.015,1.,0.15), ncol=4, mode="expand", fontsize=INPUTS_FONTSIZE)
  plt.legend((bars[0][0], bars[1][0], bars[2][0], bars[3][0], dummy[0], bars[17][0], bars[18][0], bars[19][0]), legend, loc=2, ncol=2, fontsize=INPUTS_FONTSIZE)
  #plt.show()
  plt.savefig("../results/simple.pdf", bbox_inches='tight')

def simple_simple(averages):
  N = 4

  fig = plt.figure(figsize=(30.0,15.0))
  fig.subplots_adjust(bottom=0.1)
  ax1 = fig.add_subplot(111)

  colors = ['black', 'royalblue', 'gold', 'tab:orange']
  num_bars = len(colors)
  sym = '.'
  bars = []
  rects = []

  for n in range(N):
    if N % 2 == 0:
      pos = n-N/2+0.5
    else:
      pos = n-(N-1)/2
    if n % num_bars == 0:
      c = 2
    elif n % num_bars == 1:
      c = 10
    elif n % num_bars == 2:
      c = 8
    else:
     c = 6
    i = int(n/num_bars)
    
    bars.append(ax1.bar(ind+pos*width/N, averages[c], width/N, color=colors[n % num_bars], linewidth=1, edgecolor=['black']))
    for b in range(num_apps):
      rects.append(bars[n][b])

  autolabel(ax1, rects)
  yticks = np.arange(8)
  ylabel = 'Speedup'
  create_x_axis_avg_simple(ax1, ind, yticks, ylabel, False)

  legend = ('1 In-Order Core', '2 Parallel', '1 ' + approach, '1 In-Order w/ Perfect Cache')
  chartBox = ax1.get_position()
  ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height*0.8])
  ax1.legend((bars[0][0], bars[1][0], bars[2][0], bars[3][0]), legend, bbox_to_anchor=(0.,1.015,1.,0.15), ncol=4, mode="expand", fontsize=INPUTS_FONTSIZE)
  #plt.legend((bars[0][0], bars[1][0], bars[2][0], bars[3][0]), legend, loc=2, ncol=1, fontsize=INPUTS_FONTSIZE)
  #plt.show()
  plt.savefig("../results/simple_simple.pdf", bbox_inches='tight')

def equal_area(speedups, averages):
  N = 25

  fig = plt.figure(figsize=(65.0,15.0))
  fig.subplots_adjust(bottom=0.1)
  ax1 = fig.add_subplot(111)

  colors = ['black', 'royalblue', 'tab:green', 'gold', 'tab:orange']
  num_bars = len(colors)
  sym = '.'
  bars = []

  for n in range(N):
    if N % 2 == 0:
      pos = n-N/2+0.5
    else:
      pos = n-(N-1)/2
    if n % num_bars == 0:
      c = 18
    elif n % num_bars == 1:
      c = 5
    elif n % num_bars == 2:
      c = 13
    elif n % num_bars == 3:
      c = 9
    else:
      c = 17
    i = int(n/num_bars)   
    if (n < N-num_bars): 
      bars.append(ax1.bar(ind+pos*width/N, np.divide(speedups[i][c], speedups[i][18]), width/N, color=colors[n % num_bars], linewidth=1, edgecolor=['black']))
    else:
      print("averages")
      print(np.divide(averages[c], averages[18]))
      bars.append(ax1.bar(ind+pos*width/N, np.divide(averages[c], averages[18]), width/N, color=colors[n % num_bars], hatch=sym, linewidth=1, edgecolor=['black']))

  dummy = ax1.plot([0], [0], color="w")

  yticks = np.arange(7)
  ylabel = 'Speedup'
  create_x_axis_avg(ax1, ind, yticks, ylabel, False)

  legend = ('2 Out-of-Order Cores', '', '1 DeSC Pair', '1 DeSC Pair (GeoMean)', '16 Parallel In-Order Cores', '16 Parallel In-Order Cores (GeoMean)', '1 Out-of-Order ' + approach, '1 Out-of-Order ' + approach + ' (GeoMean)', '8 In-Order ' + approach + 's', '8 In-Order' + approach + 's (GeoMean)')
  chartBox = ax1.get_position()
  ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height*0.8])
  ax1.legend((bars[0][0], dummy[0], bars[1][0], bars[16][0], bars[2][0], bars[17][0], bars[3][0], bars[18][0], bars[4][0],  bars[19][0]), legend, bbox_to_anchor=(0.,1.018,1.,0.18), ncol=5, mode="expand", fontsize=INPUTS_FONTSIZE)
  #plt.legend((psb1a[0], psb1b[0], psb1c[0], psb1d[0]), legend, fontsize=INPUTS_FONTSIZE)
  #plt.show()
  plt.savefig("../results/equal_area.pdf", bbox_inches='tight')

def scaling(speedups, averages):
  N = 9

  fig = plt.figure(figsize=(65.0,15.0))
  fig.subplots_adjust(bottom=0.25)
  ax1 = fig.add_subplot(111)

  colors = ['black', 'royalblue', 'royalblue', 'tab:green', 'tab:green', 'gold', 'gold', 'tab:orange', 'tab:orange']
  num_bars = len(colors)
  sym = '/'
  bars = []

  locs = [-4.5, -3.25, -2.25, -1, 0, 1.25, 2.25, 3.5, 4.5]

  for n in range(N):
    if N % 2 == 0:
      pos = n-N/2+0.5
    else:
      pos = n-(N-1)/2
    if n % num_bars == 0:
      c = 2
    elif n % num_bars == 1:
      c = 10
    elif n % num_bars == 2:
      c = 14
    elif n % num_bars == 3:
      c = 11
    elif n % num_bars == 4:
      c = 15
    elif n % num_bars == 5:
      c = 12
    elif n % num_bars == 6:
      c = 16
    elif n % num_bars == 7:
      c = 13
    else:
      c = 17
    i = int(n/num_bars)
    if n % num_bars == 0 or n % 2 == 1:   
      bars.append(ax1.bar(ind+locs[n % num_bars]*width/N, speedups[i][c], width/N, color=colors[n % num_bars], linewidth=1, edgecolor=['black']))
    else:
      bars.append(ax1.bar(ind+locs[n % num_bars]*width/N, speedups[i][c], width/N, color=colors[n % num_bars], hatch=sym, linewidth=1, edgecolor=['black']))
  dummy = ax1.plot([0], [0], color="w")

  yticks = np.arange(0, 66, 5)
  ylabel = 'Speedup'
  create_scaling_axis(ax1, ind, yticks, ylabel)

  legend = ['InO = In-Order Core', 'Par = Parallel', 'FLP = FAST-LLAMAs Pair']
  for l in legend:
    ax1.plot(1, 1, label = l, marker = '', ls ='')
  ax1.legend(loc=2, handlelength=0, fontsize=INPUTS_FONTSIZE)
  #legend = ('1 In-Order Core', '', '2 Parallel', '1 ' + approach, '4 Parallel', '2 ' + approach + 's', '8 Parallel', '4 ' + approach + 's', '16 Parallel', '8 ' + approach + 's')
  #chartBox = ax1.get_position()
  #ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height*0.8])
  #ax1.legend((psb1[0], dummy[0], psb2[0], psb3[0], psb4[0], psb5[0], psb6[0], psb7[0], psb8[0], psb9[0]), legend, bbox_to_anchor=(0.,1.018,1.,0.18), ncol=5, mode="expand", fontsize=1.05*INPUTS_FONTSIZE)
  #plt.show()
  plt.savefig("../results/scaling.pdf", bbox_inches='tight')

def parse_mem():
  exp_dir = "/home/ts20/share/results/isca/test1/"
  metrics = ["Percent of Total Latency Spent on Memory", "Percent of Total Latency Spent on Long-Latency Access", "Long-Latency Access L2 Hit Rate"]
  ys = []
  averages = []

  for app in apps:
    for i in range(len(inputs[app])):
      if len(ys) <= i:
        ys.append([])
      input = inputs[app][i]
      names = input.split("/")
      if app in vp:
        filename = exp_dir + app + "_" + names[len(names)-2] + "_IO/measurements.txt"
      else:
        filename = exp_dir + app + "_" + input.split(".")[0] + "_IO/measurements.txt"
      if os.path.isfile(filename):
        measurements = open(filename)
        data = measurements.read()
        measurements.close()
        for m in range(len(metrics)):
          if len(ys[i]) <= m:
            ys[i].append([])
          matches = re.findall("^" + metrics[m] + ": .*$", data, re.MULTILINE)
          match = re.match(".+:\s*(\d+\.*\d+)", matches[0])
          if m == 2:
            percent = (1-float(match.group(1)))
          else:
            percent = float(match.group(1))
          ys[i][m].append(percent)
      else:
        for m in range(len(metrics)):
          ys[i][m].append(0)

  for m in range(len(ys[0])): #metrics
    averages.append([])
    for a in range(len(ys[0][0])): #apps
      averages[m].append(0)
      for i in range(len(ys)): #inputs
        averages[m][a] += ys[i][m][a]
      averages[m][a] = averages[m][a]/len(ys)

  # PRINTING
  for i in range(len(ys)): #inputs
    for m in range(len(ys[i])): #metrics
      print(i, m, ys[i][m])

  latency_breakdown(ys, averages)
  mm(ys, averages)

  latency_breakdown_simple(averages)
  mm_simple(averages)

def parse_speedups():
  # 1 IO, 1 OOO (test1)
  # 1 IO, 1 OOO, 1 decoupled, 1 OOO decoupled, 1 IO PC, 1 OOO PC (test2) 
  # 1 IO terminal RMW, 1 OOO terminal RMW (test3)
  # 2 IO, 4 IO, 8 IO, 16 IO, 1 decoupled, 2 decoupled, 4 decoupled, 8 decoupled, 2 OOO (test4)

  runtimes = []
  speedups = []
  averages = []

  exp_dir = "/home/ts20/share/results/isca/test1/"
  for app in apps:
    for i in range(len(inputs[app])):
      if len(runtimes) <= i:
        runtimes.append([])
      input = inputs[app][i]
      names = input.split("/")
      for c in range(len(configs)):
        config = configs[c]
        if app in vp:
          filename = exp_dir + app + "_" + names[len(names)-2] + "_" + config + "/measurements.txt"
        else:
          filename = exp_dir + app + "_" + input.split(".")[0] + "_" + config + "/measurements.txt"
        index = c 
        if len(runtimes[i]) <= index:
          runtimes[i].append([])
        if os.path.isfile(filename):
          measurements = open(filename)
          data = measurements.read()
          measurements.close()
          matches = re.findall("^cycles : .*$", data, re.MULTILINE)
          match = re.match(".+:\s*(\d+\.*\d+)", matches[0])
          runtime = float(match.group(1))
          runtimes[i][index].append(runtime)
        else:
          fill = 1e20
          runtimes[i][index].append(fill)
 
  exp_dir = "/home/ts20/share/results/isca/test2/"
  for app in apps:
    for i in range(len(inputs[app])):
      input = inputs[app][i]
      names = input.split("/")
      new_modes = modes + ["PC"]
      for m in range(len(new_modes)):
        mode = new_modes[m]
        for c in range(len(configs)):
          config = configs[c]
          if app in vp:
            filename = exp_dir + app + "_" + names[len(names)-2] + "_" + config + "_" + mode + "/measurements.txt"
          else:
            filename = exp_dir + app + "_" + input.split(".")[0] + "_" + config + "_" + mode + "/measurements.txt"
          index = 2 + m*2 + c
          if len(runtimes[i]) <= index:
            runtimes[i].append([])
          if os.path.isfile(filename):
            measurements = open(filename)
            data = measurements.read()
            measurements.close()
            matches = re.findall("^cycles : .*$", data, re.MULTILINE)
            match = re.match(".+:\s*(\d+\.*\d+)", matches[0])
            runtime = float(match.group(1))
            runtimes[i][index].append(runtime)
          else:
            fill = 1e20
            runtimes[i][index].append(fill)
 
  exp_dir = "/home/ts20/share/results/isca/test3/"
  for app in apps:
    for i in range(len(inputs[app])):
      input = inputs[app][i]
      names = input.split("/")
      for c in range(len(configs)):
        config = configs[c]
        if app in vp:
          filename = exp_dir + app + "_" + names[len(names)-2] + "_" + config + "_di/measurements.txt"
        else:
          filename = exp_dir + app + "_" + input.split(".")[0] + "_" + config + "_di/measurements.txt"
        index = c + 8
        if len(runtimes[i]) <= index:
          runtimes[i].append([])
        if os.path.isfile(filename):
          measurements = open(filename)
          data = measurements.read()
          measurements.close()
          matches = re.findall("^cycles : .*$", data, re.MULTILINE)
          match = re.match(".+:\s*(\d+\.*\d+)", matches[0])
          runtime = float(match.group(1))
          runtimes[i][index].append(runtime)
        else:
          fill = 1e20
          runtimes[i][index].append(fill)
 
  exp_dir = "/home/ts20/share/results/isca/test4/"
  for app in apps:
    for i in range(len(inputs[app])):
      input = inputs[app][i]
      names = input.split("/")
      if app in vp:
        input_name = names[len(names)-2]
      else:
        input_name = input.split(".")[0]
      for m in range(len(modes)):
        mode = modes[m]
        for t in range(4):
          if mode == "db":
            num_tiles = str(int(math.pow(2, t+1)))
          else:
            num_tiles = str(int(math.pow(2, t)))
          index = m*4 + t + 10
          filename = exp_dir + app + "_" + input_name + "_IO_" + mode + "_" + num_tiles + "/measurements.txt"
          if len(runtimes[i]) <= index:
            runtimes[i].append([])
          if os.path.isfile(filename):
            measurements = open(filename)
            data = measurements.read()
            measurements.close()
            matches = re.findall("^cycles : .*$", data, re.MULTILINE)
            match = re.match(".+:\s*(\d+\.*\d+)", matches[0])
            runtime = float(match.group(1))
            runtimes[i][index].append(runtime)
          else:
            fill = 1e20
            runtimes[i][index].append(fill)
      index += 1
      filename = exp_dir + app + "_" + input_name + "_OOO_db_2/measurements.txt"
      if len(runtimes[i]) <= index:
        runtimes[i].append([])
      if os.path.isfile(filename):
        measurements = open(filename)
        data = measurements.read()
        measurements.close()
        matches = re.findall("^cycles : .*$", data, re.MULTILINE)
        match = re.match(".+:\s*(\d+\.*\d+)", matches[0])
        runtime = float(match.group(1))
        runtimes[i][index].append(runtime)
      else:
        fill = 1e20
        runtimes[i][index].append(fill)

  # CALCULATE SPEEDUPS          
  for i in range(len(runtimes)): #inputs
    if len(speedups) <= i:
      speedups.append([])
    for c in range(2): #configs
      if len(speedups[i]) <= c:
        speedups[i].append([])
      for a in range(len(runtimes[i][c])): #apps
        speedups[i][c].append(runtimes[i][0][a]/runtimes[i][c][a])
    for c in range(2, len(runtimes[i])): #configs
      if len(speedups[i]) <= c:
        speedups[i].append([])
      for a in range(len(runtimes[i][c])): #apps
        speedups[i][c].append(runtimes[i][2][a]/runtimes[i][c][a])

  for c in range(len(runtimes[0])): #configs
    averages.append([])
    for a in range(len(runtimes[0][c])): #apps
      if len(averages[c]) <= a:
        averages[c].append(1.0)
      for i in range(len(runtimes)): #inputs
        averages[c][a] = averages[c][a] * speedups[i][c][a]
      averages[c][a] = averages[c][a] ** (1./len(runtimes))

  # PRINTING
  for i in range(len(runtimes)): #inputs
    for c in range(len(runtimes[i])):
      print(i, c, speedups[i][c])

  flipped = [[],[],[]]
  for a in range(2, len(speedups[0][0])):
    for c in range(len(speedups[0])):
      for i in range(len(speedups)):
        if (len(flipped[a-2]) <= c):
          flipped[a-2].append([])
        flipped[a-2][c].append(speedups[i][c][a])

  simple(speedups, averages)
  equal_area(speedups, averages)
  scaling(speedups, averages)

  simple_simple(averages)
