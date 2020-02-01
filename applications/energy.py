from plot import *

IO_POWER = 0.28
OOO_POWER = 2.44
L1_ENERGY = 0.082
L2_ENERGY = 0.194
DRAM_ENERGY = 8.12951
FIFO_ENERGY = 0.00748

metrics = ["cycles", "l1_hits", "l1_misses", "l2_hits", "l2_misses", "dram_access_count", "LD_PROD", "TRM_ATOMIC_CAS", "TRM_ATOMIC_FADD", "TRM_ATOMIC_MIN", "SEND", "STVAL"]

def parse_energy():
  # 1 OOO DeSC (test2)
  # 1 OOO FL (test3)
  # 16 IO, 8 IO FL, 2 OOO (test4)

  energies = []
  ratios = []
  averages = []

  dir = "/home/ts20/share/results/isca/test"
  for c in range(5):
    for app in apps:
      for i in range(len(inputs[app])):
        if len(energies) <= i:
          energies.append([]) 
        input = inputs[app][i]
        names = input.split('/')
        if app in vp:
          input_name = names[len(names)-2]
        else:
          input_name = input.split(".")[0]
        if len(energies[i]) <= c:
          energies[i].append([])
        if c == 0 or c == 1:
          config = "OOO"
          mode = "di"
          exp_dir = dir + str(c+2) + "/"
          filename = exp_dir + app + "_" + input_name + "_" + config + "_" + mode + "/genStats.txt"
        else:
          exp_dir = dir + "4/"
          if c == 2:
            config = "IO"
            mode = "db"
            num_threads = "16"
          elif c == 3:
            config = "IO"
            mode = "di"
            num_threads = "8"
          else:
            config = "OOO"
            mode = "db"
            num_threads = "2"
          filename = exp_dir + app + "_" + input_name + "_" + config + "_" + mode + "_" + num_threads + "/genStats.txt"
        if os.path.isfile(filename):
          measurements = open(filename)
          data = measurements.read()
          measurements.close()
          for metric in metrics:
            matches = re.findall("^" + metric + " : .*$", data, re.MULTILINE)
            if matches == []:
              stat = 0
            else:
              match = re.match("^" + metric + " : (\d+)$", matches[len(matches)-1])
              stat = int(match.group(1))
            if metric == "cycles":
              cycles = stat
            elif metric == "l1_hits":
              l1_hits = stat
            elif metric == "l1_misses":
              l1_misses = stat
            elif metric == "l2_hits":
              l2_hits = stat
            elif metric == "l2_misses":
              l2_misses = stat
            elif metric == "dram_access_count":
              dram_accesses = stat
            elif metric == "LD_PROD":
              ld_prod = stat
            elif metric == "TRM_ATOMIC_CAS":
              atomic_cas = stat
            elif metric == "TRM_ATOMIC_FADD":
              atomic_fadd = stat
            elif metric == "TRM_ATOMIC_MIN":
              atomic_min = stat
            elif metric == "SEND":
              send = stat
            elif metric == "STVAL":
              stval = stat

          time = 5e-10*cycles

          # core energy
          num_cores = 2
          if config == "IO":
            core_power = IO_POWER
          else:
            core_power = OOO_POWER
          core_energy = num_cores*core_power*time

          # memory energy
          mem_energy = (l1_hits + l1_misses)*L1_ENERGY + (l2_hits + l2_misses)*L2_ENERGY + DRAM_ENERGY*dram_accesses

          # queues energy
          term_ld = ld_prod + atomic_cas + atomic_fadd + atomic_min
          queues_energy = term_ld*7*FIFO_ENERGY + send*4*FIFO_ENERGY + stval*4*FIFO_ENERGY

          energy = (core_energy + 1e-9*mem_energy + 1e-9*queues_energy)*time
          energies[i][c].append(energy)
        else:
          energies[i][c].append(1e20)

  for i in range(len(energies)): #inputs
    if len(ratios) <= i:
      ratios.append([])
    for c in range(len(energies[i])): #configs
      if len(ratios[i]) <= c:
        ratios[i].append([])
      for a in range(len(energies[i][c])): #apps
          ratios[i][c].append(energies[i][4][a]/energies[i][c][a])
  for i in range(len(energies)): #inputs
    for c in range(len(energies[i])): #configs    
      print(i, c, ratios[i][c])

  for c in range(len(energies[0])): #configs
    averages.append([])
    for a in range(len(energies[0][c])): #apps
      if len(averages[c]) <= a:
        averages[c].append(1.0)
      for i in range(len(energies)): #inputs
        averages[c][a] = averages[c][a] * ratios[i][c][a]
      averages[c][a] = averages[c][a] ** (1./len(energies))
  
  plot_energy(ratios, averages)
  plot_energy_simple(averages)

def plot_energy(stats, averages):
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
      c = 4
    elif n % num_bars == 1:
      c = 0
    elif n % num_bars == 2:
      c = 2
    elif n % num_bars == 3:
      c = 1
    else:
      c = 3
    i = int(n/num_bars)   
    if (n < N-num_bars): 
      bars.append(ax1.bar(ind+pos*width/N, stats[i][c], width/N, color=colors[n % num_bars], linewidth=1, edgecolor=['black']))
    else:
      bars.append(ax1.bar(ind+pos*width/N, averages[c], width/N, color=colors[n % num_bars], hatch=sym, linewidth=1, edgecolor=['black']))

  dummy = ax1.plot([0], [0], color="w")

  yticks = np.arange(0, 22, 3)
  ylabel = 'Energy-Delay Improvement'
  create_x_axis_avg(ax1, ind, yticks, ylabel, False)

  legend = ('2 Out-of-Order Cores', '', '1 DeSC Pair', '1 DeSC Pair (GeoMean)', '16 Parallel In-Order Cores', '16 Parallel In-Order Cores (GeoMean)', '1 Out-of-Order ' + approach, '1 Out-of-Order ' + approach + ' (GeoMean)', '8 In-Order ' + approach + 's', '8 In-Order' + approach + 's (GeoMean)')
  chartBox = ax1.get_position()
  ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height*0.8])
  ax1.legend((bars[0][0], dummy[0], bars[1][0], bars[16][0], bars[2][0], bars[17][0], bars[3][0], bars[18][0], bars[4][0],  bars[19][0]), legend, bbox_to_anchor=(0.,1.018,1.,0.18), ncol=5, mode="expand", fontsize=INPUTS_FONTSIZE)
  #plt.legend((psb1a[0], psb1b[0], psb1c[0], psb1d[0]), legend, fontsize=INPUTS_FONTSIZE)
  #plt.show()
  plt.savefig("../results/energy.pdf", bbox_inches='tight')

def plot_energy_simple(averages):
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
      c = 4
    elif n % num_bars == 1:
      c = 0
    elif n % num_bars == 2:
      c = 1
    else:
      c = 3
    i = int(n/num_bars)   
      
    bars.append(ax1.bar(ind+pos*width/N, averages[c], width/N, color=colors[n % num_bars], linewidth=1, edgecolor=['black']))
    for b in range(num_apps):
      rects.append(bars[n][b])

  dummy = ax1.plot([0], [0], color="w")

  autolabel(ax1, rects)
  yticks = np.arange(0, 22, 3)
  ylabel = 'Energy-Delay Improvement'
  create_x_axis_avg_simple(ax1, ind, yticks, ylabel, False)

  legend = ('2 OoO Cores', '1 DeSC Pair', '1 OoO FAST-LLAMAs', '8 FAST-LLAMAs')
  chartBox = ax1.get_position()
  ax1.set_position([chartBox.x0, chartBox.y0, chartBox.width, chartBox.height*0.8])
  ax1.legend((bars[0][0], bars[1][0], bars[2][0], bars[3][0]), legend, bbox_to_anchor=(0.,1.018,1.,0.18), ncol=4, mode="expand", fontsize=INPUTS_FONTSIZE)
  #plt.show()
  plt.savefig("../results/energy_simple.pdf", bbox_inches='tight')

def main():
  parse_mem()
  parse_speedups()
  parse_energy()

if __name__ == "__main__":
  main()
