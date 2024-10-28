# Classic Partial Alignments

Implementation of Classic Partial Alignments based on ILP-based A* algorithm in Python.

## Usage

To align a model and log, first make sure there is a `results/` folder in <directory-path>, and run:

```
python main.py classic-alignments -p <directory-path> -l <log-name> -m <model-name>
```

- _directory-path_: path to the directory where log file, model file and the `results/` folder reside
- _log-name_: name of the log (.xes)
- _model-name_: name of the model (.pnml).
  
saves results of each alignment to a .csv file in `<directory-path>/results/<model-name>.csv`

Header: ['trace_idx', 'trace_length', 'time_taken', 'queued_states', 'visited_states', 'alignment_costs']

Timeout (in seconds) is adjustable for each single alignment. Change the value at: https://github.com/ariba-work/classic-pa/blob/d0ef3c037d8df8f4c35e7e9cdb76e20bfa7866a3/util/constants.py#L5
