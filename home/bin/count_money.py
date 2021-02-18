"""
Counts the money I have based on simple files I have on my computer.

Files are lines, sorted descending by time stamp.
Have contents like organized like this:

<human-readable timestamp> <human-friendly separator> <amount>

For example, a file called RBS balances (contains the state of my balance from an RBS account):
2021-02-18 13:08:35 | 666.66 GBP
2021-02-14 08:28:57 | 1666.66 GBP
2021-02-13 12:43:01 | 300.98 GBP
"""

from pathlib import Path

storage_path = Path('~/money').expanduser()
print('Gonna be reading files from', storage_path)

for file in storage_path.iterdir():
    print(file)
