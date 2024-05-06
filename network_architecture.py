import graphviz

# You need to install the above import on your OS
# Neural Network Architecture
input_size = 7  # Number of input nodes (equal to the number of items)
hidden_sizes = [8, 6, 4]  # List of hidden layer sizes
output_size = 1  # Number of output nodes (binary classification)

# Create a graphviz graph object
graph = graphviz.Digraph(format='png')
graph.attr('node', shape='circle')

# Add the input nodes
for i in range(input_size):
    graph.node(f'input_{i}', label=f'Input {i+1}')

# Add the hidden layers
prev_layer_nodes = [f'input_{i}' for i in range(input_size)]
for i, hidden_size in enumerate(hidden_sizes):
    layer_name = f'hidden_{i+1}'
    hidden_nodes = []
    for j in range(hidden_size):
        node_name = f'{layer_name}_{j}'
        graph.node(node_name, label=f'{layer_name} {j+1}')
        hidden_nodes.append(node_name)
        for prev_node in prev_layer_nodes:
            graph.edge(prev_node, node_name)
    prev_layer_nodes = hidden_nodes

# Add the output node
output_node = 'output'
graph.node(output_node, label='Output', shape='doublecircle')
for prev_node in prev_layer_nodes:
    graph.edge(prev_node, output_node)

# Save the graph as an image
graph.render('neural_network_architecture', view=True)