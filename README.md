gdelt-tools
===========

## Aggregator

To use the aggregator right now use the following syntax from the command line:

```
python aggregator.py < data/train-sampled.csv --limit_rows 10000 > outfile.csv
```

### Options

- `-s` start year
- `-e` end year
- `-l` maximum number of rows to read in
- `-p` character that splits columns in input
- `-f` fill missing months with zeroes (True/False)
- `-d` specify header from separate file
- `--header_sep` like `-p` but for the `-d` file

## Subsetter

### Example usage

```
python subsetter.py < gdelt-file.txt -d header.txt --country2 AFG > subset.tsv
```

### Options 

- `-s` start year
- `-e` end year
- `-l` maximum number of rows to read in
- `-p` character that splits columns in input
- `-d` specify header from separate file
- `--header_sep` like `-p` but for the `-d` file
- `--country1` country desired in Actor1CountryCode column
- `--country2` country desired in Actor2CountryCode column

## Sampling 
To sample from a file: 
```
perl -ne 'print if (rand() < .01)' large_input_file.txt > sampled_output.txt
```