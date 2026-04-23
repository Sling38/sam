import csv
from pathlib import Path

def load_bits(filepath):
    with open(filepath, 'r') as f:
        content = f.read().strip()
    return [int(ch) for ch in content if ch in '01']

def calculate_uniformity(bits):
    if not bits:
        return 0.0
    return sum(bits) / len(bits)

def analyze_board_uniformity(board_folder):
    bit_files = sorted(Path(board_folder).glob("*.bits"))
    if not bit_files:
        print(f"No .bits files found in {board_folder}")
        return

    trial_uniformities = []
    
    print(f"\nAnalyzing Uniformity for: {board_folder.name}")
    print(f"{'Trial':<10} | {'Hamming Weight':<15} | {'Bias (%)':<10}")
    print("-" * 45)

    for f in bit_files:
        bits = load_bits(f)
        u = calculate_uniformity(bits)
        bias = abs(u - 0.5) * 100
        trial_uniformities.append(u)
        # print(f"{f.name:<10} | {u:.6f}        | {bias:.2f}%") # Commented out to reduce noise for many trials

    avg_u = sum(trial_uniformities) / len(trial_uniformities)
    print(f"Average Uniformity: {avg_u:.6f}")
    print(f"Average Bias:       {abs(avg_u - 0.5)*100:.2f}% (Deviation from 0.5)")
    
    return avg_u

def main():
    base_dir = Path("bits_output")
    boards = ["1724_SRAM4_data", "5223_SRAM4_data"]
    
    for board in boards:
        board_path = base_dir / board
        if board_path.is_dir():
            analyze_board_uniformity(board_path)
        else:
            print(f"Directory {board_path} not found.")

if __name__ == "__main__":
    main()
