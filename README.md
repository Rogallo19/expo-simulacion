# BeakBallot

*"No one pretends that democracy is perfect or all-wise. Indeed, it has been said that democracy is the worst form of government except all those other forms that have been tried from time to time". -Winston Churchill*

A Python simulation that runs hundreds of randomized elections using four different voting systems, then ruthlessly compares them to see how often they actually agree on a winner.

## What Does It Actually Do?

It simulates elections. 500 by default, with 100 voters each time. Every voter gets a random ranking of 4 candidates (A, B, C, D), and then four different voting systems check who "really" won.
The results are plotted into a clean chart with `matplotlib`.

Output

Running the script will:

1. Print a summary table of agreement rates between every pair of systems to your console
2. Save a `multi_simulation.png` with three charts:
   - **Bar chart** — how many times each candidate won under each system
   - **Heatmap** — how often each pair of systems agreed on the winner
   - **Stats panel** — a summary box
---


## Requirements

You'll need Python 3 and three libraries.

```bash
pip install matplotlib numpy
```

`collections` and `random` come built into Python, so those are free. You're welcome.

## Running It

```bash
python multi_simulation.py
```

---

## Configuration

At the top of `multi_simulation.py` you'll find three variables you can tweak:

```python
candidates = ["A", "B", "C", "D"]     
num_voters = 100                      
num_simulations = 500                 
```

---

##  Project Structure

```
📦 your-repo/
 ┣  BeakBallot.py    ← The whole thing.
 ┣  BeakBallot.png   ← Generated after running (not included in repo)
 ┗  README.md              ← You are here

##  License
Do whatever you want with this. It's got an MIT licence.
---
## Contributing
Found a bug? Open an issue. Have a better voting system to add? Open a PR. Thanks.
