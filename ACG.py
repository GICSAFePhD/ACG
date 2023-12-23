import networkx as nx
import matplotlib.pyplot as plt

def ACG(RML,test = False):
    
    print("#"*50+" Starting Automatic Code Generator "+"#"*50)
    
    print("Reading railML object")
    create_graphs(RML)

    print("Generating VHDL code")


def create_graphs(RML):
    options = {
    'node_color': 'lightgreen',
    'node_size': 500,
    'width': 2,
    'alpha' : 0.9
}
    
    G_Topology = nx.Graph()
    G_Switches = nx.Graph()

    NetElements = RML.Infrastructure.Topology.NetElements
    NetRelations = RML.Infrastructure.Topology.NetRelations
    SwitchesIS = RML.Infrastructure.FunctionalInfrastructure.SwitchesIS
    Crossings = RML.Infrastructure.FunctionalInfrastructure.Crossings

    Topology_labels = {}
    for NetRelation in NetRelations.NetRelation:
        if (NetRelation.PositionOnA != None):
            #print(NetRelation.ElementA.Ref,NetRelation.ElementB.Ref,NetRelation.PositionOnA,NetRelation.PositionOnB)
            navColor = 'r' if NetRelation.Navigability == "None" else 'g'
            navStyle = '--' if NetRelation.Navigability == "None" else '-'

            G_Topology.add_edge(NetRelation.ElementA.Ref,NetRelation.ElementB.Ref, weight=3, color  = navColor, style = navStyle)

            #Topology_labels[(NetRelation.ElementA.Ref,NetRelation.ElementB.Ref)] = navColor

    Switch_labels = {}

    for crossings in Crossings[0].Crossing:
        Net = crossings.External[0].Ref.split('_')[1].split('ne')
        nodeStart = 'ne' + Net[1]        
        nodeEnd = 'ne' + Net[2]  

        G_Switches.add_edge(nodeStart,nodeEnd)
        Switch_labels[(nodeStart,nodeEnd)] = crossings.Name[0].Name+'\n(X)'

        Net = crossings.External[1].Ref.split('_')[1].split('ne')
        nodeStart = 'ne' + Net[1]        
        nodeEnd = 'ne' + Net[2]  

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

    pos = nx.planar_layout(G_Topology)
  
    edges = G_Topology.edges()
    colors = [G_Topology[u][v]['color'] for u,v in edges]
    styles = [G_Topology[u][v]['style'] for u,v in edges]
    
    #edge_labels = dict([((n1, n2), f'{n1}->{n2}') for n1, n2 in G_Topology.edges])


    plt.figure(figsize =(10, 10)) 

    #plt.subplot(221)
    nx.draw(G_Topology,pos,style=styles,edge_color = colors, labels={node: node for node in G_Topology.nodes()},**options) 
    #nx.draw_networkx_edge_labels(G_Topology, pos, edge_labels = Topology_labels,font_color='red')

    nx.draw(G_Switches,pos,edge_color = 'g', labels={node: node for node in G_Switches.nodes()},**options) 
    nx.draw_networkx_edge_labels(G_Switches, pos, edge_labels = Switch_labels,font_color='red')

    plt.show()

    