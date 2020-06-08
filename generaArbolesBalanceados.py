#
# Genera arboles balanceados de altura h y factor de ramificacion r
# ejecucion: python generaArbolesBalanceados archivo_salida r h 
# 
#
import sys
import networkx as nx


fileName = sys.argv[1]
h = int(sys.argv[2])
r = int(sys.argv[3])

G = nx.balanced_tree(r, h)
heading = "%% Arbol balanceado de altura %d (raiz 0) y factor de ramificacion %d\n" % (h, r)
W = nx.convert_node_labels_to_integers(G)

# Open a file
fo = open(fileName, "w")

fo.write(heading);
heading2 = "%d %d %d\n" % (W.number_of_nodes(), W.number_of_nodes(), W.number_of_edges())
fo.write(heading2);

for e in W.edges(data=False):
	arco = "%d %d\n" % (e[0]+1, e[1]+1)
	fo.write(arco)

# Close opend file
fo.close()
