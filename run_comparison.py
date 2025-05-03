#!/usr/bin/env python3
"""
Compression Comparison Runner Script

This script runs both the dataset generation and the compression comparison in sequence.
"""

import os
import sys
import argparse
import subprocess
import time

def run_command(command):
    """Run a command and print its output in real-time"""
    print(f"Running: {' '.join(command)}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    for line in process.stdout:
        print(line, end='')
    
    process.wait()
    
    if process.returncode != 0:
        print(f"Command failed with exit code {process.returncode}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Run the complete compression comparison pipeline')
    parser.add_argument('-i', '--input-dir', default='data', help='Input directory for datasets')
    parser.add_argument('-o', '--output-dir', default='results', help='Output directory for results')
    parser.add_argument('--text-size', type=float, default=1.0, help='Size of text files in MB')
    parser.add_argument('--binary-size', type=float, default=1.0, help='Size of binary files in MB')
    parser.add_argument('--json-records', type=int, default=10000, help='Number of JSON records')
    parser.add_argument('--csv-rows', type=int, default=100000, help='Number of CSV rows')
    parser.add_argument('--image-size', type=int, default=1024, help='Size of generated images (pixels)')
    parser.add_argument('--skip-generation', action='store_true', help='Skip dataset generation step')
    
    args = parser.parse_args()
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Step 1: Generate datasets (if not skipped)
    if not args.skip_generation:
        print("\n=== Step 1: Generating datasets ===\n")
        dataset_script = os.path.join(script_dir, "generate_datasets.py")
        
        dataset_cmd = [
            sys.executable, dataset_script,
            "--output-dir", args.input_dir,
            "--text-size", str(args.text_size),
            "--binary-size", str(args.binary_size),
            "--json-records", str(args.json_records),
            "--csv-rows", str(args.csv_rows),
            "--image-size", str(args.image_size)
        ]
        
        if not run_command(dataset_cmd):
            print("Dataset generation failed. Exiting.")
            sys.exit(1)
    else:
        print("\n=== Skipping dataset generation ===\n")
    
    # Step 2: Run compression comparison
    print("\n=== Step 2: Running compression comparison ===\n")
    comparison_script = os.path.join(script_dir, "compression_comparison.py")
    
    comparison_cmd = [
        sys.executable, comparison_script,
        "--input-dir", args.input_dir,
        "--output-dir", args.output_dir
    ]
    
    if not run_command(comparison_cmd):
        print("Compression comparison failed. Exiting.")
        sys.exit(1)
    
    print("\n=== Compression comparison pipeline completed successfully! ===\n")
    print(f"Results saved to the '{args.output_dir}' directory.")

if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed_time = time.time() - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds") 