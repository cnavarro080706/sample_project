import yaml
import re

class InterfaceTransformer:
    def __init__(self, mapping_file="settings/interface_mapping.yml"):
        with open(mapping_file) as f:
            self.mappings = yaml.safe_load(f)['platform_mappings']
    
    def transform(self, interface_name, from_platform, to_platform):
        if from_platform == to_platform:
            return interface_name
            
        # Handle Nexus to Arista conversion
        if from_platform.startswith(('N3K', 'N9K')) and to_platform.startswith('Arista'):
            match = re.match(r'Ethernet(\d+)/(\d+)', interface_name)
            if match:
                module, port = match.groups()
                port_num = int(port)
                if port_num >= 49:  # Uplink ports
                    return f"Ethernet{port}/1"
                return f"Ethernet{port}"  # Host/span ports
        
        # Handle Arista to Nexus conversion
        elif from_platform.startswith('Arista') and to_platform.startswith(('N3K', 'N9K')):
            match = re.match(r'Ethernet(\d+)(?:/(\d+))?', interface_name)
            if match:
                port, subport = match.groups()
                port_num = int(port)
                return f"Ethernet1/{port}"  # All ports become Ethernet1/X in Nexus
        
        return interface_name

    def is_uplink_interface(self, interface_name, platform):
        """Check if interface is an uplink (ports 49+)"""
        if platform.startswith(('N3K', 'N9K')):
            match = re.match(r'Ethernet(\d+)/(\d+)', interface_name)
            if match:
                return int(match.group(2)) >= 49
        elif platform.startswith('Arista'):
            match = re.match(r'Ethernet(\d+)(?:/(\d+))?', interface_name)
            if match:
                return int(match.group(1)) >= 49
        return False

    def is_host_interface(self, interface_name, platform):
        """Check if interface is a host port (ports 1-46)"""
        if platform.startswith(('N3K', 'N9K')):
            match = re.match(r'Ethernet(\d+)/(\d+)', interface_name)
            if match:
                return 1 <= int(match.group(2)) <= 46
        elif platform.startswith('Arista'):
            match = re.match(r'Ethernet(\d+)$', interface_name)  # Exclude uplinks
            if match:
                return 1 <= int(match.group(1)) <= 46
        return False

    def is_span_interface(self, interface_name, platform):
        """Check if interface is a span port (ports 47-48)"""
        if platform.startswith(('N3K', 'N9K')):
            match = re.match(r'Ethernet(\d+)/(\d+)', interface_name)
            if match:
                port_num = int(match.group(2))
                return 47 <= port_num <= 48
        elif platform.startswith('Arista'):
            match = re.match(r'Ethernet(\d+)$', interface_name)
            if match:
                port_num = int(match.group(1))
                return 47 <= port_num <= 48
        return False