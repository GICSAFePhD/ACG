import networkx as nx
from IPython.display import display
import pylab as plt
import graphviz as gv

def ACG(RML,example = 1,test = False):
    
    print("#"*50+" Starting Automatic Code Generator "+"#"*50)
    
    print("Reading railML object")
    
    network = create_graph_structure(RML,example)
    print_network(network)
    create_graph(RML,network,example)
    #create_graphs(RML,example)
    print("Generating VHDL code")

    # Calculate N and M
    # Create UART files

    # Create nodes
    # Create switch
    # Create double switch
    # Create crossing
    # Connect network

    # Create railway elements
    # Connect railway elements

def create_graph_structure(RML,example = 1):

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

def print_network(network):
    for element in network:
        print(f'{element} {network[element]}\t')

def create_graph(RML,network,example = 1):

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

def create_graphs(RML,example = 1):
    options = {
    'node_color': 'lightgreen',
    'node_size': 500,
    'width': 2,
    'alpha' : 0.9
}
    
    G_Topology = nx.Graph()
    G_Switches = nx.Graph()
    G_Signals = gv.Digraph('finite_state_machine',filename='a.gv', graph_attr={'overlap':'false','rankdir':"LR",'splines':'true','center':'1'}) #node_attr={'color': 'lightgreen', 'style': 'filled', 'size' : '8.5'}
    

    NetElements = RML.Infrastructure.Topology.NetElements
    NetRelations = RML.Infrastructure.Topology.NetRelations
    SwitchesIS = RML.Infrastructure.FunctionalInfrastructure.SwitchesIS
    Crossings = RML.Infrastructure.FunctionalInfrastructure.Crossings
    SignalsIS = RML.Infrastructure.FunctionalInfrastructure.SignalsIS
    Routes = RML.Interlocking.AssetsForIL[0].Routes

    Topology_labels = {}
    for NetRelation in NetRelations.NetRelation:
        if (NetRelation.PositionOnA != None):
            #print(NetRelation.ElementA.Ref,NetRelation.ElementB.Ref,NetRelation.PositionOnA,NetRelation.PositionOnB)
            navColor = 'r' if NetRelation.Navigability == "None" else 'g'
            navStyle = '--' if NetRelation.Navigability == "None" else '-'

            G_Topology.add_edge(NetRelation.ElementA.Ref,NetRelation.ElementB.Ref, weight=3, color  = navColor, style = navStyle)

            #Topology_labels[(NetRelation.ElementA.Ref,NetRelation.ElementB.Ref)] = navColor

    Switch_labels = {}
    if Crossings != None:
        for crossings in Crossings[0].Crossing:
            Net = crossings.External[0].Ref.split('_')[1].split('ne')
            nodeStart = 'ne' + Net[1]        
            nodeEnd = 'ne' + Net[2]  

            #print(nodeStart,nodeEnd)
            G_Switches.add_edge(nodeStart,nodeEnd)
            Switch_labels[(nodeStart,nodeEnd)] = crossings.Name[0].Name+'\n(X)'

            Net = crossings.External[1].Ref.split('_')[1].split('ne')
            nodeStart = 'ne' + Net[1]        
            nodeEnd = 'ne' + Net[2]  

            #print(nodeStart,nodeEnd)
            G_Switches.add_edge(nodeStart,nodeEnd)
            Switch_labels[(nodeStart,nodeEnd)] = crossings.Name[0].Name+'\n(X)'        

    for SwitchIS in SwitchesIS[0].SwitchIS:
        if (SwitchIS.Type == "ordinarySwitch"):
            Net = SwitchIS.LeftBranch[0].NetRelationRef.split('_')[1].split('ne')
            nodeStart = 'ne' + Net[1]        
            nodeEnd = 'ne' + Net[2]  
            G_Switches.add_edge(nodeStart,nodeEnd)
            Switch_labels[(nodeStart,nodeEnd)] = SwitchIS.Name[0].Name+'\n(L)'

            Net = SwitchIS.RightBranch[0].NetRelationRef.split('_')[1].split('ne')
            nodeStart = 'ne' + Net[1]        
            nodeEnd = 'ne' + Net[2]  
            G_Switches.add_edge(nodeStart,nodeEnd)
            Switch_labels[(nodeStart,nodeEnd)] = SwitchIS.Name[0].Name+'\n(R)'

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

            #print(nodeStart,nodeEnd)
                
            G_Switches.add_edge(nodeStart,nodeEnd)
            Switch_labels[(nodeStart,nodeEnd)] = SwitchIS.Name[0].Name+'\n(S)'

            nodeStart = node
            nodeInt = turningBranch_1.split('_')[1].split('ne')[1:]
            nodeEnd = 'ne'+nodeInt[0] if str(nodeStart[2:]) == nodeInt[1] else 'ne'+nodeInt[1]

            #print(nodeStart,nodeEnd)
                
            G_Switches.add_edge(nodeStart,nodeEnd)
            Switch_labels[(nodeStart,nodeEnd)] = SwitchIS.Name[0].Name+'\n(T)'

            nodeStart = ['ne'+x for x in straightBranch_2.split('_')[1].split('ne')[1:] if x in turningBranch_2.split('_')[1].split('ne')[1:]][0]
            nodeInt = straightBranch_2.split('_')[1].split('ne')[1:]
            nodeEnd = 'ne'+nodeInt[0] if str(nodeStart[2:]) == nodeInt[1] else 'ne'+nodeInt[1]

            #print(nodeStart,nodeEnd)
                
            G_Switches.add_edge(nodeStart,nodeEnd)
            Switch_labels[(nodeStart,nodeEnd)] = SwitchIS.Name[0].Name+'\n(S)'

            nodeStart = ['ne'+x for x in straightBranch_2.split('_')[1].split('ne')[1:] if x in turningBranch_2.split('_')[1].split('ne')[1:]][0]
            nodeInt = turningBranch_2.split('_')[1].split('ne')[1:]
            nodeEnd = 'ne'+nodeInt[0] if str(nodeStart[2:]) == nodeInt[1] else 'ne'+nodeInt[1]

            #print(nodeStart,nodeEnd)
                
            G_Switches.add_edge(nodeStart,nodeEnd)
            Switch_labels[(nodeStart,nodeEnd)] = SwitchIS.Name[0].Name+'\n(T)'

    Signal_net = {}
    Signal_labels = {}
    for SignalIS in SignalsIS.SignalIS:
        Signal_net[SignalIS.Id] = {'net':SignalIS.SpotLocation[0].NetElementRef, 'equivalent':SignalIS.Designator[0].Entry[7:]}

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
            G_Signals.attr('node', shape='Mrecord')
            G_Signals.edge(entry_net,exit_net,label=f'R_{i:02d}')

            G_Signals.node(entry_net,label = f'<<table border=\"0\" cellborder=\"0\" cellpadding=\"1\" bgcolor=\"white\"><tr><td bgcolor=\"black\" align=\"center\" colspan=\"2\"><font color=\"white\">{entry_net}</font></td></tr><tr><td align=\"left\" port=\"r2\"> Signal: </td><td bgcolor=\"grey\" align=\"right\">{equivalent_entry_signal}</td></tr></table>>')

            Signal_labels[(entry_net,exit_net)] = f'R_{i:02d}'
        else:
            for p in range(len(path)-1):
                print(path[p],path[p+1])
                G_Signals.attr('node', shape='doublecircle')
                G_Signals.edge(path[p],path[p+1],label=f'R_{i:02d}')
                
                Signal_labels[(path[p],path[p+1])] = f'R_{i:02d}'

        print(f'R_{i:02d} | {entry_net} --> ({equivalent_entry_signal}) --> {path} --> ({equivalent_exit_signal}) --> {exit_net}')

        i = i + 1


    pos = nx.shell_layout(G_Topology)
  
    edges = G_Topology.edges()
    colors = [G_Topology[u][v]['color'] for u,v in edges]
    styles = [G_Topology[u][v]['style'] for u,v in edges]
    
    #edge_labels = dict([((n1, n2), f'{n1}->{n2}') for n1, n2 in G_Topology.edges])


    plt.figure(figsize=(18,18))

    #plt.subplot(211)
    nx.draw(G_Topology,pos,style=styles,edge_color = colors, labels={node: node for node in G_Topology.nodes()},**options) 
    #nx.draw_networkx_edge_labels(G_Topology, pos, edge_labels = Topology_labels,font_color='red')

    nx.draw(G_Switches,pos,edge_color = 'g', labels={node: node for node in G_Switches.nodes()},**options) 
    nx.draw_networkx_edge_labels(G_Switches, pos, edge_labels = Switch_labels,font_color='red')

    graph_file = "App//Layouts//Example_"+str(example)+"//Graphsss"

    #plt.savefig(graph_file, format="PNG",dpi=1000)

    #plt.subplot(212)
    
    #nx.draw(G_Signals,pos,edge_color = 'green', labels={node: node for node in G_Signals.nodes()},**options) 
    #nx.draw_networkx_edge_labels(G_Signals, pos, edge_labels = Signal_labels,font_color='red')

    #nx.drawing.nx_pydot.write_dot(G_Topology, graph_file)
    #gv.render('dot', 'png', graph_file)


    G_Signals.render(graph_file,format='svg', view = True)

    plt.show()    