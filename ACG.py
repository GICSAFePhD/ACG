import sys
sys.path.append('.')

import numpy as np
import math
import networkx as nx
import graphviz as gv

class ACG():
	def create_graph_structure(self,RML,example = 1):

		NetElements =       RML.Infrastructure.Topology.NetElements
		NetRelations =		RML.Infrastructure.Topology.NetRelations
		SwitchesIS =        RML.Infrastructure.FunctionalInfrastructure.SwitchesIS
		LevelCrossingsIS =  RML.Infrastructure.FunctionalInfrastructure.LevelCrossingsIS
		Platforms =         RML.Infrastructure.FunctionalInfrastructure.Platforms
		Borders =           RML.Infrastructure.FunctionalInfrastructure.Borders
		BufferStops =       RML.Infrastructure.FunctionalInfrastructure.BufferStops
		Crossings =         RML.Infrastructure.FunctionalInfrastructure.Crossings
		SignalsIS =         RML.Infrastructure.FunctionalInfrastructure.SignalsIS

		network = {}

		for netElements in NetElements.NetElement:
			if netElements.ElementCollectionUnordered == None:
				network[netElements.Id] = {}

		for netRelations in NetRelations.NetRelation:
			if netRelations.Navigability != 'None' and netRelations.PositionOnA != None:
				aux = netRelations.Id.split('_')[1].split('ne')
				#print(aux)
				#if len(aux) > 3:
				nodeBegin = 'ne'+aux[1]
				nodeEnd = 'ne'+aux[2]
				#print(nodeBegin,nodeEnd)
				if 'Neighbour' not in network[nodeBegin]:	
					network[nodeBegin] |= {'Neighbour':[]}
				if 'Neighbour' not in network[nodeEnd]:	
					network[nodeEnd] |= {'Neighbour':[]}

				network[nodeBegin]['Neighbour'].append(nodeEnd)
				network[nodeEnd]['Neighbour'].append(nodeBegin)

		if SwitchesIS != None: 
			for SwitchIS in SwitchesIS[0].SwitchIS:
				if (SwitchIS.Type == "ordinarySwitch"):

					Net = SwitchIS.LeftBranch[0].NetRelationRef.split('_')[1].split('ne')
					nodeLeft1 = 'ne' + Net[1]        
					nodeLeft2 = 'ne' + Net[2]  
					Net = SwitchIS.RightBranch[0].NetRelationRef.split('_')[1].split('ne')
					nodeRight1 = 'ne' + Net[1]        
					nodeRight2 = 'ne' + Net[2]  
					
					continueCourse = SwitchIS.ContinueCourse
					branchCourse = SwitchIS.BranchCourse

					nodeStart = nodeLeft1 if (nodeLeft1 == nodeRight1 or nodeLeft1 == nodeRight2) else nodeLeft2
					nodeLeft = nodeLeft2 if (nodeStart == nodeLeft1) else nodeLeft1
					nodeRight = nodeRight2 if (nodeStart == nodeRight1) else nodeRight1

					nodeContinue = nodeRight if continueCourse == "Right" else nodeLeft
					nodeBranch = nodeLeft if branchCourse == "Left" else nodeRight

					if 'Switch' not in network[nodeStart]:
						network[nodeStart] |= {'Switch':[]}
					if 'Switch_C' not in network[nodeContinue]:
						network[nodeContinue] |= {'Switch_C':[]}
					if 'Switch_B' not in network[nodeBranch]:
						network[nodeBranch] |= {'Switch_B':[]}

					network[nodeStart]['Switch'].append(SwitchIS.Name[0].Name)
					network[nodeContinue]['Switch_C'].append(SwitchIS.Name[0].Name)    
					network[nodeBranch]['Switch_B'].append(SwitchIS.Name[0].Name)      
				
				if (SwitchIS.Type == "doubleSwitchCrossing"):
					node = SwitchIS.SpotLocation[0].NetElementRef

					straightBranch_A = SwitchIS.StraightBranch[0].NetRelationRef#.split('_')[1]
					straightBranch_B = SwitchIS.StraightBranch[1].NetRelationRef#.split('_')[1]
					turningBranch_A = SwitchIS.TurningBranch[0].NetRelationRef#.split('_')[1]
					turningBranch_B = SwitchIS.TurningBranch[1].NetRelationRef#.split('_')[1]

					straightBranch_1 = straightBranch_A if node in straightBranch_A else straightBranch_B
					turningBranch_1 = turningBranch_A if node in turningBranch_A else turningBranch_B
					straightBranch_2 = straightBranch_B if node in straightBranch_A else straightBranch_B
					turningBranch_2 = turningBranch_B if node in turningBranch_A else turningBranch_B

					nodeStart = node
					nodeInt = straightBranch_1.split('_')[1].split('ne')[1:]
					nodeEnd = 'ne'+nodeInt[0] if str(nodeStart[2:]) == nodeInt[1] else 'ne'+nodeInt[1]

					#print(f'S:{nodeStart} {nodeEnd}')
						
					if 'Switch_X' not in network[nodeStart]:
						network[nodeStart] |= {'Switch_X':[]}
					if 'Switch_X' not in network[nodeEnd]:
						network[nodeEnd] |= {'Switch_X':[]}
					if SwitchIS.Name[0].Name not in network[nodeStart]['Switch_X']:
						network[nodeStart]['Switch_X'].append(SwitchIS.Name[0].Name)
					if SwitchIS.Name[0].Name not in network[nodeEnd]['Switch_X']:
						network[nodeEnd]['Switch_X'].append(SwitchIS.Name[0].Name)

					nodeStart = node
					nodeInt = turningBranch_1.split('_')[1].split('ne')[1:]
					nodeEnd = 'ne'+nodeInt[0] if str(nodeStart[2:]) == nodeInt[1] else 'ne'+nodeInt[1]

					#print(f'T:{nodeStart} {nodeEnd}')
						
					if 'Switch_X' not in network[nodeStart]:
						network[nodeStart] |= {'Switch_X':[]}
					if 'Switch_X' not in network[nodeEnd]:
						network[nodeEnd] |= {'Switch_X':[]}
					if SwitchIS.Name[0].Name not in network[nodeStart]['Switch_X']:
						network[nodeStart]['Switch_X'].append(SwitchIS.Name[0].Name)
					if SwitchIS.Name[0].Name not in network[nodeEnd]['Switch_X']:
						network[nodeEnd]['Switch_X'].append(SwitchIS.Name[0].Name)

					nodeStart = ['ne'+x for x in straightBranch_2.split('_')[1].split('ne')[1:] if x in turningBranch_2.split('_')[1].split('ne')[1:]][0]
					nodeInt = straightBranch_2.split('_')[1].split('ne')[1:]
					nodeEnd = 'ne'+nodeInt[0] if str(nodeStart[2:]) == nodeInt[1] else 'ne'+nodeInt[1]

					#print(f'S:{nodeStart} {nodeEnd}')
						
					if 'Switch_X' not in network[nodeStart]:
						network[nodeStart] |= {'Switch_X':[]}
					if 'Switch_X' not in network[nodeEnd]:
						network[nodeEnd] |= {'Switch_X':[]}
					if SwitchIS.Name[0].Name not in network[nodeStart]['Switch_X']:
						network[nodeStart]['Switch_X'].append(SwitchIS.Name[0].Name)
					if SwitchIS.Name[0].Name not in network[nodeEnd]['Switch_X']:
						network[nodeEnd]['Switch_X'].append(SwitchIS.Name[0].Name)

					nodeStart = ['ne'+x for x in straightBranch_2.split('_')[1].split('ne')[1:] if x in turningBranch_2.split('_')[1].split('ne')[1:]][0]
					nodeInt = turningBranch_2.split('_')[1].split('ne')[1:]
					nodeEnd = 'ne'+nodeInt[0] if str(nodeStart[2:]) == nodeInt[1] else 'ne'+nodeInt[1]

					#print(f'T:{nodeStart} {nodeEnd}')
						
					if 'Switch_X' not in network[nodeStart]:
						network[nodeStart] |= {'Switch_X':[]}
					if 'Switch_X' not in network[nodeEnd]:
						network[nodeEnd] |= {'Switch_X':[]}
					if SwitchIS.Name[0].Name not in network[nodeStart]['Switch_X']:
						network[nodeStart]['Switch_X'].append(SwitchIS.Name[0].Name)
					if SwitchIS.Name[0].Name not in network[nodeEnd]['Switch_X']:
						network[nodeEnd]['Switch_X'].append(SwitchIS.Name[0].Name)
		
		if LevelCrossingsIS != None:  
			for LevelCrossingIS in LevelCrossingsIS[0].LevelCrossingIS:
				#print(LevelCrossingIS.SpotLocation[0].NetElementRef,LevelCrossingIS.Name[0].Name)
				node = LevelCrossingIS.SpotLocation[0].NetElementRef
				levelCrossing = LevelCrossingIS.Name[0].Name

				if 'LevelCrossing' not in network[node]:
					network[node] |= {'LevelCrossing':[]}
				if levelCrossing not in network[node]['LevelCrossing']:
					network[node]['LevelCrossing'].append(levelCrossing)

		if Platforms != None:
			for Platform in Platforms[0].Platform:
				node = Platform.LinearLocation[0].AssociatedNetElement[0].NetElementRef
				platform = Platform.Name[0].Name

				if 'Platform' not in network[node]:
					network[node] |= {'Platform':[]}
				if platform not in network[node]['Platform']:
					network[node]['Platform'].append(platform)

		if Borders != None:
			for Border in Borders[0].Border:
				node = Border.SpotLocation[0].NetElementRef
				border = Border.Name[0].Name

				if 'Border' not in network[node]:
					network[node] |= {'Border':[]}
				if border not in network[node]['Border']:
					network[node]['Border'].append(border)

		if BufferStops != None:
			for BufferStop in BufferStops[0].BufferStop:
				node = BufferStop.SpotLocation[0].NetElementRef
				bufferStop = BufferStop.Name[0].Name

				if 'BufferStop' not in network[node]:
					network[node] |= {'BufferStop':[]}
				if bufferStop not in network[node]['BufferStop']:
					network[node]['BufferStop'].append(bufferStop)

		if Crossings != None:
			for Crossing in Crossings[0].Crossing:
				crossing = Crossing.Name[0].Name

				Net = Crossing.External[0].Ref.split('_')[1].split('ne')
				node1 = 'ne' + Net[1]        
				node2 = 'ne' + Net[2]  

				Net = Crossing.External[1].Ref.split('_')[1].split('ne')
				node3 = 'ne' + Net[1]        
				node4 = 'ne' + Net[2]  

				if 'Crossing' not in network[node1]:
					network[node1] |= {'Crossing':[]}
				if 'Crossing' not in network[node2]:
					network[node2] |= {'Crossing':[]}
				if 'Crossing' not in network[node3]:
					network[node3] |= {'Crossing':[]}
				if 'Crossing' not in network[node4]:
					network[node4] |= {'Crossing':[]}

				if crossing not in network[node1]['Crossing']:
					network[node1]['Crossing'].append(crossing)
				if crossing not in network[node2]['Crossing']:
					network[node2]['Crossing'].append(crossing)
				if crossing not in network[node3]['Crossing']:
					network[node3]['Crossing'].append(crossing)
				if crossing not in network[node4]['Crossing']:
					network[node4]['Crossing'].append(crossing)

		if SignalsIS != None:
			for SignalIS in SignalsIS.SignalIS:
				node = SignalIS.SpotLocation[0].NetElementRef
				signal = SignalIS.Name[0].Name

				if 'Signal' not in network[node]:
					network[node] |= {'Signal':[]}
				if signal not in network[node]['Signal']:
					network[node]['Signal'].append(signal)
		
		return network

	def print_network(self,network):
		for element in network:
			print(f'{element} {network[element]}\t')

	def create_graph(self,RML,network,example = 1):

		NetRelations =      RML.Infrastructure.Topology.NetRelations
		SignalsIS =         RML.Infrastructure.FunctionalInfrastructure.SignalsIS
		Routes =            RML.Interlocking.AssetsForIL[0].Routes

		Graph = gv.Graph('finite_state_machine',filename='a.gv', graph_attr={'overlap':'false','rankdir':"LR",'splines':'true','center':'1','labelloc':'t'},node_attr={'fillcolor': 'white', 'style': 'filled,bold', 'pendwidth':'5', 'fontname': 'Courier New', 'shape': 'Mrecord'}) #node_attr={'color': 'lightgreen', 'style': 'filled', 'size' : '8.5'}
		G_Topology = nx.Graph()

		Signal_net = {}
		Signal_labels = {}
		for SignalIS in SignalsIS.SignalIS:
			Signal_net[SignalIS.Id] = {'net':SignalIS.SpotLocation[0].NetElementRef, 'equivalent':SignalIS.Designator[0].Entry[7:]}

		for NetRelation in NetRelations.NetRelation:
			if (NetRelation.Navigability != "None" and any(i.isdigit() for i in NetRelation.ElementA.Ref)): #ONLY NAVIGABILITY
				#print(f'{NetRelation.ElementA.Ref} -> {NetRelation.ElementB.Ref}')
				#Graph.edge(NetRelation.ElementA.Ref,NetRelation.ElementB.Ref)
				G_Topology.add_edge(NetRelation.ElementA.Ref,NetRelation.ElementB.Ref)

		i = 1
		for Route in Routes.Route:
			entry_signal = Route.RouteEntry.RefersTo.Ref.split('_')[1]
			exit_signal = Route.RouteExit.RefersTo.Ref.split('_')[1]

			entry_net = Signal_net[entry_signal]['net']
			exit_net = Signal_net[exit_signal]['net']
			
			equivalent_entry_signal = Signal_net[entry_signal]['equivalent']
			equivalent_exit_signal = Signal_net[exit_signal]['equivalent']

			path = nx.shortest_path(G_Topology, source=entry_net, target=exit_net) 
			
			if len(path) == 1:
				Graph.edge(entry_net,exit_net,label = f'R_{i:02d}')
			else:
				for p in range(len(path)-1):
					Graph.edge(path[p],path[p+1],label = f'R_{i:02d}')

			#print(f'R_{i:02d} | {entry_net} --> ({equivalent_entry_signal}) --> {path} --> ({equivalent_exit_signal}) --> {exit_net}')

			i = i + 1

		routed = []
		for i in Graph.body:
			if "--" in i:
				x = i[1:-1].split(" ")
				routed.append([x[0],x[2]])

		#print(routed)

		for NetRelation in NetRelations.NetRelation:
			if (NetRelation.Navigability != "None" and any(i.isdigit() for i in NetRelation.ElementA.Ref)): #ONLY NAVIGABILITY
				if not ( [NetRelation.ElementA.Ref,NetRelation.ElementB.Ref] in routed or [NetRelation.ElementB.Ref,NetRelation.ElementA.Ref] in routed):
					Graph.edge(NetRelation.ElementA.Ref,NetRelation.ElementB.Ref)
				
		for element in network:
			data = f'<<table border=\"0\" cellborder=\"0\" cellpadding=\"3\" bgcolor=\"white\"><tr><td bgcolor=\"black\" align=\"center\" colspan=\"2\"><font color=\"white\">{element}</font></td></tr>'

			if 'Switch' in network[element]:
				data += f'<tr><td bgcolor="red" align="right">Switch</td>'
				data += f'<td align="left" port="r2">{' '.join(network[element]['Switch'])}</td></tr>'

			if 'Switch_X' in network[element]:
				data += f'<tr><td bgcolor="darkred" align="right">Double Switch</td>'
				data += f'<td align="left" port="r2">{' '.join(network[element]['Switch_X'])}</td></tr>'

			if 'Border' in network[element]:
				data += f'<tr><td bgcolor="lightslateblue" align="right">Border</td>'
				data += f'<td align="left" port="r2">{' '.join(network[element]['Border'])}</td></tr>'

			if 'BufferStop' in network[element]:
				data += f'<tr><td bgcolor="olive" align="right">BufferStop</td>'
				data += f'<td align="left" port="r2">{' '.join(network[element]['BufferStop'])}</td></tr>'

			if 'LevelCrossing' in network[element]:
				data += f'<tr><td bgcolor="darkcyan" align="right">LevelCrossing</td>'
				data += f'<td align="left" port="r2">{' '.join(network[element]['LevelCrossing'])}</td></tr>'

			if 'Platform' in network[element]:
				data += f'<tr><td bgcolor="cornflowerblue" align="right">Platform</td>'
				data += f'<td align="left" port="r2">{' '.join(network[element]['Platform'])}</td></tr>'

			if 'Crossing' in network[element]:
				data += f'<tr><td bgcolor="pink" align="right">Crossing</td>'
				data += f'<td align="left" port="r2">{' '.join(network[element]['Crossing'])}</td></tr>'

			if 'Signal' in network[element]:
				data += f'<tr><td bgcolor="yellowgreen" align="right">Signal</td>'
				data += f'<td align="left" port="r2">{' '.join(network[element]['Signal'])}</td></tr>'

			data += '</table>>'

			Graph.node(element,label = data)

		graph_file = "App//Layouts//Example_"+str(example)+"//Graph"

		Graph.render(graph_file,format='svg', view = True)

	def calculate_parameters(self,network,example = 1):

		# TODO FIX COUNTER! SWITCHES ARE UNDERCOUNTED AND DOUBLE ARE OVERCOUNTED!

		singleSwitches = []
		doubleSwitches = []
		scissorCrossings = []
		platforms = []

		n_netElements = len(network)
		n_switches = 0
		n_doubleSwitch = 0
		n_borders = 0
		n_buffers = 0
		n_levelCrossings = 0
		n_platforms = 0
		n_scissorCrossings = 0
		n_signals_1 = 0
		n_signals_2 = 0
		n_signals_3 = 0
		n_signals_S = 0
		n_signals_C = 0
		n_signals_B = 0
		n_signals_L = 0
		n_signals_T = 0
		n_signals_X = 0
		n_signals_P = 0
		n_signals_J = 0

		for element in network:
			if "Switch" in network[element]:
				for singleSwitch in network[element]['Switch']:
					if singleSwitch not in singleSwitches:
						singleSwitches.append(singleSwitch)

			if 'Switch_X' in network[element]:
				for doubleSwitch in network[element]['Switch_X']:
					if doubleSwitch not in doubleSwitches:
						doubleSwitches.append(doubleSwitch)
				
			if 'Border' in network[element]:
				n_borders = n_borders + 1

			if 'BufferStop' in network[element]:
				n_buffers = n_buffers + 1

			if 'LevelCrossing' in network[element]:
				n_levelCrossings = n_levelCrossings + 1

			if 'Platform' in network[element]:
				for platform in network[element]['Platform']:
					if platform not in platforms:
						platforms.append(platform)

			if 'Crossing' in network[element]:
				for scissorCrossing in network[element]['Crossing']:
					if scissorCrossing not in scissorCrossings:
						scissorCrossings.append(scissorCrossing)

			if 'Signal' in network[element]:
				for signal in network[element]['Signal']:
					if 'S' in signal:
						n_signals_S = n_signals_S + 1
					if 'C' in signal:
						n_signals_C = n_signals_C + 1
					if 'B' in signal:
						n_signals_B = n_signals_B + 1
					if 'L' in signal:
						n_signals_L = n_signals_L + 1
					if 'T' in signal:
						n_signals_T = n_signals_T + 1
					if 'X' in signal:
						n_signals_X = n_signals_X + 1
					if 'P' in signal:
						n_signals_P = n_signals_P + 1
					if 'J' in signal:
						n_signals_J = n_signals_J + 1

		n_switches = len(singleSwitches)
		n_doubleSwitch = len(doubleSwitches)
		n_scissorCrossings = len(scissorCrossings)
		n_platforms = len(platforms)

		n_signals_1 = 0
		n_signals_2 = n_signals_T + n_signals_B + n_signals_P
		n_signals_3 = n_signals_S + n_signals_C + n_signals_L + n_signals_X + n_signals_J

		N = n_netElements + n_switches + 2*n_doubleSwitch + n_scissorCrossings + n_levelCrossings + 2*n_signals_2 + 2*n_signals_3
		M = N - n_netElements

		print(f'n_netElements:{n_netElements}\nn_switch:{n_switches}\nn_doubleSwitch:{n_doubleSwitch}\nn_borders:{n_borders}\nn_buffers:{n_buffers}\nn_levelCrossings:{n_levelCrossings}\nn_platforms:{n_platforms}\nn_scissorCrossings:{n_scissorCrossings}\nn_signals:{n_signals_1+n_signals_2+n_signals_3}')


		return N,M,n_netElements,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings,n_signals_1,n_signals_2,n_signals_3

	def createPacket(self,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings,n_signals,example = 1):
		node = 'my_package'
				
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
		
		# Include body
		packet = 'my_package'
		f.write(f'\tpackage {packet} is\n')
		
		f.write(f'\t\ttype routeCommands is (RELEASE,RESERVE,LOCK);\r\n')
		f.write(f'\t\ttype nodeStates is (OCCUPIED,FREE);\r\n')

		f.write(f'\t\ttype objectLock is (RELEASED,RESERVED,LOCKED);\r\n')

		if n_switches > 0:
			f.write(f'\t\ttype singleSwitchStates is (NORMAL,REVERSE,TRANSITION);\r\n')	

			type = 'sSwitch_type'
			f.write(f'\t\ttype {type} is record\n')
			f.write(f'\t\t\tmsb : std_logic;\n')
			f.write(f'\t\t\tlsb : std_logic;\n')
			f.write(f'\t\tend record {type};\n')
		
		if n_switches > 1:
			type = 'sSwitches_type'
			f.write(f'\t\ttype {type} is record\n')
			f.write(f'\t\t\tmsb : std_logic_vector({n_switches}-1 downto 0);\n')
			f.write(f'\t\t\tlsb : std_logic_vector({n_switches}-1 downto 0);\n')
			f.write(f'\t\tend record {type};\n')

		if n_doubleSwitch > 0:	
			f.write(f'\t\ttype doubleSwitchStates is (DOUBLE_NORMAL,DOUBLE_REVERSE,REVERSE_NORMAL,NORMAL_REVERSE,TRANSITION);\r\n')	

			type = 'dSwitch_type'
			f.write(f'\t\ttype {type} is record\n')
			f.write(f'\t\t\tmsb : std_logic;\n')
			f.write(f'\t\t\tlsb : std_logic;\n')
			f.write(f'\t\tend record {type};\n')
		
		if n_doubleSwitch > 1:
			type = 'dSwitches_type'
			f.write(f'\t\ttype {type} is record\n')
			f.write(f'\t\t\tmsb : std_logic_vector({n_doubleSwitch}-1 downto 0);\n')
			f.write(f'\t\t\tlsb : std_logic_vector({n_doubleSwitch}-1 downto 0);\n')
			f.write(f'\t\tend record {type};\n')

		if n_scissorCrossings > 0:	
			f.write(f'\t\ttype scissorCrossingStates is (NORMAL,REVERSE,TRANSITION);\r\n')	

			type = 'scissorCrossing_type'
			f.write(f'\t\ttype {type} is record\n')
			f.write(f'\t\t\tmsb : std_logic;\n')
			f.write(f'\t\t\tlsb : std_logic;\n')
			f.write(f'\t\tend record {type};\n')
		
		if n_scissorCrossings > 1:
			type = 'scissorCrossings_type'
			f.write(f'\t\ttype {type} is record\n')
			f.write(f'\t\t\tmsb : std_logic_vector({n_scissorCrossings}-1 downto 0);\n')
			f.write(f'\t\t\tlsb : std_logic_vector({n_scissorCrossings}-1 downto 0);\n')
			f.write(f'\t\tend record {type};\n')

		if n_levelCrossings >0:
			f.write(f'\t\ttype levelCrossingStates is (DOWN,UP,TRANSITION);\r\n')

			type = 'levelCrossing_type'
			f.write(f'\t\ttype {type} is record\n')
			f.write(f'\t\t\tmsb : std_logic;\n')
			f.write(f'\t\t\tlsb : std_logic;\n')
			f.write(f'\t\tend record {type};\n')
				
		if n_levelCrossings > 1:
			type = 'levelCrossings_type'
			f.write(f'\t\ttype {type} is record\n')
			f.write(f'\t\t\tmsb : std_logic_vector({n_levelCrossings}-1 downto 0);\n')
			f.write(f'\t\t\tlsb : std_logic_vector({n_levelCrossings}-1 downto 0);\n')
			f.write(f'\t\tend record {type};\n')
		
		if n_signals > 0:
			f.write(f'\t\ttype signalStates is (RED,DOUBLE_YELLOW,YELLOW,GREEN);\r\n')

			type = 'signal_type'
			f.write(f'\t\ttype {type} is record\n')
			f.write(f'\t\t\tmsb : std_logic;\n')
			f.write(f'\t\t\tlsb : std_logic;\n')
			f.write(f'\t\tend record {type};\n')
				
		if n_signals > 1:
			type = 'signals_type'
			f.write(f'\t\ttype {type} is record\n')
			f.write(f'\t\t\tmsb : std_logic_vector({n_signals}-1 downto 0);\n')
			f.write(f'\t\t\tlsb : std_logic_vector({n_signals}-1 downto 0);\n')
			f.write(f'\t\tend record {type};\n')

		#f.write(f'\t\ttype int_array is array(0 to {n_signals}-1) of integer;\r\n')
		
		f.write(f'\tend {packet};')

		# Close file
		f.close()
		
	def initialComment(self,node,f):
		f.write(f'--  {node}.vhdl : Automatically generated using ACG\r\n')
		
	def includeLibrary(self,f,packet = False):
		f.write(f'library IEEE;\n')
		f.write(f'use IEEE.std_logic_1164.all;\n')
		f.write(f'use IEEE.numeric_std.all;\r\n')
		if (packet):
			f.write(f'--Declare the package\r\n')
			f.write(f'use work.my_package.all;\r\n')
			
	def createGlobal(self,N,M,example = 1):
			
		node = 'global'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
			
		# system entity
		wrapper = 'global'
		f.write(f'\tentity {wrapper} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tuart_rxd_i : in std_logic;\n')
		f.write(f'\t\t\tuart_txd_o : out std_logic;\n')
		f.write(f'\t\t\tleds : out std_logic_vector(4-1 downto 0);\n')
		f.write(f'\t\t\trgb_1 : out std_logic_vector(3-1 downto 0);\n')
		f.write(f'\t\t\trgb_2 : out std_logic_vector(3-1 downto 0);\n')
		f.write(f'\t\t\tselector1 : in std_logic;\n')
		f.write(f'\t\t\tselector2 : in std_logic;\n')
		f.write(f'\t\t\tReset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {wrapper};\r\n') 
	
		f.write(f'architecture Behavioral of {wrapper} is\r\n')            

		# uartControl component
		uartControl = 'uartControl'
		f.write(f'\tcomponent {uartControl} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tN : out integer;\n')
		f.write(f'\t\t\twrite : in std_logic;\n')
		f.write(f'\t\t\tempty_in : in std_logic;\n') 
		f.write(f'\t\t\trd_uart : out std_logic;\n')
		f.write(f'\t\t\twr_uart : out std_logic;\n')  
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend component {uartControl};\r\n')
		
		# system component 
		system = "system"
		f.write(f'\tcomponent {system} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		
		f.write(f'\t\t\treset_uart : out std_logic;\n')
		f.write(f'\t\t\tr_available : in std_logic;\n')
		f.write(f'\t\t\tread : out std_logic;\n')
		f.write(f'\t\t\twrite : out std_logic;\n')
		f.write(f'\t\t\tr_data : in std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\tselector1 : in std_logic;\n')
		f.write(f'\t\t\tselector2 : in std_logic;\n')
		f.write(f'\t\t\tN : in integer;\n')
		f.write(f'\t\t\tleds : out std_logic_vector(4-1 downto 0);\n')
		f.write(f'\t\t\tled_rgb_1 : out std_logic_vector(3-1 downto 0);\n')
		f.write(f'\t\t\tled_rgb_2 : out std_logic_vector(3-1 downto 0);\n')
		f.write(f'\t\t\tw_data : out std_logic_vector(8-1 downto 0);\n')
	
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend component {system};\r\n')
		
		f.write(f'\tsignal w_data_signal, r_dataSignal: std_logic_vector(7 downto 0);\n')
		f.write(f'\tsignal rd_uart_signal, wr_uart_signal: std_logic;\n')
		f.write(f'\tsignal emptySignal,empty_s,tx_empty_s,switch_s,reset_s,reset_uart: std_logic;\n')
		f.write(f'\tsignal led_s : std_logic_vector(4-1 downto 0);\n')
		f.write(f'\tsignal led_rgb_1,led_rgb_2 : std_logic_vector(3-1 downto 0);\n\r')
		f.write(f'\tsignal N_s : integer;\n')
		f.write(f'\tsignal read_s,write_s : std_logic;\n')
		
		f.write(f'begin\r\n')
		
		f.write(f'\tuart_inst : entity work.uart\n')
		
		f.write(f'\t\tgeneric map(\n')
		f.write(f'\t\t\tDVSR      => 407,	-- baud rate divisor DVSR = 125M / (16 * baud rate) baud rate = 19200\n')
		f.write(f'\t\t\tDVSR_BIT  => 9,   --  bits of DVSR\n')
		f.write(f'\t\t\tFIFO_W_RX	=> {str(int(round(np.log2(N)))+1)}, 	--  addr bits of FIFO words in FIFO=2^FIFO_W\n')
		f.write(f'\t\t\tFIFO_W_TX	=> {str(int(round(np.log2(M)))+1)} 	--  addr bits of FIFO words in FIFO=2^FIFO_W\n')			
		f.write(f'\t\t)\n')
		f.write(f'\t\tport map(\n')
		f.write(f'\t\t\tclk 		=> clock,\n')
		f.write(f'\t\t\treset 		=> reset,\n')
		f.write(f'\t\t\trd_uart 	=> rd_uart_signal,\n')
		f.write(f'\t\t\twr_uart 	=> wr_uart_signal,\n')
		f.write(f'\t\t\trx 			=> uart_rxd_i,\n')
		f.write(f'\t\t\tw_data 		=> w_data_signal,\n')
		f.write(f'\t\t\trx_empty	=> emptySignal,\n')
		f.write(f'\t\t\tr_data  	=> r_dataSignal,\n')
		f.write(f'\t\t\ttx  		=> uart_txd_o\n')	   
		f.write(f'\t\t);\n')
		
		f.write(f'\t{uartControl}_i : {uartControl}\n')
		f.write(f'\t\tport map(\n')
		f.write(f'\t\t\tclock => clock,\n')
		f.write(f'\t\t\treset => reset_uart,\n')
		f.write(f'\t\t\tN => N_s,\n')
		f.write(f'\t\t\twrite => write_s,\n')
		f.write(f'\t\t\tempty_in => emptySignal,\n')
		f.write(f'\t\t\trd_uart => rd_uart_signal,\n')
		f.write(f'\t\t\twr_uart => wr_uart_signal\n')
		f.write(f'\t\t);\r\n')
		
		f.write(f'\t{system}_i : {system}\n')
		f.write(f'\t\tport map(\n')
		f.write(f'\t\t\tclock => clock,\n')
		f.write(f'\t\t\treset => reset,\n')
		f.write(f'\t\t\treset_uart => reset_s,\n')
		f.write(f'\t\t\tr_available => rd_uart_signal,\n')
		f.write(f'\t\t\tread => read_s,\n')
		f.write(f'\t\t\twrite => write_s,\n')
		f.write(f'\t\t\tr_data => r_dataSignal,\n')
		f.write(f'\t\t\tselector1 => selector1,\n')
		f.write(f'\t\t\tselector2 => selector2,\n')
		f.write(f'\t\t\tN => N_s,\n')
		f.write(f'\t\t\tleds => led_s,\n')
		f.write(f'\t\t\tled_rgb_1 => led_rgb_1,\n')
		f.write(f'\t\t\tled_rgb_2 => led_rgb_2,\n')
		f.write(f'\t\t\tw_data => w_data_signal\n')
		f.write(f'\t\t);\r\n')  
		
		f.write(f'\trgb_1 <= led_rgb_1;\n')
		f.write(f'\trgb_2 <= led_rgb_2;\n')
		f.write(f'\tleds <= led_s;\n')
		f.write(f'\treset_uart <= Reset or reset_s;\r\n') 
			
		f.write(f'end Behavioral;')
		
		f.close()  # Close header file 
	  
	def createUARTs(self,N,M,example = 1):
		self.createUartControl(example)
		self.createUART(example)
		self.createUartBaudGenerator(example)
		self.createUartTx(example)
		self.createUartRx(example)
		self.createUartFIFO(example)
	
	def createUartControl(self,example = 1):
		node = 'uartControl'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
			
		# uartControl entity
		uartControl = "uartControl"
		f.write(f'\tentity {uartControl} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tN : out integer;\n')
		f.write(f'\t\t\twrite : in std_logic;\n')
		f.write(f'\t\t\tempty_in : in std_logic;\n')
		f.write(f'\t\t\trd_uart : out std_logic;\n')
		f.write(f'\t\t\twr_uart : out std_logic;\n')
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {uartControl};\r\n')

		f.write(f'architecture Behavioral of {uartControl} is\r\n')            
		
		f.write(f'begin\r\n')
		
		f.write(f'\treading : process(clock)\n')
		f.write(f'\t\tvariable count_i: integer := 0;\n')
		f.write(f'\t\tvariable L : integer := 0;\n')
		f.write(f'\tbegin\n')   
		f.write(f'\t\tif (clock = \'1\' and clock\'event) then\n')
		f.write(f'\t\t\tif reset = \'1\' then\n')          
		f.write(f'\t\t\t\tL := 0;\n') 
		f.write(f'\t\t\t\trd_uart <= \'0\';\n')
		f.write(f'\t\t\telsif empty_in = \'0\' then   -- Data available\n')
		f.write(f'\t\t\t\tcount_i := count_i + 1;\n')                          
		f.write(f'\t\t\t\tif count_i = 125E3 then    -- Count 100 msecs\n')
		f.write(f'\t\t\t\t\tcount_i := 0;\n')
		f.write(f'\t\t\t\t\trd_uart <= \'1\';     -- Request new data"+"\n')
		f.write(f'\t\t\t\t\tL := L + 1;\n')
		f.write(f'\t\t\t\telse\n')                    
		f.write(f'\t\t\t\t\trd_uart <= \'0\';\n');
		f.write(f'\t\t\t\tend if;\n')                     
		f.write(f'\t\t\telse                    -- No data\n')
		f.write(f'\t\t\t\tN <= L;\n')
		f.write(f'\t\t\t\trd_uart <= \'0\';\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\twriting : process(clock)\n')
		f.write(f'\t\tvariable count_j: integer := 0;\n')
		f.write(f'\tbegin\n')   
		f.write(f'\t\tif (clock = \'1\' and clock\'event) then\n')
		f.write(f'\t\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\t\twr_uart <= \'0\';\n')
		f.write(f'\t\t\telse\n')                    
		f.write(f'\t\t\t\twr_uart <= write;\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n') 
			
		f.write(f'end Behavioral;') 
		
		f.close()  # Close header file 

	def createUART(self,example = 1):
		node = 'uart'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
			
		# uart entity
		uart = "uart"
		f.write(f'\tentity {uart} is\n')
		f.write(f'\t\tgeneric(\n')
		f.write(f'\t\t\t-- 19200 baud, 8 data bits, 1 stop bit, 2^2 FIFO\n')
		f.write(f'\t\t\tDBIT: integer := 8; -- # data bits\n')
		f.write(f'\t\t\tSB_TICK: integer := 16;	-- # ticks for stop bits, 16/24/32 -- for 1/1.5/2 stop bits\n')
		f.write(f'\t\t\tDVSR: integer := 407; 	-- baud rate divisor -- DVSR = 125M / (16 * baud rate)\n')
		f.write(f'\t\t\tDVSR_BIT: integer := 9; 	-- # bits of DVSR\n')
		f.write(f'\t\t\tFIFO_W_TX: integer := 4; 	-- # addr bits of FIFO_TX # words in FIFO=2^FIFO_W\n')
		f.write(f'\t\t\tFIFO_W_RX: integer := 4 	-- # addr bits of FIFO_TX # words in FIFO=2^FIFO_W\n')
		f.write(f'\t\t);\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclk, reset : in std_logic;\n')
		f.write(f'\t\t\trd_uart, wr_uart : in std_logic;\n')
		f.write(f'\t\t\trx : in std_logic;\n')
		f.write(f'\t\t\tw_data : in std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\ttx_full, rx_empty : out std_logic;\n')
		f.write(f'\t\t\tr_data : out std_logic_vector(8-1 downto 0) ;\n')
		f.write(f'\t\t\ttx : out std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {uart};\r\n') 
	
		f.write(f'architecture Behavioral of {uart} is\r\n')            
		
		f.write(f'\tsignal rx_done_tick : std_logic;\n')
		f.write(f'\tsignal tick : std_logic;\n')
		f.write(f'\tsignal tx_fifo_out : std_logic_vector(8-1 downto 0);\n')
		f.write(f'\tsignal rx_data_out : std_logic_vector(8-1 downto 0);\n')
		f.write(f'\tsignal tx_empty, tx_fifo_not_empty : std_logic;\n')
		f.write(f'\tsignal tx_done_tick : std_logic;\r\n')
		
		f.write(f'begin\r\n')
		
		f.write(f'\tbaud_gen_unit: entity work.uart_baud_gen(Behavioral)\n')
		f.write(f'\t\tgeneric map(M => DVSR, N => DVSR_BIT)\n')
		f.write(f'\t\tport map(clk => clk, reset => reset,\n')
		f.write(f'\t\t\t\tq => open, max_tick => tick);\r\n')
		
		f.write(f'\tuart_rx_unit: entity work.uart_rx(Behavioral)\n')
		f.write(f'\t\tgeneric map(DBIT => DBIT, SB_TICK => SB_TICK)\n')
		f.write(f'\t\tport map(clk => clk, reset => reset, rx => rx,\n')
		f.write(f'\t\t\t\ts_tick => tick, rx_done_tick => rx_done_tick,\n')
		f.write(f'\t\t\t\td_out => rx_data_out);\r\n')
					
		f.write(f'\tfifo_rx_unit: entity work.fifo(Behavioral)\n')
		f.write(f'\t\tgeneric map(B => DBIT, W => FIFO_W_RX)\n')
		f.write(f'\t\tport map(clk => clk, reset => reset, rd => rd_uart,\n')
		f.write(f'\t\t\t\twr => rx_done_tick, w_data => rx_data_out,\n')
		f.write(f'\t\t\t\tempty => rx_empty, full => open, r_data => r_data);\r\n')
					
		f.write(f'\tfifo_tx_unit: entity work.fifo(Behavioral)\n')
		f.write(f'\t\tgeneric map(B => DBIT, W => FIFO_W_TX)\n')
		f.write(f'\t\tport map(clk => clk, reset => reset, rd => tx_done_tick,\n')
		f.write(f'\t\t\t\twr => wr_uart, w_data => w_data, empty => tx_empty,\n')
		f.write(f'\t\t\t\tfull => tx_full, r_data => tx_fifo_out);\r\n')
					
		f.write(f'\tuart_tx_unit: entity work.uart_tx(Behavioral)\n')
		f.write(f'\t\tgeneric map(DBIT => DBIT, SB_TICK => SB_TICK)\n')
		f.write(f'\t\tport map(clk => clk, reset => reset,\n')
		f.write(f'\t\t\t\ttx_start => tx_fifo_not_empty,\n')
		f.write(f'\t\t\t\ts_tick => tick, d_in => tx_fifo_out,\n')
		f.write(f'\t\t\t\ttx_done_tick => tx_done_tick, tx => tx);\r\n')
					
		f.write(f'\ttx_fifo_not_empty <= not tx_empty;\r\n')
			
		f.write(f'end Behavioral;') 
		
		f.close()  # Close header file

	def createUartBaudGenerator(self,example = 1):
		node = 'uart_baud_gen'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
			
		# uart_baud_gen entity
		uart_baud_gen = "uart_baud_gen"
		f.write(f'\tentity {uart_baud_gen} is\n')
		f.write(f'\t\tgeneric(\n')
		f.write(f'\t\t\tN : integer := 4; -- number of bits;\n')
		f.write(f'\t\t\tM : integer := 10 -- mod-M;\n')
		f.write(f'\t\t);\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclk, reset : in std_logic;\n')
		f.write(f'\t\t\tmax_tick : out std_logic;\n')
		f.write(f'\t\t\tq : out std_logic_vector(N-1 downto 0)\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {uart_baud_gen};\r\n') 

		f.write(f'architecture Behavioral of {uart_baud_gen} is\r\n')            
		
		f.write(f'\tsignal r_reg : unsigned(N-1 downto 0);\n')
		f.write(f'\tsignal r_next : unsigned(N-1 downto 0);\r\n')
		
		f.write(f'begin\r\n')
		
		f.write(f'\t-- printer\n')
		f.write(f'\tprocess(clk, reset)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (reset = \'1\') then\n')
		f.write(f'\t\t\tr_reg <= (others => \'0\');\n')
		f.write(f'\t\telsif rising_edge(clk) then\n')
		f.write(f'\t\t\tr_reg <= r_next;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')

		f.write(f'\t-- next-state logic\n')
		f.write(f'\tr_next <= (others => \'0\') when r_reg=(M-1) else r_reg + 1;\r\n')

		f.write(f'\t-- output logic\n')
		f.write(f'\tq <= std_logic_vector(r_reg);\n')
		f.write(f'\tmax_tick <= \'1\' when r_reg=(M-1) else \'0\';\r\n')
			
		f.write(f'end Behavioral;') 

		f.close()  # Close header file    

	def createUartTx(self,example = 1):
		node = 'uart_tx'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
			
		# uart_tx entity
		uart_tx = "uart_tx"
		f.write(f'\tentity {uart_tx} is\n')
		f.write(f'\t\tgeneric(\n')
		f.write(f'\t\t\tDBIT : integer := 8; -- # data bits;\n')
		f.write(f'\t\t\tSB_TICK : integer := 16 -- # ticks for stop bits;\n')
		f.write(f'\t\t);\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclk, reset : in std_logic;\n')
		f.write(f'\t\t\ttx_start : in std_logic;\n')
		f.write(f'\t\t\ts_tick : in std_logic;\n')
		f.write(f'\t\t\td_in : in std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\ttx_done_tick : out std_logic;\n')
		f.write(f'\t\t\ttx : out std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {uart_tx};\r\n') 
	
		f.write(f'architecture Behavioral of {uart_tx} is\r\n')            
		
		f.write(f'\ttype state_type is (idle, start, data, stop);\n')
		f.write(f'\tsignal state_reg, state_next: state_type;\n')
		f.write(f'\tsignal s_reg, s_next: unsigned(3 downto 0);\n')
		f.write(f'\tsignal n_reg, n_next: unsigned(2 downto 0);\n')
		f.write(f'\tsignal b_reg, b_next: std_logic_vector(7 downto 0);\n')
		f.write(f'\tsignal tx_reg, tx_next: std_logic;\r\n')
		
		f.write(f'begin\r\n')
		
		f.write(f'\t-- FSMD state & data registers\n')
		f.write(f'\tprocess(clk, reset)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\tstate_reg <= idle;\n')
		f.write(f'\t\t\ts_reg <= (others => \'0\');\n')
		f.write(f'\t\t\tn_reg <= (others => \'0\');\n')
		f.write(f'\t\t\tb_reg <= (others => \'0\');\n')
		f.write(f'\t\t\ttx_reg <= \'1\';\n')
		f.write(f'\t\telsif rising_edge(clk) then\n')
		f.write(f'\t\t\tstate_reg <= state_next;\n')
		f.write(f'\t\t\ts_reg <= s_next;\n')
		f.write(f'\t\t\tn_reg <= n_next;\n')
		f.write(f'\t\t\tb_reg <= b_next;\n')
		f.write(f'\t\t\ttx_reg <= tx_next;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\t-- next-state logic & datapath functional units/routing\n')
		f.write(f'\tprocess(state_reg, s_reg, n_reg, b_reg, s_tick, tx_reg, tx_start, d_in)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tstate_next <= state_reg;\n')
		f.write(f'\t\ts_next <= s_reg;\n')
		f.write(f'\t\tn_next <= n_reg;\n')
		f.write(f'\t\tb_next <= b_reg;\n')
		f.write(f'\t\ttx_next <= tx_reg;\n')
		f.write(f'\t\ttx_done_tick <= \'0\';\n')
		f.write(f'\t\tcase state_reg is\n')
		f.write(f'\t\t\twhen idle =>\n')
		f.write(f'\t\t\t\ttx_next <= \'1\';\n')
		f.write(f'\t\t\t\tif tx_start = \'1\' then\n')
		f.write(f'\t\t\t\t\tstate_next <= start;\n')
		f.write(f'\t\t\t\t\ts_next <= (others => \'0\');\n')
		f.write(f'\t\t\t\t\tb_next <= d_in;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\twhen start =>\n')
		f.write(f'\t\t\t\ttx_next <= \'0\';\n')
		f.write(f'\t\t\t\tif (s_tick = \'1\') then\n')
		f.write(f'\t\t\t\t\tif s_reg = 15 then\n')
		f.write(f'\t\t\t\t\t\tstate_next <= data;\n')
		f.write(f'\t\t\t\t\t\ts_next <= (others => \'0\');\n')
		f.write(f'\t\t\t\t\t\tn_next <= (others => \'0\');\n')
		f.write(f'\t\t\t\t\telse\n')
		f.write(f'\t\t\t\t\t\ts_next <= s_reg + 1;\n')
		f.write(f'\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\twhen data =>\n')
		f.write(f'\t\t\t\ttx_next <= b_reg(0);\n')
		f.write(f'\t\t\t\tif (s_tick = \'1\') then\n')
		f.write(f'\t\t\t\t\tif s_reg = 15 then\n')
		f.write(f'\t\t\t\t\t\ts_next <= (others => \'0\') ;\n')
		f.write(f'\t\t\t\t\t\tb_next <= \'0\' & b_reg(8-1 downto 1);\n')
		f.write(f'\t\t\t\t\t\tif n_reg = (DBIT - 1) then\n')
		f.write(f'\t\t\t\t\t\t\tstate_next <= stop;\n')
		f.write(f'\t\t\t\t\t\telse\n')
		f.write(f'\t\t\t\t\t\t\tn_next <= n_reg + 1 ;\n')
		f.write(f'\t\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\t\telse\n')
		f.write(f'\t\t\t\t\t\ts_next <= s_reg + 1;\n')
		f.write(f'\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\twhen stop =>\n')
		f.write(f'\t\t\t\ttx_next <= \'1\';\n')
		f.write(f'\t\t\t\tif (s_tick = \'1\') then\n')
		f.write(f'\t\t\t\t\tif s_reg = (SB_TICK - 1) then\n')
		f.write(f'\t\t\t\t\t\tstate_next <= idle;\n')
		f.write(f'\t\t\t\t\t\ttx_done_tick <= \'1\';\n')
		f.write(f'\t\t\t\t\telse\n')
		f.write(f'\t\t\t\t\t\ts_next <= s_reg + 1;\n')
		f.write(f'\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\tend case;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\ttx <= tx_reg;\r\n')
			
		f.write(f'end Behavioral;') 
		
		f.close()  # Close header file   

	def createUartRx(self,example = 1):
		node = 'uart_rx'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
			
		# uart_rx entity
		uart_rx = "uart_rx"
		f.write(f'\tentity {uart_rx} is\n')
		f.write(f'\t\tgeneric(\n')
		f.write(f'\t\t\tDBIT : integer := 8; -- # data bits;\n')
		f.write(f'\t\t\tSB_TICK : integer := 16 -- # ticks for stop bits;\n')
		f.write(f'\t\t);\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclk, reset : in std_logic;\n')
		f.write(f'\t\t\trx : in std_logic;\n')
		f.write(f'\t\t\ts_tick : in std_logic;\n')
		f.write(f'\t\t\trx_done_tick : out std_logic;\n')
		f.write(f'\t\t\td_out : out std_logic_vector(8-1 downto 0)\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {uart_rx};\r\n') 
	
		f.write(f'architecture Behavioral of {uart_rx} is\r\n')            
		
		f.write(f'\ttype state_type is (idle, start, data, stop);\n')
		f.write(f'\tsignal state_reg, state_next: state_type;\n')
		f.write(f'\tsignal s_reg, s_next: unsigned(3 downto 0);\n')
		f.write(f'\tsignal n_reg, n_next: unsigned(2 downto 0);\n')
		f.write(f'\tsignal b_reg, b_next: std_logic_vector(8-1 downto 0);\r\n')
		
		f.write(f'begin\r\n')
		
		f.write(f'\t-- FSMD state & data registers\n')
		f.write(f'\tprocess(clk, reset)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\tstate_reg <= idle;\n')
		f.write(f'\t\t\ts_reg <= (others => \'0\');\n')
		f.write(f'\t\t\tn_reg <= (others => \'0\');\n')
		f.write(f'\t\t\tb_reg <= (others => \'0\');\n')
		f.write(f'\t\telsif (clk\'event and clk = \'1\') then\n')
		f.write(f'\t\t\tstate_reg <= state_next;\n')
		f.write(f'\t\t\ts_reg <= s_next;\n')
		f.write(f'\t\t\tn_reg <= n_next;\n')
		f.write(f'\t\t\tb_reg <= b_next;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\t-- next_state logic & data path functional units/routing\n')
		f.write(f'\tprocess(state_reg, s_reg, n_reg, b_reg, s_tick, rx)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tstate_next <= state_reg;\n')
		f.write(f'\t\ts_next <= s_reg;\n')
		f.write(f'\t\tn_next <= n_reg;\n')
		f.write(f'\t\tb_next <= b_reg;\n')
		f.write(f'\t\trx_done_tick <= \'0\';\n')
		f.write(f'\t\tcase state_reg is\n')
		f.write(f'\t\t\twhen idle =>\n')
		f.write(f'\t\t\t\tif rx = \'0\' then\n')
		f.write(f'\t\t\t\t\tstate_next <= start;\n')
		f.write(f'\t\t\t\t\ts_next <= (others => \'0\');\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\twhen start =>\n')
		f.write(f'\t\t\t\tif (s_tick = \'1\') then\n')
		f.write(f'\t\t\t\t\tif s_reg = 8-1 then\n')
		f.write(f'\t\t\t\t\t\tstate_next <= data;\n')
		f.write(f'\t\t\t\t\t\ts_next <= (others => \'0\');\n')
		f.write(f'\t\t\t\t\t\tn_next <= (others => \'0\');\n')
		f.write(f'\t\t\t\t\telse\n')
		f.write(f'\t\t\t\t\t\ts_next <= s_reg + 1;\n')
		f.write(f'\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\twhen data =>\n')
		f.write(f'\t\t\t\tif (s_tick = \'1\') then\n')
		f.write(f'\t\t\t\t\tif s_reg = 15 then\n')
		f.write(f'\t\t\t\t\t\ts_next <= (others => \'0\');\n')
		f.write(f'\t\t\t\t\t\tb_next <= rx & b_reg(8-1 downto 1);\n')
		f.write(f'\t\t\t\t\t\tif n_reg = (DBIT-1) then\n')
		f.write(f'\t\t\t\t\t\t\tstate_next <= stop;\n')
		f.write(f'\t\t\t\t\t\telse\n')
		f.write(f'\t\t\t\t\t\t\tn_next <= n_reg + 1;\n')
		f.write(f'\t\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\t\telse\n')
		f.write(f'\t\t\t\t\t\ts_next <= s_reg + 1;\n')
		f.write(f'\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\twhen stop =>\n')
		f.write(f'\t\t\t\tif (s_tick = \'1\') then\n')
		f.write(f'\t\t\t\t\tif s_reg = (SB_TICK-1) then\n')
		f.write(f'\t\t\t\t\t\tstate_next <= idle;\n')
		f.write(f'\t\t\t\t\t\trx_done_tick <= \'1\';\n')
		f.write(f'\t\t\t\t\telse\n')
		f.write(f'\t\t\t\t\t\ts_next <= s_reg + 1;\n')
		f.write(f'\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\tend case;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\td_out <= b_reg;\r\n')
			
		f.write(f'end Behavioral;') 
		
		f.close()  # Close header file

	def createUartFIFO(self,example = 1):
		node = 'fifo'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
			
		# FIFO entity
		fifo = "fifo"
		f.write(f'\tentity {fifo} is\n')
		f.write(f'\t\tgeneric(\n')
		f.write(f'\t\t\tB : natural := 8; -- number of bits;\n')
		f.write(f'\t\t\tW : natural := 4  -- number of address bits;\n')
		f.write(f'\t\t);\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclk, reset : in std_logic;\n')
		f.write(f'\t\t\trd, wr : in std_logic;\n')
		f.write(f'\t\t\tw_data : in std_logic_vector(B-1 downto 0);\n')
		f.write(f'\t\t\tempty, full : out std_logic;\n')
		f.write(f'\t\t\tr_data : out std_logic_vector(B-1 downto 0)\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {fifo};\r\n') 
	
		f.write(f'architecture Behavioral of {fifo} is\r\n')            
		
		f.write(f'\ttype reg_file_type is array (2**W-1 downto 0) of std_logic_vector(B-1 downto 0);\n') 
		f.write(f'\tsignal array_reg: reg_file_type;\n')
		f.write(f'\tsignal w_ptr_reg, w_ptr_next, w_ptr_succ: std_logic_vector(W-1 downto 0);\n')
		f.write(f'\tsignal r_ptr_reg, r_ptr_next, r_ptr_succ: std_logic_vector(W-1 downto 0);\n')
		f.write(f'\tsignal full_reg, empty_reg, full_next, empty_next: std_logic;\n')
		f.write(f'\tsignal wr_op: std_logic_vector (1 downto 0);\n')
		f.write(f'\tsignal wr_en: std_logic;\r\n')
		
		f.write(f'begin\r\n')
		
		f.write(f'\t----------------\n')
		f.write(f'\t-- register file\n')
		f.write(f'\t----------------\n')
		f.write(f'\tprocess(clk, reset)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (reset = \'1\') then\n')
		f.write(f'\t\t\tarray_reg <= (others => (others => \'0\'));\n')
		f.write(f'\t\telsif (clk\'event and clk = \'1\') then\n')
		f.write(f'\t\t\tif wr_en = \'1\' then\n')
		f.write(f'\t\t\t\tarray_reg(to_integer(unsigned(w_ptr_reg))) <= w_data;\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\t\tend process;\r\n')
		
		f.write(f'\t-- read port\n')
		f.write(f'\tr_data <= array_reg(to_integer(unsigned(r_ptr_reg)));\r\n')
		
		f.write(f'\t-- write enabled only when FIFO is not full\n')
		f.write(f'\twr_en <= wr and (not full_reg);\r\n')
			
		f.write(f'\t--\n')
		f.write(f'\t-- fifo control logic\n')
		f.write(f'\t--\n')
		f.write(f'\t-- register for read and write pointers\n')
		f.write(f'\tprocess(clk, reset)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (reset = \'1\') then\n')
		f.write(f'\t\t\tw_ptr_reg <= ( others => \'0\');\n')
		f.write(f'\t\t\tr_ptr_reg <= ( others => \'0\');\n')
		f.write(f'\t\t\tfull_reg <= \'0\';\n')
		f.write(f'\t\t\tempty_reg <= \'1\';\n')
		f.write(f'\t\telsif (clk\'event and clk = \'1\') then	\n')
		f.write(f'\t\t\tw_ptr_reg <= w_ptr_next;\n')
		f.write(f'\t\t\tr_ptr_reg <= r_ptr_next;\n')
		f.write(f'\t\t\tfull_reg <= full_next;\n')
		f.write(f'\t\t\tempty_reg <= empty_next;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')

		f.write(f'\t-- successive pointer values\n')
		f.write(f'\tw_ptr_succ <= std_logic_vector(unsigned(w_ptr_reg) + 1);\n')
		f.write(f'\tr_ptr_succ <= std_logic_vector(unsigned(r_ptr_reg) + 1);\r\n')

		f.write(f'\t-- next-state logic for read and write pointers\n')
		f.write(f'\twr_op <= wr & rd;\r\n')
		
		f.write(f'\tprocess(w_ptr_reg, w_ptr_succ, r_ptr_reg, r_ptr_succ ,wr_op, empty_reg, full_reg)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tw_ptr_next <= w_ptr_reg;\n')
		f.write(f'\t\tr_ptr_next <= r_ptr_reg;\n')
		f.write(f'\t\tfull_next <= full_reg;\n')
		f.write(f'\t\tempty_next <= empty_reg;\n')	
		f.write(f'\t\tcase wr_op is\n')
		f.write(f'\t\t\twhen "00" => -- no op\n')
		f.write(f'\t\t\twhen "01" => -- read\n')
		f.write(f'\t\t\t\tif (empty_reg /= \'1\') then -- not empty\n')
		f.write(f'\t\t\t\t\tr_ptr_next <= r_ptr_succ;\n')
		f.write(f'\t\t\t\t\tfull_next <= \'0\';\n')
		f.write(f'\t\t\t\t\tif (r_ptr_succ=w_ptr_reg) then\n')
		f.write(f'\t\t\t\t\t\tempty_next <= \'1\';\n')
		f.write(f'\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\twhen "10" => -- write\n')
		f.write(f'\t\t\t\tif (full_reg /= \'1\') then -- not full\n')
		f.write(f'\t\t\t\t\tw_ptr_next <= w_ptr_succ;\n')
		f.write(f'\t\t\t\t\tempty_next <= \'0\';\n')
		f.write(f'\t\t\t\t\tif (w_ptr_succ = r_ptr_reg) then\n')
		f.write(f'\t\t\t\t\t\tfull_next <= \'1\';\n')
		f.write(f'\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\twhen others => -- write / read;\n')
		f.write(f'\t\t\t\tw_ptr_next <= w_ptr_succ;\n')
		f.write(f'\t\t\t\tr_ptr_next <= r_ptr_succ;\n')
		f.write(f'\t\tend case;\n')
		f.write(f'\tend process;\r\n')

		f.write(f'\t-- output\n')
		f.write(f'\tfull <= full_reg;\n')
		f.write(f'\tempty <= empty_reg;\r\n')
			
		f.write(f'end Behavioral;') 
		
		f.close()  # Close header file    

	def createSystem(self,N,M,example = 1):
		node = 'system'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
			
		# system entity
		system = "system"
		f.write(f'\tentity {system} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock :  in std_logic;\n')
		f.write(f'\t\t\tr_data :  in std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\tr_available :  in std_logic;\n')
		f.write(f'\t\t\tread :  out std_logic;\n')
		f.write(f'\t\t\twrite :  out std_logic;\n')
		f.write(f'\t\t\tselector1 :  in std_logic;\n')
		f.write(f'\t\t\tselector2 :  in std_logic;\n')
		f.write(f'\t\t\treset_uart :  out std_logic;\n')
		f.write(f'\t\t\tN :  in integer;\n')
		f.write(f'\t\t\tleds :  out std_logic_vector(4-1 downto 0);\n')
		f.write(f'\t\t\tled_rgb_1 :  out std_logic_vector(3-1 downto 0);\n')
		f.write(f'\t\t\tled_rgb_2 :  out std_logic_vector(3-1 downto 0);\n')
		f.write(f'\t\t\tw_data :  out std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\treset :  in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {system};\r\n') 

		f.write(f'architecture Behavioral of {system} is\r\n')

		# detector component
		detector = 'detector'
		f.write(f'\tcomponent {detector} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock :  in std_logic;\n')
		f.write(f'\t\t\tr_data :  in std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\tr_available :  in std_logic;\n')
		f.write(f'\t\t\tled_rgb_1 :  out std_logic_vector(3-1 downto 0);\n')
		f.write(f'\t\t\tled_rgb_2 :  out std_logic_vector(3-1 downto 0);\n')
		f.write(f'\t\t\tpacket :  out std_logic_vector({str(N)}-1 downto 0);\n')
		f.write(f'\t\t\tprocessing :  in std_logic;\n')
		f.write(f'\t\t\tprocessed :  out std_logic;\n')
		f.write(f'\t\t\tN :  in integer;\n')
		f.write(f'\t\t\twr_uart :  out std_logic;\n')
		f.write(f'\t\t\tw_data :  out std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\treset :  in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend component {detector};\r\n')

		# interlocking component
		interlocking = 'interlocking'
		f.write(f'\tcomponent {interlocking} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock :  in std_logic;\n')
		f.write(f'\t\t\tprocessing :  in std_logic;\n')
		f.write(f'\t\t\tprocessed :  out std_logic;\n')
		f.write(f'\t\t\tpacket_i :  in std_logic_vector({str(N)}-1 downto 0);\n')
		f.write(f'\t\t\tpacket_o :  out std_logic_vector({str(M)}-1 downto 0);\n')
		f.write(f'\t\t\treset :  in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend component {interlocking};\r\n')

		# selector component
		selector = 'selector'
		f.write(f'\tcomponent {selector} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock :  in std_logic;\n')
		f.write(f'\t\t\tselector :  in std_logic;\n')
		f.write(f'\t\t\tleds :  out std_logic_vector(2-1 downto 0);\n')
		f.write(f'\t\t\twr_uart_1 :  in std_logic;\n')
		f.write(f'\t\t\twr_uart_2 :  in std_logic;\n')
		f.write(f'\t\t\twr_uart_3 :  out std_logic;\n')
		f.write(f'\t\t\tw_data_1 :  in std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\tw_data_2 :  in std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\tw_data_3 :  out std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\treset :  in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend component {selector};\r\n')
		
		# printer component
		printer = 'printer'
		f.write(f'\tcomponent {printer} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock :  in std_logic;\n')
		f.write(f'\t\t\tprocessing :  in std_logic;\n')
		f.write(f'\t\t\tprocessed :  out std_logic;\n')
		f.write(f'\t\t\tpacket_i :  in std_logic_vector({str(M)}-1 downto 0);\n')
		f.write(f'\t\t\tw_data :  out std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\twr_uart :  out std_logic;\n')
		f.write(f'\t\t\treset :  in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend component {printer};\r\n')
		
		f.write(f'\tSignal packet_i_s : std_logic_vector({str(N)}-1 downto 0);\n')
		f.write(f'\tSignal packet_o_s : std_logic_vector({str(M)}-1 downto 0);\n')
		
		f.write(f'\tSignal w_data_1,w_data_2,w_data_3 : std_logic_vector(8-1 downto 0);\n')
		f.write(f'\tSignal wr_uart_1_s,wr_uart_2_s : std_logic;\n')
		f.write(f'\tSignal pro_int_reg,pro_det_enc,pro_reg_det : std_logic;\n\r')
		
		f.write(f'begin\r\n')
		
		f.write(f'\t{detector}_i : {detector}\n')
		f.write(f'\t\tport map(\n')
		f.write(f'\t\t\tclock => clock,\n')
		f.write(f'\t\t\treset => reset,\n')
		f.write(f'\t\t\tr_data => r_data,\n')
		f.write(f'\t\t\tr_available => r_available,\n')
		f.write(f'\t\t\tled_rgb_1 => led_rgb_1,\n')
		f.write(f'\t\t\tled_rgb_2 => led_rgb_2,\n')
		f.write(f'\t\t\tN => N,\n')
		f.write(f'\t\t\twr_uart => wr_uart_1_s,\n')
		f.write(f'\t\t\tprocessing => pro_reg_det,\n')
		f.write(f'\t\t\tprocessed => pro_det_enc,\n')
		f.write(f'\t\t\tpacket => packet_i_s,\n')
		f.write(f'\t\t\tw_data => w_data_1\n')
		f.write(f'\t\t);\r\n')
		
		f.write(f'\t{interlocking}_i : {interlocking}\n')
		f.write(f'\t\tport map(\n')
		f.write(f'\t\t\tclock => clock,\n')
		f.write(f'\t\t\treset => reset,\n')
		f.write(f'\t\t\tprocessing => pro_det_enc,\n')
		f.write(f'\t\t\tprocessed => pro_int_reg,\n')
		f.write(f'\t\t\tpacket_i => packet_i_s,\n')
		f.write(f'\t\t\tpacket_o => packet_o_s\n')
		f.write(f'\t\t);\r\n')
		
		f.write(f'\t{printer}_i : {printer}\n')
		f.write(f'\t\tport map(\n')
		f.write(f'\t\t\tclock => clock,\n')
		f.write(f'\t\t\treset => reset,\n')
		f.write(f'\t\t\tprocessing => pro_int_reg,\n')
		f.write(f'\t\t\tprocessed => pro_reg_det,\n')
		f.write(f'\t\t\tpacket_i => packet_o_s,\n')
		f.write(f'\t\t\tw_data => w_data_2,\n')
		f.write(f'\t\t\twr_uart => wr_uart_2_s\n')
		f.write(f'\t\t);\r\n')
		
		f.write(f'\t{selector}_i : {selector}\n')
		f.write(f'\t\tport map(\n')
		f.write(f'\t\t\tclock => clock,\n')
		f.write(f'\t\t\treset => reset,\n')
		f.write(f'\t\t\tselector => selector1,\n')
		f.write(f'\t\t\twr_uart_1 => wr_uart_1_s,\n')
		f.write(f'\t\t\twr_uart_2 => wr_uart_2_s,\n')
		f.write(f'\t\t\twr_uart_3 => write,\n')
		f.write(f'\t\t\tw_data_1 => w_data_1,\n')
		f.write(f'\t\t\tw_data_2 => w_data_2,\n')
		f.write(f'\t\t\tw_data_3 => w_data_3\n')
		f.write(f'\t\t);\r\n')
		
		f.write(f'\t\tw_data <= w_data_3;\r\n')
		
		f.write(f'\t\tprocess(clock)\n')
		f.write(f'\t\tbegin\n')
		f.write(f'\t\t\tif (clock\'event and clock = \'1\') then\n')
		f.write(f'\t\t\t\tif selector2 = \'1\' then\n')
		f.write(f'\t\t\t\t\tleds <= std_logic_vector(to_unsigned(N,4));\n')
		f.write(f'\t\t\t\telse\n')
		f.write(f'\t\t\t\t\tleds(3) <= packet_i_s(3);\n')
		f.write(f'\t\t\t\t\tleds(2) <= packet_i_s(2);\n')
		f.write(f'\t\t\t\t\tleds(1) <= packet_i_s(1);\n') 
		f.write(f'\t\t\t\t\tleds(0) <= packet_i_s(0);\n')  
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend process;\r\n') 
			
		f.write(f'\t\tprocess(clock)\n')
		f.write(f'\t\tvariable counter: integer := 0;\n')
		f.write(f'\t\tbegin\n')
		f.write(f'\t\t\tif (clock = \'1\' and clock\'event) then\n')
		f.write(f'\t\t\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\t\t\treset_uart <= \'0\';\n')
		f.write(f'\t\t\t\telse\n')
		f.write(f'\t\t\t\t\tcounter := counter + 1;\n')
		f.write(f'\t\t\t\t\tif counter = 10*125E6 then\n')
		f.write(f'\t\t\t\t\t\tcounter := 0;\n') 
		f.write(f'\t\t\t\t\t\treset_uart <= \'1\';\n')  
		f.write(f'\t\t\t\t\telse\n')
		f.write(f'\t\t\t\t\t\treset_uart <= \'0\';\n')
		f.write(f'\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend process;\r\n') 
			
		f.write(f'end Behavioral;') 
		
		f.close()  # Close header file

	def createDetector(self,N,example = 1):
		node = 'detector'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
			
		# detector entity
		detector = "detector"
		f.write(f'\tentity {detector} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tClock : in std_logic;\n')
		f.write(f'\t\t\tr_data : in std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\tr_available : in std_logic;\n')
		f.write(f'\t\t\tled_rgb_1 : out std_logic_vector(3-1 downto 0);\n')
		f.write(f'\t\t\tled_rgb_2 : out std_logic_vector(3-1 downto 0);\n')
		f.write(f'\t\t\tpacket : out std_logic_vector({str(N)}-1 downto 0);\n')
		f.write(f'\t\t\tprocessing : in std_logic;\n')
		f.write(f'\t\t\tprocessed : out std_logic;\n')
		f.write(f'\t\t\tN : in integer;\n')
		f.write(f'\t\t\twr_uart : out std_logic;\n')
		f.write(f'\t\t\tw_data : out std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {detector};\r\n') 
	
		f.write(f'architecture Behavioral of {detector} is\r\n')
		
		f.write(f'\ttype states_t is (start,reading,final,error);\n') 
		f.write(f'\tsignal state, next_state : states_t;\n') 
	
		f.write(f'\tshared variable counter : integer range 0 to {str(round(N*1.5))} := 0;\n')
		
		f.write(f'\tsignal packet_aux : std_logic_vector({str(N)}-1 downto 0);\n')
		f.write(f'\tsignal new_data : std_logic;\n')
		f.write(f'\tsignal length_ok,tags_ok : std_logic;\n')
		f.write(f'\tsignal tags_start,tags_end : std_logic;\n')
		
		f.write(f'\tconstant tag_start : std_logic_vector(8-1 downto 0) := "00111100"; -- r_data = \'<\'\n')
		f.write(f'\tconstant tag_end : std_logic_vector(8-1 downto 0) := "00111110"; -- r_data = \'>\'\n')
		f.write(f'\tconstant char_0 : std_logic_vector(8-1 downto 0) := "00110000"; -- r_data = \'0\'\n')
		f.write(f'\tconstant char_1 : std_logic_vector(8-1 downto 0) := "00110001"; -- r_data = \'1\' \r\n')

		f.write(f'begin\r\n')

		f.write(f'\tstates_transition : process(clock)\n')
		f.write(f'\tbegin\n')   
		f.write(f'\t\tif (clock = \'1\' and clock\'event) then\n')
		f.write(f'\t\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\t\tstate <= start;\n') 
		f.write(f'\t\t\telse\n')
		f.write(f'\t\t\t\tif processing = \'1\' then\n')
		f.write(f'\t\t\t\t\tstate <= start;\n')
		f.write(f'\t\t\t\telse\n')
		f.write(f'\t\t\t\t\tstate <= next_state;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\tincrease_counter : process(clock)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (clock = \'1\' and clock\'event) then\n')
		f.write(f'\t\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\t\tcounter := 0;\n')
		f.write(f'\t\t\telse\n')
		f.write(f'\t\t\t\tif r_available = \'1\' then\n')
		f.write(f'\t\t\t\t\tif state = reading then\n')
		f.write(f'\t\t\t\t\t\tif counter < {str(N+2)} then\n')
		f.write(f'\t\t\t\t\t\t\tcounter := counter + 1;\n')
		f.write(f'\t\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tif counter > {str(N)} and counter < {str(N+2)} then\n')
		f.write(f'\t\t\t\t\tcounter := counter + 1;\n')
		f.write(f'\t\t\t\tend if;\n')   
		f.write(f'\t\t\t\tif state = final or state = error then\n')
		f.write(f'\t\t\t\t\tcounter := 0;\n')
		f.write(f'\t\t\t\tend if;\n') 
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\tpacking : process(clock)\n') 
		f.write(f'\tbegin\n') 
		f.write(f'\t\tif (clock = \'1\' and clock\'event) then\n')
		f.write(f'\t\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\t\tpacket_aux <= (others => \'0\');\n')
		f.write(f'\t\t\t\tnew_data <= \'0\';\n')
		f.write(f'\t\t\telse\n')
		f.write(f'\t\t\t\tif state = reading then\n')
		f.write(f'\t\t\t\t\tif r_available = \'1\' then\n')
		f.write(f'\t\t\t\t\t\tif counter < {str(N+1)} then\n')
		f.write(f'\t\t\t\t\t\t\tif r_data = char_0 then\n')
		f.write(f'\t\t\t\t\t\t\t\tpacket_aux({str(N)}-counter) <= \'0\';\n')
		f.write(f'\t\t\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\t\t\t\tif r_data = char_1 then\n')
		f.write(f'\t\t\t\t\t\t\t\tpacket_aux({str(N)}-counter) <= \'1\';\n')
		f.write(f'\t\t\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\t\t\tnew_data <= \'1\';\n')
		f.write(f'\t\t\t\t\telse\n')
		f.write(f'\t\t\t\t\t\tnew_data <= \'0\';\n')
		f.write(f'\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\tstates : process(clock,state)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (clock = \'1\' and clock\'event) then\n')
		f.write(f'\t\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\t\tnext_state <= start;\n')
		f.write(f'\t\t\t\ttags_start <= \'0\';\n') 
		f.write(f'\t\t\t\ttags_end <= \'0\';\n')
		f.write(f'\t\t\telse\n')
		f.write(f'\t\t\t\tnext_state <= state;\n')
		f.write(f'\t\t\t\t-- LED4 = RGB2 | LED5 => RGB1\n')
		f.write(f'\t\t\t\t-- BGR -> 001 = R | 010 = G | 100 = B\n')
		f.write(f'\t\t\t\tcase(state) is\n')
		f.write(f'\t\t\t\t\twhen start =>\n')
		f.write(f'\t\t\t\t\t\ttags_start <= \'0\';\n') 
		f.write(f'\t\t\t\t\t\tif r_data = tag_start then -- r_data = \'<\'\n')
		f.write(f'\t\t\t\t\t\t\ttags_start <= \'1\';\n')
		f.write(f'\t\t\t\t\t\t\ttags_end <= \'0\';\n')
		f.write(f'\t\t\t\t\t\t\tnext_state <= reading;\n')
		f.write(f'\t\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\t\twhen reading =>\n')
		f.write(f'\t\t\t\t\t\tif counter = {str(N+2)} then -- {str(N)} (it fits {str(N)})\n')
		f.write(f'\t\t\t\t\t\t\tif r_data = tag_end then --  r_data = \'>\'\n')
		f.write(f'\t\t\t\t\t\t\t\ttags_end <= \'1\';\n')
		f.write(f'\t\t\t\t\t\t\t\tnext_state <= final;\n')
		f.write(f'\t\t\t\t\t\t\telse\n')
		f.write(f'\t\t\t\t\t\t\t\ttags_end <= \'0\';\n')
		f.write(f'\t\t\t\t\t\t\t\tnext_state <= error;\n')
		f.write(f'\t\t\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\t\t\telse\n')
		f.write(f'\t\t\t\t\t\t\ttags_end <= \'0\';\n')
		f.write(f'\t\t\t\t\t\tend if;\n') 
		f.write(f'\t\t\t\t\twhen final =>\n')
		f.write(f'\t\t\t\t\t\tif processing = \'1\' then\n')
		f.write(f'\t\t\t\t\t\t\tnext_state <= start;\n')
		f.write(f'\t\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\t\twhen error =>\n') 
		f.write(f'\t\t\t\t\t\ttags_start <= \'0\';\n')
		f.write(f'\t\t\t\t\t\ttags_end <= \'0\';\n')
		f.write(f'\t\t\t\t\t\tnext_state <= start;\n')
		f.write(f'\t\t\t\t\twhen others => null;\n')
		f.write(f'\t\t\t\tend case;\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\tpacket_ready : process(clock)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (clock = \'1\' and clock\'event) then\n')
		f.write(f'\t\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\t\tprocessed <= \'0\';\n')
		f.write(f'\t\t\telse\n')
		f.write(f'\t\t\t\tif state = final then\n')
		f.write(f'\t\t\t\t\tprocessed <= length_ok and tags_ok;\n')
		f.write(f'\t\t\t\telse\n')
		f.write(f'\t\t\t\t\tprocessed <= \'0\';\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\ttag_analyzer : process(clock)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (clock = \'1\' and clock\'event) then\n')
		f.write(f'\t\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\t\ttags_ok <= \'0\';\n') 
		f.write(f'\t\t\t\tled_rgb_1 <= "001"; -- red\n')
		f.write(f'\t\t\telse\n')
		f.write(f'\t\t\t\ttags_ok <= tags_start and tags_end;\n')
		f.write(f'\t\t\t\tif tags_ok = \'1\' then\n')
		f.write(f'\t\t\t\t\tled_rgb_1 <= "010"; -- green\n')
		f.write(f'\t\t\t\telse\n')
		f.write(f'\t\t\t\t\tled_rgb_1 <= "001"; -- red\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tif state = reading then\n')
		f.write(f'\t\t\t\t\tled_rgb_1 <= "001"; -- red\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\tlength_analyzer : process(clock)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (clock = \'1\' and clock\'event) then\n')
		f.write(f'\t\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\t\tlength_ok <= \'0\';\n')
		f.write(f'\t\t\t\tled_rgb_2 <= "001"; -- red\n')
		f.write(f'\t\t\telse\n')
		f.write(f'\t\t\t\tif N = {str(N+2)} then\n')
		f.write(f'\t\t\t\t\tlength_ok <= \'1\';\n') 
		f.write(f'\t\t\t\t\tled_rgb_2 <= "010"; -- green\n')
		f.write(f'\t\t\t\telse\n')
		f.write(f'\t\t\t\t\tlength_ok <= \'0\';\n')
		f.write(f'\t\t\t\t\tled_rgb_2 <= "001"; -- red\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tif state = reading then\n')
		f.write(f'\t\t\t\t\tled_rgb_2 <= "001"; -- red\n')
		f.write(f'\t\t\t\tend if;   \n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\tpacket_valid : process(clock)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (clock = \'1\' and Clock\'event) then\n')
		f.write(f'\t\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\t\tpacket <= (others => \'0\');\n')
		f.write(f'\t\t\telse\n')
		f.write(f'\t\t\t\tif state = final and length_ok = \'1\' and tags_ok = \'1\' then\n')
		f.write(f'\t\t\t\t\tpacket <= packet_aux;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\tw_data <= r_data;\n')
		f.write(f'\twr_uart <= r_available;\r\n')

		f.write(f'end Behavioral;') 

		f.close()  # Close header file

	def createInterlocking(self,N,M,n_netElements,n_routes,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings,n_signals,example = 1):
		node = 'interlocking'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f,True)
			
		# interlocking wrapper
		interlocking = "interlocking"
		f.write(f'\tentity {interlocking} is\n')
		f.write(f'\t\tgeneric(\n')
		f.write(f'\t\t\tN : natural := {str(N)};\n')  
		f.write(f'\t\t\tN_SIGNALS : natural := {str(n_signals)};\n')
		if n_levelCrossings > 0:
			f.write(f'\t\t\tN_LEVELCROSSINGS : natural := {str(n_levelCrossings)};\n')
		if n_switches > 0:         
			f.write(f'\t\t\tN_SINGLESWITCHES : natural := {str(n_switches)};\n')
		if n_doubleSwitch > 0:         
			f.write(f'\t\t\tN_DOUBLEWITCHES : natural := {str(n_doubleSwitch)};\n')
		if n_scissorCrossings > 0:         
			f.write(f'\t\t\tN_SCISSORCROSSINGS : natural := {str(n_scissorCrossings)};\n')
		f.write(f'\t\t\tN_TRACKCIRCUITS : natural := {str(n_netElements)}\n')
		f.write(f'\t\t);\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tprocessing : in std_logic;\n')
		f.write(f'\t\t\tprocessed : out std_logic;\n')
		f.write(f'\t\t\tpacket_i : in std_logic_vector({str(N)}-1 downto 0);\n')
		f.write(f'\t\t\tpacket_o : out std_logic_vector({str(M)}-1 downto 0);\n')
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {interlocking};\n')
	
		f.write(f'architecture Behavioral of {interlocking} is\r\n') 
		
		# splitter component
		splitter = 'splitter'
		f.write(f'\tcomponent {splitter} is\n')
		f.write(f'\t\tgeneric(\n')
		f.write(f'\t\t\tN : natural := {str(N)};\n')
		f.write(f'\t\t\tN_SIGNALS : natural := {str(n_signals)};\n')
		if n_levelCrossings > 0:
			f.write(f'\t\t\tN_ROUTES : natural := {str(n_routes)};\n')
		if n_levelCrossings > 0:
			f.write(f'\t\t\tN_LEVELCROSSINGS : natural := {str(n_levelCrossings)};\n')
		if n_switches > 0:    
			f.write(f'\t\t\tN_SINGLESWITCHES : natural := {str(n_switches)};\n')
		if n_doubleSwitch > 0:         
			f.write(f'\t\t\tN_DOUBLESWITCHES : natural := {str(n_doubleSwitch)};\n')
		if n_scissorCrossings > 0:         
			f.write(f'\t\t\tN_SCISSORCROSSINGS : natural := {str(n_scissorCrossings)};\n')
		f.write(f'\t\t\tN_TRACKCIRCUITS : natural := {str(n_netElements)}\n')
		f.write(f'\t\t);\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tprocessing : in std_logic;\n')
		f.write(f'\t\t\tprocessed : out std_logic;\n')
		f.write(f'\t\t\tpacket : in std_logic_vector(N-1 downto 0);\n')
		f.write(f'\t\t\tocupation : out std_logic_vector(N_TRACKCIRCUITS-1 downto 0);\n')
		f.write(f'\t\t\tsignals : out signals_type;\n')
		if n_routes > 1:
			f.write(f'\t\t\troutes :  out std_logic_vector(N_ROUTES-1 downto 0);\n')
		if n_routes == 1:
			f.write(f'\t\t\troutes :  out std_logic;\n')
		if n_levelCrossings > 1:
			f.write(f'\t\t\tlevelCrossings :  out std_logic_vector(N_LEVELCROSSINGS-1 downto 0);\n')
		if n_levelCrossings == 1:
			f.write(f'\t\t\tlevelCrossings :  out std_logic;\n')
		if n_switches > 1:
			f.write(f'\t\t\tsingleSwitches :  out std_logic_vector(N_SINGLESWITCHES-1 downto 0);\n')    
		if n_switches == 1:
			f.write(f'\t\t\tsingleSwitches :  out std_logic;\n')
		if n_doubleSwitch > 0:
			f.write(f'\t\t\tdoubleSwitches :  out dSwitches_type;\n')    
		if n_scissorCrossings > 1:
			f.write(f'\t\t\tscissorCrossings :  out std_logic_vector(N_SCISSORCROSSINGS-1 downto 0);\n')    
		if n_scissorCrossings == 1:
			f.write(f'\t\t\tscissorCrossings :  out std_logic;\n')
		f.write(f'\t\t\treset :  in std_logic\n')    
		f.write(f'\t\t);\n')
		f.write(f'\tend component {splitter};\r\n')
		
		# network component
		network = 'network'
		f.write(f'\tcomponent {network} is\n')
		f.write(f'\t\tgeneric(\n')
		f.write(f'\t\t\tN : natural := {str(N)};\n')
		
		f.write(f'\t\t\tN_SIGNALS : natural := {str(n_signals)};\n')
		if n_routes > 0:
			f.write(f'\t\t\tN_ROUTES : natural := {str(n_routes)};\n')
		if n_levelCrossings > 0:
			f.write(f'\t\t\tN_LEVELCROSSINGS : natural := {str(n_levelCrossings)};\n')
		if n_switches > 0:    
			f.write(f'\t\t\tN_SINGLESWITCHES : natural := {str(n_switches)};\n')
		if n_doubleSwitch > 0:    
			f.write(f'\t\t\tN_DOUBLEWITCHES : natural := {str(n_doubleSwitch)};\n')
		if n_scissorCrossings > 0:    
			f.write(f'\t\t\tN_SCISSORCROSSINGS : natural := {str(n_scissorCrossings)};\n')
		f.write(f'\t\t\tN_TRACKCIRCUITS : natural := {str(n_netElements)}\n')
		f.write(f'\t\t);\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tprocessing : in std_logic;\n')
		f.write(f'\t\t\tprocessed : out std_logic;\n')
		f.write(f'\t\t\tocupation : in std_logic_vector(N_TRACKCIRCUITS-1 downto 0);\n') 
		f.write(f'\t\t\tsignals_i : in signals_type;\n')
		f.write(f'\t\t\tsignals_o : out signals_type;\n')
		if n_routes > 1:
			f.write(f'\t\t\troutes_i : in std_logic_vector(N_ROUTES-1 downto 0);\n')
			f.write(f'\t\t\troutes_o : out std_logic_vector(N_ROUTES-1 downto 0);\n')
		if n_routes == 1:
			f.write(f'\t\t\troutes_i : in std_logic;\n')
			f.write(f'\t\t\troutes_o : out std_logic;\n')
		if n_levelCrossings > 1:
			f.write(f'\t\t\tlevelCrossings_i : in std_logic_vector(N_LEVELCROSSINGS-1 downto 0);\n')
			f.write(f'\t\t\tlevelCrossings_o : out std_logic_vector(N_LEVELCROSSINGS-1 downto 0);\n')
		if n_levelCrossings == 1:
			f.write(f'\t\t\tlevelCrossings_i : in std_logic;\n')
			f.write(f'\t\t\tlevelCrossings_o : out std_logic;\n')
		if n_switches > 1:
			f.write(f'\t\t\tsingleSwitches_i : in std_logic_vector(N_SINGLESWITCHES-1 downto 0);\n')  
			f.write(f'\t\t\tsingleSwitches_o : out std_logic_vector(N_SINGLESWITCHES-1 downto 0);\n')
		if n_switches == 1:
			f.write(f'\t\t\tsingleSwitches_i : in std_logic;\n')  
			f.write(f'\t\t\tsingleSwitches_o : out std_logic;\n')

		if n_doubleSwitch > 0:
			f.write(f'\t\t\tdoubleSwitches_i : in dSwitches_type;\n')  
			f.write(f'\t\t\tdoubleSwitches_o : out dSwitches_type;\n')

		if n_scissorCrossings > 1:
			f.write(f'\t\t\tscissorCrossings_i : in std_logic_vector(N_SCISSORCROSSINGS-1 downto 0);\n')  
			f.write(f'\t\t\tscissorCrossings_o : out std_logic_vector(N_SCISSORCROSSINGS-1 downto 0);\n')
		if n_scissorCrossings == 1:
			f.write(f'\t\t\tscissorCrossings_i : in std_logic;\n')  
			f.write(f'\t\t\tscissorCrossings_o : out std_logic;\n')
	
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend component {network};\r\n')
		
		# mediator component
		mediator = 'mediator'
		f.write(f'\tcomponent {mediator} is\n')
		f.write(f'\t\tgeneric(\n')
		f.write(f'\t\t\tN : natural := {str(N)};\n')
		
		f.write(f'\t\t\tN_SIGNALS : natural := {str(n_signals)};\n')
		if n_levelCrossings > 0:
			f.write(f'\t\t\tN_ROUTES : natural := {str(n_routes)};\n')
		if n_levelCrossings > 0:
			f.write(f'\t\t\tN_LEVELCROSSINGS : natural := {str(n_levelCrossings)};\n')
		if n_switches > 0:    
			f.write(f'\t\t\tN_SINGLESWITCHES : natural := {str(n_switches)};\n')
		if n_doubleSwitch > 0:
			f.write(f'\t\t\tN_DOUBLESWITCHES : natural := {str(n_doubleSwitch)};\n')
		if n_scissorCrossings > 0:
			f.write(f'\t\t\tN_SCISSORCROSSINGS : natural := {str(n_scissorCrossings)};\n')

		f.write(f'\t\t\tN_TRACKCIRCUITS : natural := {str(n_netElements)}\n')    
		f.write(f'\t\t);\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tprocessing : in std_logic;\n')
		f.write(f'\t\t\tprocessed : out std_logic;\n')
		f.write(f'\t\t\tsignals : in signals_type;\n')
		if n_routes > 1:
			f.write(f'\t\t\troutes : in std_logic_vector(N_ROUTES-1 downto 0);\n')
		if n_routes == 1:
			f.write(f'\t\t\troutes : in std_logic;\n')
		if n_levelCrossings > 1:
			f.write(f'\t\t\tlevelCrossings : in std_logic_vector(N_LEVELCROSSINGS-1 downto 0);\n')
		if n_levelCrossings == 1:
			f.write(f'\t\t\tlevelCrossings : in std_logic;\n')
		if n_switches > 1:
			f.write(f'\t\t\tsingleSwitches : in std_logic_vector(N_SINGLESWITCHES-1 downto 0);\n')
		if n_switches == 1:
			f.write(f'\t\t\tsingleSwitches : in std_logic;\n')
		if n_scissorCrossings > 1:
			f.write(f'\t\t\tscissorCrossings : in std_logic_vector(N_SCISSORCROSSINGS-1 downto 0);\n')
		if n_scissorCrossings == 1:
			f.write(f'\t\t\tscissorCrossings : in std_logic;\n')

		if n_doubleSwitch > 0:
			f.write(f'\t\t\tdoubleSwitches : in dSwitches_type;\n')
		f.write(f'\t\t\toutput : out std_logic_vector({str(M)}-1 downto 0);\n')
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend component {mediator};\r\n')
		
		f.write(f'\tSignal tc_s : std_logic_vector({str(n_netElements)}-1 downto 0);\n')    
		f.write(f'\tSignal sig_s_i,sig_s_o : signals_type;\n')
		if n_routes > 1:
			f.write(f'\tSignal rt_s_i,rt_s_o : std_logic_vector({str(n_routes)}-1 downto 0);\n')
		if n_routes == 1:
			f.write(f'\tSignal rt_s_i,rt_s_o : std_logic;\n')
		if n_levelCrossings > 1:
			f.write(f'\tSignal lc_s_i,lc_s_o : std_logic_vector({str(n_levelCrossings)}-1 downto 0);\n')
		if n_levelCrossings == 1:
			f.write(f'\tSignal lc_s_i,lc_s_o : std_logic;\n')
		if n_switches > 1:
			f.write(f'\tSignal ssw_s_i,ssw_s_o : std_logic_vector({str(n_switches)}-1 downto 0);\n')
		if n_switches == 1:
			f.write(f'\tSignal ssw_s_i,ssw_s_o : std_logic;\n')
		if n_scissorCrossings > 1:
			f.write(f'\tSignal sc_s_i,sc_s_o : std_logic_vector({str(n_scissorCrossings)}-1 downto 0);\n')
		if n_scissorCrossings == 1:
			f.write(f'\tSignal sc_s_i,sc_s_o : std_logic;\n')
		if n_doubleSwitch > 0:
			f.write(f'\tSignal dsw_s_i,dsw_s_o : dSwitches_type;\n')
		f.write(f'\tSignal process_spt_int, process_int_med : std_logic;\n')
		
		f.write(f'\nbegin\r\n')  
		
		self.instantiateSplitter(f,splitter,n_routes,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings)
		
		self.instantiateMediator(f,mediator,n_routes,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings)
		
		self.instantiateNetwork(f,network,n_routes,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings)
		
		f.write(f'end Behavioral;') 
		
		f.close()  # Close header file

	def instantiateSplitter(self,f,name,n_routes,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings):
    		
		# instantiate splitter
		f.write(f'\t{name}_i : {name} port map(\n')
		
		f.write(f'\t\tclock => clock,\n')
		
		f.write(f'\t\tpacket => packet_i,\n')
		f.write(f'\t\tprocessing => processing,\n')
		f.write(f'\t\tprocessed => process_spt_int,\n')
		f.write(f'\t\tocupation => tc_s,\n')

		f.write(f'\t\tsignals => sig_s_i,\n')
		if n_routes > 0:
			f.write(f'\t\troutes => rt_s_i,\n')
		if n_levelCrossings > 0:
			f.write(f'\t\tlevelCrossings => lc_s_i,\n')
		if n_switches > 0:    
			f.write(f'\t\tsingleSwitches => ssw_s_i,\n')
		if n_doubleSwitch > 0:    
			f.write(f'\t\tdoubleSwitches => dsw_s_i,\n')
		if n_scissorCrossings > 0:    
			f.write(f'\t\tscissorCrossings => sc_s_i,\n')
		f.write(f'\t\treset => reset\n')    
		f.write(f'\t\t);\r\n')

	def instantiateMediator(self,f,name,n_routes,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings):
    		
    	# instantiate mediator
		f.write(f'\t{name}_i : {name} port map(\n')
		
		f.write(f'\t\tclock => clock,\n')
		f.write(f'\t\tprocessing => process_int_med,\n')
		f.write(f'\t\tprocessed => processed,\n')
		
		f.write(f'\t\tsignals => sig_s_o,\n')
		if n_routes > 0:
			f.write(f'\t\troutes => rt_s_o,\n')
		if n_levelCrossings > 0:
			f.write(f'\t\tlevelCrossings => lc_s_o,\n')
		if n_switches > 0:    
			f.write(f'\t\tsingleSwitches => ssw_s_o,\n')
		if n_doubleSwitch > 0:    
			f.write(f'\t\tdoubleSwitches => dsw_s_o,\n')
		if n_scissorCrossings > 0:    
			f.write(f'\t\tscissorCrossings => sc_s_o,\n')

		f.write(f'\t\toutput => packet_o,\n')
		f.write(f'\t\treset => reset\n')    
		f.write(f'\t\t);\r\n')

	def instantiateNetwork(self,f,name,n_routes,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings):
    		
    	# instantiate network
		f.write(f'\t{name}_i : {name} port map(\n')
		
		f.write(f'\t\tclock => clock,\n')
		f.write(f'\t\tocupation => tc_s,\n')
		f.write(f'\t\tprocessing => process_spt_int,\n')
		f.write(f'\t\tprocessed => process_int_med,\n')
		f.write(f'\t\tsignals_i => sig_s_i,\n')
		f.write(f'\t\tsignals_o => sig_s_o,\n')

		if n_routes > 0:
			f.write(f'\t\troutes_i => rt_s_i,\n')
			f.write(f'\t\troutes_o => rt_s_o,\n')	
		if n_levelCrossings > 0:
			f.write(f'\t\tlevelCrossings_i => lc_s_i,\n')
			f.write(f'\t\tlevelCrossings_o => lc_s_o,\n')
		if n_switches > 0:    
			f.write(f'\t\tsingleSwitches_i => ssw_s_i,\n')
			f.write(f'\t\tsingleSwitches_o => ssw_s_o,\n') 
		if n_doubleSwitch > 0:    
			f.write(f'\t\tdoubleSwitches_i => dsw_s_i,\n')
			f.write(f'\t\tdoubleSwitches_o => dsw_s_o,\n') 
		if n_scissorCrossings > 0:    
			f.write(f'\t\tscissorCrossings_i => sc_s_i,\n')
			f.write(f'\t\tscissorCrossings_o => sc_s_o,\n')

		f.write(f'\t\treset => reset\n')
		
		f.write(f'\t\t);\r\n')

	def createSplitter(self,N,n_netElements,n_routes,n_signals,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings,example = 1):
		node = 'splitter'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f,True)
			
		# splitter entity
		splitter = "splitter"
		f.write(f'\tentity {splitter} is\n')
		f.write(f'\t\tgeneric(\n')
		f.write(f'\t\t\tN : natural := {str(N)};\n')   
		f.write(f'\t\t\tN_SIGNALS : natural := {str(n_signals)};\n')
		if n_levelCrossings > 0:
			f.write(f'\t\t\tN_LEVELCROSSINGS : natural := {str(n_levelCrossings)};\n')
		if n_switches > 0:         
			f.write(f'\t\t\tN_SINGLESWITCHES : natural := {str(n_switches)};\n')
		if n_doubleSwitch > 0:         
			f.write(f'\t\t\tN_DOUBLEWITCHES : natural := {str(n_doubleSwitch)};\n')
		if n_scissorCrossings > 0:         
			f.write(f'\t\t\tN_SCRISSORCROSSINGS : natural := {str(n_scissorCrossings)};\n')
		if n_routes > 0:         
			f.write(f'\t\t\tN_ROUTES : natural := {str(n_routes)};\n')
		f.write(f'\t\t\tN_TRACKCIRCUITS : natural := {str(n_netElements)}\n')
		f.write(f'\t\t);\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		
		f.write(f'\t\t\tpacket :  in std_logic_vector(N-1 downto 0);\n')
		f.write(f'\t\t\tprocessing :  in std_logic;\n')
		f.write(f'\t\t\tprocessed :  out std_logic;\n')
		f.write(f'\t\t\tocupation :  out std_logic_vector(N_TRACKCIRCUITS-1 downto 0);\n')
		f.write(f'\t\t\tsignals :  out signals_type;\n')
		if n_routes > 1:
			f.write(f'\t\t\troutes : out std_logic_vector(N_ROUTES-1 downto 0);\n')		
		if n_routes == 1:
			f.write(f'\t\t\troutes : out std_logic;\n')
		if n_levelCrossings > 1:
			f.write(f'\t\t\tlevelCrossings : out std_logic_vector(N_LEVELCROSSINGS-1 downto 0);\n')
		if n_levelCrossings == 1:
			f.write(f'\t\t\tlevelCrossings : out std_logic;\n')
		if n_switches > 1:
			f.write(f'\t\t\tsingleSwitches : out std_logic_vector(N_SINGLESWITCHES-1 downto 0);\n')  
		if n_switches == 1:
			f.write(f'\t\t\tsingleSwitches : out std_logic;\n')  
		if n_scissorCrossings > 1:
			f.write(f'\t\t\tscissorCrossings : out std_logic_vector(N_SCRISSORCROSSINGS-1 downto 0);\n')  
		if n_scissorCrossings == 1:
			f.write(f'\t\t\tscissorCrossings : out std_logic;\n')
		if n_doubleSwitch > 0:
			f.write(f'\t\t\tdoubleSwitches : out dSwitches_type;\n') 
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {splitter};\r\n')
	
		f.write(f'architecture Behavioral of {splitter} is\r\n') 
			
		f.write(f'\tSignal tc_s : std_logic_vector({str(n_netElements)}-1 downto 0);\n')    
		f.write(f'\tSignal sig_s_i,sig_s_o : signals_type;\n')
		if n_routes > 1:
			f.write(f'\tSignal rt_s_i,rt_s_o : std_logic_vector({str(n_routes)}-1 downto 0);\n')
		if n_routes == 1:
			f.write(f'\tSignal rt_s_i,rt_s_o : std_logic;\n')
		if n_levelCrossings > 1:
			f.write(f'\tSignal lc_s_i,lc_s_o : std_logic_vector({str(n_levelCrossings)}-1 downto 0);\n')
		if n_levelCrossings == 1:
			f.write(f'\tSignal lc_s_i,lc_s_o : std_logic;\n')
		if n_switches > 1:
			f.write(f'\tSignal ssw_s_i,ssw_s_o : std_logic_vector({str(n_switches)}-1 downto 0);\n')
		if n_switches == 1:
			f.write(f'\tSignal ssw_s_i,ssw_s_o : std_logic;\n')
		if n_scissorCrossings > 1:
			f.write(f'\tSignal sc_s_i,sc_s_o : std_logic_vector({str(n_scissorCrossings)}-1 downto 0);\n')
		if n_scissorCrossings == 1:
			f.write(f'\tSignal sc_s_i,sc_s_o : std_logic;\n')
		if n_doubleSwitch > 0:
			f.write(f'\tSignal dsw_s_i,dsw_s_o : dSwitches_type;\n')
		f.write(f'begin\r\n')  
		
		# Ocupation | Routes | signals | levelCrossings | singleSwitches | doubleSwitches | scissorCrossinges

		f.write(f'\tprocess(clock,reset)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\n')
		f.write(f'\t\t\tif (reset = \'1\') then\n')
		f.write(f'\t\t\t\tocupation <= "{str('0'*n_netElements)}";\n')
		f.write(f'\t\t\t\tsignals.lsb <= "{str('0'*n_signals)}";\n')
		f.write(f'\t\t\t\tsignals.msb <= "{str('0'*n_signals)}";\n') 
		if n_routes > 1:
			f.write(f'\t\t\t\troutes <= "{str('0'*n_routes)}";\n')
		if n_routes == 1:
			f.write(f'\t\t\t\troutes <= \'0\';\n')  
		if n_levelCrossings > 1:
			f.write(f'\t\t\t\tlevelCrossings <= "{str('0'*n_levelCrossings)}";\n')
		if n_levelCrossings == 1:
			f.write(f'\t\t\t\tlevelCrossings <= \'0\';\n')    
		if n_switches > 1:
			f.write(f'\t\t\t\tsingleSwitches <= "{str('0'*n_switches)}";\n')
		if n_switches == 1:
			f.write(f'\t\t\t\tsingleSwitches <= \'0\';\n')
		if n_scissorCrossings > 1:
			f.write(f'\t\t\t\tscissorCrossings <= "{str('0'*n_scissorCrossings)}";\n')
		if n_scissorCrossings == 1:
			f.write(f'\t\t\t\tscissorCrossings <= \'0\';\n')
		if n_doubleSwitch > 0:
			f.write(f'\t\t\t\tdoubleSwitches.lsb <= "{str('0'*n_doubleSwitch)}";\n')
			f.write(f'\t\t\t\tdoubleSwitches.msb <= "{str('0'*n_doubleSwitch)}";\n')
		f.write(f'\t\t\t\tprocessed <= \'0\';\n')    
		f.write(f'\t\t\telse\n')
		f.write(f'\t\t\t\tprocessed <= processing;\n') 
		f.write(f'\t\t\t\tif processing = \'1\' then\n')

		for i in range(n_netElements):
			f.write(f'\t\t\t\t\tocupation({str(i)}) <= packet({str(N-1-i)});\n')
	
		for i in range(n_routes):
			f.write(f'\t\t\t\t\troutes({str(i)}) <= packet({str(N-1-n_netElements-i)});\n')
    
		for i in range(2*n_signals):
			if i%2:
				#print ('LSB: {}'.format(i+1))
				f.write(f'\t\t\t\t\tsignals.lsb({str(int((i+1)/2-1))}) <= packet({str(N-1-n_routes-n_netElements-i)});\n')
			else:
				#print ('MSB: {}'.format(i+1))
				f.write(f'\t\t\t\t\tsignals.msb({str(int(i/2))}) <= packet({str(N-1-n_routes-n_netElements-i)});\n')

		if n_levelCrossings > 1:
			for i in range(n_levelCrossings):
				f.write(f'\t\t\t\t\tlevelCrossings({str(i)}) <= packet({str(N-1-n_routes-n_netElements-2*n_signals-i)});\n')
		if n_levelCrossings == 1:
			f.write(f'\t\t\t\t\tlevelCrossings <= packet({str(N-1-n_routes-n_netElements-2*n_signals)});\n')

		if n_switches > 1:
			for i in range(n_switches):
				f.write(f'\t\t\t\t\tsingleSwitches({str(i)}) <= packet({str(N-1-n_routes-n_netElements-2*n_signals-n_levelCrossings-i)});\n')
		if n_switches == 1:
			f.write(f'\t\t\t\t\tsingleSwitches <= packet({str(N-1-n_routes-n_netElements-2*n_signals-n_levelCrossings-1)});\n')
		
		if n_doubleSwitch > 0:
			for i in range(2*n_doubleSwitch):
				if i%2:
					#print ('LSB: {}'.format(i+1))
					f.write(f'\t\t\t\t\tdoubleSwitches.lsb({str(int((i+1)/2-1))}) <= packet({str(N-1-n_routes-n_netElements-2*n_signals-n_levelCrossings-n_switches-i)});\n')
				else:
					#print ('MSB: {}'.format(i+1))
					f.write(f'\t\t\t\t\tdoubleSwitches.msb({str(int(i/2))}) <= packet({str(N-1-n_routes-n_netElements-2*n_signals-n_levelCrossings-n_switches-i)});\n')

		if n_scissorCrossings > 1:
			for i in range(n_scissorCrossings):
				f.write(f'\t\t\t\t\tscissorCrossings({str(i)}) <= packet({str(N-1-n_routes-n_netElements-2*n_signals-n_levelCrossings-n_switches-2*n_doubleSwitch-i)});\n')
		if n_scissorCrossings == 1:
			f.write(f'\t\t\t\t\tscissorCrossings <= packet({str(N-1-n_routes-n_netElements-2*n_signals-n_levelCrossings-n_switches-2*n_doubleSwitch)});\n')

		f.write(f'\t\t\t\tend if;\n')    
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')    
		
		f.write(f'end Behavioral;') 
		
		f.close()  # Close header file 

	def createMediator(self,N,M,n_netElements,n_routes,n_signals,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings,example = 1):
		node = 'mediator'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f,True)
			
		# mediator entity
		mediator = "mediator"
		f.write(f'\tentity {mediator} is\n')
		f.write(f'\t\tgeneric(\n')
		f.write(f'\t\t\tN : natural := {str(N)};\n')
		
		f.write(f'\t\t\tN_SIGNALS : natural := {str(n_signals)};\n')
		if n_routes > 0:
			f.write(f'\t\t\tN_ROUTES : natural := {str(n_routes)};\n')
		if n_levelCrossings > 0:
			f.write(f'\t\t\tN_LEVELCROSSINGS : natural := {str(n_levelCrossings)};\n')
		if n_switches > 0:    
			f.write(f'\t\t\tN_SINGLESWITCHES : natural := {str(n_switches)};\n')
		if n_doubleSwitch > 0:
			f.write(f'\t\t\tN_DOUBLESWITCHES : natural := {str(n_doubleSwitch)};\n')
		if n_scissorCrossings > 0:
			f.write(f'\t\t\tN_SCISSORCROSSINGS : natural := {str(n_scissorCrossings)};\n')
		f.write(f'\t\t\tN_TRACKCIRCUITS : natural := {str(n_netElements)}\n')    
		f.write(f'\t\t);\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tprocessing : in std_logic;\n')
		f.write(f'\t\t\tprocessed : out std_logic;\n')
		f.write(f'\t\t\tsignals : in signals_type;\n')
		if n_routes > 1:
			f.write(f'\t\t\troutes : in std_logic_vector(N_ROUTES-1 downto 0);\n')
		if n_routes == 1:
			f.write(f'\t\t\troutes : in std_logic;\n')
		if n_levelCrossings > 1:
			f.write(f'\t\t\tlevelCrossings : in std_logic_vector(N_LEVELCROSSINGS-1 downto 0);\n')
		if n_levelCrossings == 1:
			f.write(f'\t\t\tlevelCrossings : in std_logic;\n')
		if n_switches > 1:
			f.write(f'\t\t\tsingleSwitches : in std_logic_vector(N_SINGLESWITCHES-1 downto 0);\n')
		if n_switches == 1:
			f.write(f'\t\t\tsingleSwitches : in std_logic;\n')
		if n_scissorCrossings > 1:
			f.write(f'\t\t\tscissorCrossings : in std_logic_vector(N_SCISSORCROSSINGS-1 downto 0);\n')
		if n_scissorCrossings == 1:
			f.write(f'\t\t\tscissorCrossings : in std_logic;\n')
		if n_doubleSwitch > 0:
			f.write(f'\t\t\tdoubleSwitches : in dSwitches_type;\n')
		
		f.write(f'\t\t\toutput : out std_logic_vector({str(M)}-1 downto 0);\n')
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {mediator};\r\n') 
	
		f.write(f'architecture Behavioral of {mediator} is\r\n')      
		
		f.write(f'begin\r\n')  
		
	# Ocupation | Routes | signals | levelCrossings | singleSwitches | doubleSwitches | scissorCrossings
		
		f.write(f'\tprocess(clock,reset)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (clock = \'1\' and Clock\'Event) then\n')
		f.write(f'\t\t\tif (reset = \'1\') then\n')
		f.write(f'\t\t\t\toutput <= (others => \'0\');\n')  
		f.write(f'\t\t\t\tprocessed <= \'0\';\n')   
		f.write(f'\t\t\telse\n')
		
		f.write(f'\t\t\t\tprocessed <= processing;\n')
		f.write(f'\t\t\t\tif (processing = \'1\') then\n')

		if n_routes > 1:
			f.write(f'\t\t\t\t\toutput({str(n_routes-1)} downto 0) <= routes;\n')
		if n_routes == 1:
			f.write(f'\t\t\t\t\toutput(0) <= routes;\n')

		for i in range(2*n_signals):
			if i%2:
				f.write(f'\t\t\t\t\toutput({str(n_routes+i)}) <= signals.lsb({str(int((i+1)/2-1))});\n')
			else:
				f.write(f'\t\t\t\t\toutput({str(n_routes+i)}) <= signals.msb({str(int((i+1)/2))});\n')
		
		if n_levelCrossings > 1:
			f.write(f'\t\t\t\t\toutput({str(n_routes+2*n_signals+n_levelCrossings-1)} downto {str(n_routes+2*n_signals)}) <= levelCrossings;\n')
		if n_levelCrossings == 1:
			f.write(f'\t\t\t\t\toutput({str(n_routes+2*n_signals)}) <= levelCrossings;\n')

		if n_switches > 1:
			f.write(f'\t\t\t\t\toutput({str(n_routes+2*n_signals+n_levelCrossings+n_switches-1)} downto {str(n_routes+2*n_signals+n_levelCrossings)}) <= singleSwitches;\n')
		if n_switches == 1:
			f.write(f'\t\t\t\t\toutput({str(n_routes+2*n_signals+n_levelCrossings)}) <= singleSwitches;\n')

		for i in range(2*n_doubleSwitch):
			if i%2:
				#print ('MSB: {}'.format(i+1))
				f.write(f'\t\t\t\t\toutput({str(n_routes+2*n_signals+n_levelCrossings+n_switches+i)}) <= doubleSwitches.lsb({str(int((i+1)/2-1))});\n')
			else:
				#print ('LSB: {}'.format(i+1))
				f.write(f'\t\t\t\t\toutput({str(n_routes+2*n_signals+n_levelCrossings+n_switches+i)}) <= doubleSwitches.msb({str(int((i+1)/2))});\n')
		
		if n_scissorCrossings > 1:
			f.write(f'\t\t\t\t\toutput({str(n_routes+2*n_signals+n_levelCrossings+n_switches+2*n_doubleSwitch+n_scissorCrossings-1)} downto {str(n_routes+2*n_signals+n_levelCrossings+n_switches+2*n_doubleSwitch)}) <= scissorCrossings;\n')
		if n_scissorCrossings == 1:
			f.write(f'\t\t\t\t\toutput({str(n_routes+2*n_signals+n_levelCrossings++n_switches+2*n_doubleSwitch)}) <= scissorCrossings;\n')


		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')   
			
		f.write(f'end Behavioral;') 
		
		f.close()  # Close header file  

	def createNetwork(self,graph,routes,N,n_netElements,n_signals,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings,example = 1):
		# Eliminate nodes
		# Create routes
		# Add interlock to dynamic elements
		# Routes disable after X seconds if not succesfull
		print('')
		n_routes = len(routes)
		
		node = 'network'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f,True)

		# network entity
		network = "network"
		f.write(f'\tentity {network} is\n')
		f.write(f'\t\tgeneric(\n')
		f.write(f'\t\t\tN : natural := {str(N)};\n')
		
		f.write(f'\t\t\tN_SIGNALS : natural := {str(n_signals)};\n')
		if n_routes > 0:
			f.write(f'\t\t\tN_ROUTES : natural := {str(n_routes)};\n')
		if n_levelCrossings > 0:
			f.write(f'\t\t\tN_LEVELCROSSINGS : natural := {str(n_levelCrossings)};\n')
		if n_switches > 0:    
			f.write(f'\t\t\tN_SINGLESWITCHES : natural := {str(n_switches)};\n')
		if n_doubleSwitch > 0:    
			f.write(f'\t\t\tN_DOUBLEWITCHES : natural := {str(n_doubleSwitch)};\n')
		if n_scissorCrossings > 0:    
			f.write(f'\t\t\tN_SCISSORCROSSINGS : natural := {str(n_scissorCrossings)};\n')
		f.write(f'\t\t\tN_TRACKCIRCUITS : natural := {str(n_netElements)}\n')
		f.write(f'\t\t);\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tprocessing : in std_logic;\n')
		f.write(f'\t\t\tprocessed : out std_logic;\n')
		f.write(f'\t\t\tocupation : in std_logic_vector(N_TRACKCIRCUITS-1 downto 0);\n') 
		f.write(f'\t\t\tsignals_i : in signals_type;\n')
		f.write(f'\t\t\tsignals_o : out signals_type;\n')
		if n_routes > 0:
			f.write(f'\t\t\troutes_i : in std_logic{"_vector(N_ROUTES-1 downto 0)" if n_routes > 1 else ""};\n')
			f.write(f'\t\t\troutes_o : out std_logic{"_vector(N_ROUTES-1 downto 0)" if n_routes > 1 else ""};\n')
		if n_levelCrossings > 0:
			f.write(f'\t\t\tlevelCrossings_i : in std_logic{"_vector(N_LEVELCROSSINGS-1 downto 0)" if n_levelCrossings > 1 else ""};\n')
			f.write(f'\t\t\tlevelCrossings_o : out std_logic{"_vector(N_LEVELCROSSINGS-1 downto 0)" if n_levelCrossings > 1 else ""};\n')
		if n_switches > 0:
			f.write(f'\t\t\tsingleSwitches_i : in std_logic{"_vector(N_SINGLESWITCHES-1 downto 0)" if n_switches > 1 else ""};\n')
			f.write(f'\t\t\tsingleSwitches_o : out std_logic{"_vector(N_SINGLESWITCHES-1 downto 0)" if n_switches > 1 else ""};\n')
		if n_scissorCrossings > 0:
			f.write(f'\t\t\tscissorCrossings_i : in std_logic{"_vector(N_SCISSORCROSSINGS-1 downto 0)" if n_scissorCrossings > 1 else ""};\n')
			f.write(f'\t\t\tscissorCrossings_o : out std_logic{"_vector(N_SCISSORCROSSINGS-1 downto 0)" if n_scissorCrossings > 1 else ""};\n')
		if n_doubleSwitch > 0:
			f.write(f'\t\t\tdoubleSwitches_i : in dSwitches_type;\n')  
			f.write(f'\t\t\tdoubleSwitches_o : out dSwitches_type;\n')
			
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {network};\r\n')

		f.write(f'architecture Behavioral of {network} is\r\n')

		levelCrossingData = self.getLevelCrossings(graph,routes)
		#print(levelCrossingData)
		singleSwitchData = self.getSingleSwitch(graph,routes)
		#print(singleSwitchData)
		scissorCrossingData = self.getScissorCrossing(graph,routes)
		#print(scissorCrossingData)
		doubleSwitchData = self.getDoubleSwitch(graph,routes)
		#print(doubleSwitchData)
		signalData = self.getSignal(graph,routes)
		#print(signalData)

		# component levelCrossing  
		if n_levelCrossings > 0:
			for levelCrossingId in levelCrossingData:
				index = list(levelCrossingData.keys()).index(levelCrossingId)
				self.createLevelCrossing(index,levelCrossingId,levelCrossingData[levelCrossingId],mode = 'component',f = f)
				self.createLevelCrossing(index,levelCrossingId,levelCrossingData[levelCrossingId],mode = 'entity',f = None, example = example)
		# component singleSwitch  
		if n_switches > 0:  	
			for singleSwitchId in singleSwitchData:
				index = list(singleSwitchData.keys()).index(singleSwitchId)
				self.createSingleSwitch(index,singleSwitchId,singleSwitchData[singleSwitchId],mode = 'component',f = f)
				self.createSingleSwitch(index,singleSwitchId,singleSwitchData[singleSwitchId],mode = 'entity',f = None, example = example)
		# component scissorCrossing  
		if n_scissorCrossings > 0:  	
			for scissorCrossingId in scissorCrossingData:
				index = list(scissorCrossingData.keys()).index(scissorCrossingId)
				self.createScissorCrossing(index,scissorCrossingId,scissorCrossingData[scissorCrossingId],mode = 'component',f = f)
				self.createScissorCrossing(index,scissorCrossingId,scissorCrossingData[scissorCrossingId],mode = 'entity',f = None, example = example)
		# component doubleSwitch  
		if n_doubleSwitch > 0:  
			for doubleSwitchId in doubleSwitchData:
				index = list(doubleSwitchData.keys()).index(doubleSwitchId)
				self.createDoubleSwitch(index,doubleSwitchId,doubleSwitchData[doubleSwitchId],mode = 'component',f = f)
				self.createDoubleSwitch(index,doubleSwitchId,doubleSwitchData[doubleSwitchId],mode = 'entity',f = None, example = example)
		# component signals  
		if n_signals > 0:  	
			for signalId in signalData:
				index = list(signalData.keys()).index(signalId)
				self.createSignal(index,signalId,signalData,mode = 'component',f = f)
				self.createSignal(index,signalId,signalData,mode = 'entity',f = None, example = example)
		# component node
		if n_netElements > 0:
			for netElementId in list(graph.keys()):
				index = list(graph.keys()).index(netElementId)
				self.createNode(index,netElementId,routes,mode = 'component',f = f)
				self.createNode(index,netElementId,routes,mode = 'entity',f = None, example = example)
		# component route
		if n_routes > 0:
			for routeId in list(routes.keys()):
				index = list(routes.keys()).index(routeId)
				self.createRoute(index,routes[routeId],mode = 'component',f = f)
				self.createRoute(index,routes[routeId],mode = 'entity',f = None, example = example)

		# intersignals
		if n_levelCrossings > 0:
			levelCrossings = " , ".join([f'state_{i}' for i in list(levelCrossingData.keys())])
			f.write(f'\tsignal {levelCrossings} : levelCrossingStates;\n')
			levelCrossings = " , ".join([f'{i}_locking' for i in list(levelCrossingData.keys())])
			f.write(f'\tsignal {levelCrossings} : objectLock;\n')
		if n_switches > 0: 
			singleSwitches = " , ".join([f'state_{i}' for i in list(singleSwitchData.keys())])
			f.write(f'\tsignal {singleSwitches} : singleSwitchStates;\n')
			singleSwitches = " , ".join([f'{"s" if i[0].isdigit() else ""}{i}_locking' for i in list(singleSwitchData.keys())])
			f.write(f'\tsignal {singleSwitches} : objectLock;\n')
		if n_scissorCrossings > 0:
			scissorCrossings = " , ".join([f'state_{i}' for i in list(scissorCrossingData.keys())])
			f.write(f'\tsignal {scissorCrossings} : scissorCrossingStates;\n')
			scissorCrossings = " , ".join([f'{"s" if i[0].isdigit() else ""}{i}_locking' for i in list(scissorCrossingData.keys())])
			f.write(f'\tsignal {scissorCrossings} : objectLock;\n')
		if n_doubleSwitch > 0: 
			doubleSwitches = " , ".join([f'state_{i}' for i in list(doubleSwitchData.keys())])
			f.write(f'\tsignal {doubleSwitches} : doubleSwitchStates;\n')
			doubleSwitches = " , ".join([f'{"s" if i[0].isdigit() else ""}{i}_locking' for i in list(doubleSwitchData.keys())])
			f.write(f'\tsignal {doubleSwitches} : objectLock;\n')
		if n_signals > 0: 
			signals = " , ".join([f'state_{i}' for i in list(signalData.keys())])
			f.write(f'\tsignal {signals} : signalStates;\n')
			signals = " , ".join([f'{i}_locking' for i in list(signalData.keys())])
			f.write(f'\tsignal {signals} : objectLock;\n')

		if n_netElements > 0:
			netElements = " , ".join([f'state_{i}' for i in list(graph.keys())])
			f.write(f'\tsignal {netElements} : nodeStates;\n')
			netElements = " , ".join([f'{i}_locking' for i in list(graph.keys())])
			f.write(f'\tsignal {netElements} : objectLock;\n')
			commands = " , ".join([f'cmd_R{i}_{j}' for i in routes for j in routes[i]['Path']])
			f.write(f'\tsignal {commands} : routeCommands;\n')
		if n_levelCrossings > 0:
			commands = " , ".join([f'cmd_R{i}_{j}' for i in routes for j in routes[i]['LevelCrossings']])
			f.write(f'\tsignal {commands} : routeCommands;\n')
		if n_switches+n_doubleSwitch > 0: 
			commands = " , ".join([f'cmd_R{i}_{j.split('_')[0]}' for i in routes for j in routes[i]['Switches']])
			f.write(f'\tsignal {commands} : routeCommands;\n')
		if n_scissorCrossings > 0:
			commands = " , ".join([f'cmd_R{i}_{j.split('_')[0]}' for i in routes for j in routes[i]['ScissorCrossings']])
			f.write(f'\tsignal {commands} : routeCommands;\n')
		if n_signals > 0: 
			commands = " , ".join([f'cmd_R{i}_{routes[i]['Start']}' for i in routes])
			f.write(f'\tsignal {commands} : routeCommands;\r\n')
			
		f.write(f'begin\r\n') 

		#print(list(graph.keys()))

		# instantiate levelCrossings
		for levelCrossingId in levelCrossingData:
			index = list(levelCrossingData.keys()).index(levelCrossingId)
			f.write(f'\tlevelCrossing_{levelCrossingId} : levelCrossing_{index} port map(')
			f.write(f'clock => clock, ')

			for element in levelCrossingData[levelCrossingId]['Routes']:
				f.write(f'{element}_command => cmd_{element}_{levelCrossingId}, ')

			for element in levelCrossingData[levelCrossingId]['Neighbour']:
				netElement = list(graph.keys()).index(element)
				f.write(f'ocupation_{element} => ocupation({netElement}), ')

			if n_levelCrossings > 1:
				f.write(f'indication => levelCrossings_i({index}), command  => levelCrossings_o({index}), ')
			if n_levelCrossings == 1:
				f.write(f'indication => levelCrossings_i, command  => levelCrossings_o, ')

			f.write(f'lock_{levelCrossingId} => {levelCrossingId}_locking, ')
			f.write(f'correspondence_{levelCrossingId} => state_{levelCrossingId});\r\n')		

		# instantiate singleSwitches
		for singleSwitchId in singleSwitchData:
			index = list(singleSwitchData.keys()).index(singleSwitchId)
			f.write(f'\tsingleSwitch_{singleSwitchId} : singleSwitch_{index} port map(')
			f.write(f'clock => clock, ')

			for element in singleSwitchData[singleSwitchId]['Routes']:
				f.write(f'{element}_command => cmd_{element}_{singleSwitchId}, ')

			if n_switches > 1:
				f.write(f'indication => singleSwitches_i({index}), command => singleSwitches_o({index}), ')
			if n_switches == 1:
				f.write(f'indication => singleSwitches_i, command => singleSwitches_o, ')
			f.write(f'correspondence_{singleSwitchId} => state_{singleSwitchId});\r\n')

		# instantiate scissorCrossings
		for scissorCrossingId in scissorCrossingData:
			index = list(scissorCrossingData.keys()).index(scissorCrossingId)
			f.write(f'\tscissorCrossing_{scissorCrossingId} : scissorCrossing_{index} port map(')
			f.write(f'clock => clock, ')

			for element in scissorCrossingData[scissorCrossingId]['Routes']:
				f.write(f'{element}_command => cmd_{element}_{scissorCrossingId}, ')

			if n_scissorCrossings > 1:
				f.write(f'indication => scissorCrossings_i({index}), command => scissorCrossings_o({index}), ')
			if n_scissorCrossings == 1:
				f.write(f'indication => scissorCrossings_i, command => scissorCrossings_o, ')
			f.write(f'correspondence_{scissorCrossingId} => state_{scissorCrossingId});\r\n')

		# instantiate doubleSwitches
		for doubleSwitchId in doubleSwitchData:
			index = list(doubleSwitchData.keys()).index(doubleSwitchId)
			f.write(f'\tdoubleSwitch_{doubleSwitchId} : doubleSwitch_{index} port map(')
			f.write(f'clock => clock, ')

			for element in doubleSwitchData[doubleSwitchId]['Routes']:
				f.write(f'{element}_command => cmd_{element}_{doubleSwitchId}, ')

			if n_doubleSwitch > 1:
				f.write(f'indication.msb => doubleSwitches_i.msb({index}), indication.lsb => doubleSwitches_i.lsb({index}), ')
				f.write(f'command.msb => doubleSwitches_o.msb({index}), command.lsb => doubleSwitches_o.lsb({index}),')
			if n_doubleSwitch == 1:
				f.write(f'indication => doubleSwitches_i, command => doubleSwitches_o, ')
			f.write(f'correspondence_{doubleSwitchId} => state_{doubleSwitchId});\r\n')

		# instantiate signals
		for signalId in signalData:
			index = list(signalData.keys()).index(signalId)
			f.write(f'\trailwaySignal_{signalId} : railwaySignal_{index} port map(')
			f.write(f'clock => clock, ')

			if 'Routes' in signalData[signalId]:
				for element in signalData[signalId]['Routes']:
					f.write(f'{element}_command => cmd_{element}_{signalId}, ')

			ocupationLevel_0,ocupationLevel_1,ocupationLevel_2,signal_0,signal_1,signal_2,switches_1,switches_2,paths = self.getSignalGraph(signalId,signalData)

			netElement = list(graph.keys()).index(ocupationLevel_0)
			f.write(f'ocupation_{ocupationLevel_0} => ocupation({netElement}), ')
			if ocupationLevel_1 != []:
				for i in ocupationLevel_1:
					if i != ocupationLevel_0:
						netElement = list(graph.keys()).index(i)
						f.write(f'ocupation_{i} => ocupation({netElement}), ')		
			if ocupationLevel_2 != []:
				for i in ocupationLevel_2:
					if i not in ocupationLevel_1 and i != ocupationLevel_0:
						netElement = list(graph.keys()).index(i)
						f.write(f'ocupation_{i} => ocupation({netElement}), ')

			if signal_1 != []:
				for i in signal_1:
					f.write(f'correspondence_{i} => state_{i}, ')		
			if signal_2 != []:
				for i in signal_2:
					if i not in signal_1:
						f.write(f'correspondence_{i} => state_{i}, ')

			sw_print = []
			for path in paths:
				if paths[path]['Switches'] != []:
					for i in paths[path]['Switches']:
						if i.split('_')[0] not in sw_print:
							sw_print.append(i.split('_')[0])
			if sw_print != []:
				for i in sw_print:
					f.write(f'{"s" if i[0].isdigit() else ""}{i.split('_')[0]}_state => state_{i.split('_')[0]}, ')	

			lc_print = []
			for path in paths:
				if paths[path]['LevelCrossings'] != []:
					for i in paths[path]['LevelCrossings']:
						if i not in lc_print:
							lc_print.append(i.split('_')[0])
			if lc_print != []:
				for i in lc_print:
					f.write(f'{i}_state => state_{i}, ')	

			if n_signals > 1:
				f.write(f'indication.msb => signals_i.msb({index}), indication.lsb => signals_i.lsb({index}), ')
				f.write(f'command.msb => signals_o.msb({index}), command.lsb => signals_o.lsb({index}), ')
			if n_signals == 1:
				f.write(f'indication => signals_i, command => signals_o, ')
			f.write(f'lock_{signalId} => {signalId}_locking, ')	
			f.write(f'correspondence_{signalId} => state_{signalId});\r\n')
				
		# instantiate nodes
		for netElementId in list(graph.keys()):
			index = list(graph.keys()).index(netElementId)
			f.write(f'\tnode_{netElementId} : node_{index} port map(')

			if n_netElements > 1:
				f.write(f'clock => clock, ocupation => ocupation({index}), ')
			if n_netElements == 1:	
				f.write(f'clock => clock, ocupation => ocupation, ')	

			for route in routes:
				if netElementId in routes[route]['Path']:
					f.write(f'R{route}_command => cmd_R{route}_{netElementId}, ')
			f.write(f'state => state_{netElementId}, ')
			f.write(f'locking => {netElementId}_locking);\r\n')

		# instantiate routes
		for routeId in list(routes.keys()):
			index = list(routes.keys()).index(routeId)
			f.write(f'\troute_R{routeId} : route_{index} port map(')

			if n_routes > 1:
				f.write(f'clock => clock, routeRequest => routes_i({index}), ')
			if n_routes == 1:
				f.write(f'clock => clock, routeRequest => routes_i, ')	

			for netElementId in list(graph.keys()):
				if netElementId in routes[routeId]['Path']:
					f.write(f'{netElementId}_command => cmd_R{routeId}_{netElementId}, ')
					f.write(f'{netElementId}_state => state_{netElementId}, ')
					f.write(f'{netElementId}_lock => {netElementId}_locking, ')
			for levelCrossingId in routes[routeId]['LevelCrossings']:
				f.write(f'{levelCrossingId}_command => cmd_R{routeId}_{levelCrossingId}, ')	
				f.write(f'{levelCrossingId}_state => state_{levelCrossingId}, ')
				f.write(f'{levelCrossingId}_lock => {levelCrossingId}_locking, ')		
			for singleSwitchId in routes[routeId]['Switches']:
				f.write(f'{"s" if singleSwitchId[0].isdigit() else ""}{singleSwitchId.split('_')[0]}_command => cmd_R{routeId}_{singleSwitchId.split('_')[0]}, ')	
				f.write(f'{"s" if singleSwitchId[0].isdigit() else ""}{singleSwitchId.split('_')[0]}_state => state_{singleSwitchId.split('_')[0]}, ')
				f.write(f'{"s" if singleSwitchId[0].isdigit() else ""}{singleSwitchId.split('_')[0]}_lock => {"s" if singleSwitchId[0].isdigit() else ""}{singleSwitchId.split('_')[0]}_locking, ')
			for scissorCrossingId in routes[routeId]['ScissorCrossings']:
				f.write(f'{"s" if scissorCrossingId[0].isdigit() else ""}{scissorCrossingId.split('_')[0]}_command => cmd_R{routeId}_{scissorCrossingId.split('_')[0]}, ')	
				f.write(f'{"s" if scissorCrossingId[0].isdigit() else ""}{scissorCrossingId.split('_')[0]}_state => state_{scissorCrossingId.split('_')[0]}, ')
				f.write(f'{"s" if scissorCrossingId[0].isdigit() else ""}{scissorCrossingId.split('_')[0]}_lock => {"s" if scissorCrossingId[0].isdigit() else ""}{scissorCrossingId.split('_')[0]}_locking, ')

			f.write(f'{routes[routeId]['Start']}_state => state_{routes[routeId]['Start']}, ')
			f.write(f'{routes[routeId]['Start']}_lock => {routes[routeId]['Start']}_locking, ')
			f.write(f'{routes[routeId]['Start']}_command => cmd_R{routeId}_{routes[routeId]['Start']}, ')	

			f.write(f'{routes[routeId]['End']}_state => state_{routes[routeId]['End']}, ')
			#f.write(f'{routes[routeId]['End']}_command => cmd_R{routeId}_{routes[routeId]['End']}, ')	

			f.write(f'routeState => routes_o({index}));\r\n')

		f.write(f'end Behavioral;') 
    
		f.close()  # Close header file	

	def getLevelCrossings(self,network,routes):
		levelCrossingId = {}

		for element in network:
			if 'LevelCrossing' in network[element]:
				for levelCrossing in network[element]['LevelCrossing']:
					if levelCrossing not in levelCrossingId:
						levelCrossingId[levelCrossing] = {'Neighbour':[]}
					
					if element not in levelCrossingId[levelCrossing]['Neighbour']:
						levelCrossingId[levelCrossing]['Neighbour'].append(element)

					if network[element]['Neighbour'] not in levelCrossingId[levelCrossing]['Neighbour']:
						for i in network[element]['Neighbour']:
							levelCrossingId[levelCrossing]['Neighbour'].append(i)

		for levelCrossing in levelCrossingId:
			for route in routes:
				if levelCrossing in routes[route]['LevelCrossings']:
					if 'Routes' not in levelCrossingId[levelCrossing]:
						levelCrossingId[levelCrossing] |= {'Routes':[]}
					if route not in levelCrossingId[levelCrossing]['Routes']:
						levelCrossingId[levelCrossing]['Routes'].append(f'R{route}')

		return levelCrossingId

	def getSingleSwitch(self,network,routes):
		singleSwitchId = {}

		for element in network:
			if 'Switch' in network[element]:
				for switch in network[element]['Switch']:
					if switch not in singleSwitchId:
						singleSwitchId[switch] = {'Neighbour':3*[None]} 

					if element not in singleSwitchId[switch]['Neighbour']:
						singleSwitchId[switch]['Neighbour'][0] = element

			if 'Switch_B' in network[element]:
				for switch in network[element]['Switch_B']:
					if switch not in singleSwitchId:
						singleSwitchId[switch] = {'Neighbour':3*[None]} 

					if element not in singleSwitchId[switch]['Neighbour']:
						singleSwitchId[switch]['Neighbour'][1] = element
			if 'Switch_C' in network[element]:
				for switch in network[element]['Switch_C']:
					if switch not in singleSwitchId:
						singleSwitchId[switch] = {'Neighbour':3*[None]} 

					if element not in singleSwitchId[switch]['Neighbour']:
						singleSwitchId[switch]['Neighbour'][2] = element

		for singleSwitch in singleSwitchId:
			for route in routes:
				if singleSwitch+'_N' in routes[route]['Switches']:
					if 'Routes' not in singleSwitchId[singleSwitch]:
						singleSwitchId[singleSwitch] |= {'Routes':[]}
						singleSwitchId[singleSwitch] |= {'Position':[]}
					if route not in singleSwitchId[singleSwitch]['Routes']:
						singleSwitchId[singleSwitch]['Routes'].append(f'R{route}')
						singleSwitchId[singleSwitch]['Position'].append(f'N')
				if singleSwitch+'_R' in routes[route]['Switches']:
					if 'Routes' not in singleSwitchId[singleSwitch]:
						singleSwitchId[singleSwitch] |= {'Routes':[]}
						singleSwitchId[singleSwitch] |= {'Position':[]}
					if route not in singleSwitchId[singleSwitch]['Routes']:
						singleSwitchId[singleSwitch]['Routes'].append(f'R{route}')
						singleSwitchId[singleSwitch]['Position'].append(f'R')
		return singleSwitchId

	def getScissorCrossing(self,network,routes):
		scissorCrossingId = {}

		for element in network:
			if 'Crossing' in network[element]:
				for scissorCrossing in network[element]['Crossing']:
					if scissorCrossing not in scissorCrossingId:
						scissorCrossingId[scissorCrossing] = {'Neighbour':[]} 
					
					if element not in scissorCrossingId[scissorCrossing]['Neighbour']:
						scissorCrossingId[scissorCrossing]['Neighbour'].append(element)

		for scissorCrossing in scissorCrossingId:
			for route in routes:
				if scissorCrossing+'_XN' in routes[route]['ScissorCrossings']:
					if 'Routes' not in scissorCrossingId[scissorCrossing]:
						scissorCrossingId[scissorCrossing] |= {'Routes':[]}
						scissorCrossingId[scissorCrossing] |= {'Position':[]}
					if route not in scissorCrossingId[scissorCrossing]['Routes']:
						scissorCrossingId[scissorCrossing]['Routes'].append(f'R{route}')
						scissorCrossingId[scissorCrossing]['Position'].append(f'N')
				if scissorCrossing+'_XR' in routes[route]['ScissorCrossings']:
					if 'Routes' not in scissorCrossingId[scissorCrossing]:
						scissorCrossingId[scissorCrossing] |= {'Routes':[]}
						scissorCrossingId[scissorCrossing] |= {'Position':[]}
					if route not in scissorCrossingId[scissorCrossing]['Routes']:
						scissorCrossingId[scissorCrossing]['Routes'].append(f'R{route}')
						scissorCrossingId[scissorCrossing]['Position'].append(f'R')
		return scissorCrossingId

	def getDoubleSwitch(self,network,routes):
		doubleSwitchId = {}

		for element in network:
			if 'Switch_X' in network[element]:
				for doubleSwitch in network[element]['Switch_X']:
					if doubleSwitch not in doubleSwitchId:
						doubleSwitchId[doubleSwitch] = {'Neighbour':[]} 
					
					if element not in doubleSwitchId[doubleSwitch]['Neighbour']:
						doubleSwitchId[doubleSwitch]['Neighbour'].append(element)

		for doubleSwitch in doubleSwitchId:
			for route in routes:
				if doubleSwitch+'_NN' in routes[route]['Switches']:
					if 'Routes' not in doubleSwitchId[doubleSwitch]:
						doubleSwitchId[doubleSwitch] |= {'Routes':[]}
						doubleSwitchId[doubleSwitch] |= {'Position':[]}
					if route not in doubleSwitchId[doubleSwitch]['Routes']:
						doubleSwitchId[doubleSwitch]['Routes'].append(f'R{route}')
						doubleSwitchId[doubleSwitch]['Position'].append(f'NN')
				if doubleSwitch+'_NR' in routes[route]['Switches']:
					if 'Routes' not in doubleSwitchId[doubleSwitch]:
						doubleSwitchId[doubleSwitch] |= {'Routes':[]}
						doubleSwitchId[doubleSwitch] |= {'Position':[]}
					if route not in doubleSwitchId[doubleSwitch]['Routes']:
						doubleSwitchId[doubleSwitch]['Routes'].append(f'R{route}')
						doubleSwitchId[doubleSwitch]['Position'].append(f'NR')
				if doubleSwitch+'_RN' in routes[route]['Switches']:
					if 'Routes' not in doubleSwitchId[doubleSwitch]:
						doubleSwitchId[doubleSwitch] |= {'Routes':[]}
						doubleSwitchId[doubleSwitch] |= {'Position':[]}
					if route not in doubleSwitchId[doubleSwitch]['Routes']:
						doubleSwitchId[doubleSwitch]['Routes'].append(f'R{route}')
						doubleSwitchId[doubleSwitch]['Position'].append(f'RN')
				if doubleSwitch+'_RR' in routes[route]['Switches']:
					if 'Routes' not in doubleSwitchId[doubleSwitch]:
						doubleSwitchId[doubleSwitch] |= {'Routes':[]}
						doubleSwitchId[doubleSwitch] |= {'Position':[]}
					if route not in doubleSwitchId[doubleSwitch]['Routes']:
						doubleSwitchId[doubleSwitch]['Routes'].append(f'R{route}')
						doubleSwitchId[doubleSwitch]['Position'].append(f'RR')
		return doubleSwitchId

	def getSignal(self,network,routes):
		signalId = {}

		for element in network:
			if 'Signal' in network[element]:
				for signal in network[element]['Signal']:
					if signal not in signalId:
						signalId[signal] = {}
						signalId[signal] |= {'Start':element}

		for signal in signalId:
			switch_aux = []
			lc_aux = []
			for route in routes:
				if signal == routes[route]['Start']:
					if 'Routes' not in signalId[signal]:
						signalId[signal] |= {'Routes':[]}
					if f'R{route}' not in signalId[signal]['Routes']:
						signalId[signal]['Routes'].append(f'R{route}')

					if 'Next' not in signalId[signal]:
						signalId[signal] |= {'Next':[]}
					if routes[route]['Path'][1:] not in signalId[signal]['Next']:
						signalId[signal]['Next'].append(routes[route]['End'])

					if 'Switches' not in signalId[signal]:
						signalId[signal] |= {'Switches':[]}

					if routes[route]['Switches'] != [] or routes[route]['ScissorCrossings'] != []:

						if routes[route]['Switches'] != [] and routes[route]['Switches'] not in switch_aux:
							switch_aux.append(routes[route]['Switches'])
						if routes[route]['ScissorCrossings'] != [] and routes[route]['ScissorCrossings'] not in switch_aux:
							switch_aux.append(routes[route]['ScissorCrossings'])

					signalId[signal]['Switches'] = switch_aux

					if 'LevelCrossings' not in signalId[signal]:
						signalId[signal] |= {'LevelCrossings':[]}
					#if routes[route]['LevelCrossings'] not in signalId[signal]['LevelCrossings']:
					signalId[signal]['LevelCrossings'].append(routes[route]['LevelCrossings'])	

					if 'Path' not in signalId[signal]:
						signalId[signal] |= {'Path':[]}
					if routes[route]['Path'][1:] not in signalId[signal]['Path']:
						signalId[signal]['Path'].append(routes[route]['Path'][1:])						

		print('')
		for signal in signalId:
			print(f'{signal} > {signalId[signal]}')	
		print('')
		return signalId

	def createLevelCrossing(self,index,name,data,mode, f = None,example = 1):	
		if mode == 'entity':
			node = f'levelCrossing_{index}'
			f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
			
			# Initial comment
			self.initialComment(node,f)
			
			# Include library
			self.includeLibrary(f,True)
		
		levelCrossing = f'levelCrossing_{index}'
		f.write(f'\t{mode} {levelCrossing} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		 
		for neighbour in data['Neighbour']:
			f.write(f'\t\t\tocupation_{neighbour} : in std_logic;\n')

		ocupation = " and ".join([f'ocupation_{i}' for i in data['Neighbour']])

		commands = []
		for routes in data['Routes']:
			f.write(f'\t\t\t{routes}_command : in routeCommands;\r\n')
			commands.append(routes)

		f.write(f'\t\t\tindication : in std_logic;\n')
		f.write(f'\t\t\tcommand : out std_logic;\n')
		f.write(f'\t\t\tcorrespondence_{name} : out levelCrossingStates;\n')
		f.write(f'\t\t\tlock_{name} : out objectLock\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend {mode} {levelCrossing};\n')

		if mode == 'entity':
			freeState = " and ".join([f'{i}_command = RELEASE' for i in commands])
			reserveState = " or ".join([f'{i}_command = RESERVE' for i in commands])
			lockState = " or ".join([f'{i}_command = LOCK' for i in commands])

			freq = 10e6
			timeout = 7

			FF = math.ceil(math.log2(timeout*freq))

			t = [(2**(i+1))/freq for i in range(FF)]
			sequence = [0]*FF
			total = 0
			for i in range(FF-1,-1,-1):
				if total + t[i] <= timeout:
					total += t[i]
					sequence[i] = 1
			timeout_stop = " and ".join([f'Q({i}) = \'{sequence[i]}\'' for i in range(FF)])
	
			f.write(f'architecture Behavioral of {node} is\r\n')

			f.write(f'\tcomponent flipFlop is\r\n')
			f.write(f'\t\tport(\r\n')
			f.write(f'\t\t\tclock : in std_logic;\r\n')
			f.write(f'\t\t\treset : in std_logic;\r\n')
			f.write(f'\t\t\tQ : out std_logic\r\n')
			f.write(f'\t\t);\r\n')
			f.write(f'\tend component flipFlop;\r\n')

			f.write(f'\tsignal reset : std_logic := \'0\';\r\n')
			f.write(f'\tsignal Q : std_logic_vector({FF} downto 0) := (others => \'0\');\r\n')
			f.write(f'\tsignal commandState : routeCommands;\r\n')
			f.write(f'\tsignal commandAux : std_logic;\r\n')

			f.write(f'begin\r\n')

			f.write(f'\tgen : for i in 0 to {FF-1} generate\r\n')
			f.write(f'\t\tinst: flipFlop port map(Q(i),reset,Q(i+1));\r\n')
			f.write(f'\tend generate;\r\n')

			f.write(f'\tQ(0) <= clock;\r\n')

			f.write(f'\n\tprocess(clock)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')
			f.write(f'\t\t\tif ({freeState}) then\r\n')
			f.write(f'\t\t\t\tcommandState <= RELEASE;\r\n')
			f.write(f'\t\t\telse\r\n')
			f.write(f'\t\t\t\tif ({reserveState}) then\r\n')
			f.write(f'\t\t\t\t\tcommandState <= RESERVE;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif ({lockState}) then\r\n')
			f.write(f'\t\t\t\t\rcommandState <= LOCK;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\tend if;\r\n')
			f.write(f'\t\tend if;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(commandState)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tcase commandState is\r\n')
			f.write(f'\t\t\twhen RELEASE => -- AUTOMATIC\r\n')
			f.write(f'\t\t\t\tlock_{name} <= RELEASED;\n')
			f.write(f'\t\t\twhen RESERVE => -- DONT CHANGE\r\n')
			f.write(f'\t\t\t\tlock_{name} <= RESERVED;\n')
			f.write(f'\t\t\twhen LOCK => -- DONT CHANGE\r\n')
			f.write(f'\t\t\t\tlock_{name} <= LOCKED;\n')
			f.write(f'\t\t\twhen others =>\r\n')
			f.write(f'\t\t\t\tlock_{name} <= LOCKED;\n')
			f.write(f'\t\tend case;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(commandState)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tcase commandState is\r\n')
			f.write(f'\t\t\twhen RELEASE => -- AUTOMATIC\r\n')
			f.write(f'\t\t\t\tcommandAux <= {ocupation};\r\n')
			f.write(f'\t\t\twhen RESERVE => -- DONT CHANGE\r\n')
			f.write(f'\t\t\t\tcommandAux <= \'0\';\r\n')
			f.write(f'\t\t\twhen LOCK => -- DONT CHANGE\r\n')
			f.write(f'\t\t\t\tcommandAux <= \'0\';\r\n')
			f.write(f'\t\t\twhen others =>\r\n')
			f.write(f'\t\t\t\tcommandAux <= \'0\';\r\n')
			f.write(f'\t\tend case;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(clock)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')

			f.write(f'\t\t\tif({timeout_stop}) then\r\n')
			f.write(f'\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tif(indication = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= DOWN;\r\n')
			f.write(f'\t\t\t\telse\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= UP;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\telse\r\n')
			
			f.write(f'\t\t\t\tif (commandAux = \'0\' and indication = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= DOWN;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			
			f.write(f'\t\t\t\tif (commandAux = \'1\' and indication = \'1\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= UP;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')

			f.write(f'\t\t\t\tif (commandAux /= indication) then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= TRANSITION;\r\n')
			f.write(f'\t\t\t\t\treset <= \'0\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\tend if;\r\n')
			f.write(f'\t\tend if;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\tcommand <= commandAux;\r\n')
			f.write(f'end Behavioral;') 
			f.close()  # Close header file

	def createSingleSwitch(self,index,name,data,mode, f = None,example = 1):
		if mode == 'entity':
			node = f'singleSwitch_{index}'
			f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
			
			# Initial comment
			self.initialComment(node,f)
			
			# Include library
			self.includeLibrary(f,True)
		
		singleSwitch = f'singleSwitch_{index}'
		f.write(f'\t{mode} {singleSwitch} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')

		commands = []
		commands_N = []
		commands_R = []
		for element in range(len(data['Routes'])):
			f.write(f'\t\t\t{data['Routes'][element]}_command : in routeCommands;\n')
			commands.append(data['Routes'][element])
			if data['Position'][element] == 'N':
				commands_N.append(data['Routes'][element])
			else:
				commands_R.append(data['Routes'][element])	

		f.write(f'\t\t\tindication : in std_logic;\n')
		f.write(f'\t\t\tcommand : out std_logic;\n')
		f.write(f'\t\t\tcorrespondence_{name} : out singleSwitchStates;\n')
		f.write(f'\t\t\tlock_{name} : out objectLock\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend {mode} {singleSwitch};\n')

		if mode == 'entity':
			freeState = " and ".join([f'{i}_command = RELEASE' for i in commands])
			freeState_N = " and ".join([f'{i}_command = RELEASE' for i in commands_N])
			freeState_R = " and ".join([f'{i}_command = RELEASE' for i in commands_R])
			reserveState = " or ".join([f'{i}_command = RESERVE' for i in commands])
			reserveState_N = " or ".join([f'{i}_command = RESERVE' for i in commands_N])
			reserveState_R = " or ".join([f'{i}_command = RESERVE' for i in commands_R])
			lockState = " or ".join([f'{i}_command = LOCK' for i in commands])
			lockState_N = " or ".join([f'{i}_command = LOCK' for i in commands_N])
			lockState_R = " or ".join([f'{i}_command = LOCK' for i in commands_R])

			freq = 10e6
			timeout = 7

			FF = math.ceil(math.log2(timeout*freq))

			t = [(2**(i+1))/freq for i in range(FF)]
			sequence = [0]*FF
			total = 0
			for i in range(FF-1,-1,-1):
				if total + t[i] <= timeout:
					total += t[i]
					sequence[i] = 1
			timeout_stop = " and ".join([f'Q({i}) = \'{sequence[i]}\'' for i in range(FF)])

			f.write(f'architecture Behavioral of {node} is\n')

			f.write(f'\tcomponent flipFlop is\r\n')
			f.write(f'\t\tport(\r\n')
			f.write(f'\t\t\tclock : in std_logic;\r\n')
			f.write(f'\t\t\treset : in std_logic;\r\n')
			f.write(f'\t\t\tQ : out std_logic\r\n')
			f.write(f'\t\t);\r\n')
			f.write(f'\tend component flipFlop;\r\n')

			f.write(f'\tsignal reset : std_logic := \'0\';\r\n')
			f.write(f'\tsignal Q : std_logic_vector({FF} downto 0) := (others => \'0\');\r\n')
			f.write(f'\tsignal commandState : routeCommands;\r\n')
			f.write(f'\tsignal commandAux : std_logic;\r\n')

			f.write(f'begin\n')

			f.write(f'\tgen : for i in 0 to {FF-1} generate\r\n')
			f.write(f'\t\tinst: flipFlop port map(Q(i),reset,Q(i+1));\r\n')
			f.write(f'\tend generate;\r\n')

			f.write(f'\tQ(0) <= clock;\r\n')

			f.write(f'\n\tprocess(clock)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')
			f.write(f'\t\t\tif ({freeState}) then\r\n')
			f.write(f'\t\t\t\tcommandState <= RELEASE;\r\n')
			f.write(f'\t\t\telse\r\n')
			f.write(f'\t\t\t\tif ({reserveState}) then\r\n')
			f.write(f'\t\t\t\t\tcommandState <= RESERVE;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif ({lockState}) then\r\n')
			f.write(f'\t\t\t\t\rcommandState <= LOCK;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\tend if;\r\n')
			f.write(f'\t\tend if;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(commandState)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tcase commandState is\r\n')
			f.write(f'\t\t\twhen RELEASE => -- AUTOMATIC\r\n')
			f.write(f'\t\t\t\tlock_{name} <= RELEASED;\n')
			f.write(f'\t\t\twhen RESERVE => -- DONT CHANGE\r\n')
			f.write(f'\t\t\t\tlock_{name} <= RESERVED;\n')
			f.write(f'\t\t\twhen LOCK => -- DONT CHANGE\r\n')
			f.write(f'\t\t\t\tlock_{name} <= LOCKED;\n')
			f.write(f'\t\t\twhen others =>\r\n')
			f.write(f'\t\t\t\tlock_{name} <= LOCKED;\n')
			f.write(f'\t\tend case;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(commandState)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tcase commandState is\r\n')
			f.write(f'\t\t\twhen RELEASE => -- AUTOMATIC\r\n')
			f.write(f'\t\t\t\tcommandAux <= indication;\n')
			f.write(f'\t\t\twhen RESERVE =>\r\n')
			f.write(f'\t\t\t\tif (({reserveState_N}) and ({freeState_R})) then\n')
			f.write(f'\t\t\t\t\tcommandAux <= \'0\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\t\tif (({freeState_N}) and ({reserveState_R})) then\n')
			f.write(f'\t\t\t\t\tcommandAux <= \'1\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\twhen LOCK =>\r\n')
			f.write(f'\t\t\t\tif (({lockState_N}) and ({freeState_R})) then\n')
			f.write(f'\t\t\t\t\tcommandAux <= \'0\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\t\tif (({freeState_N}) and ({lockState_R})) then\n')
			f.write(f'\t\t\t\t\tcommandAux <= \'1\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\twhen others =>\r\n')
			f.write(f'\t\t\t\tcommandAux <= indication;\n')
			f.write(f'\t\tend case;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(clock)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')

			f.write(f'\t\t\tif({timeout_stop}) then\r\n')
			f.write(f'\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tif(indication = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= NORMAL;\r\n')
			f.write(f'\t\t\t\telse\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= REVERSE;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\telse\r\n')
			
			f.write(f'\t\t\t\tif (commandAux = \'0\' and indication = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= NORMAL;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			
			f.write(f'\t\t\t\tif (commandAux = \'1\' and indication = \'1\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= REVERSE;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')

			f.write(f'\t\t\t\tif (commandAux /= indication) then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= TRANSITION;\r\n')
			f.write(f'\t\t\t\t\treset <= \'0\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\tend if;\r\n')
			f.write(f'\t\tend if;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\tcommand <= commandAux;\r\n')
			f.write(f'end Behavioral;') 
			f.close()  # Close header file

	def createDoubleSwitch(self,index,name,data,mode, f = None,example = 1):
		if mode == 'entity':
			node = f'doubleSwitch_{index}'
			f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
			
			# Initial comment
			self.initialComment(node,f)
			
			# Include library
			self.includeLibrary(f,True)
		
		doubleSwitch = f'doubleSwitch_{index}'
		f.write(f'\t{mode} {doubleSwitch} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')

		commands = []
		commands_NN = []
		commands_RR = []
		commands_RN = []
		commands_NR = []
		for element in range(len(data['Routes'])):
			f.write(f'\t\t\t{data['Routes'][element]}_command : in routeCommands;\n')
			commands.append(data['Routes'][element])
			if data['Position'][element] == 'NN':
				commands_NN.append(data['Routes'][element])
			if data['Position'][element] == 'RR':
				commands_RR.append(data['Routes'][element])
			if data['Position'][element] == 'RN':
				commands_RN.append(data['Routes'][element])
			if data['Position'][element] == 'NR':
				commands_NR.append(data['Routes'][element])

		f.write(f'\t\t\tindication : in dSwitch_type;\n')
		f.write(f'\t\t\tcommand : out dSwitch_type;\n')
		f.write(f'\t\t\tcorrespondence_{name} : out doubleSwitchStates;\n')
		f.write(f'\t\t\tlock_{name} : out objectLock\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend {mode} {doubleSwitch};\n')

		if mode == 'entity':
			freeState = " and ".join([f'{i}_command = RELEASE' for i in commands])
			freeState_NN = " and ".join([f'{i}_command = RELEASE' for i in commands_NN])
			freeState_RR = " and ".join([f'{i}_command = RELEASE' for i in commands_RR])
			freeState_RN = " and ".join([f'{i}_command = RELEASE' for i in commands_RN])
			freeState_NR = " and ".join([f'{i}_command = RELEASE' for i in commands_NR])

			reserveState = " or ".join([f'{i}_command = RESERVE' for i in commands])
			reserveState_NN = " or ".join([f'{i}_command = RESERVE' for i in commands_NN])
			reserveState_RR = " or ".join([f'{i}_command = RESERVE' for i in commands_RR])
			reserveState_RN = " or ".join([f'{i}_command = RESERVE' for i in commands_RN])
			reserveState_NR = " or ".join([f'{i}_command = RESERVE' for i in commands_NR])

			lockState = " or ".join([f'{i}_command = LOCK' for i in commands])
			lockState_NN = " or ".join([f'{i}_command = LOCK' for i in commands_NN])
			lockState_RR = " or ".join([f'{i}_command = LOCK' for i in commands_RR])
			lockState_RN = " or ".join([f'{i}_command = LOCK' for i in commands_RN])
			lockState_NR = " or ".join([f'{i}_command = LOCK' for i in commands_NR])

			freq = 10e6
			timeout = 7

			FF = math.ceil(math.log2(timeout*freq))

			t = [(2**(i+1))/freq for i in range(FF)]
			sequence = [0]*FF
			total = 0
			for i in range(FF-1,-1,-1):
				if total + t[i] <= timeout:
					total += t[i]
					sequence[i] = 1
			timeout_stop = " and ".join([f'Q({i}) = \'{sequence[i]}\'' for i in range(FF)])

			f.write(f'architecture Behavioral of {node} is\n')

			f.write(f'\tcomponent flipFlop is\r\n')
			f.write(f'\t\tport(\r\n')
			f.write(f'\t\t\tclock : in std_logic;\r\n')
			f.write(f'\t\t\treset : in std_logic;\r\n')
			f.write(f'\t\t\tQ : out std_logic\r\n')
			f.write(f'\t\t);\r\n')
			f.write(f'\tend component flipFlop;\r\n')

			f.write(f'\tsignal reset : std_logic := \'0\';\r\n')
			f.write(f'\tsignal Q : std_logic_vector({FF} downto 0) := (others => \'0\');\r\n')
			f.write(f'\tsignal commandState : routeCommands;\r\n')
			f.write(f'\tsignal commandAux : dSwitch_type;\r\n')

			f.write(f'begin\n')

			f.write(f'\tgen : for i in 0 to {FF-1} generate\r\n')
			f.write(f'\t\tinst: flipFlop port map(Q(i),reset,Q(i+1));\r\n')
			f.write(f'\tend generate;\r\n')

			f.write(f'\tQ(0) <= clock;\r\n')

			f.write(f'\n\tprocess(clock)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')
			f.write(f'\t\t\tif ({freeState}) then\r\n')
			f.write(f'\t\t\t\tcommandState <= RELEASE;\r\n')
			f.write(f'\t\t\telse\r\n')
			f.write(f'\t\t\t\tif ({reserveState}) then\r\n')
			f.write(f'\t\t\t\t\tcommandState <= RESERVE;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif ({lockState}) then\r\n')
			f.write(f'\t\t\t\t\rcommandState <= LOCK;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\tend if;\r\n')
			f.write(f'\t\tend if;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(commandState)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tcase commandState is\r\n')
			f.write(f'\t\t\twhen RELEASE => -- AUTOMATIC\r\n')
			f.write(f'\t\t\t\tlock_{name} <= RELEASED;\n')
			f.write(f'\t\t\twhen RESERVE => -- DONT CHANGE\r\n')
			f.write(f'\t\t\t\tlock_{name} <= RESERVED;\n')
			f.write(f'\t\t\twhen LOCK => -- DONT CHANGE\r\n')
			f.write(f'\t\t\t\tlock_{name} <= LOCKED;\n')
			f.write(f'\t\t\twhen others =>\r\n')
			f.write(f'\t\t\t\tlock_{name} <= LOCKED;\n')
			f.write(f'\t\tend case;\r\n')
			f.write(f'\tend process;\r\n')

			f.write(f'\n\tprocess(commandState)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tcase commandState is\r\n')
			f.write(f'\t\t\twhen RELEASE => -- AUTOMATIC\r\n')
			f.write(f'\t\t\t\tcommandAux.msb <= indication.msb;\n')
			f.write(f'\t\t\t\tcommandAux.lsb <= indication.lsb;\n')
			f.write(f'\t\t\twhen RESERVE =>\r\n')
			f.write(f'\t\t\t\tif (({reserveState_NN}) and ({freeState_RR}) and ({freeState_RN}) and ({freeState_NR})) then\n')
			f.write(f'\t\t\t\t\tcommandAux.msb <= \'0\';\n')
			f.write(f'\t\t\t\t\tcommandAux.lsb <= \'0\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\t\tif (({freeState_NN}) and ({reserveState_RR}) and ({freeState_RN}) and ({freeState_NR})) then\n')
			f.write(f'\t\t\t\t\tcommandAux.msb <= \'0\';\n')
			f.write(f'\t\t\t\t\tcommandAux.lsb <= \'1\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\t\tif (({freeState_NN}) and ({freeState_RR}) and ({reserveState_RN}) and ({freeState_NR})) then\n')
			f.write(f'\t\t\t\t\tcommandAux.msb <= \'1\';\n')
			f.write(f'\t\t\t\t\tcommandAux.lsb <= \'0\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\t\tif (({freeState_NN}) and ({freeState_RR}) and ({freeState_RN}) and ({reserveState_NR})) then\n')
			f.write(f'\t\t\t\t\tcommandAux.msb <= \'1\';\n')
			f.write(f'\t\t\t\t\tcommandAux.lsb <= \'1\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\twhen LOCK =>\r\n')
			f.write(f'\t\t\t\tif (({lockState_NN}) and ({freeState_RR}) and ({freeState_RN}) and ({freeState_NR})) then\n')
			f.write(f'\t\t\t\t\tcommandAux.msb <= \'0\';\n')
			f.write(f'\t\t\t\t\tcommandAux.lsb <= \'0\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\t\tif (({freeState_NN}) and ({lockState_RR}) and ({freeState_RN}) and ({freeState_NR})) then\n')
			f.write(f'\t\t\t\t\tcommandAux.msb <= \'0\';\n')
			f.write(f'\t\t\t\t\tcommandAux.lsb <= \'1\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\t\tif (({freeState_NN}) and ({freeState_RR}) and ({lockState_RN}) and ({freeState_NR})) then\n')
			f.write(f'\t\t\t\t\tcommandAux.msb <= \'1\';\n')
			f.write(f'\t\t\t\t\tcommandAux.lsb <= \'0\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\t\tif (({freeState_NN}) and ({freeState_RR}) and ({freeState_RN}) and ({lockState_NR})) then\n')
			f.write(f'\t\t\t\t\tcommandAux.msb <= \'1\';\n')
			f.write(f'\t\t\t\t\tcommandAux.lsb <= \'1\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\twhen others =>\r\n')
			f.write(f'\t\t\t\tcommandAux.msb <= indication.msb;\n')
			f.write(f'\t\t\t\tcommandAux.lsb <= indication.lsb;\n')
			f.write(f'\t\tend case;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(clock)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')

			f.write(f'\t\t\tif({timeout_stop}) then\r\n')
			f.write(f'\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tif(indication.msb = \'0\' and indication.lsb = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= DOUBLE_NORMAL;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif(indication.msb = \'1\' and indication.lsb = \'1\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= DOUBLE_REVERSE;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif(indication.msb = \'0\' and indication.lsb = \'1\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= NORMAL_REVERSE;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif(indication.msb = \'1\' and indication.lsb = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= REVERSE_NORMAL;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\telse\r\n')
			
			f.write(f'\t\t\t\tif (commandAux.msb = \'0\' and commandAux.lsb = \'0\' and indication.msb = \'0\' and indication.lsb = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= DOUBLE_NORMAL;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif (commandAux.msb = \'1\' and commandAux.lsb = \'1\' and indication.msb = \'1\' and indication.lsb = \'1\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= DOUBLE_REVERSE;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif (commandAux.msb = \'0\' and commandAux.lsb = \'1\' and indication.msb = \'0\' and indication.lsb = \'1\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= NORMAL_REVERSE;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif (commandAux.msb = \'1\' and commandAux.lsb = \'0\' and indication.msb = \'1\' and indication.lsb = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= REVERSE_NORMAL;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif ((commandAux.msb /= indication.msb) or (commandAux.lsb /= indication.lsb)) then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= TRANSITION;\r\n')
			f.write(f'\t\t\t\t\treset <= \'0\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')

			f.write(f'\t\t\tend if;\r\n')
			f.write(f'\t\tend if;\r\n')
			f.write(f'\tend process;\r\n') 
			
			f.write(f'\tcommand <= commandAux;\r\n')

			f.write(f'end Behavioral;') 
			f.close()  # Close header file

	def createScissorCrossing(self,index,name,data,mode, f = None,example = 1):	
		if mode == 'entity':
			node = f'scissorCrossing_{index}'
			f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
			
			# Initial comment
			self.initialComment(node,f)
			
			# Include library
			self.includeLibrary(f,True)
		
		scissorCrossing = f'scissorCrossing_{index}'
		f.write(f'\t{mode} {scissorCrossing} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		 
		commands = []
		commands_N = []
		commands_R = []
		for element in range(len(data['Routes'])):
			f.write(f'\t\t\t{data['Routes'][element]}_command : in routeCommands;\n')
			commands.append(data['Routes'][element])
			if data['Position'][element] == 'N':
				commands_N.append(data['Routes'][element])
			else:
				commands_R.append(data['Routes'][element])	

		f.write(f'\t\t\tindication : in std_logic;\n')
		f.write(f'\t\t\tcommand : out std_logic;\n')
		f.write(f'\t\t\tcorrespondence_{name} : out scissorCrossingStates;\n')
		f.write(f'\t\t\tlock_{name} : out objectLock\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend {mode} {scissorCrossing};\n')

		if mode == 'entity':
			freeState = " and ".join([f'{i}_command = RELEASE' for i in commands])
			freeState_N = " and ".join([f'{i}_command = RELEASE' for i in commands_N])
			freeState_R = " and ".join([f'{i}_command = RELEASE' for i in commands_R])
			reserveState = " or ".join([f'{i}_command = RESERVE' for i in commands])
			reserveState_N = " or ".join([f'{i}_command = RESERVE' for i in commands_N])
			reserveState_R = " or ".join([f'{i}_command = RESERVE' for i in commands_R])
			lockState = " or ".join([f'{i}_command = LOCK' for i in commands])
			lockState_N = " or ".join([f'{i}_command = LOCK' for i in commands_N])
			lockState_R = " or ".join([f'{i}_command = LOCK' for i in commands_R])

			freq = 10e6
			timeout = 7

			FF = math.ceil(math.log2(timeout*freq))

			t = [(2**(i+1))/freq for i in range(FF)]
			sequence = [0]*FF
			total = 0
			for i in range(FF-1,-1,-1):
				if total + t[i] <= timeout:
					total += t[i]
					sequence[i] = 1
			timeout_stop = " and ".join([f'Q({i}) = \'{sequence[i]}\'' for i in range(FF)])

			f.write(f'architecture Behavioral of {node} is\n')

			f.write(f'\tcomponent flipFlop is\r\n')
			f.write(f'\t\tport(\r\n')
			f.write(f'\t\t\tclock : in std_logic;\r\n')
			f.write(f'\t\t\treset : in std_logic;\r\n')
			f.write(f'\t\t\tQ : out std_logic\r\n')
			f.write(f'\t\t);\r\n')
			f.write(f'\tend component flipFlop;\r\n')

			f.write(f'\tsignal reset : std_logic := \'0\';\r\n')
			f.write(f'\tsignal Q : std_logic_vector({FF} downto 0) := (others => \'0\');\r\n')
			f.write(f'\tsignal commandState : routeCommands;\r\n')
			f.write(f'\tsignal commandAux : std_logic;\r\n')

			f.write(f'begin\n')

			f.write(f'\tgen : for i in 0 to {FF-1} generate\r\n')
			f.write(f'\t\tinst: flipFlop port map(Q(i),reset,Q(i+1));\r\n')
			f.write(f'\tend generate;\r\n')

			f.write(f'\tQ(0) <= clock;\r\n')

			f.write(f'\n\tprocess(clock)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')
			f.write(f'\t\t\tif ({freeState}) then\r\n')
			f.write(f'\t\t\t\tcommandState <= RELEASE;\r\n')
			f.write(f'\t\t\telse\r\n')
			f.write(f'\t\t\t\tif ({reserveState}) then\r\n')
			f.write(f'\t\t\t\t\tcommandState <= RESERVE;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif ({lockState}) then\r\n')
			f.write(f'\t\t\t\t\rcommandState <= LOCK;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\tend if;\r\n')
			f.write(f'\t\tend if;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(commandState)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tcase commandState is\r\n')
			f.write(f'\t\t\twhen RELEASE => -- AUTOMATIC\r\n')
			f.write(f'\t\t\t\tlock_{name} <= RELEASED;\n')
			f.write(f'\t\t\twhen RESERVE => -- DONT CHANGE\r\n')
			f.write(f'\t\t\t\tlock_{name} <= RESERVED;\n')
			f.write(f'\t\t\twhen LOCK => -- DONT CHANGE\r\n')
			f.write(f'\t\t\t\tlock_{name} <= LOCKED;\n')
			f.write(f'\t\t\twhen others =>\r\n')
			f.write(f'\t\t\t\tlock_{name} <= LOCKED;\n')
			f.write(f'\t\tend case;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(commandState)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tcase commandState is\r\n')
			f.write(f'\t\t\twhen RELEASE => -- AUTOMATIC\r\n')
			f.write(f'\t\t\t\tcommandAux <= indication;\n')
			f.write(f'\t\t\twhen RESERVE =>\r\n')
			f.write(f'\t\t\t\tif (({reserveState_N}) and ({freeState_R})) then\n')
			f.write(f'\t\t\t\t\tcommandAux <= \'0\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\t\tif (({freeState_N}) and ({reserveState_R})) then\n')
			f.write(f'\t\t\t\t\tcommandAux <= \'1\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\twhen LOCK =>\r\n')
			f.write(f'\t\t\t\tif (({lockState_N}) and ({freeState_R})) then\n')
			f.write(f'\t\t\t\t\tcommandAux <= \'0\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\t\tif (({freeState_N}) and ({lockState_R})) then\n')
			f.write(f'\t\t\t\t\tcommandAux <= \'1\';\n')
			f.write(f'\t\t\t\tend if;\n')
			f.write(f'\t\t\twhen others =>\r\n')
			f.write(f'\t\t\t\tcommandAux <= indication;\n')
			f.write(f'\t\tend case;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(clock)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')

			f.write(f'\t\t\tif({timeout_stop}) then\r\n')
			f.write(f'\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tif(indication = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= NORMAL;\r\n')
			f.write(f'\t\t\t\telse\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= REVERSE;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\telse\r\n')
			
			f.write(f'\t\t\t\tif (commandAux = \'0\' and indication = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= NORMAL;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			
			f.write(f'\t\t\t\tif (commandAux = \'1\' and indication = \'1\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= REVERSE;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')

			f.write(f'\t\t\t\tif (commandAux /= indication) then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= TRANSITION;\r\n')
			f.write(f'\t\t\t\t\treset <= \'0\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\tend if;\r\n')
			f.write(f'\t\tend if;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\tcommand <= commandAux;\r\n')
			
			f.write(f'end Behavioral;') 
			f.close()  # Close header file

	def createSignal(self,index,name,data,mode, f = None,example = 1):
		if mode == 'entity':
			node = f'railwaySignal_{index}'
			f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
			
			# Initial comment
			self.initialComment(node,f)
			
			# Include library
			self.includeLibrary(f,True)
		
		railwaySignal = f'railwaySignal_{index}'
		f.write(f'\t{mode} {railwaySignal} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')

		commands = []
		if 'Routes' in data[name]:
			for element in range(len(data[name]['Routes'])):
				f.write(f'\t\t\t{data[name]['Routes'][element]}_command : in routeCommands;\n')
				commands.append(data[name]['Routes'][element])
				#if data['Position'][element] == 'NN':
				#	commands_NN.append(data['Routes'][element])

		ocupationLevel_0,ocupationLevel_1,ocupationLevel_2,signal_0,signal_1,signal_2,switches_1,switches_2,paths = self.getSignalGraph(name,data)
		
		for path in paths:
			if 'LevelCrossings' in paths[path]:
				for i in paths[path]['LevelCrossings']:
					if i != []:
						f.write(f'\t\t\t{i}_state : in levelCrossingStates;\r\n')


		f.write(f'\t\t\t--Ocupation level 0\n')	
		f.write(f'\t\t\tocupation_{ocupationLevel_0} : in std_logic;\n')	
		f.write(f'\t\t\tcorrespondence_{signal_0} : out signalStates;\n')
		f.write(f'\t\t\tlock_{name} : out objectLock;\n')

		sw_string_1 = []
		if len(ocupationLevel_1) > 0:
			f.write(f'\t\t\t--Ocupation level 1\n')	
			for i in ocupationLevel_1:
				if i != ocupationLevel_0:
					f.write(f'\t\t\tocupation_{i} : in std_logic;\n')	
		if len(signal_1) > 0:
			for j in signal_1:
				if j != signal_0:
					f.write(f'\t\t\tcorrespondence_{j} : in signalStates;\n')
		if len(switches_1) > 0:
			for k in switches_1:
				switc_type = 'singleSwitchStates' if len(k.split('_')[1]) == 1 else ('doubleSwitchStates' if 'X' not in k.split('_')[1] else 'scissorCrossingStates')
				if f'\t\t\t{"s" if k[0].isdigit() else ""}{k.split('_')[0]}_state : in {switc_type};\n' not in sw_string_1:
					sw_string_1.append(f'\t\t\t{"s" if k[0].isdigit() else ""}{k.split('_')[0]}_state : in {switc_type};\n')
			for aux in sw_string_1:
				f.write(aux)

		sw_string_2 = []
		if len(ocupationLevel_2) > 0:
			f.write(f'\t\t\t--Ocupation level 2\n')	
			for i in ocupationLevel_2:
				if i != ocupationLevel_0 and i not in ocupationLevel_1:
					f.write(f'\t\t\tocupation_{i} : in std_logic;\n')	
		if len(signal_2) > 0:
			for j in signal_2:
				if j != signal_0 and j not in signal_1:
					f.write(f'\t\t\tcorrespondence_{j} : in signalStates;\n')
		if len(switches_2) > 0:
			for k in switches_2:
				switc_type = 'singleSwitchStates' if len(k.split('_')[1]) == 1 else ('doubleSwitchStates' if 'X' not in k.split('_')[1] else 'scissorCrossingStates')
				if f'\t\t\t{"s" if k[0].isdigit() else ""}{k.split('_')[0]}_state : in {switc_type};\n' not in sw_string_2:
					sw_string_2.append(f'\t\t\t{"s" if k[0].isdigit() else ""}{k.split('_')[0]}_state : in {switc_type};\n')
			for aux in sw_string_2:
				if sw_string_1 == []:
					f.write(aux)
				else:	
					if aux not in sw_string_1:
						f.write(aux)

		f.write(f'\t\t\tindication : in signal_type;\n')
		f.write(f'\t\t\tcommand : out signal_type\n')
		
		f.write(f'\t\t);\n')
		f.write(f'\tend {mode} {railwaySignal};\n')

		if mode == 'entity':
			print(f'{name}')
			for path in paths:
				print(f'\t{paths[path]}')	

			freeState = " and ".join([f'{i}_command = RELEASE' for i in commands])
			reserveState = " or ".join([f'{i}_command = RESERVE' for i in commands])
			lockState = " or ".join([f'{i}_command = LOCK' for i in commands])

			freq = 10e6
			timeout = 7

			FF = math.ceil(math.log2(timeout*freq))

			t = [(2**(i+1))/freq for i in range(FF)]
			sequence = [0]*FF
			total = 0
			for i in range(FF-1,-1,-1):
				if total + t[i] <= timeout:
					total += t[i]
					sequence[i] = 1
			timeout_stop = " and ".join([f'Q({i}) = \'{sequence[i]}\'' for i in range(FF)])

			f.write(f'architecture Behavioral of {node} is\r\n')

			f.write(f'\tcomponent flipFlop is\r\n')
			f.write(f'\t\tport(\r\n')
			f.write(f'\t\t\tclock : in std_logic;\r\n')
			f.write(f'\t\t\treset : in std_logic;\r\n')
			f.write(f'\t\t\tQ : out std_logic\r\n')
			f.write(f'\t\t);\r\n')
			f.write(f'\tend component flipFlop;\r\n')

			f.write(f'\tsignal reset : std_logic := \'0\';\r\n')
			f.write(f'\tsignal Q : std_logic_vector({FF} downto 0) := (others => \'0\');\r\n')
			f.write(f'\tsignal commandState : routeCommands;\r\n')
			f.write(f'\tsignal aspectState : signalStates;\r\n')
			f.write(f'\tsignal commandAux : signal_type;\r\n')
			f.write(f'\tsignal path : integer := 0;\r\n')

			f.write(f'begin\r\n')
			
			if commands != []:
				f.write(f'\n\tprocess(clock)\r\n')
				f.write(f'\tbegin\r\n')
				f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')
				f.write(f'\t\t\tif ({freeState}) then\r\n')
				f.write(f'\t\t\t\tcommandState <= RELEASE;\r\n')
				f.write(f'\t\t\telse\r\n')
				f.write(f'\t\t\t\tif ({reserveState}) then\r\n')
				f.write(f'\t\t\t\t\tcommandState <= RESERVE;\r\n')
				f.write(f'\t\t\t\tend if;\r\n')
				f.write(f'\t\t\t\tif ({lockState}) then\r\n')
				f.write(f'\t\t\t\t\tcommandState <= LOCK;\r\n')
				f.write(f'\t\t\t\tend if;\r\n')
				f.write(f'\t\t\tend if;\r\n')
				f.write(f'\t\tend if;\r\n')
				f.write(f'\tend process;\r\n') 

				f.write(f'\n\tprocess(commandState)\r\n')
				f.write(f'\tbegin\r\n')
				f.write(f'\t\tcase commandState is\r\n')
				f.write(f'\t\t\twhen RELEASE => -- AUTOMATIC\r\n')
				f.write(f'\t\t\t\tlock_{name} <= RELEASED;\n')
				f.write(f'\t\t\twhen RESERVE => -- DONT CHANGE\r\n')
				f.write(f'\t\t\t\tlock_{name} <= RESERVED;\n')
				f.write(f'\t\t\twhen LOCK => -- DONT CHANGE\r\n')
				f.write(f'\t\t\t\tlock_{name} <= LOCKED;\n')
				f.write(f'\t\t\twhen others =>\r\n')
				f.write(f'\t\t\t\tlock_{name} <= LOCKED;\n')
				f.write(f'\t\tend case;\r\n')
				f.write(f'\tend process;\r\n') 
			else:
				f.write(f'\tlock_{name} <= LOCKED;\n')

			if paths != {}:
				f.write(f'\n\tprocess(commandState)\r\n')
				f.write(f'\tbegin\r\n')
				f.write(f'\t\tcase commandState is\r\n')
				f.write(f'\t\t\twhen RELEASE | LOCK =>\r\n')

				sw_conditions = []
				lc_conditions = []
				sw_dict = {'N':'NORMAL','R':'REVERSE','NN':'DOUBLE_NORMAL','RR':'DOUBLE_REVERSE','RN':'REVERSE_NORMAL','NR':'NORMAL_REVERSE','XN':'NORMAL','XR':'REVERSE'}
				for path in paths:
					if 'Switches' in paths[path]:
						sw_conditions.append(" and ".join(f'{x.split('_')[0]}_state = {sw_dict[x.split('_')[1]]}' for x in paths[path]['Switches']))
				for path in paths:
					if 'LevelCrossings' in paths[path] and paths[path]['LevelCrossings'] != []:
						lc_conditions.append(" and ".join(f'{x}_state = DOWN' for x in paths[path]['LevelCrossings'] if x != None))
					else:
						lc_conditions.append(None)

				#f.write(f'{sw_conditions} {lc_conditions}\r\n')			

				main_conditions = [f"{x} and {y}" if x is not '' and y is not None else x or y for x, y in zip(sw_conditions, lc_conditions)]

				#f.write(f'{main_conditions}\r\n')

				if main_conditions != [None]:
					f.write(f'\t\t\t\tif ({" or ".join([f"({main_condition})" for main_condition in main_conditions])}) then\r\n')

					for condition in range(len(main_conditions)):	
						conditions = main_conditions[condition]
						#if 'LevelCrossings' in paths[sw_condition+1] and paths[sw_condition+1]['LevelCrossings'] != []:
						#	lc_condition = " and ".join(f'{x}_state = DOWN' for x in paths[sw_condition+1]['LevelCrossings'] if x != [])
						#	conditions = conditions + f' and ({lc_condition})'	
							
						f.write(f'\t\t\t\t\tif ({conditions}) then\r\n')
						f.write(f'\t\t\t\t\t\tpath <= {condition+1};\n')
						f.write(f'\t\t\t\t\tend if;\r\n')		
				else:
					f.write(f'\t\t\t\tpath <= 1;\n')

				if main_conditions != [None]:
					f.write(f'\t\t\t\telse\r\n')
					f.write(f'\t\t\t\t\tpath <= 0;\n')
					f.write(f'\t\t\t\tend if;\r\n')

				f.write(f'\t\t\twhen RESERVE =>\r\n')
				f.write(f'\t\t\t\tpath <= 0;\n')				
				f.write(f'\t\t\twhen others =>\r\n')
				f.write(f'\t\t\t\tpath <= 0;\n')
				f.write(f'\t\tend case;\r\n')
				f.write(f'\tend process;\r\n') 
			else:
				if name[0] == 'T':
					f.write(f'\taspectState <= RED;\r\n')
				if name[0] == 'L':
					f.write(f'\taspectState <= DOUBLE_YELLOW;\r\n')
			
			if paths != {}:
				f.write(f'\n\tprocess(clock)\r\n')
				f.write(f'\tbegin\r\n')
				f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')

				f.write(f'\t\t\tcase path is\r\n')
				f.write(f'\t\t\t\twhen 0 =>\r\n')
				f.write(f'\t\t\t\t\taspectState <= RED;\r\n')
				for i in range(len(paths)):
					f.write(f'\t\t\t\twhen {i+1} =>\r\n')
				
					
					if 'Share' not in paths[path]:
						conditions = " or ".join(f'ocupation_{x} = \'0\'' for x in paths[i+1]['Subpath'])
						f.write(f'\t\t\t\t\tif ({conditions}) then\r\n')
						f.write(f'\t\t\t\t\t\taspectState <= RED;\r\n')
						# ELSE!!!
						f.write(f'\t\t\t\t\tend if;\r\n')
					else:
						f.write(f'\t\t\t\t\tif (OTRA COSA) then\r\n')

					#if 'Path' in paths[i+1]:
					#	fullPath = paths[i+1]['Path'][1:]
					#	stop = data[paths[i+1]['Signals'][-1]]['Start']
						
					#	subPath = [j for j in fullPath if (fullPath.index(j) < fullPath.index(stop) if stop in fullPath else len(fullPath))]

					#	conditions = " or ".join(f'ocupation_{x} = \'0\'' for x in subPath)


					#f.write(f'\t\t\t\t\tif ({conditions}) then\r\n')
					#f.write(f'\t\t\t\t\t\taspectState <= RED;\r\n')
					#f.write(f'\t\t\t\t\telse\r\n')

					#f.write(f'\t\t\t\t\tend if;\r\n')

				f.write(f'\t\t\t\twhen others =>\r\n')
				
				f.write(f'\t\t\tend case;\r\n')
		
				f.write(f'\t\tend if;\r\n')
				f.write(f'\tend process;\r\n') 
			

			'''
			If ocupado
				aspectState <= RED
			else
				if vecino ocupado
					aspectState <= DOUBLE_YELLOW
				else
					if vecino RED
						aspectState <= DOUBLE_YELLOW
					if vecino DOUBLE_YELLOW
						aspectState <= YELLOW
					if vecino YELLOW
						aspectState <= GREEN
			'''
			

			#f.write(f'\t\t\t\t\tif (ocupation_{ocupationLevel_0} = \'0\') then\r\n')
			#f.write(f'\t\t\t\t\taspectState <= RED;\r\n')
			#f.write(f'\t\t\ttend if;\r\n')










			f.write(f'\n\tprocess(clock)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')

			f.write(f'\t\t\tif({timeout_stop}) then\r\n')
			f.write(f'\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tif(indication.msb = \'0\' and indication.lsb = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= RED;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif(indication.msb = \'1\' and indication.lsb = \'1\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= GREEN;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif(indication.msb = \'0\' and indication.lsb = \'1\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= DOUBLE_YELLOW;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif(indication.msb = \'1\' and indication.lsb = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= YELLOW;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\telse\r\n')
			
			f.write(f'\t\t\t\tif (commandAux.msb = \'0\' and commandAux.lsb = \'0\' and indication.msb = \'0\' and indication.lsb = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= RED;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif (commandAux.msb = \'1\' and commandAux.lsb = \'1\' and indication.msb = \'1\' and indication.lsb = \'1\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= GREEN;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif (commandAux.msb = \'0\' and commandAux.lsb = \'1\' and indication.msb = \'0\' and indication.lsb = \'1\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= DOUBLE_YELLOW;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif (commandAux.msb = \'1\' and commandAux.lsb = \'0\' and indication.msb = \'1\' and indication.lsb = \'0\') then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= YELLOW;\r\n')
			f.write(f'\t\t\t\t\treset <= \'1\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif ((commandAux.msb /= indication.msb) or (commandAux.lsb /= indication.lsb)) then\r\n')
			f.write(f'\t\t\t\t\tcorrespondence_{name} <= RED;\r\n')
			f.write(f'\t\t\t\t\treset <= \'0\';\r\n')
			f.write(f'\t\t\t\tend if;\r\n')

			f.write(f'\t\t\tend if;\r\n')
			f.write(f'\t\tend if;\r\n')
			f.write(f'\tend process;\r\n')  


			f.write(f'\n\tprocess(aspectState)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tcase aspectState is\r\n')
			f.write(f'\t\t\twhen RED =>\r\n')
			f.write(f'\t\t\t\tcommandAux.msb <= \'0\';\r\n')
			f.write(f'\t\t\t\tcommandAux.lsb <= \'0\';\r\n')
			f.write(f'\t\t\twhen DOUBLE_YELLOW =>\r\n')
			f.write(f'\t\t\t\tcommandAux.msb <= \'0\';\r\n')
			f.write(f'\t\t\t\tcommandAux.lsb <= \'1\';\r\n')
			f.write(f'\t\t\twhen YELLOW =>\r\n')
			f.write(f'\t\t\t\tcommandAux.msb <= \'1\';\r\n')
			f.write(f'\t\t\t\tcommandAux.lsb <= \'0\';\r\n')
			f.write(f'\t\t\twhen GREEN =>\r\n')
			f.write(f'\t\t\t\tcommandAux.msb <= \'1\';\r\n')
			f.write(f'\t\t\t\tcommandAux.lsb <= \'1\';\r\n')
			f.write(f'\t\t\twhen others =>\r\n')
			f.write(f'\t\t\t\tcommandAux.msb <= \'0\';\r\n')
			f.write(f'\t\t\t\tcommandAux.lsb <= \'0\';\r\n')
			f.write(f'\t\tend case;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\tcommand <= commandAux;\r\n')
			
			f.write(f'end Behavioral;') 
			f.close()  # Close header file
		
	def getSignalGraph(self,name,data):
		ocupationLevel_0 = data[name]['Start']
		signal_0 = name

		paths = {}
		ocupationLevel_1 = []
		subLevel_order = []
		signal_1 = []
		switches_1 = []
		sub_switch_order = []
		# level 1
		if 'Path' in data[name]:
			subLevel = [item for sublist in data[name]['Path'] for item in sublist]
			for item in subLevel:
				if item not in subLevel_order:
					subLevel_order.append(item)
			for i in subLevel_order:
				if i not in ocupationLevel_1:
					ocupationLevel_1.append(i)
			for j in data[name]['Next']:
				if j not in signal_1:
					signal_1.append(j)

			sub_switch = [item for sublist in data[name]['Switches'] for item in sublist]	

			path = 0
			if data[name]['Switches'] != []:
				for i in range(len(data[name]['Switches'])):
					if 'Next' in data[name]:
						next = data[name]['Next'][i]
						net = data[name]['Path'][i]
		
						if 'Switches' in data[next] and data[next]['Switches'] != []:
							for j in range(len(data[next]['Switches'])):
								path = path + 1
								#print(f'{path} {data[name]['Switches'][i]} {data[next]['Switches'][j]}')
								paths[path] = {'Switches':[],'Path':[],'LevelCrossings':[],'Signals':[]}
								for k in data[name]['Switches'][i]:
									paths[path]['Switches'].append(k)
								paths[path]['Path'].append(data[name]['Start'])
								paths[path]['Signals'].append(signal_0)
								paths[path]['Signals'].append(next)
								paths[path]['Signals'].append(data[next]['Next'][j])
					
								for k in net:
									paths[path]['Path'].append(k)
								for k in data[next]['Switches'][j]:
									paths[path]['Switches'].append(k)

								if 'LevelCrossings' in data[name]:
									for k in data[name]['LevelCrossings'][i]:
										if k != []:
											paths[path]['LevelCrossings'].append(k)

								for k in data[next]['Path'][j]:
									paths[path]['Path'].append(k)
						else:
							path = path +1
							#print(f'{path} {data[name]['Switches'][i]}')
							paths[path] = {'Switches':[],'Path':[],'LevelCrossings':[],'Signals':[]}
							for k in data[name]['Switches'][i]:
								paths[path]['Switches'].append(k)
							paths[path]['Path'].append(data[name]['Start'])
							paths[path]['Signals'].append(signal_0)
							paths[path]['Signals'].append(next)
							
							if 'Next' in data[next]:
								paths[path]['Signals'].append(data[next]['Next'][0])
							
							if 'LevelCrossings' in data[name]:
								for k in data[name]['LevelCrossings']:
									for n in k:
										if n != []:
											paths[path]['LevelCrossings'].append(n)

							if 'LevelCrossings' in data[next]:
								for k in data[next]['LevelCrossings']:
									for n in k:
										if n != []:
											paths[path]['LevelCrossings'].append(n)

							for k in net:
								paths[path]['Path'].append(k)
			else:
				if 'Next' in data[name]:
					path = path + 1		
					paths[path] = {'Switches':[],'Path':[],'LevelCrossings':[],'Signals':[]}
					
					next = data[name]['Next'][0]
					
					paths[path]['Path'].append(data[name]['Start'])
					
					if 'LevelCrossings' in data[name]:
						for i in data[name]['LevelCrossings'][0]:
							if i != []:
								paths[path]['LevelCrossings'].append(i)

					paths[path]['Signals'].append(name)
					paths[path]['Signals'].append(next)
					
					if 'Switches' in data[next]:
						for i in range(len(data[next]['Switches'])):
							paths[path+i] = paths[path]	
							paths[path+i]['Signals'].append(data[next]['Next'][i])
							for j in data[next]['Switches'][i]:
								paths[path+i]['Switches'].append(j)
							for j in data[next]['Path'][i]:
								paths[path+i]['Path'].append(j)
							for j in data[next]['LevelCrossings'][i]:
								paths[path+i]['LevelCrossings'].append(j)

			for item in sub_switch:
				if item not in sub_switch_order:
					sub_switch_order.append(item)
			for i in sub_switch_order:
				if i not in switches_1:
					switches_1.append(i)

		for path in paths:
			if 'Path' in paths[path]:
				paths[path]['Subpath'] = paths[path]['Path'][1:]
			if paths[path]['Path'][0] == data[paths[path]['Signals'][1]]['Start']:
				paths[path]['Share'] = True

		#print(f'{name}')
		#for path in paths:
		#	print(f'\t{path} {paths[path]}')	

		ocupationLevel_2 = []
		signal_2 = []
		switches_2 = []
		sub_switch_order = []
		# level 2
		if 'Next' in data[name]:
			for next in data[name]['Next']:
				if data[next]['Start'] not in ocupationLevel_2:
					ocupationLevel_2.append(data[next]['Start'])
				if 'Path' in data[next]:
					sub_level = list(set([item for sublist in data[next]['Path'] for item in sublist]))
					for i in sub_level:
						if i not in ocupationLevel_2:
							ocupationLevel_2.append(i)
					for j in data[next]['Next']:
						if j not in signal_2:
							signal_2.append(j)

				if 'Switches' in data[next]:
					sub_switch = [item for sublist in data[next]['Switches'] for item in sublist]	
					for item in sub_switch:
						if item not in sub_switch_order:
							sub_switch_order.append(item)
					for i in sub_switch_order:
						if i not in switches_2:
							switches_2.append(i)

		#print(f'{name} {ocupationLevel_0} {[i for i in ocupationLevel_1 if i not in ocupationLevel_0]} {[i for i in ocupationLevel_2 if i not in ocupationLevel_1 if i != ocupationLevel_0]} | {signal_0} {signal_1} {signal_2} | {switches_1} {switches_2}')	
							
		return ocupationLevel_0,[i for i in ocupationLevel_1 if i != ocupationLevel_0],[i for i in ocupationLevel_2 if i not in ocupationLevel_1],signal_0,signal_1,signal_2,switches_1,switches_2,paths

	def createNode(self,index,nodeId,routes,mode, f = None,example = 1):
		if mode == 'entity':
			node = f'node_{index}'
			f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
			
			# Initial comment
			self.initialComment(node,f)
			
			# Include library
			self.includeLibrary(f,True)
		
		node = f'node_{index}'
		f.write(f'\t{mode} {node} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tocupation : in std_logic;\n')
	
		commands = []
		for route in routes:
			if nodeId in routes[route]['Path']:
				f.write(f'\t\t\tR{route}_command : in routeCommands;\n')	
				commands.append(f'R{route}')

		f.write(f'\t\t\tstate : out nodeStates;\n')
		f.write(f'\t\t\tlocking : out objectLock\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend {mode} {node};\n')

		if mode == 'entity':
			freeState = " and ".join([f'{i}_command = RELEASE' for i in commands])
			reserveState = " or ".join([f'{i}_command = RESERVE' for i in commands])
			lockState = " or ".join([f'{i}_command = LOCK' for i in commands])

			f.write(f'architecture Behavioral of {node} is\r\n')

			f.write(f'\tsignal commandState : routeCommands;\r\n')

			f.write(f'begin\r\n')

			f.write(f'\n\tprocess(clock)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')
			f.write(f'\t\t\tif ({freeState}) then\r\n')
			f.write(f'\t\t\t\tcommandState <= RELEASE;\r\n')
			f.write(f'\t\t\telse\r\n')
			f.write(f'\t\t\t\tif ({reserveState}) then\r\n')
			f.write(f'\t\t\t\t\tcommandState <= RESERVE;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\t\tif ({lockState}) then\r\n')
			f.write(f'\t\t\t\t\rcommandState <= LOCK;\r\n')
			f.write(f'\t\t\t\tend if;\r\n')
			f.write(f'\t\t\tend if;\r\n')
			f.write(f'\t\tend if;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(commandState)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tcase commandState is\r\n')
			f.write(f'\t\t\twhen RELEASE => -- AUTOMATIC\r\n')
			f.write(f'\t\t\t\tlocking <= RELEASED;\n')
			f.write(f'\t\t\twhen RESERVE => -- DONT CHANGE\r\n')
			f.write(f'\t\t\t\tlocking <= RESERVED;\n')
			f.write(f'\t\t\twhen LOCK => -- DONT CHANGE\r\n')
			f.write(f'\t\t\t\tlocking <= LOCKED;\n')
			f.write(f'\t\t\twhen others =>\r\n')
			f.write(f'\t\t\t\tlocking <= LOCKED;\n')
			f.write(f'\t\tend case;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'\n\tprocess(clock)\r\n')
			f.write(f'\tbegin\r\n')
			f.write(f'\t\tif (clock = \'1\' and clock\'Event) then\r\n')
			f.write(f'\t\t\tif (ocupation = \'1\') then\r\n')
			f.write(f'\t\t\t\tstate <= FREE;\r\n')
			f.write(f'\t\t\telse\r\n')
			f.write(f'\t\t\t\tstate <= OCCUPIED;\r\n')
			f.write(f'\t\t\tend if;\r\n')
			f.write(f'\t\tend if;\r\n')
			f.write(f'\tend process;\r\n') 

			f.write(f'end Behavioral;') 
			f.close()  # Close header file

	def createRoute(self,index,route,mode, f = None,example = 1):
		if mode == 'entity':
			node = f'route_{index}'
			f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
			
			# Initial comment
			self.initialComment(node,f)
			
			# Include library
			self.includeLibrary(f,True)
		
		node = f'route_{index}'
		f.write(f'\t{mode} {node} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\trouteRequest : in std_logic;\n')
	
		for netElement in route['Path']:
			f.write(f'\t\t\t{netElement}_state : in nodeStates;\r\n')
			f.write(f'\t\t\t{netElement}_lock : in objectLock;\n')
			f.write(f'\t\t\t{netElement}_command : out routeCommands;\r\n')	

		for levelCrossing in route['LevelCrossings']:
			f.write(f'\t\t\t{levelCrossing}_state : in levelCrossingStates;\r\n')
			f.write(f'\t\t\t{levelCrossing}_lock : in objectLock;\r\n')
			f.write(f'\t\t\t{levelCrossing}_command : out routeCommands;\r\n')	

		for switches in route['Switches']:
			switch_aux = switches.split('_')
			if len(switch_aux[1]) == 1:
				f.write(f'\t\t\t{"s" if switch_aux[0][0].isdigit() else ""}{switch_aux[0]}_state : in singleSwitchStates;\r\n')
				f.write(f'\t\t\t{"s" if switch_aux[0][0].isdigit() else ""}{switch_aux[0]}_lock : in objectLock;\r\n')
				f.write(f'\t\t\t{"s" if switch_aux[0][0].isdigit() else ""}{switch_aux[0]}_command : out routeCommands;\r\n')	
			if len(switch_aux[1]) == 2:
				f.write(f'\t\t\t{"s" if switch_aux[0][0].isdigit() else ""}{switch_aux[0]}_state : in doubleSwitchStates;\r\n')
				f.write(f'\t\t\t{"s" if switch_aux[0][0].isdigit() else ""}{switch_aux[0]}_lock : in objectLock;\r\n')
				f.write(f'\t\t\t{"s" if switch_aux[0][0].isdigit() else ""}{switch_aux[0]}_command : out routeCommands;\r\n')

		for scissorCrossings in route['ScissorCrossings']:
			scissor_aux = scissorCrossings.split('_')
			f.write(f'\t\t\t{"s" if scissor_aux[0][0].isdigit() else ""}{scissor_aux[0]}_state : in scissorCrossingStates;\r\n')
			f.write(f'\t\t\t{"s" if scissor_aux[0][0].isdigit() else ""}{scissor_aux[0]}_lock : in objectLock;\r\n')
			f.write(f'\t\t\t{"s" if scissor_aux[0][0].isdigit() else ""}{scissor_aux[0]}_command : out routeCommands;\r\n')	

		f.write(f'\t\t\t{route['Start']}_state : in signalStates;\r\n')
		f.write(f'\t\t\t{route['Start']}_lock : in objectLock;\r\n')
		f.write(f'\t\t\t{route['Start']}_command : out routeCommands;\r\n')	

		f.write(f'\t\t\t{route['End']}_state : in signalStates;\r\n')
		#f.write(f'\t\t\t{route['End']}_command : out routeCommands;\r\n')	

		f.write(f'\t\t\trouteState : out std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend {mode} {node};\n')

		if mode == 'entity':
			f.write(f'architecture Behavioral of {node} is\r\n')
			f.write(f'begin\r\n')

			f.write(f'\trouteState <= \'0\';\r\n')

			f.write(f'end Behavioral;') 
			f.close()  # Close header file
    		
	def createPrinter(self,M,example = 1):
		node = 'printer'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
			
		# printer entity
		printer = 'printer'
		f.write(f'\tentity {printer} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tprocessing : in std_logic;\n')
		f.write(f'\t\t\tprocessed : out std_logic;\n')
		f.write(f'\t\t\tpacket_i : in std_logic_vector({str(M)}-1 downto 0);\n')
		f.write(f'\t\t\tw_data : out std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\twr_uart : out std_logic; -- \'char_disp\'\n')
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {printer};\r\n') 
	
		f.write(f'architecture Behavioral of {printer} is\r\n') 

		f.write(f'\ttype states_t is (RESTART,CYCLE_1,CYCLE_2);\n') 
		f.write(f'\tsignal state, next_state : states_t;\n') 
		f.write(f'\tsignal mux_out_s,ena_s,rst_s,reg_aux : std_logic;\n') 
		f.write(f'\tsignal mux_s : std_logic_vector({str(math.ceil(np.log2(M+1)))}-1 downto 0);\r\n')  ### TODO:
	
		f.write(f'begin\r\n')
		
		f.write(f'\tcontador : process(clock)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (clock = \'1\' and clock\'event) then\n')
		f.write(f'\t\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\t\tmux_s <= "{str('0'*math.ceil(np.log2(M+1)))}";\n')               ### TODO:
		f.write(f'\t\t\telse\n')
		f.write(f'\t\t\t\tif (ena_s = \'1\') then\n')        
		f.write(f'\t\t\t\t\tif (mux_s /= "{'{0:b}'.format(M)}") then\n')     ### TODO:
		f.write(f'\t\t\t\t\t\tif (state = CYCLE_1 or state = CYCLE_2) then\n')
		f.write(f'\t\t\t\t\t\t\tmux_s <= std_logic_vector(to_unsigned(to_integer(unsigned(mux_s)) + 1 , {str(math.ceil(np.log2(M+1)))}));\n')     ### TODO:     
		f.write(f'\t\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\t\tif (processing = \'0\') then\n')
		f.write(f'\t\t\t\t\tmux_s <= "{str('0'*math.ceil(np.log2(M+1)))}";\n')             ### TODO:
		f.write(f'\t\t\t\tend if;\n')             
		f.write(f'\t\t\tend if;\n') 
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
		
		f.write(f'\tmultiplexor : process(packet_i,mux_s)\n')
		f.write(f'\tbegin\n')
		f.write(f'\t\tcase mux_s is\n')
		
		for i in range(M):
			f.write(f'\t\t\twhen "{str(bin(i))[2:].zfill(math.ceil(np.log2(M+1)))}" => mux_out_s <= packet_i({str(i)});\n')

		f.write(f'\t\t\twhen others => mux_out_s <= \'0\';\n')
		f.write(f'\t\tend case;\n')     
		f.write(f'\tend process;\r\n')   
					
		f.write(f'\tw_data <= "00110001" when mux_out_s = \'1\' else "00110000";\r\n')

		f.write(f'\tFSM_reset : process(clock)\n') 
		f.write(f'\tbegin\n') 
		f.write(f'\t\tif (clock = \'1\' and clock\'event) then\n') 
		f.write(f'\t\t\tif reset = \'1\' then\n') 
		f.write(f'\t\t\t\tstate <= RESTART;\n')           
		f.write(f'\t\t\telse\n')                  
		f.write(f'\t\t\t\tif (processing = \'1\') then\n')           
		f.write(f'\t\t\t\t\tstate <= next_state;\n') 
		f.write(f'\t\t\t\telse\n') 
		f.write(f'\t\t\t\t\tstate <= RESTART;\n') 
		f.write(f'\t\t\t\tend if;\n') 
		f.write(f'\t\t\tend if;\n')  
		f.write(f'\t\tend if;\n') 
		f.write(f'\tend process;\r\n') 
		
		f.write(f'\tFSM : process(processing,state,mux_s)\n') 
		f.write(f'\tbegin\n') 
		f.write(f'\t\tnext_state <= state;\n')    
		f.write(f'\t\tcase state is\n') 
		f.write(f'\t\t\twhen RESTART =>\n') 
		f.write(f'\t\t\t\twr_uart <= \'0\';\n') 
		f.write(f'\t\t\t\trst_s <= \'1\';\n') 
		f.write(f'\t\t\t\tena_s <= \'0\';\n') 
		f.write(f'\t\t\t\tprocessed <= \'0\';\n') 
		f.write(f'\t\t\t\treg_aux <= \'0\';\n')  
		f.write(f'\t\t\t\tif (processing = \'1\' and mux_s /= "{'{0:b}'.format(M)}" ) then\n') 
		f.write(f'\t\t\t\t\tnext_state <= CYCLE_1;\n') 
		f.write(f'\t\t\t\tend if;\n') 
		f.write(f'\t\t\twhen CYCLE_1 =>\n') 
		f.write(f'\t\t\t\twr_uart <= \'0\';\n') 
		f.write(f'\t\t\t\trst_s <= \'0\';\n') 
		f.write(f'\t\t\t\tena_s <= \'0\';\n') 
		f.write(f'\t\t\t\t--processed <= \'0\';\n')                
		f.write(f'\t\t\t\tnext_state <= CYCLE_2;\n')              
		f.write(f'\t\t\twhen CYCLE_2 =>\n') 
		f.write(f'\t\t\t\twr_uart <= \'1\';\n') 
		f.write(f'\t\t\t\trst_s <= \'0\';\n') 
		f.write(f'\t\t\t\tena_s <= \'1\';\n')               
		f.write(f'\t\t\t\tprocessed <= \'0\';\n') 
		f.write(f'\t\t\t\treg_aux <= \'0\';\n')          
		f.write(f'\t\t\t\tif mux_s = "{'{0:b}'.format(M-1)}" then\n') 
		f.write(f'\t\t\t\t\tprocessed <= \'1\';\n') 
		f.write(f'\t\t\t\t\treg_aux <= \'1\';\n') 
		f.write(f'\t\t\t\t\tnext_state <= RESTART;\n')            
		f.write(f'\t\t\t\telse\n') 
		f.write(f'\t\t\t\t\tnext_state <= CYCLE_1;\n') 
		f.write(f'\t\t\t\tend if;\n') 
		f.write(f'\t\t\twhen others => null;\n') 
		f.write(f'\t\tend case;\n') 
		f.write(f'\tend process;\r\n') 
			
		f.write(f'end Behavioral;') 
		
		f.close()  # Close header file

	def createSelector(self,example = 1):
		
		node = 'selector'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
			
		# selector entity
		selector = "selector"
		f.write(f'\tentity {selector} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tselector : in std_logic;\n')
		f.write(f'\t\t\tleds : out std_logic_vector(2-1 downto 0);\n')
		f.write(f'\t\t\twr_uart_1 : in std_logic;\n')
		f.write(f'\t\t\twr_uart_2 : in std_logic;\n')
		f.write(f'\t\t\twr_uart_3 : out std_logic;\n')
		f.write(f'\t\t\tw_data_1 : in std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\tw_data_2 : in std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\tw_data_3 : out std_logic_vector(8-1 downto 0);\n')
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {selector};\r\n') 
	
		f.write(f'architecture Behavioral of {selector} is\r\n')            
		
		f.write(f'\tsignal disp_aux : std_logic_vector(8-1 downto 0);\r\n') 
	
		f.write(f'begin\r\n')
		
		f.write(f'\tselectors : process(clock)\n')   
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (clock = \'1\' and clock\'event) then\n')
		f.write(f'\t\t\tif reset = \'1\' then\n')
		f.write(f'\t\t\t\tw_data_3 <= "00000000";\n')
		f.write(f'\t\t\t\twr_uart_3 <= \'0\';\n')
		f.write(f'\t\t\telse\n') 
		f.write(f'\t\t\t\tif selector = \'1\' then\n')                                    
		f.write(f'\t\t\t\t\tdisp_aux <= w_data_2;\n')                  
		f.write(f'\t\t\t\t\tw_data_3 <= disp_aux;\n')                               
		f.write(f'\t\t\t\t\twr_uart_3 <= wr_uart_2;\n')                            
		f.write(f'\t\t\t\t\t--leds <= \'10\';\n')
		f.write(f'\t\t\t\telse\n')         
		f.write(f'\t\t\t\t\tdisp_aux <= w_data_1;\n')                   
		f.write(f'\t\t\t\t\tw_data_3 <= disp_aux;\n')                               
		f.write(f'\t\t\t\t\twr_uart_3 <= wr_uart_1;\n')
		f.write(f'\t\t\t\t\t--leds <= \'01\';\n')
		f.write(f'\t\t\t\tend if;\n')
		f.write(f'\t\t\tend if;\n')
		f.write(f'\t\tend if;\n')
		f.write(f'\tend process;\r\n')
			
		f.write(f'end Behavioral;') 
		
		f.close()  # Close header file   
	
	def createFlipFlop(self,example):
		node = 'flipFlop'
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
			
		# flipFlop entity
		flipFlop = "flipFlop"
		f.write(f'\tentity {flipFlop} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\treset : in std_logic;\n')
		f.write(f'\t\t\tQ : out std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {flipFlop};\r\n') 
	
		f.write(f'architecture Behavioral of {flipFlop} is\r\n')            
		
		f.write(f'\tsignal Q_aux : std_logic;\r\n') 
	
		f.write(f'begin\r\n')
		
		f.write(f'\tflip_flop : process(clock)\n')   
		f.write(f'\tbegin\n')
		f.write(f'\t\tif (reset = \'1\') then\n')
		f.write(f'\t\t\tQ_aux <= \'0\';\n')
		f.write(f'\t\telsif(rising_edge(clock)) then\n')
		f.write(f'\t\t\tQ_aux <= not Q_aux;\n')
		f.write(f'\t\tend if;\n') 
		f.write(f'\tend process;\r\n')
		f.write(f'\tQ <= Q_aux;\r\n')	
		f.write(f'end Behavioral;') 
		
		f.close()  # Close header file

	def __init__(self,RML,routes,example = 1):
		print("#"*50+' Reading railML object '+"#"*50)
		
		network = self.create_graph_structure(RML,example)
		self.print_network(network)
		
		n_routes = len(routes)
		#for route in routes:
		#	print('R'+str(route),routes[route])

		# Enable to plot graph
		#self.create_graph(RML,network,example)

		# Calculate N and M
		N,M,n_netElements,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings,n_signals_1,n_signals_2,n_signals_3 = self.calculate_parameters(network)
		N = N + n_routes
		M = M + n_routes
		print(f'N : {N}\nM : {M}')

		n_signals = n_signals_1 + n_signals_2 + n_signals_3

		print("#"*30+' Creating VHDL files '+"#"*30)
		
		print(f'Creating package ... ',end='')
		self.createPacket(n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings,n_signals,example)
		print(f'Done')
		
		print(f'Creating global wrapper ... ',end='')
		self.createGlobal(N,M,example)
		print(f'Done')
		
		print(f'Creating UARTs ... ',end='')
		self.createUARTs(N,M,example)
		print(f'Done')

		print(f'Creating system ... ',end='')
		self.createSystem(N,M,example)
		print(f'Done')
		
		print(f'Creating detector ... ',end='')
		self.createDetector(N,example)
		print(f'Done')
		
		print(f'Creating interlocking ... ',end='')
		self.createInterlocking(N,M,n_netElements,n_routes,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings,n_signals,example)
		print(f'Done')
		
		print(f'Creating splitter ... ',end='')
		self.createSplitter(N,n_netElements,n_routes,n_signals,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings,example)
		print(f'Done')
		
		print(f'Creating mediator ... ',end='')
		self.createMediator(N,M,n_netElements,n_routes,n_signals,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings,example)
		print(f'Done')
		
		print(f'Creating network ... ',end='')
		self.createNetwork(network,routes,N,n_netElements,n_signals,n_switches,n_doubleSwitch,n_scissorCrossings,n_levelCrossings,example)
		print(f'Done')
	
		print(f'Creating printer ... ',end='')
		self.createPrinter(M,example)
		print(f'Done')
		
		print(f'Creating selector ... ',end='')
		self.createSelector(example)
		print(f'Done')
		
		print(f'Creating timers ... ',end='')
		self.createFlipFlop(example)
		print(f'Done')

		print("#"*30+' VHDL files Created '+"#"*30)