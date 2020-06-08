#
# Genera grafos tipo mesh2D de n x m nodos
# ejecucion: python generaMesh2D.py archivo_salida n m
# 
#
import sys
import networkx as nx


fileName = sys.argv[1]
n = int(sys.argv[2])
m = int(sys.argv[3])

G = nx.grid_2d_graph(n,m)
W = nx.convert_node_labels_to_integers(G)

# Open a file
fo = open(fileName, "w")

heading = "%% Mesh2D con (%dx%d) = %d nodes y m=%d arcos\n" % (n, m, n*m, (2*m*n)-n-m)
fo.write(heading);
heading2 = "%d %d %d\n" % (W.number_of_nodes(), W.number_of_nodes(), W.number_of_edges())
fo.write(heading2);


for e in W.edges(data=False):
	arco = "%d %d\n" % (e[0], e[1])
	fo.write(arco)

# Close opend file
fo.close()
