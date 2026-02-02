import zarr
import json
from pathlib import Path

filename = r'/path/to/file.brim.zarr'

store = zarr.storage.LocalStore(filename)
root = zarr.open(store=store, mode='r')

def recurse_nodes(node):
    node_dict = {}
    node_dict['attributes'] = node.attrs.asdict()
    if isinstance(node, zarr.Group):
        node_dict['node_type'] = 'group' 
    else:
        node_dict['node_type'] = 'array'
        node_dict['shape'] = node.shape
        node_dict['dtype'] = str(node.dtype)
    
    if isinstance(node, zarr.Group):
        for key in node.keys():
            child_dict = recurse_nodes(node[key])
            node_dict[key] = child_dict
    
    return node_dict

out_dict = recurse_nodes(root)

# convert the Python dict to json and save to file
json_filename = Path(filename).with_suffix('.json')
with open(json_filename, 'w') as f:
    json.dump(out_dict, f, indent=4)