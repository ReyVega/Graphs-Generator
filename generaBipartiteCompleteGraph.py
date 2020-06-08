#
# Genera grafos bipartitas completos con n nodos (n1+n2)
# ejecucion: python generaBipartiteCompleteGraph.py archivo_salida n1 n2 
# 
#
import sys
import networkx as nx


fileName = sys.argv[1]
n1 = int(sys.argv[2])
n2 = int(sys.argv[3])


G = nx.complete_bipartite_graph(n1, n2)
heading = "%% Grafo bipartita completo con %d nodos (%d,%d)\n" % (n1+n2, n1, n2)
W = nx.convert_node_labels_to_integers(G)

# Open a file
fo = open(fileName, "w")

fo.write(heading);
heading2 = "%d %d %d\n" % (W.number_of_nodes(), W.number_of_nodes(), W.number_of_edges())
fo.write(heading2);

for e in W.edges(data=False):
	arco = "%d %d\n" % (e[0], e[1])
	fo.write(arco)

# Close opend file
fo.close()
