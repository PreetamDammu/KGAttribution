from typing import List, Tuple, Dict, Set
from tqdm import tqdm

def find_paths(triplets: List[Tuple[int, int, int]], end_node1: int, end_node2: int) -> List[List[Tuple[int, int, int]]]:
    # Build the graph
    graph = build_graph(triplets)

    # Find all paths using DFS
    all_paths = dfs(graph, end_node1, end_node2, [], set(), triplets)

    return all_paths

def build_graph(triplets: List[Tuple[int, int, int]]) -> Dict[int, Set[int]]:
    graph = {}
    for triplet in triplets:
        src, _, dst = triplet

        if src not in graph:
            graph[src] = set()
        graph[src].add(dst)

        if dst not in graph:
            graph[dst] = set()
        graph[dst].add(src)

    return graph

def dfs(graph: Dict[int, Set[int]], current: int, target: int, path: List[Tuple[int, int, int]], visited: Set[int], triplets: List[Tuple[int, int, int]]) -> List[List[Tuple[int, int, int]]]:
    if current == target:
        # Found a path, return it
        return [path.copy()]

    paths = []
    visited.add(current)

    for neighbor in graph[current]:
        if neighbor not in visited:
            # Check if the edge (current, neighbor) or (neighbor, current) exists in the original triplets
            for triplet in triplets:
                if (triplet[0] == current and triplet[2] == neighbor) or (triplet[2] == current and triplet[0] == neighbor):
                    path.append(triplet)
                    paths.extend(dfs(graph, neighbor, target, path, visited, triplets))
                    path.pop()  # Backtrack

    visited.remove(current)
    return paths

def process_raw_text_to_paths(raw_text):
    lines = raw_text.split('\n')  
    data_dict = {}  
    current_key = ''  

    for i in tqdm(range(len(lines))):
        line = lines[i]
        
        if 'Processing nodes:' in line:
            # Extract node numbers and create the key.
            nodes = line.split('[')[1].split(']')[0]
            nodes_list = nodes.split(', ')
            current_key = f"{nodes_list[0]}_{nodes_list[1]}"
            data_dict[current_key] = []  
        elif 'Edge To Text:' in line:
            # Extract edge information and add it to the current key's list.
            edge_info = line.split('{')[1].split('}')[0]
            edge_parts = edge_info.split('->')
            edge_tuple = (int(edge_parts[0]), int(edge_parts[1]), int(edge_parts[2]))
            data_dict[current_key].append(edge_tuple)
        elif 'Finally:' in line:
            pass

    return data_dict