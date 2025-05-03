#!/usr/bin/env python3
"""
Compression Algorithm Comparison - Main Entry Point

This script serves as the main entry point for the compression algorithm comparison project.
It provides a simple command-line interface to run the project components.
"""

import os
import sys
import argparse
from run_comparison import main as run_comparison_main

def print_header():
    """Print a header for the application"""
    print("\n" + "=" * 80)
    print("Compression Algorithm Comparison Tool".center(80))
    print("Comparing gzip, bzip2, and LZMA algorithms".center(80))
    print("=" * 80 + "\n")

def main():
    """Main entry point for the application"""
    print_header()
    
    parser = argparse.ArgumentParser(
        description='Compression Algorithm Comparison Tool',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument('--version', action='version', version='Compression Algorithm Comparison v1.0.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Generate datasets command
    generate_parser = subparsers.add_parser('generate', help='Generate test datasets')
    generate_parser.add_argument('-o', '--output-dir', default='data', help='Output directory for datasets')
    generate_parser.add_argument('--text-size', type=float, default=1.0, help='Size of text files in MB')
    generate_parser.add_argument('--binary-size', type=float, default=1.0, help='Size of binary files in MB')
    generate_parser.add_argument('--json-records', type=int, default=10000, help='Number of JSON records')
    generate_parser.add_argument('--csv-rows', type=int, default=100000, help='Number of CSV rows')
    generate_parser.add_argument('--image-size', type=int, default=1024, help='Size of generated images (pixels)')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Run compression comparison')
    compare_parser.add_argument('-i', '--input-dir', default='data', help='Input directory for datasets')
    compare_parser.add_argument('-o', '--output-dir', default='results', help='Output directory for results')
    
    # Run all command (generate + compare)
    run_all_parser = subparsers.add_parser('run-all', help='Run the complete pipeline (generate + compare)')
    run_all_parser.add_argument('-i', '--input-dir', default='data', help='Input directory for datasets')
    run_all_parser.add_argument('-o', '--output-dir', default='results', help='Output directory for results')
    run_all_parser.add_argument('--text-size', type=float, default=1.0, help='Size of text files in MB')
    run_all_parser.add_argument('--binary-size', type=float, default=1.0, help='Size of binary files in MB')
    run_all_parser.add_argument('--json-records', type=int, default=10000, help='Number of JSON records')
    run_all_parser.add_argument('--csv-rows', type=int, default=100000, help='Number of CSV rows')
    run_all_parser.add_argument('--image-size', type=int, default=1024, help='Size of generated images (pixels)')
    
    args = parser.parse_args()
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.command == 'generate':
        # Import and run the dataset generator
        from generate_datasets import main as generate_main
        sys.argv = [
            sys.argv[0],
            '--output-dir', args.output_dir,
            '--text-size', str(args.text_size),
            '--binary-size', str(args.binary_size),
            '--json-records', str(args.json_records),
            '--csv-rows', str(args.csv_rows),
            '--image-size', str(args.image_size)
        ]
        generate_main()
    
    elif args.command == 'compare':
        # Import and run the compression comparison
        from compression_comparison import main as compare_main
        sys.argv = [
            sys.argv[0],
            '--input-dir', args.input_dir,
            '--output-dir', args.output_dir
        ]
        compare_main()
    
    elif args.command == 'run-all':
        # Run the complete pipeline
        sys.argv = [
            sys.argv[0],
            '--input-dir', args.input_dir,
            '--output-dir', args.output_dir,
            '--text-size', str(args.text_size),
            '--binary-size', str(args.binary_size),
            '--json-records', str(args.json_records),
            '--csv-rows', str(args.csv_rows),
            '--image-size', str(args.image_size)
        ]
        run_comparison_main()
    
    else:
        # If no command is provided, show help
        parser.print_help()

if __name__ == '__main__':
    main() 