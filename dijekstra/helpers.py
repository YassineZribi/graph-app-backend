def transform_graph_with_ids(graph):

    nodes = graph['nodes']
    edges = graph['edges']

    transformed_graph_with_ids={}

    for node in nodes:
        neighbors = {}
        for edge in edges:
            if (node['id'] == edge['from'] and edge['arrows'] == "to") or ((node['id'] == edge['from'] or node['id'] == edge['to']) and edge['arrows'] != "to"):
                neighbors[edge['to'] if edge['to'] != node['id'] else edge['from']] = int(edge['label'])
        transformed_graph_with_ids[node['id']] = neighbors
    
    return transformed_graph_with_ids

def getSelectedNodes(graph, selected_nodes_ids):
    nodes = graph['nodes']
    selected_nodes = []
    for id in selected_nodes_ids:
        for node in nodes:
            if node["id"] == id:
                selected_nodes.append(node)
                break
    return selected_nodes

def getSelectedEdges(graph, selected_nodes_ids):
    edges = graph['edges']
    selected_edges = []
    for i in range(len(selected_nodes_ids)-1):
        currentNodeId = selected_nodes_ids[i]
        nextNodeId = selected_nodes_ids[i+1]
        for edge in edges:
            if edge["arrows"] == "to":
                if edge["from"] == currentNodeId and edge["to"] == nextNodeId:
                    selected_edges.append(edge)
            else:
                if (edge["from"] == currentNodeId and edge["to"] == nextNodeId) or (edge["from"] == nextNodeId and edge["to"] == currentNodeId):
                    selected_edges.append(edge)
    return selected_edges