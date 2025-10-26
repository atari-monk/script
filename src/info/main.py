import argparse

PROJECTS = {
    'info': 'prints out my utils',
    'log': 'log project note with timestamp'
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