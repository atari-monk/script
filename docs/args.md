# Cli args examples

## Path

Py Example of getting a patha as argument using argparse:

```py
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path')
args = parser.parse_args()

print(f"Path: {args.path}")
```
