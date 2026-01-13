"""
Generate env.yml for ASV benchmarks from conda-lock.yml

This script extracts pinned package versions from conda-lock.yml
and creates an env.yml file that ASV can use for reproducible benchmarks.

ASV (AirSpeed Velocity) does not natively support lockfiles, so we need
to manually extract the pinned versions into a standard conda environment file.

Usage:
    python generate_benchmark_env.py

This will create/update env.yml in the repository root.
"""

import yaml
from pathlib import Path


def generate_env_from_lock():
    """Generate env.yml from conda-lock.yml for ASV benchmarks."""
    
    repo_root = Path(__file__).parent
    lock_file = repo_root / "conda-lock.yml"
    env_file = repo_root / "env.yml"
    
    if not lock_file.exists():
        raise FileNotFoundError(f"conda-lock.yml not found at {lock_file}")
    
    print(f"Reading {lock_file}...")
    with open(lock_file, 'r') as f:
        lock_data = yaml.safe_load(f)
    
    channels = []
    if 'metadata' in lock_data and 'channels' in lock_data['metadata']:
        for ch in lock_data['metadata']['channels']:
            if 'url' in ch:
                channels.append(ch['url'])
    
    if not channels:
        channels = ['conda-forge']
    
    # Extract packages for linux-64 platform (standard CI platform)
    packages = []
    if 'package' in lock_data:
        for pkg in lock_data['package']:
            if pkg.get('platform') == 'linux-64' and pkg.get('manager') == 'conda':
                name = pkg.get('name')
                version = pkg.get('version')
                if name and version:
                    packages.append(f"{name}={version}")
    
    if not packages:
        raise ValueError("No packages found in conda-lock.yml for linux-64 platform")
    
    packages.sort()
    
    env_data = {
        'name': 'tardis-benchmark',
        'channels': channels,
        'dependencies': packages
    }
    
    print(f"Writing {env_file}...")
    with open(env_file, 'w') as f:
        # Header comments explaining the purpose
        f.write('# This file is auto-generated from conda-lock.yml for ASV benchmarks\n')
        f.write('# DO NOT EDIT MANUALLY\n')
        f.write('#\n')
        f.write('# To regenerate this file, run:\n')
        f.write('#   python generate_benchmark_env.py\n')
        f.write('#\n')
        f.write(f'# Source: conda-lock.yml (linux-64 platform)\n')
        f.write(f'# Total packages: {len(packages)}\n')
        f.write('#\n\n')
        
        yaml.dump(env_data, f, default_flow_style=False, sort_keys=False)
    
    print(f"✓ Successfully created env.yml with {len(packages)} pinned packages")
    print(f"  Channels: {', '.join(channels)}")
    print(f"  Platform: linux-64")
    return env_file


if __name__ == '__main__':
    generate_env_from_lock()
