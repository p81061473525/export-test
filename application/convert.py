import glob
import yaml

# Get YAML files in the current directory
yaml_files = glob.glob('*.yaml')

# Parse YAML files and extract data
entries = []
for yaml_file in yaml_files:
    with open(yaml_file, 'r') as file:
        yaml_data = yaml.safe_load(file)
        entry = {
            "port": yaml_data[0]["port"],
            "mode": yaml_data[0]["mode"],
            "applicant": yaml_data[0]["applicant"],
            "department": yaml_data[0]["department"],
            "host": f"redis-master.{yaml_file.split('.')[0]}.svc.cluster.local" if yaml_data[0]["mode"] == "standalone" else f"redis.{yaml_file.split('.')[0]}.svc.cluster.local",
            "service": yaml_file.split('.')[0]
        }
        entries.append(entry)

# Sort entries based on the 'service' field
sorted_entries = sorted(entries, key=lambda x: int(x['service'].split('i')[-1]))

# Write sorted entries to ../total.txt
with open('../total.txt', 'w') as total_file:
    for entry in sorted_entries:
        total_file.write(f'{{"port": {entry["port"]}, "mode": "{entry["mode"]}", "applicant": "{entry["applicant"]}", "department": "{entry["department"]}", "host": "{entry["host"]}", "service": "{entry["service"]}"}}\n')
