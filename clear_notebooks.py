#!/usr/bin/env python3
"""
Script to clear outputs from Jupyter notebooks.
Can be used manually or as a pre-commit hook.
"""
import json
import sys
from pathlib import Path


def clear_notebook_outputs(notebook_path):
    """Clear all outputs from a Jupyter notebook"""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    modified = False
    
    # Clear outputs from all cells
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            if cell.get('outputs') or cell.get('execution_count'):
                cell['outputs'] = []
                cell['execution_count'] = None
                modified = True
    
    # Write back if modified
    if modified:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
            f.write('\n')  # Add trailing newline
    
    return modified


def main():
    """Clear outputs from all notebooks passed as arguments, or all .ipynb files if none specified"""
    if len(sys.argv) > 1:
        # Use notebooks passed as arguments
        notebooks = [Path(nb) for nb in sys.argv[1:] if nb.endswith('.ipynb')]
    else:
        # Find all notebooks in current directory
        notebooks = list(Path('.').glob('*.ipynb'))
    
    if not notebooks:
        print("No notebooks found.")
        return 0
    
    print(f"Checking {len(notebooks)} notebook(s)...")
    modified_count = 0
    
    for nb in notebooks:
        if clear_notebook_outputs(nb):
            print(f"  ✓ Cleared outputs from {nb.name}")
            modified_count += 1
        else:
            print(f"  - {nb.name} (no outputs to clear)")
    
    print(f"\nCleaned {modified_count} notebook(s).")
    return 0


if __name__ == '__main__':
    sys.exit(main())
