#!/usr/bin/env python3
"""
Dataset Generator for Compression Algorithm Comparison

This script generates various types of datasets to test different compression algorithms.
Data types include:
1. Text data (random text, repetitive text)
2. Binary data (random binary, structured binary)
3. JSON data (structured data with repetition)
4. CSV data (tabular data)
5. Image data (generated patterns)
"""

import os
import random
import string
import json
import csv
import numpy as np
from PIL import Image
import argparse

def ensure_dir(directory):
    """Ensure directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def generate_text_data(output_dir, size_mb=1, repetition_factor=0.2):
    """Generate text data files with varying degrees of repetition"""
    ensure_dir(output_dir)
    
    # Random text
    filename = os.path.join(output_dir, "random_text.txt")
    size_bytes = size_mb * 1024 * 1024
    chars = string.ascii_letters + string.digits + string.punctuation + " \n\t"
    
    with open(filename, 'w') as f:
        bytes_written = 0
        while bytes_written < size_bytes:
            # Generate a random chunk of text
            chunk_size = min(1024, size_bytes - bytes_written)
            random_text = ''.join(random.choice(chars) for _ in range(chunk_size))
            f.write(random_text)
            bytes_written += chunk_size
    
    print(f"Generated random text file: {filename}")
    
    # Repetitive text
    filename = os.path.join(output_dir, "repetitive_text.txt")
    
    # Create a set of repeated patterns
    patterns = [
        ''.join(random.choice(chars) for _ in range(random.randint(10, 50)))
        for _ in range(int(100 * repetition_factor))
    ]
    
    with open(filename, 'w') as f:
        bytes_written = 0
        while bytes_written < size_bytes:
            # Choose between a random pattern and truly random text
            if random.random() < repetition_factor:
                pattern = random.choice(patterns)
            else:
                pattern = ''.join(random.choice(chars) for _ in range(random.randint(5, 20)))
            
            f.write(pattern)
            bytes_written += len(pattern)
    
    print(f"Generated repetitive text file: {filename}")

def generate_binary_data(output_dir, size_mb=1):
    """Generate binary data files"""
    ensure_dir(output_dir)
    
    # Random binary
    filename = os.path.join(output_dir, "random_binary.bin")
    size_bytes = int(size_mb * 1024 * 1024)
    
    with open(filename, 'wb') as f:
        bytes_written = 0
        while bytes_written < size_bytes:
            # Generate random bytes
            chunk_size = min(1024, size_bytes - bytes_written)
            random_bytes = bytes([random.randint(0, 255) for _ in range(chunk_size)])
            f.write(random_bytes)
            bytes_written += chunk_size
    
    print(f"Generated random binary file: {filename}")
    
    # Structured binary (with patterns)
    filename = os.path.join(output_dir, "structured_binary.bin")
    
    with open(filename, 'wb') as f:
        bytes_written = 0
        while bytes_written < size_bytes:
            # Create structured data with patterns
            if random.random() < 0.7:  # 70% chance of a pattern
                pattern = bytes([random.randint(0, 255) for _ in range(random.randint(10, 30))])
                repeat = random.randint(5, 20)
                data = pattern * repeat
            else:
                # Random section
                data = bytes([random.randint(0, 255) for _ in range(random.randint(50, 100))])
            
            to_write = min(len(data), size_bytes - bytes_written)
            # Convert to_write to integer
            to_write = int(to_write)
            f.write(data[:to_write])
            bytes_written += to_write
    
    print(f"Generated structured binary file: {filename}")

def generate_json_data(output_dir, num_records=10000):
    """Generate JSON data file"""
    ensure_dir(output_dir)
    filename = os.path.join(output_dir, "data.json")
    
    # Define some common values that will be repeated
    common_names = ["John", "Jane", "Bob", "Alice", "Charlie", "David", "Eva", "Frank", "Grace", "Helen"]
    common_cities = ["New York", "London", "Tokyo", "Paris", "Berlin", "Sydney", "Toronto", "Moscow", "Beijing", "Delhi"]
    common_domains = ["example.com", "test.org", "domain.net", "site.io", "web.dev"]
    
    # Generate records
    records = []
    for i in range(num_records):
        record = {
            "id": i,
            "name": random.choice(common_names) + " " + ''.join(random.choice(string.ascii_uppercase) for _ in range(1)) + ".",
            "age": random.randint(18, 80),
            "email": f"user{i}@{random.choice(common_domains)}",
            "address": {
                "street": f"{random.randint(1, 999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple', 'Cedar'])} {random.choice(['St', 'Ave', 'Blvd', 'Rd'])}",
                "city": random.choice(common_cities),
                "zipcode": str(random.randint(10000, 99999))
            },
            "phone": f"+{random.randint(1, 99)}-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "tags": [random.choice(["work", "personal", "important", "urgent", "casual", "business", "family"]) for _ in range(random.randint(1, 5))],
            "active": random.choice([True, False])
        }
        records.append(record)
    
    with open(filename, 'w') as f:
        json.dump(records, f)
    
    print(f"Generated JSON file with {num_records} records: {filename}")

def generate_csv_data(output_dir, num_rows=100000):
    """Generate CSV data file"""
    ensure_dir(output_dir)
    filename = os.path.join(output_dir, "data.csv")
    
    # Define column headers and possible values for categorical columns
    headers = ['id', 'date', 'category', 'subcategory', 'value', 'quantity', 'status', 'region', 'notes']
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Sports', 'Home', 'Garden', 'Toys']
    subcategories = {
        'Electronics': ['Phones', 'Laptops', 'Cameras', 'Audio', 'TV', 'Gaming', 'Accessories'],
        'Clothing': ['Shirts', 'Pants', 'Dresses', 'Shoes', 'Jackets', 'Underwear', 'Socks'],
        'Food': ['Fruits', 'Vegetables', 'Meat', 'Dairy', 'Grains', 'Snacks', 'Drinks'],
        'Books': ['Fiction', 'Nonfiction', 'Science', 'History', 'Biography', 'Children', 'Reference'],
        'Sports': ['Football', 'Basketball', 'Tennis', 'Swimming', 'Cycling', 'Running', 'Yoga'],
        'Home': ['Furniture', 'Decor', 'Appliances', 'Bedding', 'Kitchen', 'Bathroom', 'Lighting'],
        'Garden': ['Plants', 'Tools', 'Fertilizers', 'Pots', 'Seeds', 'Ornaments', 'Irrigation'],
        'Toys': ['Action Figures', 'Dolls', 'Board Games', 'Puzzles', 'Outdoor', 'Educational', 'Plush']
    }
    statuses = ['Available', 'Out of Stock', 'Discontinued', 'Back Order', 'Pre-Order']
    regions = ['North', 'South', 'East', 'West', 'Central', 'Northeast', 'Southeast', 'Northwest', 'Southwest']
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for i in range(num_rows):
            category = random.choice(categories)
            subcategory = random.choice(subcategories[category])
            
            # Generate a date between 2018-2023
            year = random.randint(2018, 2023)
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # Simplified to avoid month length issues
            date = f"{year}-{month:02d}-{day:02d}"
            
            row = [
                i,  # id
                date,  # date
                category,  # category
                subcategory,  # subcategory
                round(random.uniform(1.0, 1000.0), 2),  # value
                random.randint(1, 100),  # quantity
                random.choice(statuses),  # status
                random.choice(regions),  # region
                'Sample product description ' + ''.join(random.choice(string.ascii_lowercase + ' ') for _ in range(random.randint(10, 50)))  # notes
            ]
            
            writer.writerow(row)
    
    print(f"Generated CSV file with {num_rows} rows: {filename}")

def generate_image_data(output_dir, size=1024):
    """Generate image data with different patterns"""
    ensure_dir(output_dir)
    
    # Generate a gradient image
    gradient = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            r = int(255 * i / size)
            g = int(255 * j / size)
            b = int(255 * (i + j) / (2 * size))
            gradient[i, j] = [r, g, b]
    
    img = Image.fromarray(gradient)
    filename = os.path.join(output_dir, "gradient.png")
    img.save(filename)
    print(f"Generated gradient image: {filename}")
    
    # Generate a pattern image
    pattern = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            pattern[i, j] = [
                (i % 64) * 4,
                (j % 64) * 4,
                ((i + j) % 64) * 4
            ]
    
    img = Image.fromarray(pattern)
    filename = os.path.join(output_dir, "pattern.png")
    img.save(filename)
    print(f"Generated pattern image: {filename}")
    
    # Generate a fractal-like image (simple)
    fractal = np.zeros((size, size, 3), dtype=np.uint8)
    for i in range(size):
        for j in range(size):
            x = i / size * 3 - 1.5
            y = j / size * 3 - 1.5
            c = x + y * 1j
            z = 0
            itermax = 20
            for n in range(itermax):
                if abs(z) > 2:
                    break
                z = z*z + c
            
            if n == itermax - 1:
                fractal[i, j] = [0, 0, 0]
            else:
                fractal[i, j] = [
                    n * 255 // itermax,
                    (n * 255 // itermax) // 2,
                    255 - (n * 255 // itermax)
                ]
    
    img = Image.fromarray(fractal)
    filename = os.path.join(output_dir, "fractal.png")
    img.save(filename)
    print(f"Generated fractal image: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Generate datasets for compression algorithm comparison')
    parser.add_argument('-o', '--output-dir', default='data', help='Output directory for datasets')
    parser.add_argument('--text-size', type=float, default=1.0, help='Size of text files in MB')
    parser.add_argument('--binary-size', type=float, default=1.0, help='Size of binary files in MB')
    parser.add_argument('--json-records', type=int, default=10000, help='Number of JSON records')
    parser.add_argument('--csv-rows', type=int, default=100000, help='Number of CSV rows')
    parser.add_argument('--image-size', type=int, default=1024, help='Size of generated images (pixels)')
    
    args = parser.parse_args()
    
    # Generate datasets
    print(f"Generating datasets in {args.output_dir}")
    generate_text_data(args.output_dir, size_mb=args.text_size)
    generate_binary_data(args.output_dir, size_mb=args.binary_size)
    generate_json_data(args.output_dir, num_records=args.json_records)
    generate_csv_data(args.output_dir, num_rows=args.csv_rows)
    generate_image_data(args.output_dir, size=args.image_size)
    
    print("Dataset generation complete!")

if __name__ == '__main__':
    main() 