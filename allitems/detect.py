#coding:utf-8
import argparse
import sys
from os import listdir
from os.path import isfile, join
from typing import Dict, List, Optional, Tuple
import re
import imagehash
import numpy as np
import requests
from PIL import Image
from io import BytesIO
import time
import codecs
reload(sys)
sys.setdefaultencoding('utf8')

lss=[]
f=open('/media/sf_UbuntuFile/allitems/test.txt' , 'r')
for line in f.xreadlines():
    lss.append(line)
f.close()
print (lss)

file=codecs.open('/media/sf_UbuntuFile/allitems/query.txt' , 'w',encoding='utf-8')
file.close()

def calculate_signature_file(image_file, hash_size=16):
    """ 
    Calculate the dhash signature of a given file
    
    Args:
        image_file: the image (path as string) to calculate the signature for
        hash_size: hash size to use, signatures will be of length hash_size^2
    
    Returns:
        Image signature as Numpy n-dimensional array or None if the file is not a PIL recognized image
    """
    try:
        pil_image = Image.open(image_file).convert("L").resize(
                            (hash_size+1, hash_size),
                            Image.ANTIALIAS)
        dhash = imagehash.dhash(pil_image, hash_size)
        signature = dhash.hash.flatten()
        pil_image.close()
        return signature
    except IOError as e:
        raise e





def calculate_signature_url(image_file, hash_size=16):
    """ 
    Calculate the dhash signature of a given file
    
    Args:
        image_file: the image (path as string) to calculate the signature for
        hash_size: hash size to use, signatures will be of length hash_size^2
    
    Returns:
        Image signature as Numpy n-dimensional array or None if the file is not a PIL recognized image
    """
    try:
	try:
            print image_file
	    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
	    response = requests.get(image_file)
	    print response
	except Exception as e:
	    print e
        pil_image = Image.open(BytesIO(response.content)).convert("L").resize(
                            (hash_size+1, hash_size), 
                            Image.ANTIALIAS)
        dhash = imagehash.dhash(pil_image, hash_size)
        signature = dhash.hash.flatten()
        pil_image.close()
        return signature
    except IOError as e:
        raise e

        
def find_near_duplicates(input_dir, threshold, hash_size, bands):
    """
    Find near-duplicate images
    
    Args:
        input_dir: Directory with images to check
        threshold: Images with a similarity ratio >= threshold will be considered near-duplicates
        hash_size: Hash size to use, signatures will be of length hash_size^2
        bands: The number of bands to use in the locality sensitve hashing process
        
    Returns:
        A list of near-duplicates found. Near duplicates are encoded as a triple: (filename_A, filename_B, similarity)
    """
    rows = int(hash_size**2/bands)
    signatures = dict()
    hash_buckets_list = [dict() for _ in range(bands)]
    # Build a list of candidate files in given input_dir
    try:
        file_list = [join(input_dir , f) for f in listdir(input_dir) if isfile(join(input_dir, f))]
    except OSError as e:
        raise e
    for i in lss:
        file_list.append(str(i))
    # Iterate through all files in input directory
    for fh in file_list:
        try:
            signature = calculate_signature_file(fh, hash_size)
        except IOError:
            # Not a PIL image, skip this file b
            continue
        # Keep track of each image's signature
        signatures[fh] = np.packbits(signature)

        # Locality Sensitive Hashing
        for i in range(bands):
            signature_band = signature[i * rows:(i + 1) * rows]
            signature_band_bytes = tuple(signature_band)
            if len(hash_buckets_list[i]) == 0:
                hash_buckets_list[i][signature_band_bytes] = list()
                hash_buckets_list[i][signature_band_bytes].append(fh)
            else:
                count = 0
                for q in hash_buckets_list[i]:
                    for j in range(rows):
                        if (signature_band_bytes[j] == q[j]):
                            count = count + 1
                        if count > 2:
                            hash_buckets_list[i][q].append(fh)
                        if count <= threshold * rows:
                            hash_buckets_list[i][signature_band_bytes] = list()
                            hash_buckets_list[i][signature_band_bytes].append(fh)
                        break;
                    break;
    # Build candidate pairs based on bucket membership
    candidate_pairs = set()
    for hash_buckets in hash_buckets_list:
        for hash_bucket in hash_buckets.values():
            if len(hash_bucket) > 1:
                hash_bucket = sorted(hash_bucket)
                for i in range(len(hash_bucket)):
                    for j in range(i+1, len(hash_bucket)):
                        candidate_pairs.add(
                            tuple([hash_bucket[i],hash_bucket[j]])
                        )

    # Check candidate pairs for similarity
    near_duplicates = list()
    for cpa, cpb in candidate_pairs:
        hd = sum(np.bitwise_xor(
                np.unpackbits(signatures[cpa]),
                np.unpackbits(signatures[cpb])
        ))
        similarity = float (hash_size**2 - hd) / hash_size**2
        if similarity > threshold:
            near_duplicates.append((cpa, cpb, similarity))
            
    # Sort near-duplicates by descending similarity and return
    near_duplicates.sort(key=lambda x:x[2], reverse=True)
    return near_duplicates



def main(argv):
    # Argument parser
    parser = argparse.ArgumentParser(description="Efficient detection of near-duplicate images using locality sensitive hashing")
    #parser.add_argument("-i", "--inputdir", type=str, default="", help="directory containing images to check")
    parser.add_argument("-t", "--threshold", type=float, default=0.4, help="similarity threshold")
    parser.add_argument("-s", "--hash-size", type=int, default=16, help="hash size to use, signature length = hash_size^2", dest="hash_size")
    parser.add_argument("-b", "--bands", type=int, default=16, help="number of bands")

    args = parser.parse_args()
    #input_dir = args.inputdir
    threshold = args.threshold
    hash_size = args.hash_size
    bands = args.bands

    input_dir='/media/sf_UbuntuFile/allitems/dombapic/'
    input_dir1='/media/sf_UbuntuFile/allitems/glbapic'
    try:
        near_duplicates = find_near_duplicates(input_dir, threshold, hash_size, bands)
        if near_duplicates:
            print "Found {} near-duplicate images in {} (threshold {})".format(len(near_duplicates),input_dir,threshold)
            for a,b,s in near_duplicates:
                if(a==str(lss[0]) or b==str(lss[0])):
                    print "{} similarity: file 1: {} - file 2: {}".format(s,a,b)
                    f=open('/media/sf_UbuntuFile/allitems/sinadombaimg.txt' , 'r')
                    opp=[]
                    for line in f.xreadlines():
                        op = re.split(r"(\*my_sep\*)",line)
                        op.append("")
                        op = ["".join(i) for i in zip(op[0::2],op[1::2])]
                        opp.append(op)
                    f.close()
                    if(a!=str(lss[0])):
                        i = a.split("/")[-1]
                        i = i.split(".")[0]
                        print int(i)
                        file=codecs.open('/media/sf_UbuntuFile/allitems/query.txt' , 'a' ,encoding='utf-8')
                        file.writelines(opp[int(i)-1])
                        file.flush()
                        file.close()
                    else:
                        i = b.split("/")[-1]
                        i = i.split(".")[0]
                        print int(i)
                        file=codecs.open('/media/sf_UbuntuFile/allitems/query.txt' , 'a',encoding='utf-8')
                        file.writelines(opp[int(i)-1])
                        file.flush()
                        file.close()
        else:
            print "No near-duplicates found in {} (threshold {})".format(input_dir,threshold)
    except OSError:
        print "Couldn't open input directory {}".format(input_dir)


    try:
        near_duplicates = find_near_duplicates(input_dir1, threshold, hash_size, bands)
        if near_duplicates:
            print "Found {} near-duplicate images in {} (threshold {})".format(len(near_duplicates),input_dir1,threshold)
            for a,b,s in near_duplicates:
                if(a==str(lss[0]) or b==str(lss[0])):
                    print "{} similarity: file 1: {} - file 2: {}".format(s,a,b)
                    f=open('/media/sf_UbuntuFile/allitems/sinaglbaimg.txt' , 'r')
                    opp=[]
                    for line in f.xreadlines():
                        op = re.split(r"(\*my_sep\*)",line)
                        op.append("")
                        op = ["".join(i) for i in zip(op[0::2],op[1::2])]
                        opp.append(op)
                    f.close()
                    if(a!=str(lss[0])):
                        i = a.split("/")[-1]
                        i = i.split(".")[0]
                        print int(i)
                        file=codecs.open('/media/sf_UbuntuFile/allitems/query.txt' , 'a',encoding='utf-8')
                        file.writelines(opp[int(i)-1])
                        file.flush()
                        file.close()
                    else:
                        i = b.split("/")[-1]
                        i = i.split(".")[0]
                        print int(i)
                        file=codecs.open('/media/sf_UbuntuFile/allitems/query.txt' , 'a' ,encoding='utf-8')
                        file.writelines(opp[int(i)-1])
                        file.flush()
                        file.close()

        else:
            print "No near-duplicates found in {} (threshold {})".format(input_dir,threshold)
    except OSError:
        print "Couldn't open input directory {}".format(input_dir)
                    

if __name__ == "__main__":
    main(sys.argv)
