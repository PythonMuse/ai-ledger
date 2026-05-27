#!/usr/bin/env python
"""Create article directory structure with visuals subdirectories."""

import os

base_path = r'c:\Users\sgruz\OneDrive\Documents\PythonMuse\Development\PythonMuse\articles'

dirs_to_create = [
    '20a-final-v2-xlsx-disaster',
    '20b-git-in-accounting-terms',
    '20c-finance-repo-structure',
    '20d-github-vs-shared-drives',
    '20e-pull-requests-are-controls',
    '20f-reproducible-financial-reporting'
]

print("Creating article directories with visuals subdirectories...\n")

# Create all directories with visuals subdirectories
for dir_name in dirs_to_create:
    visuals_path = os.path.join(base_path, dir_name, 'visuals')
    os.makedirs(visuals_path, exist_ok=True)
    print(f'✓ Created: {dir_name}/visuals')

# Verify all directories exist
print('\n--- Verification ---\n')
created_count = 0
visuals_count = 0

for item in sorted(os.listdir(base_path)):
    item_path = os.path.join(base_path, item)
    if os.path.isdir(item_path) and item.startswith('20'):
        created_count += 1
        visuals_path = os.path.join(item_path, 'visuals')
        visuals_exists = os.path.isdir(visuals_path)
        status = '✓' if visuals_exists else '✗'
        print(f'{status} {item}/')
        if visuals_exists:
            print(f'  └─ visuals/')
            visuals_count += 1

print(f'\n--- Summary ---')
print(f'✓ All {created_count} directories created')
print(f'✓ All {visuals_count} visuals subdirectories created')
if created_count == 6 and visuals_count == 6:
    print('\n✅ SUCCESS: All 6 directories + visuals subdirectories created successfully!')
else:
    print(f'\n⚠️  Expected 6 directories with 6 visuals, but got {created_count} with {visuals_count}')
