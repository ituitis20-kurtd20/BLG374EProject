#!/usr/bin/env python3
"""
Compression Algorithm Comparison Tool

This script compares the performance of multiple compression algorithms 
(gzip, bzip2, and LZMA) on various types of data.

Author: Doruk Kurt
"""

import os
import time
import gzip
import bz2
import lzma
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from tabulate import tabulate
from datetime import datetime
import re

class CompressionComparison:
    """Class to compare different compression algorithms"""
    
    def __init__(self, input_dir="data", output_dir="results"):
        """Initialize the compression comparison tool"""
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.results = []
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def compress_file(self, file_path):
        """Compress a file using different algorithms and measure performance"""
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        # Determine file type based on extension or filename pattern
        file_type = self._determine_file_type(file_name)
        
        with open(file_path, 'rb') as f:
            data = f.read()
        
        algorithms = {
            'gzip': (gzip.compress, '.gz'),
            'bzip2': (bz2.compress, '.bz2'),
            'lzma': (lzma.compress, '.xz')
        }
        
        file_results = []
        
        for algo_name, (compress_func, extension) in algorithms.items():
            # Measure compression time
            start_time = time.time()
            compressed_data = compress_func(data)
            compression_time = time.time() - start_time
            
            # Calculate compression ratio
            compressed_size = len(compressed_data)
            compression_ratio = file_size / compressed_size if compressed_size > 0 else 0
            
            # Measure decompression time
            if algo_name == 'gzip':
                decompress_func = gzip.decompress
            elif algo_name == 'bzip2':
                decompress_func = bz2.decompress
            else:  # lzma
                decompress_func = lzma.decompress
            
            start_time = time.time()
            decompressed_data = decompress_func(compressed_data)
            decompression_time = time.time() - start_time
            
            # Save compressed file
            compressed_file_path = os.path.join(self.output_dir, file_name + extension)
            with open(compressed_file_path, 'wb') as f:
                f.write(compressed_data)
            
            # Store results
            result = {
                'File': file_name,
                'File Type': file_type,
                'Original Size (bytes)': file_size,
                'Algorithm': algo_name,
                'Compressed Size (bytes)': compressed_size,
                'Compression Ratio': compression_ratio,
                'Compression Time (s)': compression_time,
                'Decompression Time (s)': decompression_time,
                'Space Saving (%)': (1 - (compressed_size / file_size)) * 100 if file_size > 0 else 0,
                'Compression Speed (MB/s)': (file_size / 1024 / 1024) / compression_time if compression_time > 0 else 0,
                'Decompression Speed (MB/s)': (file_size / 1024 / 1024) / decompression_time if decompression_time > 0 else 0
            }
            
            file_results.append(result)
            self.results.append(result)
        
        return file_results
    
    def _determine_file_type(self, file_name):
        """Determine the type of file based on its name or extension"""
        # Check by extension
        if file_name.endswith('.txt'):
            if 'random' in file_name:
                return 'Random Text'
            elif 'repetitive' in file_name:
                return 'Repetitive Text'
            else:
                return 'Text'
        elif file_name.endswith('.bin'):
            if 'random' in file_name:
                return 'Random Binary'
            elif 'structured' in file_name:
                return 'Structured Binary'
            else:
                return 'Binary'
        elif file_name.endswith('.json'):
            return 'JSON'
        elif file_name.endswith('.csv'):
            return 'CSV'
        elif file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            if 'gradient' in file_name:
                return 'Gradient Image'
            elif 'pattern' in file_name:
                return 'Pattern Image'
            elif 'fractal' in file_name:
                return 'Fractal Image'
            else:
                return 'Image'
        else:
            # Try to infer from name
            if 'text' in file_name.lower():
                return 'Text'
            elif 'binary' in file_name.lower():
                return 'Binary'
            elif 'json' in file_name.lower():
                return 'JSON'
            elif 'csv' in file_name.lower():
                return 'CSV'
            elif any(img in file_name.lower() for img in ['image', 'img', 'picture', 'photo']):
                return 'Image'
            
            # Default
            return 'Other'
    
    def run_comparison(self):
        """Run compression comparison on all files in the input directory"""
        files = [os.path.join(self.input_dir, f) for f in os.listdir(self.input_dir) 
                 if os.path.isfile(os.path.join(self.input_dir, f))]
        
        if not files:
            print(f"No files found in {self.input_dir}")
            return
        
        for file_path in files:
            print(f"Processing: {file_path}")
            self.compress_file(file_path)
        
        self.generate_report()
    
    def generate_report(self):
        """Generate a comprehensive report of the compression comparison"""
        if not self.results:
            print("No results to report")
            return
        
        # Convert results to DataFrame
        df = pd.DataFrame(self.results)
        
        # Save results to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = os.path.join(self.output_dir, f"compression_results_{timestamp}.csv")
        df.to_csv(csv_file, index=False)
        print(f"Results saved to: {csv_file}")
        
        # Print summary table by algorithm
        algo_summary = df.groupby('Algorithm').agg({
            'Compression Ratio': 'mean',
            'Compression Time (s)': 'mean',
            'Decompression Time (s)': 'mean',
            'Space Saving (%)': 'mean',
            'Compression Speed (MB/s)': 'mean',
            'Decompression Speed (MB/s)': 'mean'
        }).reset_index()
        
        print("\nCompression Algorithm Comparison Summary:")
        print(tabulate(algo_summary, headers='keys', tablefmt='grid', floatfmt='.4f'))
        
        # Print summary table by file type and algorithm
        type_algo_summary = df.groupby(['File Type', 'Algorithm']).agg({
            'Compression Ratio': 'mean',
            'Space Saving (%)': 'mean'
        }).reset_index()
        
        print("\nCompression Ratio by File Type and Algorithm:")
        print(tabulate(type_algo_summary, headers='keys', tablefmt='grid', floatfmt='.4f'))
        
        # Generate plots
        self._generate_general_plots(df, timestamp)
        self._generate_per_file_type_plots(df, timestamp)
        self._generate_per_file_plots(df, timestamp)
    
    def _generate_general_plots(self, df, timestamp):
        """Generate general plots comparing algorithms across all data"""
        # Set a modern style for plots
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Create a figure with multiple subplots
        fig, axs = plt.subplots(2, 3, figsize=(20, 14), dpi=100)
        fig.suptitle('Compression Algorithm Comparison - Overall Performance', fontsize=22, fontweight='bold', y=0.98)
        
        # Color palette
        colors = ['#3498db', '#e74c3c', '#2ecc71']
        
        # Plot 1: Compression Ratio by Algorithm
        avg_ratio = df.groupby('Algorithm')['Compression Ratio'].mean()
        bars1 = axs[0, 0].bar(avg_ratio.index, avg_ratio.values, color=colors, alpha=0.8)
        axs[0, 0].set_title('Average Compression Ratio', fontsize=16, pad=10)
        axs[0, 0].set_ylabel('Compression Ratio\n(higher is better)', fontsize=14)
        
        # Add value labels on top of bars
        for bar in bars1:
            height = bar.get_height()
            axs[0, 0].annotate(f'{height:.2f}x',
                              xy=(bar.get_x() + bar.get_width() / 2, height),
                              xytext=(0, 3),  # 3 points vertical offset
                              textcoords="offset points",
                              ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Add explanatory note
        axs[0, 0].text(0.5, -0.15, 'Higher ratio means better compression efficiency', 
                      transform=axs[0, 0].transAxes, ha='center', fontsize=11, style='italic')
        
        # Plot 2: Compression Time by Algorithm
        avg_comp_time = df.groupby('Algorithm')['Compression Time (s)'].mean()
        bars2 = axs[0, 1].bar(avg_comp_time.index, avg_comp_time.values, color=colors, alpha=0.8)
        axs[0, 1].set_title('Average Compression Time', fontsize=16, pad=10)
        axs[0, 1].set_ylabel('Time (seconds)\n(lower is better)', fontsize=14)
        
        # Add value labels
        for bar in bars2:
            height = bar.get_height()
            axs[0, 1].annotate(f'{height:.4f}s',
                              xy=(bar.get_x() + bar.get_width() / 2, height),
                              xytext=(0, 3),
                              textcoords="offset points",
                              ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Plot 3: Decompression Time by Algorithm
        avg_decomp_time = df.groupby('Algorithm')['Decompression Time (s)'].mean()
        bars3 = axs[0, 2].bar(avg_decomp_time.index, avg_decomp_time.values, color=colors, alpha=0.8)
        axs[0, 2].set_title('Average Decompression Time', fontsize=16, pad=10)
        axs[0, 2].set_ylabel('Time (seconds)\n(lower is better)', fontsize=14)
        
        # Add value labels
        for bar in bars3:
            height = bar.get_height()
            axs[0, 2].annotate(f'{height:.4f}s',
                              xy=(bar.get_x() + bar.get_width() / 2, height),
                              xytext=(0, 3),
                              textcoords="offset points",
                              ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Plot 4: Space Saving by Algorithm
        avg_space_saving = df.groupby('Algorithm')['Space Saving (%)'].mean()
        bars4 = axs[1, 0].bar(avg_space_saving.index, avg_space_saving.values, color=colors, alpha=0.8)
        axs[1, 0].set_title('Average Space Saving', fontsize=16, pad=10)
        axs[1, 0].set_ylabel('Space Saving (%)', fontsize=14)
        
        # Add value labels
        for bar in bars4:
            height = bar.get_height()
            axs[1, 0].annotate(f'{height:.1f}%',
                              xy=(bar.get_x() + bar.get_width() / 2, height),
                              xytext=(0, 3),
                              textcoords="offset points",
                              ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Plot 5: Compression Speed
        avg_comp_speed = df.groupby('Algorithm')['Compression Speed (MB/s)'].mean()
        bars5 = axs[1, 1].bar(avg_comp_speed.index, avg_comp_speed.values, color=colors, alpha=0.8)
        axs[1, 1].set_title('Average Compression Speed', fontsize=16, pad=10)
        axs[1, 1].set_ylabel('Speed (MB/s)\n(higher is better)', fontsize=14)
        
        # Add value labels
        for bar in bars5:
            height = bar.get_height()
            axs[1, 1].annotate(f'{height:.1f} MB/s',
                              xy=(bar.get_x() + bar.get_width() / 2, height),
                              xytext=(0, 3),
                              textcoords="offset points",
                              ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Plot 6: Decompression Speed
        avg_decomp_speed = df.groupby('Algorithm')['Decompression Speed (MB/s)'].mean()
        bars6 = axs[1, 2].bar(avg_decomp_speed.index, avg_decomp_speed.values, color=colors, alpha=0.8)
        axs[1, 2].set_title('Average Decompression Speed', fontsize=16, pad=10)
        axs[1, 2].set_ylabel('Speed (MB/s)\n(higher is better)', fontsize=14)
        
        # Add value labels
        for bar in bars6:
            height = bar.get_height()
            axs[1, 2].annotate(f'{height:.1f} MB/s',
                              xy=(bar.get_x() + bar.get_width() / 2, height),
                              xytext=(0, 3),
                              textcoords="offset points",
                              ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Add overall insights
        # Find best algorithm for each metric
        best_ratio = avg_ratio.idxmax()
        best_comp_time = avg_comp_time.idxmin()
        best_decomp_time = avg_decomp_time.idxmin()
        best_space = avg_space_saving.idxmax()
        
        insights = (
            f"Key Insights:\n"
            f"• Best compression ratio: {best_ratio} ({avg_ratio.max():.2f}x)\n"
            f"• Fastest compression: {best_comp_time} ({avg_comp_time.min():.4f}s)\n"
            f"• Fastest decompression: {best_decomp_time} ({avg_decomp_time.min():.4f}s)\n"
            f"• Best space saving: {best_space} ({avg_space_saving.max():.1f}%)"
        )
        
        fig.text(0.5, 0.01, insights, ha='center', va='bottom', fontsize=14, 
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.5))
        
        # Add a footer with timestamp
        fig.text(0.99, 0.01, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                ha='right', va='bottom', fontsize=8, color='gray')
        
        # Adjust layout
        plt.tight_layout()
        plt.subplots_adjust(top=0.92, bottom=0.12)
        
        # Save the plot
        plot_file = os.path.join(self.output_dir, f"compression_comparison_overall_{timestamp}.png")
        plt.savefig(plot_file, bbox_inches='tight')
        plt.close()
        print(f"Overall comparison plots saved to: {plot_file}")
    
    def _generate_per_file_type_plots(self, df, timestamp):
        """Generate plots comparing algorithms for each file type"""
        # Set a modern style for plots
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Get unique file types
        file_types = df['File Type'].unique()
        
        # Create a figure with subplots for each metric
        metrics = ['Compression Ratio', 'Space Saving (%)', 'Compression Time (s)', 'Decompression Time (s)']
        metric_descriptions = {
            'Compression Ratio': 'Higher is better - shows how many times smaller the compressed file is',
            'Space Saving (%)': 'Higher is better - percentage of space saved by compression',
            'Compression Time (s)': 'Lower is better - time taken to compress data',
            'Decompression Time (s)': 'Lower is better - time taken to decompress data'
        }
        
        for metric in metrics:
            # Create a figure
            plt.figure(figsize=(16, 10), dpi=100)
            
            # Prepare data for grouped bar chart
            pivot_data = df.pivot_table(
                index='File Type', 
                columns='Algorithm', 
                values=metric,
                aggfunc='mean'
            )
            
            # Sort data for better visualization (based on the metric)
            if metric in ['Compression Ratio', 'Space Saving (%)']:
                # For these metrics, higher is better
                pivot_data = pivot_data.sort_values(by=pivot_data.columns[0], ascending=False)
            else:
                # For time metrics, lower is better
                pivot_data = pivot_data.sort_values(by=pivot_data.columns[0], ascending=True)
            
            # Plot grouped bar chart with custom colors
            ax = pivot_data.plot(
                kind='bar', 
                figsize=(16, 10),
                color=['#3498db', '#e74c3c', '#2ecc71'],
                width=0.8,
                edgecolor='white',
                linewidth=1
            )
            
            # Add value labels on the bars
            for container in ax.containers:
                ax.bar_label(container, fmt='%.2f', fontsize=9, fontweight='bold')
            
            # Add titles and labels
            ax.set_title(f'Comparison of {metric} by File Type', fontsize=20, pad=20)
            ax.set_ylabel(metric, fontsize=14)
            ax.set_xlabel('File Type', fontsize=14)
            
            # Add a description of the metric
            plt.figtext(0.5, 0.01, metric_descriptions.get(metric, ''), 
                       ha='center', fontsize=12, style='italic')
            
            # Highlight best performer for each file type
            if pivot_data.shape[0] > 0:  # Make sure there's data
                # Find best algorithm for each file type
                if metric in ['Compression Ratio', 'Space Saving (%)']:
                    best_algo = pivot_data.idxmax(axis=1)
                    best_values = pivot_data.max(axis=1)
                    comparison = "Best"
                else:
                    best_algo = pivot_data.idxmin(axis=1)
                    best_values = pivot_data.min(axis=1)
                    comparison = "Fastest"
                
                # Create insights text
                insights = f"{comparison} Algorithm by File Type:\n"
                for idx, (file_type, algo) in enumerate(best_algo.items()):
                    if idx < 10:  # Limit to 10 entries to avoid cluttering
                        if pd.notna(algo):  # Check if algorithm is not NaN
                            value = best_values.loc[file_type]
                            insights += f"• {file_type}: {algo} ({value:.2f})\n"
                
                # Add insights box
                plt.figtext(0.01, 0.02, insights, fontsize=12, 
                           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.5))
            
            # Adjust layout
            plt.tight_layout()
            plt.subplots_adjust(bottom=0.15)
            
            # Add a footer with timestamp
            plt.figtext(0.99, 0.01, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                       ha='right', va='bottom', fontsize=8, color='gray')
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha='right')
            
            # Add grids for easier reading
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Save the plot
            plot_file = os.path.join(self.output_dir, f"comparison_by_file_type_{metric.replace(' ', '_').replace('(', '').replace(')', '')}_{timestamp}.png")
            plt.savefig(plot_file, bbox_inches='tight')
            plt.close()
            print(f"File type comparison for {metric} saved to: {plot_file}")
            
        # Generate a heatmap visualization for compression ratio
        plt.figure(figsize=(14, 10), dpi=100)
        heatmap_data = df.pivot_table(
            index='File Type', 
            columns='Algorithm', 
            values='Compression Ratio',
            aggfunc='mean'
        )
        
        # Sort by the average compression ratio
        mean_vals = heatmap_data.mean(axis=1)
        heatmap_data = heatmap_data.loc[mean_vals.sort_values(ascending=False).index]
        
        # Plot heatmap using seaborn
        ax = sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="YlGnBu", linewidths=.5, cbar_kws={'label': 'Compression Ratio'})
        
        plt.title('Compression Ratio Heatmap by File Type and Algorithm', fontsize=18, pad=20)
        plt.xlabel('Algorithm', fontsize=14)
        plt.ylabel('File Type', fontsize=14)
        
        plt.tight_layout()
        
        # Save the heatmap
        heatmap_file = os.path.join(self.output_dir, f"compression_ratio_heatmap_{timestamp}.png")
        plt.savefig(heatmap_file, bbox_inches='tight')
        plt.close()
        print(f"Compression ratio heatmap saved to: {heatmap_file}")
    
    def _generate_per_file_plots(self, df, timestamp):
        """Generate detailed plots for each individual file"""
        # Set a modern style for plots
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Get unique files
        files = df['File'].unique()
        
        for file in files:
            # Filter data for this file
            file_df = df[df['File'] == file]
            file_type = file_df['File Type'].iloc[0]
            
            # Create a figure with multiple subplots
            fig, axs = plt.subplots(2, 2, figsize=(16, 14), dpi=100)
            fig.suptitle(f'Compression Analysis: {file}', fontsize=22, fontweight='bold', y=0.98)
            
            # Colors for the algorithms
            colors = ['#3498db', '#e74c3c', '#2ecc71']
            
            # Plot 1: Compression Ratio by Algorithm
            bars1 = axs[0, 0].bar(file_df['Algorithm'], file_df['Compression Ratio'], color=colors, alpha=0.8)
            axs[0, 0].set_title('Compression Ratio', fontsize=16, pad=10)
            axs[0, 0].set_ylabel('Compression Ratio\n(higher is better)', fontsize=14)
            
            # Add value labels
            for bar in bars1:
                height = bar.get_height()
                axs[0, 0].annotate(f'{height:.2f}x',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),
                                textcoords="offset points",
                                ha='center', va='bottom', fontsize=12, fontweight='bold')
            
            # Plot 2: Space Saving by Algorithm
            bars2 = axs[0, 1].bar(file_df['Algorithm'], file_df['Space Saving (%)'], color=colors, alpha=0.8)
            axs[0, 1].set_title('Space Saving', fontsize=16, pad=10)
            axs[0, 1].set_ylabel('Space Saving (%)', fontsize=14)
            
            # Add value labels
            for bar in bars2:
                height = bar.get_height()
                axs[0, 1].annotate(f'{height:.1f}%',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),
                                textcoords="offset points",
                                ha='center', va='bottom', fontsize=12, fontweight='bold')
            
            # Plot 3: Compression & Decompression Time
            x = np.arange(len(file_df['Algorithm']))
            width = 0.35
            
            # Compression time bars
            comp_bars = axs[1, 0].bar(x - width/2, file_df['Compression Time (s)'], width, label='Compression', color='#3498db', alpha=0.8)
            # Decompression time bars
            decomp_bars = axs[1, 0].bar(x + width/2, file_df['Decompression Time (s)'], width, label='Decompression', color='#e74c3c', alpha=0.8)
            
            axs[1, 0].set_title('Processing Time Comparison', fontsize=16, pad=10)
            axs[1, 0].set_ylabel('Time (seconds)\n(lower is better)', fontsize=14)
            axs[1, 0].set_xticks(x)
            axs[1, 0].set_xticklabels(file_df['Algorithm'])
            axs[1, 0].legend()
            
            # Add value labels
            for bars in [comp_bars, decomp_bars]:
                for bar in bars:
                    height = bar.get_height()
                    axs[1, 0].annotate(f'{height:.4f}s',
                                     xy=(bar.get_x() + bar.get_width() / 2, height),
                                     xytext=(0, 3),
                                     textcoords="offset points",
                                     ha='center', va='bottom', fontsize=9, fontweight='bold')
            
            # Plot 4: File Size Comparison
            sizes = [file_df['Original Size (bytes)'].iloc[0]] + list(file_df['Compressed Size (bytes)'])
            labels = ['Original'] + list(file_df['Algorithm'])
            colors = ['#95a5a6'] + colors  # Gray for original, colors for algorithms
            
            bars4 = axs[1, 1].bar(labels, sizes, color=colors, alpha=0.8)
            axs[1, 1].set_title('File Size Comparison', fontsize=16, pad=10)
            axs[1, 1].set_ylabel('Size (bytes)', fontsize=14)
            
            # Add value labels with formatting for better readability
            for bar in bars4:
                height = bar.get_height()
                # Format bytes for better readability
                if height >= 1_000_000:
                    label = f'{height/1_000_000:.2f} MB'
                elif height >= 1_000:
                    label = f'{height/1_000:.2f} KB'
                else:
                    label = f'{height:.0f} B'
                
                axs[1, 1].annotate(label,
                                  xy=(bar.get_x() + bar.get_width() / 2, height),
                                  xytext=(0, 3),
                                  textcoords="offset points",
                                  ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            # Add file details as a rich text box
            file_type = file_df['File Type'].iloc[0]
            original_size = file_df['Original Size (bytes)'].iloc[0]
            
            # Format original size for readability
            if original_size >= 1_000_000:
                size_str = f"{original_size/1_000_000:.2f} MB"
            elif original_size >= 1_000:
                size_str = f"{original_size/1_000:.2f} KB"
            else:
                size_str = f"{original_size} bytes"
            
            # Find best algorithm for this file type (based on compression ratio)
            best_algo = file_df.loc[file_df['Compression Ratio'].idxmax()]['Algorithm']
            best_ratio = file_df['Compression Ratio'].max()
            
            details = (
                f"File: {file}\n"
                f"Type: {file_type}\n"
                f"Size: {size_str}\n"
                f"Best Algorithm: {best_algo} ({best_ratio:.2f}x compression)"
            )
            
            fig.text(0.02, 0.02, details, fontsize=12, 
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.5))
            
            # Add timestamp
            fig.text(0.99, 0.01, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                    ha='right', va='bottom', fontsize=8, color='gray')
            
            # Adjust layout
            plt.tight_layout()
            plt.subplots_adjust(top=0.92, bottom=0.12)
            
            # Save the plot
            safe_filename = re.sub(r'[^\w\-_]', '_', file)  # Replace non-word chars with underscore
            plot_file = os.path.join(self.output_dir, f"compression_file_{safe_filename}_{timestamp}.png")
            plt.savefig(plot_file, bbox_inches='tight')
            plt.close()
            print(f"File-specific plots for {file} saved to: {plot_file}")
        
        # Generate a summary comparison across all files
        self._generate_file_comparison_summary(df, timestamp)

    def _generate_file_comparison_summary(self, df, timestamp):
        """Generate a summary visualization comparing compression across all files"""
        # Set a modern style for plots
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Create a figure for the summary
        plt.figure(figsize=(16, 12), dpi=100)
        
        # Get unique files and algorithms
        files = df['File'].unique()
        algorithms = df['Algorithm'].unique()
        
        # Create a DataFrame to hold the compression ratios for each file and algorithm
        summary_data = df.pivot_table(
            index='File', 
            columns='Algorithm', 
            values='Compression Ratio',
            aggfunc='mean'
        )
        
        # Sort by the average compression ratio across all algorithms
        mean_vals = summary_data.mean(axis=1)
        summary_data = summary_data.loc[mean_vals.sort_values(ascending=False).index]
        
        # Create a new column for file types (for coloring)
        file_types = {}
        for file in files:
            file_type = df[df['File'] == file]['File Type'].iloc[0]
            file_types[file] = file_type
        
        summary_data['File Type'] = pd.Series(file_types)
        
        # Define a colormap based on file types
        unique_types = sorted(summary_data['File Type'].unique())
        colors = plt.cm.tab10(np.linspace(0, 1, len(unique_types)))
        color_map = dict(zip(unique_types, colors))
        
        # Create bar colors based on file type
        bar_colors = [color_map[file_type] for file_type in summary_data['File Type']]
        
        # Plot the data
        ax = summary_data[algorithms].plot(
            kind='bar',
            figsize=(16, 12),
            width=0.8,
            color=['#3498db', '#e74c3c', '#2ecc71'],
            edgecolor='white',
            linewidth=1
        )
        
        # Add value labels on the bars (for the best algorithm only)
        max_vals = summary_data[algorithms].max(axis=1)
        for i, (file, max_val) in enumerate(max_vals.items()):
            best_algo = summary_data.loc[file, algorithms].idxmax()
            idx = list(algorithms).index(best_algo)
            x_pos = i + (idx - 1) * 0.25  # Adjust this based on your bar positioning
            plt.annotate(f'{max_val:.2f}x',
                        xy=(i, max_val),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Add titles and labels
        plt.title('Compression Ratio Comparison Across All Files', fontsize=20, pad=20)
        plt.ylabel('Compression Ratio (higher is better)', fontsize=14)
        plt.xlabel('File', fontsize=14)
        
        # Create a custom legend for file types
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=color_map[file_type],
                                edgecolor='black',
                                label=file_type) for file_type in unique_types]
        
        ax.legend(title='Algorithm', loc='upper right')
        plt.legend(handles=legend_elements, title='File Type', loc='center left', bbox_to_anchor=(1, 0.5))
        
        # Add insights
        best_overall = summary_data[algorithms].max().max()
        best_file = summary_data[algorithms].max(axis=1).idxmax()
        best_algo_overall = summary_data.loc[best_file, algorithms].idxmax()
        
        worst_overall = summary_data[algorithms].max(axis=1).min()
        worst_file = summary_data[algorithms].max(axis=1).idxmin()
        
        insights = (
            f"Key Insights:\n"
            f"• Best compression: {best_file} with {best_algo_overall} ({best_overall:.2f}x)\n"
            f"• Lowest compression: {worst_file} ({worst_overall:.2f}x)\n"
            f"• JSON and structured data typically show the best compression\n"
            f"• Random data is the most difficult to compress efficiently"
        )
        
        plt.figtext(0.02, 0.02, insights, fontsize=12, 
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.5))
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        # Add grids for easier reading
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Add a footer with timestamp
        plt.figtext(0.99, 0.01, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                   ha='right', va='bottom', fontsize=8, color='gray')
        
        # Adjust layout
        plt.tight_layout()
        plt.subplots_adjust(right=0.85, bottom=0.2)
        
        # Save the plot
        plot_file = os.path.join(self.output_dir, f"compression_ratio_all_files_{timestamp}.png")
        plt.savefig(plot_file, bbox_inches='tight')
        plt.close()
        print(f"All files compression comparison saved to: {plot_file}")
        
        # Create a radar chart comparing algorithms
        self._generate_algorithm_radar_chart(df, timestamp)
        
    def _generate_algorithm_radar_chart(self, df, timestamp):
        """Generate a radar chart comparing algorithms across metrics"""
        # Set a modern style for plots
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Get metrics for comparison
        metrics = [
            'Compression Ratio', 
            'Compression Speed (MB/s)', 
            'Decompression Speed (MB/s)',
            'Space Saving (%)'
        ]
        
        # Get algorithm data
        algorithms = df['Algorithm'].unique()
        
        # Compute average values for each algorithm and metric
        avg_data = {}
        for algo in algorithms:
            algo_data = df[df['Algorithm'] == algo]
            avg_data[algo] = [algo_data[metric].mean() for metric in metrics]
        
        # Normalize the data to [0, 1] for radar chart
        normalized_data = {}
        for metric_idx, metric in enumerate(metrics):
            metric_values = [avg_data[algo][metric_idx] for algo in algorithms]
            min_val = min(metric_values)
            max_val = max(metric_values)
            
            # Handle case where min and max are equal
            if max_val == min_val:
                normalized_values = [1.0 for _ in metric_values]
            else:
                normalized_values = [(val - min_val) / (max_val - min_val) for val in metric_values]
            
            for algo_idx, algo in enumerate(algorithms):
                if algo not in normalized_data:
                    normalized_data[algo] = []
                normalized_data[algo].append(normalized_values[algo_idx])
        
        # Radar chart setup
        plt.figure(figsize=(10, 10), dpi=100)
        
        # Compute number of angles
        angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
        
        # Make the plot circular by connecting the last point to the first
        angles += angles[:1]
        
        # Add metrics labels for the last point
        metrics += metrics[:1]
        
        # Add metric values to the chart
        for algo_idx, algo in enumerate(algorithms):
            values = normalized_data[algo] + normalized_data[algo][:1]  # Close the loop
            
            # Plot the radar for this algorithm
            color = ['#3498db', '#e74c3c', '#2ecc71'][algo_idx % 3]
            plt.polar(angles, values, marker='o', color=color, linestyle='-', linewidth=2, label=algo, alpha=0.7)
            
            # Fill the area
            plt.fill(angles, values, color=color, alpha=0.1)
        
        # Set labels and title
        plt.xticks(angles[:-1], metrics[:-1], fontsize=12)
        plt.title('Algorithm Performance Comparison', fontsize=20, y=1.1)
        
        # Add legend
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        # Add a note explaining the radar chart
        note = (
            "Note: Each axis represents a performance metric normalized to [0,1].\n"
            "Larger radar area indicates better overall performance."
        )
        plt.figtext(0.5, 0.01, note, ha='center', fontsize=10, style='italic')
        
        # Save the radar chart
        radar_file = os.path.join(self.output_dir, f"algorithm_radar_comparison_{timestamp}.png")
        plt.savefig(radar_file, bbox_inches='tight')
        plt.close()
        print(f"Algorithm radar comparison saved to: {radar_file}")


def main():
    """Main entry point for the script"""
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Compare compression algorithms (gzip, bzip2, LZMA)')
    parser.add_argument('-i', '--input-dir', default='data', help='Input directory containing files to compress')
    parser.add_argument('-o', '--output-dir', default='results', help='Output directory for results')
    args = parser.parse_args()
    
    # Run the comparison
    comparison = CompressionComparison(input_dir=args.input_dir, output_dir=args.output_dir)
    comparison.run_comparison()


if __name__ == '__main__':
    main() 