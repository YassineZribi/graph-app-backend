from dijekstra.dijekstra_shortest_path import shortest_path
from dijekstra.helpers import transform_graph_with_ids, getSelectedEdges, getSelectedNodes

def get_shortest_path(G, start_point, end_point):
    transformed_graph = transform_graph_with_ids(G)
    selected_nodes_ids = shortest_path(transformed_graph, start_point, end_point)
    # print(selected_nodes_ids)
    selected_nodes = getSelectedNodes(G, selected_nodes_ids)
    selected_edges = getSelectedEdges(G, selected_nodes_ids)
    return {"selectedNodes": selected_nodes, "selectedEdges": selected_edges}