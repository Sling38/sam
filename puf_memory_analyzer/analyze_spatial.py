import csv
from pathlib import Path

def analyze_spatial_blocks(stability_csv, block_size_bits=1024*8):
    """
    Analyzes uniformity and stability in blocks (default 1KB = 8192 bits).
    """
    print(f"\nSpatial Analysis for {stability_csv.name}")
    print(f"{'Block':<6} | {'Uniformity':<12} | {'Avg Stability':<15}")
    print("-" * 45)

    with open(stability_csv, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)

    num_bits = len(data)
    for i in range(0, num_bits, block_size_bits):
        block = data[i : i + block_size_bits]
        if not block:
            break
        
        # Uniformity: mean of the majority bits in this block (approximation)
        # or better: average of ones_count / (zeros+ones)
        
        block_ones = 0
        block_total_trials = 0
        block_stability_sum = 0
        
        for row in block:
            z = int(row['zeros_count'])
            o = int(row['ones_count'])
            block_ones += o
            block_total_trials += (z + o)
            block_stability_sum += float(row['stability'])
            
        avg_uniformity = block_ones / block_total_trials if block_total_trials > 0 else 0
        avg_stability = block_stability_sum / len(block)
        
        block_idx = i // block_size_bits
        print(f"{block_idx:<6} | {avg_uniformity:.6f}     | {avg_stability:.6f}")

def main():
    base_dir = Path("bits_output")
    stability_files = list(base_dir.glob("*_stability.csv"))
    
    for csv_file in stability_files:
        analyze_spatial_blocks(csv_file)

if __name__ == "__main__":
    main()
