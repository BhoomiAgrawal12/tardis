# This script shows how to update env.yml from conda-lock.yml
# Run this whenever conda-lock.yml is updated

set -e

echo "Generating env.yml from conda-lock.yml using explicit format..."
/home/bhoomi/miniforge3/bin/conda-lock render --kind explicit

mv conda-linux-64.lock env.yml

echo " env.yml updated with full package URLs and hashes"

rm -f conda-osx-64.lock conda-osx-arm64.lock conda-linux-64.lock.yml conda-osx-64.lock.yml conda-osx-arm64.lock.yml

wc -l env.yml
