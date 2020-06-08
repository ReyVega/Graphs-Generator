import sys
import networkx as nx

fileName = sys.argv[1]
n = int(sys.argv[2])

G = nx.grid_graph(dim = [n,n])

heading = "%% Path con n=%d nodes y m=%d arcos\n" % (n, n-1)
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