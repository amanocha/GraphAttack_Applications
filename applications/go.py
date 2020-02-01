import argparse
import math
import os
import sys

# APPS
ewsd = ["ewsd"]
gp = ["graph_projections"]
vp = ["bfs", "sssp", "pagerank"]
apps = ewsd + gp + vp

# INPUTS
inputs = {
           "ewsd": ["Kronecker_15.el", "Sinkhorn.tsv", "Amazon.tsv", "YouTube.tsv"],
           "graph_projections": ["Power.tsv", "Dbpedia.tsv", "Amazon.tsv", "YouTube.tsv"],
           "bfs": ["Kronecker_25/", "Twitter/", "Wikipedia/", "Sd1_Arc/"],
           "sssp": ["Kronecker_25/", "Twitter/", "Wikipedia/", "Sd1_Arc/"],
           "pagerank": ["Kronecker_25/", "Twitter/", "Wikipedia/", "Sd1_Arc/"]
         }

# CONFIGS
modes = ["db", "di"]
configs = ["IO", "OOO"]
epochs = {
           "bfs": {"Kronecker_25/": "3", "Twitter/": "4", "Wikipedia/": "4", "Sd1_Arc/": "5"},
           "sssp": {"Kronecker_25/": "3", "Twitter/": "5", "Wikipedia/": "4", "Sd1_Arc/": "5"},
           "pagerank": {"Kronecker_25/": "2", "Twitter/": "2", "Wikipedia/": "2", "Sd1_Arc/": "2"}
         }

COMPUTE_EDGES = 20000000

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("-a", "--app", type=str, help="Application to run (ewsd, graph_projections, bfs, sssp, pagerank)")
  parser.add_argument("-x", "--experiment", type=int, help="Experiment to run (1-4)")
  args = parser.parse_args()
  return args

def run(cmd, tmp_output, output):
  print(cmd)
  exit = os.system(cmd)
  if not exit:
    os.system("rm " + tmp_output + "memStats")
    if os.path.isfile(tmp_output + "decouplingStats"):
      cmd1 = "sed -e '1,6d' < " + tmp_output + "decouplingStats > " + tmp_output + "tmp"
      print(cmd1)
      os.system(cmd1)
      cmd2 = "cut -d \" \" -f 3- " + tmp_output + "tmp > " + tmp_output + "runahead_dists"
      print(cmd2)
      os.system(cmd2)
      os.system("rm " + tmp_output + "tmp")
    os.system("cp -r " + tmp_output + " " + output)
    os.system("rm -r " + tmp_output)
    print("Done! Navigate to " + output + "measurements.txt to see the results!")
  else:
    print("Experiment failed!")

# Experiment 1
def run_one():
  exp_dir = "/home/ts20/share/results/isca/test1/"
  for config in configs:
    for app in apps:
      for input in inputs[app]:
        if app in vp:
          names = input.split("/")
          output = app + "_" + names[len(names)-2] + "_" + config + "/"
        else:
          output = app + "_" + input.split(".")[0] + "_" + config + "/"
        if not os.path.isdir(exp_dir + output):
          tmp_output = exp_dir + "tmp_" + output
          source = app + "/original_desc/decades_baseline/main.cpp"
          if app in vp:
            data = "/home/ts20/share/graphs/vp/" + input
            cmd_args = ["time python measure.py", "-s", source, "-d", data, "-c", config, "-o", tmp_output, "-e", epochs[app][input], "-n", str(COMPUTE_EDGES)]
          else:
            data = "/home/ts20/share/graphs/" + app + "/" + input
            cmd_args = ["time python measure.py", "-s", source, "-d", data, "-c", config, "-o", tmp_output]
          cmd = " ".join(cmd_args)
          run(cmd, tmp_output, exp_dir + output)
          
        '''
        output = app + "_" + input.split(".")[0] + "_" + config + "_PC/"
        if os.path.isdir(exp_dir + output):
          continue
        else:
          tmp_output = exp_dir + "tmp_" + output
          source = app + "/original_desc/decades_baseline/main.cpp"
          if app in vp:
            data = "/home/ts20/share/graphs/vp/" + input
            cmd_args = ["time python measure.py", "-s", source, "-d", data, "-c", config, "-m", "PC", "-o", tmp_output, "-e", epochs[app][input]]
          else:
            data = "/home/ts20/share/graphs/" + app + "/" + input
            cmd_args = ["time python measure.py", "-s", source, "-d", data, "-c", config, "-m", "PC", "-o", tmp_output]
          cmd = " ".join(cmd_args)
          run(cmd, tmp_output, exp_dir + output)
        '''

# Experiment 2
def run_two():
  exp_dir = "/home/ts20/share/results/isca/test2/"
  for app in apps:
    for input in inputs[app]:
      source = app + "/original_desc/decades_decoupled/main.cpp"
      for config in configs:
        for mode in modes:
          if app in vp:
            names = input.split("/")
            output = app + "_" + names[len(names)-2] + "_" + config + "_" + mode + "/"
          else:
            output = app + "_" + input.split(".")[0] + "_" + config + "_" + mode + "/"
          if os.path.isdir(exp_dir + output):
            continue
          else:
            tmp_output = exp_dir + "tmp_" + output
            if app in vp:
              data = "/home/ts20/share/graphs/vp/" + input
              cmd_args = ["time python measure.py", "-s", source, "-d", data, "-c", config, "-m", mode, "-o", tmp_output, "-e", epochs[app][input], "-n", str(COMPUTE_EDGES)]
            else:
              data = "/home/ts20/share/graphs/" + app + "/" + input
              cmd_args = ["time python measure.py", "-s", source, "-d", data, "-c", config, "-m", mode, "-o", tmp_output]
            cmd = " ".join(cmd_args)
            run(cmd, tmp_output, exp_dir + output)

        if app in vp:
          names = input.split("/")
          output = app + "_" + names[len(names)-2] + "_" + config + "_PC/"
        else:
          output = app + "_" + input.split(".")[0] + "_" + config + "_PC/"
        if os.path.isdir(exp_dir + output):
          continue
        else:
          tmp_output = exp_dir + "tmp_" + output
          if app in vp:
            data = "/home/ts20/share/graphs/vp/" + input
            cmd_args = ["time python measure.py", "-s", source, "-d", data, "-c", config, "-m", "PC", "-o", tmp_output, "-e", epochs[app][input], "-n", str(COMPUTE_EDGES)]
          else:
            data = "/home/ts20/share/graphs/" + app + "/" + input
            cmd_args = ["time python measure.py", "-s", source, "-d", data, "-c", config, "-m", "PC", "-o", tmp_output]
          cmd = " ".join(cmd_args)
          run(cmd, tmp_output, exp_dir + output)

def run_three():
  exp_dir = "/home/ts20/share/results/isca/test3/"
  for app in apps:
    for input in inputs[app]:
      source = app + "/new_desc/terminal_rmw/main.cpp"
      for config in configs:
        if app in vp:
          names = input.split("/")
          output = app + "_" + names[len(names)-2] + "_" + config + "_di/"
        else:
          output = app + "_" + input.split(".")[0] + "_" + config + "_di/"
        if os.path.isdir(exp_dir + output):
          continue
        else:
          tmp_output = exp_dir + "tmp_" + output
          if app in vp:
            data = "/home/ts20/share/graphs/vp/" + input
            cmd_args = ["time python measure.py", "-s", source, "-d", data, "-c", config, "-m", "di", "-o", tmp_output, "-e", epochs[app][input], "-n", str(COMPUTE_EDGES)]
          else:
            data = "/home/ts20/share/graphs/" + app + "/" + input
            cmd_args = ["time python measure.py", "-s", source, "-d", data, "-c", config, "-m", "di", "-o", tmp_output]
          cmd = " ".join(cmd_args)
          run(cmd, tmp_output, exp_dir + output)

def run_four():
  exp_dir = "/home/ts20/share/results/isca/test4/"
  for app in apps:
    for input in inputs[app]:
      for t in range(4):
        num_tiles = str(int(math.pow(2, t+1)))
        for mode in modes: 
          if mode == "di":
            source = app + "/new_desc/terminal_rmw/main.cpp"
            num_tiles = str(int(math.pow(2, t)))
          else:
            source = app + "/original_desc/decades_decoupled/main.cpp"
          if app in vp:
            names = input.split("/")
            output = app + "_" + names[len(names)-2] + "_IO_" + mode + "_" + num_tiles + "/"
          else:
            output = app + "_" + input.split(".")[0] + "_IO_" + mode + "_" + num_tiles + "/"
          if (os.path.isdir(exp_dir + output)):
            continue
          else:
            tmp_output = exp_dir + "tmp_" + output
            if app in vp:
              data = "/home/ts20/share/graphs/vp/" + input
              cmd_args = ["time python measure.py", "-s", source, "-d", data, "-m", mode, "-t", num_tiles, "-o", tmp_output, "-e", epochs[app][input], "-n", str(COMPUTE_EDGES)]
            else:
              data = "/home/ts20/share/graphs/" + app + "/" + input
              cmd_args = ["time python measure.py", "-s", source, "-d", data, "-m", mode, "-t", num_tiles, "-o", tmp_output]
            cmd = " ".join(cmd_args)
            run(cmd, tmp_output, exp_dir + output)

      for t in range(1):
        num_tiles = str(int(math.pow(2, t+1)))
        source = app + "/original_desc/decades_decoupled/main.cpp"
        if app in vp:
          output = app + "_" + names[len(names)-2] + "_OOO_db_" + num_tiles + "/"
        else:
          output = app + "_" + input.split(".")[0] + "_OOO_db_" + num_tiles + "/"
        if os.path.isdir(exp_dir + output):
          continue
        else:
          tmp_output = exp_dir + "tmp_" + output
          if app in vp:
            data = "/home/ts20/share/graphs/vp/" + input
            cmd_args = ["time python measure.py", "-s", source, "-d", data, "-c", "OOO", "-t", num_tiles, "-o", tmp_output, "-e", epochs[app][input], "-n", str(COMPUTE_EDGES)]
          else:
            data = "/home/ts20/share/graphs/" + app + "/" + input
            cmd_args = ["time python measure.py", "-s", source, "-d", data, "-c", "OOO", "-t", num_tiles, "-o", tmp_output]
          cmd = " ".join(cmd_args)
          run(cmd, tmp_output, exp_dir + output) 

# EXPERIMENTS
experiments = {
                1: run_one,
                2: run_two,
                3: run_three,
                4: run_four
              }

def main():
  global apps

  args = parse_args()

  if args.app:
    apps = [args.app]
  if args.experiment:
    experiments[args.experiment]()
  else:
    run_one()
    #run_two()
    #run_three()
    #run_four()

if __name__ == "__main__":
  main()
