# remisol-log-condenser

A small project to clean up Remisol Viewer logs.  Remisol is a Normand/Beckman Coulter LIS product and sometimes I need to pull a ton of log data to review.  This script essentially converts the text file into an Excel file that is easier to read and sort/filter.

## Dependencies

* [Python](https://www.python.org/)
* [openpyxl](https://pypi.org/project/openpyxl/)

## Installation

Be sure to install the dependencies

```
pip install -r requirements.txt
```

## Usage

Collect the Viewer log files.

Extract the contents into a new directory.

Run the script for a single file:

```
# runs the script for a specific file
python3 reimsol-log-condenser.py -i <inputfile> -o <outputfile>
```

Do note that you must include the .xlsx file extension for the output file.

Or process the entire directory:

```
# runs the script for an entire directory
python3 remisol-log-condenser.py -d <directory>
```

## Contributing

Open a pull request I guess.

## License

GNU General Public License v3.0

## Contributors

[alesparza](https://github.com/alesparza)


