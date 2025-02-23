# Characterization of Students Based on Solved Exercises and Social Networking Techniques

A proposal based on data mining and social networks for characterizing students based on their attemps for solving exercises.

## Run

```bash
python3 -m venv .env
source .env/bin/activate
python3 -m pip install -r requirements.txt
python3 src/experiment.py
```

### Data Analysis

Some data analysis metrics can be computed with:
```bash
python3 src/data_analysis.py
```

### Examples

Some examples can be seen in `data/examples/` directory. The DOT files and images can be generated with:
```bash
python3 src/examples.py
```

The DOT files can be converted to images with:
```bash
dot -Tpng [dot_filename].dot -o [image_filename].png
```
