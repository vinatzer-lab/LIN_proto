#!/usr/bin/python

"""
    This script will read the k-mer profile into array/matrix in the memory and calculate them with newly uploaded
    genomes.
"""

# IMPORT
import h5py
import numpy as np
import scipy
import sys
import os

# FUNCTIONS
def read_by_iteration(count_profile):
    """
    :param count_profile:
    :return: K-mer counting in arrays
    """
    f = h5py.File(count_profile,'r')
    data = f['profiles']
    genomes = data.keys()
    kmer_profiles = data[genomes[0]][:]
    i = 1
    while i < len(genomes):
        kmer_profiles = np.vstack((kmer_profiles,genomes[i]))
        i += 1
    return kmer_profiles

# Use os.system(cmd) count the k-mer profile of newly uploaded genome(s)
def KmerCountNew(filepath):
    """
    :param filepath:
    :return: A k-mer counting profile will be generated on the hardisk
    """
    if filepath.endswith('/'):
        filepath = filepath
    else:
        filepath = filepath + '/'
    cmd = "kpal count -k %s*.fasta %stmp_count"%(filepath, filepath)
    os.system(cmd)

def transform_2_frequency(row):
    """
    Convert the k-mer counting to frequency per k-mer
    :param row
    :return: frequency
    """
    sigma = sum(row)
    get_frequency = map(lambda x: float(x)/sigma, row)
    return get_frequency


def main(filepath):
    # First generate k-mer profile for the new genomes
    KmerCountNew(filepath=filepath)
    # Use h5py, read k-mer profiles of both the original and new one
    # And read them into arrays
    original_kmer = read_by_iteration(count_profile='/home/vinatzerlab/Data/kPALEvaluation/Psy/countk12')
    new_kmer_profile_path = filepath+'tmp_count'
    new_kmer = read_by_iteration(count_profile=new_kmer_profile_path)
    # Concatenate these two arrays together, either concatenate/vstack will do, but better try which one is faster
    total_kmer_profile = np.vstack((original_kmer,new_kmer))
    # Probably need to transform to k-mer frequency matrix first
    total_frequency = map(transform_2_frequency,total_kmer_profile)
    # Calculate the pairwise distance (Could be ALLvsALL or only calculate the distances between the original ones and new
    # ones)
    total_cosine_similarity = scipy.spatial.distance.pdist(total_frequency,'cosine')
    # Create Tree based on this distance matrix


if __name__ == '__main__':
    filepath = sys.argv[1]
    main(filepath=filepath)