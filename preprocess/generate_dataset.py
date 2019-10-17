# coding=utf-8
""" Generate the dataset from stanford format """

import argparse
import logging
import os

logger = logging.getLogger(__name__)


def write_to_file(file_dir, filename, snippets):
    if os.path.isfile(os.path.join(file_dir, filename)):
        os.remove(os.path.join(file_dir, filename))
    with open(os.path.join(file_dir, filename), "w", encoding='utf-8') as output_file:
        for snippet in snippets:
            output_file.write("\n".join(sentence for sentence in snippet))
            output_file.write("\n\n")

def main():
    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("--input_train_data", default=None, type=str, required=True,
                        help="The input data file path e.g. ../data/train.tsv")
    parser.add_argument("--input_dev_data", default=None, type=str, required=True,
                        help="The input data file path e.g. ../data/devel.tsv")
    parser.add_argument("--input_test_data", default=None, type=str, required=True,
                        help="The input data file path e.g. ../data/test.tsv")
    parser.add_argument("--output_dir", default=None, type=str, required=True,
                        help="The output directory e.g. ../data/")
    parser.add_argument("--keep_only_tag", default=None, type=str,
                        help="Keep only annotations with this tag label (e.g. 'indications' will keep tags "
                             "['O', 'B-indications', 'I-indications'])")

    args = parser.parse_args()


    if not os.path.isfile(args.input_train_data) or not os.path.isfile(args.input_dev_data):
        raise ValueError("The input data file path ({} or {}) does not exist.".format(args.input_train_data, args.input_dev_data))

    fo = open(os.path.join(args.output_dir, "train.txt"), "w")
    for tempfile in [args.input_train_data, args.input_dev_data]:
        with open(tempfile, 'r') as fi:
            for line in fi:
                line = line.replace("\t", " ")
                if args.keep_only_tag is not None:
                    splits = line.split()
                    if len(splits) > 1:
                        label = splits[-1]
                        if len(label)>1 and label[2:] != args.keep_only_tag:
                            line = "{} O\n".format(splits[:-1])
                fo.write(line)
            # add new line at the end fo the file to break the sentence
            fo.write("\n")

    fo = open(os.path.join(args.output_dir, "test.txt"), "w")
    with open(args.input_test_data, 'r') as fi:
        for line in fi:
            line = line.replace("\t", " ")
            if args.keep_only_tag is not None:
                splits = line.split()
                if len(splits) > 1:
                    label = splits[-1]
                    if len(label) > 1 and label[2:] != args.keep_only_tag:
                        line = "{} O\n".format(splits[:-1])
            fo.write(line)
        # add new line at the end fo the file to break the sentence
        fo.write("\n")

if __name__ == "__main__":
    main()
