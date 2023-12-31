import os
import sys
import numpy as np


def produce_features(args):
    os.mkdir('output')
    illumina_list = []
    all_files = args.nanopore
    for i in range(0, len(args.illumina), 2):
        string = args.illumina[i] + ' ' + args.illumina[i+1]
        illumina_list.append(string)
        all_files.append(string)
    produce_kmers(args)
    matrix_9mers = np.zeros((len(all_files), len(all_files)))
    for i in range(len(matrix_9mers)):
        for j in range(len(matrix_9mers)):
            if i == j:
                matrix_9mers[i][j] = 1
            else:
                file_1 = all_files[i]
                file_2 = all_files[j]
                if len(file_1.split(' ')) == 1:
                    name_1 = file_1.split('/')[-1].split('.')[0]
                else:
                    name_1 = file_1.split(' ')[0].split('/')[-1].split('.')[0]
                if len(file_2.split(' ')) == 1:
                    name_2 = file_2.split('/')[-1].split('.')[0]
                else:
                    name_2 = file_2.split(' ')[0].split('/')[-1].split('.')[0]
                read_set_1 = read_file_to_set('output/{}_9mers.txt'.format(name_1))
                read_set_2 = read_file_to_set('output/{}_9mers.txt'.format(name_2))
                matrix_9mers[i][j] = jaccard_index(read_set_1, read_set_2)

    print ('9mers')
    print (matrix_9mers)

    matrix_15mers = np.zeros((len(all_files), len(all_files)))
    for i in range(len(matrix_15mers)):
        for j in range(len(matrix_15mers)):
            if i == j:
                matrix_15mers[i][j] = 1
            else:
                file_1 = all_files[i]
                file_2 = all_files[j]
                if len(file_1.split(' ')) == 1:
                    name_1 = file_1.split('/')[-1].split('.')[0]
                else:
                    name_1 = file_1.split(' ')[0].split('/')[-1].split('.')[0]
                if len(file_2.split(' ')) == 1:
                    name_2 = file_2.split('/')[-1].split('.')[0]
                else:
                    name_2 = file_2.split(' ')[0].split('/')[-1].split('.')[0]
                read_set_1 = read_file_to_set('output/{}_15mers.txt'.format(name_1))
                read_set_2 = read_file_to_set('output/{}_15mers.txt'.format(name_2))
                matrix_15mers[i][j] = jaccard_index(read_set_1, read_set_2)
    print ('15mers')
    print (matrix_15mers)


    matrix_21mers = np.zeros((len(all_files), len(all_files)))
    for i in range(len(matrix_21mers)):
        for j in range(len(matrix_21mers)):
            if i == j:
                matrix_21mers[i][j] = 1
            else:
                file_1 = all_files[i]
                file_2 = all_files[j]
                if len(file_1.split(' ')) == 1:
                    name_1 = file_1.split('/')[-1].split('.')[0]
                else:
                    name_1 = file_1.split(' ')[0].split('/')[-1].split('.')[0]
                if len(file_2.split(' ')) == 1:
                    name_2 = file_2.split('/')[-1].split('.')[0]
                else:
                    name_2 = file_2.split(' ')[0].split('/')[-1].split('.')[0]
                read_set_1 = read_file_to_set('output/{}_21mers.txt'.format(name_1))
                read_set_2 = read_file_to_set('output/{}_21mers.txt'.format(name_2))
                matrix_21mers[i][j] = jaccard_index(read_set_1, read_set_2)

    print ('21mers')
    print (matrix_21mers)

    for item in all_files:
        nucleotide_counts = read_nucleotide_counts(item)
        gc_content = calculate_gc_content(nucleotide_counts)

    print(f"GC content: {gc_content:.2f}%")

    return 'test'


def read_nucleotide_counts(filename):
    """Reads nucleotide counts from a file and returns a dictionary."""
    nucleotide_counts = {}
    if len(filename.split(' ')) == 1:
        name = filename.split('/')[-1].split('.')[0]
        with open('output/{}_1mers.txt', 'r') as f:
            for line in f:
                nucleotide, count = line.strip().split('\t')
                nucleotide_counts[nucleotide] = int(count)
    else:
        name = filename.split(' ')[0].split('/')[-1].split('.')[0]
        with open('output/{}_1mers.txt'.format(name), 'r') as f:
            for line in f:
                nucleotide, count = line.strip().split('\t')
                nucleotide_counts[nucleotide] = int(count)
        name = filename.split(' ')[1].split('/')[-1].split('.')[0]
        with open('output/{}_1mers.txt'.format(name), 'r') as f:
            for line in f:
                nucleotide, count = line.strip().split('\t')
                nucleotide_counts[nucleotide] += int(count)
    return nucleotide_counts


def calculate_gc_content(nucleotide_counts):
    """Calculates GC content from a dictionary of nucleotide counts."""
    gc_count = nucleotide_counts.get('G', 0) + nucleotide_counts.get('C', 0)
    total_count = sum(nucleotide_counts.values())

    if total_count == 0:
        return 0

    return (gc_count / total_count) * 100
def produce_kmers(args):
    """Produces kmer files for the input file."""
    for item in args.illumina:
        name = item.split('/')[-1].split('.')[0]
        os.system('kmc -k1 -cs1000000000000 -b {} output/{}_1mers . > output/{}_1mers_stats.txt'.format(item, name, name))
        os.system('kmc_dump output/{}_1mers output/{}_1mers.txt'.format(name, name))
        os.system('kmc -k9 -cs1000000000 {} output/{}_9mers . > output/{}_9mers_stats.txt'.format(item, name, name))
        os.system('kmc_dump output/{}_9mers output/{}_9mers.txt'.format(name, name))
        os.system('kmc -k15 -cs1000000000 {} output/{}_15mers . > output/{}_15mers_stats.txt'.format(item, name, name))
        os.system('kmc_dump output/{}_15mers output/{}_15mers.txt'.format(name, name))
        os.system('kmc -k21 -cs1000000000 {} output/{}_21mers . > output/{}_21mers_stats.txt'.format(item, name, name))
        os.system('kmc_dump output/{}_21mers output/{}_21mers.txt'.format(name, name))

    for item in args.nanopore:
        name = item.split('/')[-1].split('.')[0]
        os.system('kmc -k1 -cs1000000000000 -b {} output/{}_1mers output/ > output/{}_1mers_stats.txt'.format(item, name, name))
        os.system('kmc_dump output/{}_1mers output/{}_1mers.txt'.format(name, name))
        os.system('kmc -k9 -cs1000000000 {} output/{}_9mers output/ > output/{}_9mers_stats.txt'.format(item, name, name))
        os.system('kmc_dump output/{}_9mers output/{}_9mers.txt'.format(name, name))
        os.system('kmc -k15 -cs1000000000 {} output/{}_15mers output/ > output/{}_15mers_stats.txt'.format(item, name, name))
        os.system('kmc_dump output/{}_15mers output/{}_15mers.txt'.format(name, name))
        os.system('kmc -k21 -cs1000000000 {} output/{}_21mers output/ > output/{}_21mers_stats.txt'.format(item, name, name))
        os.system('kmc_dump output/{}_21mers output/{}_21mers.txt'.format(name, name))
def read_file_to_set(filename):
    """Reads kmer strings from a file and returns a set of those kmers."""
    kmers = set()
    if len(filename.split(' ')) == 1:
        with open(filename, 'r') as f:
            for line in f:
                kmer, _ = line.strip().split('\t')
                kmers.add(kmer)
    else:
        with open(filename.split(' ')[0], 'r') as f:
            for line in f:
                kmer, _ = line.strip().split('\t')
                kmers.add(kmer)
        with open(filename.split(' ')[1], 'r') as f:
            for line in f:
                kmer, _ = line.strip().split('\t')
                kmers.add(kmer)
    return kmers

def jaccard_index(set1, set2):
    """Calculates the Jaccard index between two sets."""
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

def main():
    file1 = input("Enter the path to the first file: ")
    file2 = input("Enter the path to the second file: ")

    kmers1 = read_file_to_set(file1)
    kmers2 = read_file_to_set(file2)

    jaccard = jaccard_index(kmers1, kmers2)

    print(f"Jaccard Index between the two files: {jaccard:.4f}")
