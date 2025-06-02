# Sample NRE Project 

This program is intended to generate device configuration from EOL devices

## Getting Started

1.  Clone the repository.
2.  Install dependencies.

## Cloning the repository

`https://github.com/cnavarro080706/sample_project.git`

## Install dependencies
Ensure your requirements.txt file is within the same directory of project

`pip install -r requirements.txt`

This will install all listted packages and their specified versions.

## Directory Structure
```
main_project/
├── devices/
│   ├── input/
|   |__ output/
|   |
├── settings/
│   ├── interface_mapping.yml
|   |__ settings.yml
|   
├── templates/
│   ├── nxos/
│   │   ├── features/
│   │   │   ├── system.j2
│   │   │   ├── interfaces.j2
│   │   │   └── bgp.j2
│   │   └── ip_fabric/
│   │       └── leaf/
│   │           ├── even.j2
│   │           └── odd.j2
│   └── nxos.j2
├── utils/
│   ├── interface_transformer.py
├── render_config.py
├── requirements.txt
├── README.md
```
## nxos.j2 template

```
! =======================================================
! Generated from Jinja2 template
! Created by: Chris Navarro
! Last update: 2025-06-01
! Device: {{ data.data.device.hostname }}
! Model: {{ data.data.device.device_type.model }}
! Platform: {{ data.data.device.platform.name }}
! Fabric: {{ data.data.device.component_architecture[0].name }}
! Fabric Type: {{ data.data.device.component_architecture_type[0].name }}
! Role: {{ data.data.device.role.name }}
! Location: {{ data['data']['device']['location']['name'] }}
! =======================================================

{% include 'templates/nxos/features/system.j2' %}
{%- if data.data.device.component_architecture[0].name == 'IP Fabric' -%}
  {# IP Fabric Specific Configuration #}
  {% if data.data.device.function_code_instance[0].function_code == 'lea' %}
    {% if data.parity == 'even' %}
      {% include 'templates/nxos/ip_fabric/lea/lea_base_even.j2' %}
    {% else %}
      {% include 'templates/nxos/ip_fabric/lea/lea_base_odd.j2' %}
    {% endif %}
  {% endif %}
{%- endif -%}

{%- include 'templates/nxos/features/interfaces.j2' -%}
{%- include 'templates/nxos/features/bgp.j2' -%}

```


## Contributing

Contributions are welcome!

## License

[Link: MIT License https://opensource.org/licenses/MIT]