gdelt-tools
===========
This package provides some command line tools for working iwth GDELT data.  It assumes that you are comfortable with [Unix style IO Redirection](http://www.tuxfiles.org/linuxhelp/iodirection.html).  Note if you are using raw GDELT files you can port multiple files into stdin via wildcards (e.g. *.export.csv)

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

### Sampling
To sample from a file:
```
perl -ne 'print if (rand() < .01)' large_input_file.txt > sampled_output.txt
```
Note that the 0.01 yields 1% of the rows.