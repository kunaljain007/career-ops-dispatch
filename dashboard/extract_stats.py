import os
import re
import json
from datetime import datetime

def parse_applications(filepath):
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    apps = []
    # Skip header
    for line in lines[4:]:
        line = line.strip()
        if not line.startswith('|'):
            continue
        
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 7:
            continue
            
        apps.append({
            'date': parts[1],
            'company': parts[2],
            'role': parts[3],
            'resume': parts[4],
            'status': parts[5],
            'url': parts[6]
        })
    return apps

def generate_stats(apps):
    stats = {
        'total': len(apps),
        'submitted': len([a for a in apps if 'submitted' in a['status']]),
        'failed': len([a for a in apps if 'failed' in a['status']]),
        'pending': len([a for a in apps if 'pending' in a['status'] or 'todo' in a['status']]),
        'companies': {},
        'timeline': {}
    }
    
    for a in apps:
        # Company count
        name = a['company']
        stats['companies'][name] = stats['companies'].get(name, 0) + 1
        
        # Timeline
        date = a['date']
        if date:
            stats['timeline'][date] = stats['timeline'].get(date, 0) + 1
            
    return stats

if __name__ == "__main__":
    apps = parse_applications('data/applications.md')
    stats = generate_stats(apps)
    
    with open('dashboard/data.json', 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"Generated stats for {len(apps)} applications.")
