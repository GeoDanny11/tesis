import subprocess
import re
import os

def modify_file(filename, params):
	file = open(filename,"r")
	lines = list(file.read().split("\n"))
	file.close()
	file = open(filename,"w")
	for line in lines:
		found = False
		for message, value in params:
			if(line.find(message) != -1):
				found = True
				file.write(message + "\t" + value)
				break
		if(found == False):
			file.write(line)
		file.write("\n")


def execute(cmd, message = ""):
	print("******** START COMMAND = " + str(cmd) + " *************")
	popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
	for stdout_line in iter(popen.stdout.readline, ""):
		if(str(stdout_line).strip() == ""):
			continue
		print(str(stdout_line), end = '')
		if message != "" and str(stdout_line).find(message) != -1:
			popen.kill()
	print("******** FINISH COMMAND = " + str(cmd) + " *************")
		


file = open("SOURCE.txt", "r")
lines = list(file.read().split('\n'))
for simulation_number, line in enumerate(lines):
	modify_file("inparam_basic", [ ["SIMULATION_TYPE", "single"], ["SEISMOGRAM_LENGTH", "1800."], ["RECFILE_TYPE", "stations"], 
	["MESHNAME", "PREM_50s"], ["ATTENUATION", "true"], ["SAVE_SNAPSHOTS", "true"]])
	data = line.split()
	if len(data) < 3:
		continue
	modify_file("inparam_source", [ ["SOURCE_DEPTH", data[0]], ["SOURCE_LAT", data[1]], ["SOURCE_LON", data[2]] ])
	execute(["./submit.csh", "source" + str(simulation_number+1)])
	execute(["tail", "-f", "./source" + str(simulation_number+1) + "/OUTPUT_source" + str(simulation_number+1)], "PROGRAM axisem FINISHED")

	#descomentar esto para ejecutar el punto 3 del SOLVER
	#modify_file("inparam_basic", [ ["SIMULATION_TYPE", "moment"], ["SAVE_SNAPSHOTS", "false"]])
	#execute(["./submit.csh", "source" + str(simulation_number+1) + + "_run"], "")
	#execute(["tail", "-f", "./source" + str(simulation_number+1) + "_run/MZZ/OUTPUT_MZZ"], "PROGRAM axisem FINISHED")
	execute(["./start_helper.sh", "source" + str(simulation_number+1)], "")
	#execute(["./bash_executer.sh", "source" + str(simulation_number+1) + "_run"], "")



file.close()


