import yaml
import re

class InterfaceTransformer:
    def __init__(self, mapping_file="settings/interface_mapping.yml"):
        with open(mapping_file) as f:
            self.mappings = yaml.safe_load(f)['platform_mappings']
    
    def transform(self, interface_name, from_platform, to_platform):
        if from_platform == to_platform:
            return interface_name
            
        # Parse source interface
        src_fmt = self.mappings[from_platform]['format']
        if 'uplink' in interface_name and 'uplink_format' in self.mappings[from_platform]:
            src_fmt = self.mappings[from_platform]['uplink_format']
        
        # Parse destination format
        dst_fmt = self.mappings[to_platform]['format']
        if 'uplink' in interface_name and 'uplink_format' in self.mappings[to_platform]:
            dst_fmt = self.mappings[to_platform]['uplink_format']
        
        # Extract components
        if from_platform.startswith('N3K') or from_platform.startswith('N9K'):
            match = re.match(r'Ethernet(\d+)/(\d+)', interface_name)
            if match:
                module, port = match.groups()
                if to_platform.startswith('Arista'):
                    if int(port) >= 49:  # Uplink ports
                        return f"Ethernet{port}/1"
                    return f"Ethernet{port}"
                return interface_name
        elif from_platform.startswith('Arista'):
            match = re.match(r'Ethernet(\d+)(?:/(\d+))?', interface_name)
            if match:
                port, subport = match.groups()
                if to_platform.startswith('N3K') or to_platform.startswith('N9K'):
                    if int(port) >= 49:  # Uplink ports
                        return f"Ethernet1/{port}"
                    return f"Ethernet1/{port}"
        return interface_name