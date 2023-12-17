import networkx as nx
import matplotlib.pyplot as plt

def ACG(RML,test = False):
    
    print(RML)
    
    print("#"*50+" Starting Automatic Code Generator "+"#"*50)
    print("Reading railML object")

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

    Topology_labels = {}
    for NetRelation in NetRelations.NetRelation:
        #print(NetRelation.ElementA.Ref,NetRelation.ElementB.Ref,NetRelation.PositionOnA,NetRelation.PositionOnB)
        navColor = 'r' if NetRelation.Navigability == "None" else 'g'
        navStyle = '--' if NetRelation.Navigability == "None" else '-'

        G_Topology.add_edge(NetRelation.ElementA.Ref,NetRelation.ElementB.Ref, weight=3, color  = navColor, style = navStyle)

        #Topology_labels[(NetRelation.ElementA.Ref,NetRelation.ElementB.Ref)] = navColor

    Switch_labels = {}
    for SwitchIS in SwitchesIS[0].SwitchIS:
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

    #print("Generating interlocking table")
    #print("Generating VHDL code")