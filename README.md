# Compression Algorithm Comparison

This project compares the performance of different compression algorithms (gzip, bzip2, and LZMA) on various types of data.

## Features

- Compares multiple compression algorithms (gzip, bzip2, LZMA)
- Analyzes compression ratio, compression time, decompression time, and space savings
- Generates comprehensive reports with tables and visualizations
- Includes a dataset generator for creating test data of different types

## Dataset Types

The dataset generator can create the following types of data:

1. Text data
   - Random text (low compression potential)
   - Repetitive text (high compression potential)

2. Binary data
   - Random binary (low compression potential)
   - Structured binary with patterns (medium compression potential)

3. JSON data
   - Structured data with repeated fields and values (high compression potential)

4. CSV data
   - Tabular data with repeating categories (medium-high compression potential)

5. Image data
   - Gradient patterns
   - Regular patterns
   - Fractal-like patterns

## Installation

```bash
# Clone the repository
# Navigate to the project directory
cd compression_comparison

# Install dependencies
pip install -r requirements.txt
```

## Usage

There are multiple ways to run the project:

### Option 1: Using the main entry point

The simplest way to run the project is using the `main.py` entry point:

```bash
# Show available commands
python main.py

# Generate datasets only
python main.py generate --output-dir data --text-size 2 --binary-size 2

# Run comparison only
python main.py compare --input-dir data --output-dir results

# Run the complete pipeline (generate + compare)
python main.py run-all --input-dir data --output-dir results --text-size 2 --binary-size 2
```

### Option 2: Step by step

#### Step 1: Generate datasets

Generate various test datasets:

```bash
python generate_datasets.py --output-dir data --text-size 2 --binary-size 2 --json-records 5000 --csv-rows 50000 --image-size 1024
```

Parameters:
- `--output-dir`: Directory to save generated datasets (default: 'data')
- `--text-size`: Size of text files in MB (default: 1.0)
- `--binary-size`: Size of binary files in MB (default: 1.0)
- `--json-records`: Number of JSON records to generate (default: 10000)
- `--csv-rows`: Number of CSV rows to generate (default: 100000)
- `--image-size`: Size of generated images in pixels (default: 1024)

#### Step 2: Run compression comparison

Run the comparison on all files in the data directory:

```bash
python compression_comparison.py --input-dir data --output-dir results
```

Parameters:
- `--input-dir`: Input directory containing files to compress (default: 'data')
- `--output-dir`: Output directory for results (default: 'results')

### Option 3: Using the combined runner

Run both steps in sequence:

```bash
python run_comparison.py --input-dir data --output-dir results --text-size 2 --binary-size 2
```

Additional parameter:
- `--skip-generation`: Skip the dataset generation step and only run the comparison

## Results

After running the comparison, you'll find:

1. Compressed versions of each input file using each algorithm
2. A CSV file with detailed results
3. A PNG file with visualizations of the comparison
4. A summary table displayed in the console

## Example Output

```
Compression Algorithm Comparison Summary:
+----------+--------------------+----------------------+------------------------+------------------+
| Algorithm | Compression Ratio | Compression Time (s) | Decompression Time (s) | Space Saving (%) |
+----------+--------------------+----------------------+------------------------+------------------+
| gzip     |           2.3456   |            0.1234    |              0.0567    |        57.4567   |
| bzip2    |           2.8765   |            0.2345    |              0.0892    |        65.2345   |
| lzma     |           3.4567   |            0.3456    |              0.1123    |        71.0123   |
+----------+--------------------+----------------------+------------------------+------------------+
```

## Project Structure

```
compression_comparison/
├── main.py                     # Main entry point
├── compression_comparison.py   # Compression comparison tool
├── generate_datasets.py        # Dataset generator
├── run_comparison.py           # Combined runner script
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
├── data/                       # Directory for input datasets
└── results/                    # Directory for output results
```

## License

MIT # BLG374EProject
