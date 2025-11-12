import argparse

PROJECTS = {
    'info': 'prints out my utils',
    'log': 'validates proj logs',
    'note': 'note with timestamp',
    'pymsg':'extract msgs form pylance',
    'fstree':'file tree to clipboard',
    'checkgit':'check if there are uncommited changes in projs',
    'fslash':'convert path to forward slashes',
    'zip':'zip proj by config'
}

def main():
    parser = argparse.ArgumentParser(description='Cli Utilities')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='alias with description')
    
    args = parser.parse_args()
    
    if args.verbose:
        print("Alias with desc:")
        for key, description in PROJECTS.items():
            print(f"  {key}: {description}")
    else:
        print("Alias:")
        for key in PROJECTS.keys():
            print(f"  {key}")

if __name__ == "__main__":
    main()