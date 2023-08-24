import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import random

def get_links(url):
    links = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    content_div = soup.find('div', {'class': 'mw-parser-output'})
    paragraphs = content_div.find_all('p', recursive=False)
    count = 0
    for paragraph in paragraphs:
        if count >= 5:
            break
        for link in paragraph.find_all('a'):
            if count >= 5:
                break
            href = link.get('href')
            if href and href.startswith('/wiki/') and not href.startswith('/wiki/File:'):
                links.append(('https://en.wikipedia.org' + href, link.text))
                count += 1
    return links

def build_tree(url, depth):
    G = nx.DiGraph()
    visited = set()
    stack = [(url, depth)]
    G.add_node(url, title=url.split('/')[-1])
    while stack:
        node, level = stack.pop()
        visited.add(node)
        if level > 0:
            links = get_links(node)
            for link, label in links:
                G.add_edge(node, link)
                G.nodes[link]['title'] = label
                if link not in visited:
                    stack.append((link, level - 1))
    return G

def draw_tree(G):
    pos = nx.spring_layout(G)
    
    # Generate unique colors for each node
    color_map = {}
    for node in G.nodes:
        color_map[node] = (random.random(), random.random(), random.random())

    # Draw edges with unique colors
    for u, v in G.edges:
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=color_map[u])

    # Draw nodes 
    nx.draw_networkx_nodes(G, pos, node_color=list(color_map.values()))

    # Draw node labels
    node_labels = {node: G.nodes[node]['title'] for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_weight='bold')

    plt.rcParams['figure.figsize'] = [30, 30]
    plt.rcParams.update({'font.size': 3})
    plt.show()

url = 'https://en.wikipedia.org/wiki/Attention'
depth = 1
G = build_tree(url, depth)
draw_tree(G)


