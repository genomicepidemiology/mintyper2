from Bio import Align
from Bio.Align import PairwiseAligner

def align_sequences(seq_a, seq_b):
    aligner = PairwiseAligner()
    aligner.mode = 'local'  # Use local alignment
    alignments = aligner.align(seq_a, seq_b)
    best_alignment = alignments[0]
    print("Alignment:\n", best_alignment)  # Print the alignment
    return alignments[0]  # Return the best alignment

def extract_gap_positions(alignment):
    seqs_alignment = alignment.format()

    seqs_a_alignment = seqs_alignment.split('\n')[0]
    seqs_b_alignment = seqs_alignment.split('\n')[2]
    return seqs_a_alignment, seqs_b_alignment

def find_gap_positions(aligned_sequence):
    gap_positions = []
    for i, char in enumerate(aligned_sequence):
        if char == '-':
            gap_positions.append(str(i))
    return ','.join(gap_positions)


def recreate_alignment(seq, gap_string):
    if not gap_string:
        return seq
    result = []
    gap_positions = set(map(int, gap_string.split(',')))
    for i, char in enumerate(seq):
        if i in gap_positions:
            result.append('-')
        result.append(char)
    return ''.join(result)

# Example usage
aligned_seq_a = "AAATTTAAAAAAAAAAATAAAAAAAAAA"
aligned_seq_b = "AAA---AAAAAAAAAAA-AAAAAAAAAAA"

gap_positions_a = find_gap_positions(aligned_seq_a)
gap_positions_b = find_gap_positions(aligned_seq_b)

print("Gap positions in Sequence A:", gap_positions_a)
print("Gap positions in Sequence B:", gap_positions_b)