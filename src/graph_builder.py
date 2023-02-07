import requests
import re
from bs4 import BeautifulSoup
from graphviz import Digraph

def create_graph(g, start):
    
    visited = set()
    queue = [start]
    num_edges = 0

    # Javascript Pattern Matching
    pattern = re.compile(r"window\.location\.href\s*=\s*([^;]*);") 

    while queue:
        current_vertex = queue.pop(0)
        if len(current_vertex) > 1:
            if current_vertex not in visited and current_vertex[0] == '/':
                visited.add(current_vertex)
                g.node(current_vertex)
                url = "https://protein.monster" + current_vertex
                
                # Get all href tags
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a', href=True)
                
                for link in links:
                    neighbour_vertex = link['href'].replace('\'',"")
                    if '#' not in neighbour_vertex and 'mailto' not in neighbour_vertex and len(neighbour_vertex) > 1:
                        g.edge(current_vertex, neighbour_vertex.replace('\'',""))
                        queue.append(neighbour_vertex.replace('\'',""))
                
                # Get all class = link tags
                links = soup.find_all(class_ = 'link')
                for link in links:
                    try:
                        neighbour_vertex = link['onclick'].split('=')[-1].replace('\'', "")
                    except:
                        if link.has_attr('href'):
                            neighbour_vertex = link['href'].replace('\'',"")
                        else:
                            current_vertex = ''
                    if '#' not in neighbour_vertex and 'mailto' not in neighbour_vertex and len(neighbour_vertex) > 1:
                        g.edge(current_vertex, neighbour_vertex.replace('\'',""))
                        queue.append(neighbour_vertex.replace('\'',""))

                # Get all onclick tags
                # Get all class = link tags
                elements_with_onclick = soup.find_all(lambda x: x.has_attr('onclick'))
                for link in elements_with_onclick:
                    try:
                        neighbour_vertex = link['onclick'].split('=')[-1].replace('\'', "")
                    except:
                        if link.has_attr('href'):
                            neighbour_vertex = link['href'].replace('\'',"")
                        else:
                            current_vertex = ''
                    if '#' not in neighbour_vertex and 'mailto' not in neighbour_vertex and len(neighbour_vertex) > 1:
                        g.edge(current_vertex, neighbour_vertex.replace('\'',""))
                        queue.append(neighbour_vertex.replace('\'',""))

                # Read javascript and get the window.location.href assignments
                response = requests.get(url + "/index.js")
                
                # Access the contents of the file as a string
                js_string = response.text

                # Find all matches for the pattern in the string
                matches = pattern.findall(js_string)

                for match in matches:
                    neighbour_vertex = match.replace('"', "")
                    if '#' not in neighbour_vertex and 'mailto' not in neighbour_vertex and len(neighbour_vertex) > 1:
                        g.edge(current_vertex, neighbour_vertex.replace('\'',""))
                        queue.append(neighbour_vertex.replace('\'',""))
            num_edges += 1
    print("no. pages:", len(visited))
    print("no. edges:", num_edges)
    g.view()
        
g = Digraph(strict=True)
create_graph(g, '/mantra')
