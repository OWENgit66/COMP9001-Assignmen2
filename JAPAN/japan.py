"""
japan.py

A program that allows a user to reforge an imperfect katana blueprint
to match a master blacksmith's perfect design. The katana is represented
using '#' for the blade, and '=' and '|' for the handle.

The program compares similarity scores, accepts or rejects katanas,
and repeatedly prompts the user to reforge the blade until it meets
the required similarity threshold.

Usage:
    python3 japan.py <imperfect_blueprint.bp> <min_similarity>
"""
import sys
import os

def print_katana(bp: str):
    """
    Prints the contents of a katana blueprint file upside down.

    Parameters:
        bp (str): The filename of the katana blueprint (.bp file).
    """
    with open(bp, 'r') as f:
        for line in f:
            print(line.rstrip('\n'))


def get_similarity_score(imperfect_bp: str) -> float:
    """
    Compares the blade of an imperfect katana against the perfect katana
    in perfect_katana.bp.

    Calculates and returns a similarity score between 0 and 1, where 1 means
    a perfect match. The similarity is based on the number of '#' symbols
    per line in the blade section only.

    Parameters:
        imperfect_bp (str): The filename of the imperfect katana blueprint.

    Returns:
        float: The average line similarity between the two blueprints.
    """
     # Read two blueprints
    with open('perfect_katana.bp', 'r') as f:
        perfect_lines = [line.rstrip('\n') for line in f]
    with open(imperfect_bp, 'r') as f:
        imperfect_lines = [line.rstrip('\n') for line in f]

    # Ignore the handle (the first four lines) and only compare the blade
    perfect_blade   = perfect_lines[4:]
    imperfect_blade = imperfect_lines[4:]

    # Ensure that the number of rows on the blade is consistent
    total = len(perfect_blade)
    if total == 0:
        return 1.0  

    sim_sum = 0.0
    for p_line, i_line in zip(perfect_blade, imperfect_blade):
        p_cnt = p_line.count('#')
        i_cnt = i_line.count('#')
        if p_cnt == 0 and i_cnt == 0:
            line_sim = 1.0
        else:
            line_sim = min(p_cnt, i_cnt) / max(p_cnt, i_cnt)
        sim_sum += line_sim

    return sim_sum / total

def reforge_imperfect_katana(imperfect_bp: str):
    """
    Prompts the user to reshape the blade of the imperfect katana by entering
    the number of '#' symbols for each line. 
    
    Updates the imperfect blueprint with the new blade while keeping the handle
    intact, getting it as close as the perfect katana in perfect_katana.bp. 

    Parameters:
        imperfect_bp (str): The filename of the imperfect katana blueprint.
    """
    with open('perfect_katana.bp', 'r') as f:
        perfect_lines = [line.rstrip('\n') for line in f]
    with open(imperfect_bp, 'r') as f:
        imperfect_lines = [line.rstrip('\n') for line in f]

    # Ensure that the number of rows on the blade is consistent
    handle = imperfect_lines[:4]
    separator_line = handle[3]
    max_width = len(separator_line) - 2  

    perfect_blade = perfect_lines[4:]
    total_lines = len(perfect_blade)

    print(">> REFORGING KATANA.\n")
    print("Katana Details:")
    print(f"- Blade (lines): {total_lines}")
    print(f"- Maximum width: {max_width}\n")

    new_blade_counts = []
    for idx, p_line in enumerate(perfect_blade, start=1):
        target_count = p_line.count('#')
        # 显示为 [###] 的提示
        prompt_hint = '#' * target_count if target_count > 0 else ''
        while True:
            user_in = input(f"Line ({idx}/{total_lines}) [{prompt_hint}]: ").strip()
            # 必须是整数
            try:
                val = int(user_in)
            except ValueError:
                print("Error: Input must be an integer.")
                continue
            # It must be in 1... max_width
            if not (1 <= val <= max_width):
                print(f"Error: Input must be between 1 to {max_width} (inclusive).")
                continue
            new_blade_counts.append(val)
            break

    # Ensure that the number of rows on the blade is consistent
    new_lines = []
    new_lines.extend(handle)
    for cnt in new_blade_counts:
        new_lines.append(' ' + ('#' * cnt))

    # Ensure that the number of rows on the blade is consistent
    with open(imperfect_bp, 'w') as f:
        for line in new_lines:
            f.write(line + '\n')

    print("\n>> FORGING COMPLETE.")
    ans = input("Would you like to print the katana [yes/no]? ").strip().lower()
    if ans in ('y', 'yes'):
        print()
        print_katana(imperfect_bp)


def main():
    """
    Runs the full katana forging simulation from start to finish.

    Handles command line arguments, loads the blueprints, checks the
    similarity score, and repeatedly prompts the user to reforge the katana
    until it meets the required threshold.
    """
     # ---------- 1️ Missing arguments ----------
    if len(sys.argv) != 3:
        print("Error: Missing arguments.")
        print("Usage: python3 japan.py <imperfect_blueprint.bp> <min_similarity>")
        sys.exit(1)

    imperfect_bp = sys.argv[1]
    sim_arg = sys.argv[2]

    # ---------- 2️ Invalid file extension ----------
    if not imperfect_bp.endswith(".bp"):
        print("Error: Invalid file extension. Expected a filename ending in .bp")
        sys.exit(1)

    # ---------- 3️ Invalid similarity (not float) ----------
    try:
        min_similarity = float(sim_arg)
    except ValueError:
        print("Error: Invalid similarity score. Expected a float value.")
        sys.exit(1)

    # ---------- 4️ File not found ----------
    if not os.path.exists(imperfect_bp):
        print(f"Error: File not found. Please check that {imperfect_bp} exists.")
        sys.exit(1)

    # ---------- 5️ Similarity not between 0–1 ----------
    if not (0 <= min_similarity <= 1):
        print("Error: Similarity score must be between 0 and 1 (inclusive).")
        sys.exit(1)

    # ---------- Start program ----------
    print(">> READING IN BLUEPRINTS.")

    # ---------- Similarity analysis ----------
    print("\n>> ANALYSING THEIR SIMILARITY.")
    score = get_similarity_score(imperfect_bp)
    print(f"Similarity score: {score:.2f}")

    # ---------- Results ----------
    if score < min_similarity:
        print("Denied: You must reforge it.")
    else:
        print("Accepted: The blacksmith is satisfied.")
        return  # end program if accepted

    # ---------- Reforge loop ----------
    while score < min_similarity:
        print()
        reforge_imperfect_katana(imperfect_bp)
        print("\n>> ANALYSING THEIR SIMILARITY.")
        score = get_similarity_score(imperfect_bp)
        print(f"Similarity score: {score:.2f}")
        if score < min_similarity:
            print("Denied: You must reforge it.")
        else:
            print("Accepted: The blacksmith is satisfied.")


# Do not modify this!
if __name__ == '__main__':
    main()

