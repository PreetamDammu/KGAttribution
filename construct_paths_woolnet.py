import numpy as np
from tqdm import tqdm
from utils.graph_helpers import find_paths, process_raw_text_to_paths
import concurrent.futures
import json
split = 'train'



with open(f'inputs/wikiqa_answers_{split}_woolnet_output.txt', 'r') as f:
    woolnet_text_raw = f.read()
edges_dict = process_raw_text_to_paths(woolnet_text_raw)
def process_edge(key_edges_dict):
    key, edges = key_edges_dict
    node1, node2 = key.split('_')
    if len(edges) == 0:
        return key, None
    paths = find_paths(edges, int(node1), int(node2))
    return key, paths

def save_intermediate_results(data, filename="intermediate_results.json"):
    """Save intermediate results to a JSON file."""
    with open(f'outputs/path_dicts/{filename}', "w") as f:
        json.dump(data, f)
paths_dict = {}
keys_to_process = [(key, edges_dict[key]) for key in edges_dict.keys() if len(edges_dict[key]) > 0 and len(edges_dict[key]) < 300]

progress_bar = tqdm(total=len(keys_to_process))
timeout_duration = 10  # Adjust based on expected task duration

# Intermediate saving setup
save_interval = 2000  # Number of tasks after which to save intermediate results
tasks_completed = 0  # Counter for completed tasks

#Change workers according to CPU cores
with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
    future_to_key = {executor.submit(process_edge, item): item[0] for item in keys_to_process}
    
    for future in concurrent.futures.as_completed(future_to_key):
        key = future_to_key[future]
        try:
            _, paths = future.result(timeout=timeout_duration)
            if paths is not None:
                paths_dict[key] = paths
        except concurrent.futures.TimeoutError:
            print(f"Task for {key} timed out.")
        except Exception as e:
            print(f"Error processing {key}: {e}")
        finally:
            tasks_completed += 1
            progress_bar.update(1)
            # Save intermediate results after every 'save_interval' tasks
            if tasks_completed % save_interval == 0:
                save_intermediate_results(paths_dict, filename=f"intermediate_constructed_paths_dict_{split}_wikiqa.json")
                print(f"Saved intermediate results after {tasks_completed} tasks.")

progress_bar.close()

# Save the final results at the end
save_intermediate_results(paths_dict, filename=f"constructed_paths_dict_{split}_wikiqa.json")
print("Final results saved.")
