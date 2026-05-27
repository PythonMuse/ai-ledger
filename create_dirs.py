#!/usr/bin/env python3
import os
import sys

base_path = r'c:\Users\sgruz\OneDrive\Documents\PythonMuse\Development\PythonMuse\articles'
dirs = [
    '20a-final-v2-xlsx-disaster',
    '20b-git-in-accounting-terms',
    '20c-finance-repo-structure',
    '20d-github-vs-shared-drives',
    '20e-pull-requests-are-controls',
    '20f-reproducible-financial-reporting'
]

print("Creating directories...")
for d in dirs:
    visuals_path = os.path.join(base_path, d, 'visuals')
    os.makedirs(visuals_path, exist_ok=True)
    print(f'✓ Created: {d}/visuals')

print('\n--- Verification: All directories starting with 20 ---')
count = 0
for item in sorted(os.listdir(base_path)):
    item_path = os.path.join(base_path, item)
    if item.startswith('20') and os.path.isdir(item_path):
        print(f'{item}/')
        count += 1
        for subitem in sorted(os.listdir(item_path)):
            subitem_path = os.path.join(item_path, subitem)
            if os.path.isdir(subitem_path):
                print(f'  └─ {subitem}/')

print(f'\nTotal directories starting with 20: {count}')
print('✓ All 6 folders + visuals subdirectories created successfully!')
