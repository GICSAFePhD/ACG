import sys
sys.path.append('.')

import numpy as np
import networkx as nx
import graphviz as gv

class ACG():
	def create_graph_structure(self,RML,example = 1):

		NetElements =       RML.Infrastructure.Topology.NetElements
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

		n_netElements = len(network)
		n_switches = 0
		n_doubleSwitch = 0
		n_borders = 0
		n_buffers = 0
		n_levelCrossings = 0
		n_platforms = 0
		n_crossings = 0
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
				n_switches = n_switches + 1

			if 'Switch_X' in network[element]:
				n_doubleSwitch = n_doubleSwitch + 1
				
			if 'Border' in network[element]:
				n_borders = n_borders + 1

			if 'BufferStop' in network[element]:
				n_buffers = n_buffers + 1

			if 'LevelCrossing' in network[element]:
				n_levelCrossings = n_levelCrossings + 1

			if 'Platform' in network[element]:
				n_platforms = n_platforms + 1

			if 'Crossing' in network[element]:
				n_crossings = n_crossings + 1

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

		n_signals_1 = 0
		n_signals_2 = n_signals_T + n_signals_B + n_signals_P
		n_signals_3 = n_signals_S + n_signals_C + n_signals_L + n_signals_X + n_signals_J

		N = n_netElements + n_switches + 2*n_doubleSwitch + n_levelCrossings + n_signals_2 + 2*n_signals_3
		M = N - n_netElements

		print(f'n_netElements:{n_netElements}\nn_switch:{n_switches}\nn_doubleSwitch:{n_doubleSwitch}\nn_borders:{n_borders}\nn_buffers:{n_buffers}\nn_levelCrossings:{n_levelCrossings}\nn_platforms:{n_platforms}\nn_crossings:{n_crossings}\nn_signals_1:{n_signals_1}\nn_signals_2:{n_signals_2}\nn_signals_3:{n_signals_3}')


		return N,M,n_netElements,n_switches,n_doubleSwitch,n_levelCrossings,n_signals_1,n_signals_2,n_signals_3

	def createPacket(self,n_signals,example = 1):
		node = 'my_package'
				
		f = open(f'App/Layouts/Example_{example}/VHDL/{node}.vhd',"w+")
		
		# Initial comment
		self.initialComment(node,f)
		
		# Include library
		self.includeLibrary(f)
		
		# Include body
		packet = 'my_package'
		f.write(f'\tpackage {packet} is\n')
		
		type = 'signals_type'
		f.write(f'\t\ttype {type} is record\n')
		f.write(f'\t\t\tmsb : std_logic_vector({n_signals}-1 downto 0);\n')
		f.write(f'\t\t\tlsb : std_logic_vector({n_signals}-1 downto 0);\n')
		f.write(f'\t\tend record {type};\r\n')
		
		type = 'signal_type'
		f.write(f'\t\ttype {type} is record\n')
		f.write(f'\t\t\tmsb : std_logic;\n')
		f.write(f'\t\t\tlsb : std_logic;\n')
		f.write(f'\t\tend record {type};\r\n')
		
		f.write(f'\t\ttype int_array is array(0 to {n_signals}-1) of integer;\r\n')
		
		f.write(f'\tend {packet};\n')

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
		f.write(f'\t\t\tswitch1 : in std_logic;\n')
		f.write(f'\t\t\tswitch2 : in std_logic;\n')
		f.write(f'\t\t\tReset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend entity {wrapper};\r\n') 
	
		f.write(f'architecture Behavioral of {wrapper} is\r\n')            

		# uart_control component
		uart_control = 'uart_control'
		f.write(f'\tcomponent {uart_control} is\n')
		f.write(f'\t\tport(\n')
		f.write(f'\t\t\tclock : in std_logic;\n')
		f.write(f'\t\t\tN : out integer;\n')
		f.write(f'\t\t\twrite : in std_logic;\n')
		f.write(f'\t\t\tempty_in : in std_logic;\n') 
		f.write(f'\t\t\trd_uart : out std_logic;\n')
		f.write(f'\t\t\twr_uart : out std_logic;\n')  
		f.write(f'\t\t\treset : in std_logic\n')
		f.write(f'\t\t);\n')
		f.write(f'\tend component {uart_control};\r\n')
		
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
		f.write(f'\t\t\tswitch1 : in std_logic;\n')
		f.write(f'\t\t\tswitch2 : in std_logic;\n')
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
		
		f.write(f'\t{uart_control}_i : {uart_control}\n')
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
		f.write(f'\t\t\tswitch1 => switch1,\n')
		f.write(f'\t\t\tswitch2 => switch2,\n')
		f.write(f'\t\t\tN => N_s,\n')
		f.write(f'\t\t\tleds => "ed_s,\n')
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
	  
	def createUART(self):
		return 0
	def createFIFO(self):
		return 0
	def createSystem(self):
		return 0
	def createDetector(self):
		return 0
	def createInterlocking(self):
		return 0
	def createSplitter(self):
		return 0
	def createMediator(self):
		return 0
	def createNetwork(self):
		return 0
	def createNodes(self):
		return 0
	def createSwitches(self):
		return 0
	def createLevelCrossings(self):
		return 0
	def createSignals(self):
		return 0
	def createRegister(self):
		return 0
	def createSelector(self):
		return 0
	
	def __init__(self,RML,example = 1):
		print("#"*50+' Reading railML object '+"#"*50)
		
		network = self.create_graph_structure(RML,example)
		self.print_network(network)
		self.create_graph(RML,network,example)

		# Calculate N and M
		N,M,n_netElements,n_switches,n_doubleSwitch,n_levelCrossings,n_signals_1,n_signals_2,n_signals_3 = self.calculate_parameters(network)
		print(f'N : {N}\nM : {M}')

		n_signals = n_signals_1 + n_signals_2 + n_signals_3

		print("#"*30+' Creating VHDL files '+"#"*30)
		
		print(f'Creating package ... ',end='')
		self.createPacket(n_signals,example)
		print(f'Done')
		
		print(f'Creating global wrapper ... ',end='')
		self.createGlobal(N,M,example)
		print(f'Done')
		
		print(f'Creating UART ... ',end='')
		self.createUART()
		print(f'Done')
		
		print(f'Creating FIFO ... ',end='')
		self.createFIFO()
		print(f'Done')
		
		print(f'Creating system ... ',end='')
		self.createSystem()
		print(f'Done')
		
		print(f'Creating detector ... ',end='')
		self.createDetector()
		print(f'Done')
		
		print(f'Creating interlocking ... ',end='')
		self.createInterlocking()
		print(f'Done')
		
		print(f'Creating splitter ... ',end='')
		self.createSplitter()
		print(f'Done')
		
		print(f'Creating mediator ... ',end='')
		self.createMediator()
		print(f'Done')
		
		print(f'Creating network ... ',end='')
		self.createNetwork()
		print(f'Done')
		
		print(f'Creating nodes ... ',end='')
		self.createNodes()
		print(f'Done')
		
		print(f'Creating switches ... ',end='')
		self.createSwitches()
		print(f'Done')
		
		print(f'Creating level crossings ... ',end='')
		self.createLevelCrossings()
		print(f'Done')
		
		print(f'Creating signals ... ',end='')
		self.createSignals()
		print(f'Done')
		
		print(f'Creating register ... ',end='')
		self.createRegister()
		print(f'Done')
		
		print(f'Creating selector ... ',end='')
		self.createSelector()
		print(f'Done')
		
		print("#"*30+' VHDL files Created '+"#"*30)