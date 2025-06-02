import yaml
import json
import os
import jinja2
from ipaddress import IPv4Interface
from utils.interface_transformer import InterfaceTransformer

# Calculate spine IP based on leaf IP
def calculate_spine_ip(leaf_ip):
    interface = IPv4Interface(leaf_ip)
    return str(interface.ip - 1)

# Load configuration
with open("settings/settings.yml") as f:
    config = yaml.safe_load(f)
    
# Load device metadata
with open(f"devices/input/{config['device']}.json") as f:
    device_metadata = json.load(f)

# Initialize interface transformer
transformer = InterfaceTransformer()
    
# Set up Jinja2 environment
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.getcwd()),
    trim_blocks=True,
    lstrip_blocks=True
)
env.filters['spine_ip'] = calculate_spine_ip
env.globals['transformer'] = transformer

# Add metadata
device_metadata['parity'] = config['parity']

# Render template
template = env.get_template(f"{config['platform']}.j2")
rendered = template.render(data=device_metadata)

# Write output
os.makedirs('devices/output', exist_ok=True)
output_file = f"{config['device']}.cfg"
with open(f"devices/output/{output_file}", 'w') as f:
    f.write(rendered)
    
print(f"Successfully generated device configuration for {config['device']}")

