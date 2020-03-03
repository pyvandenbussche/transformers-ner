# transformers-ner
[![Documentation Status](https://img.shields.io/badge/Blog-link_to_the_post-brightgreen.svg)](http://pyvandenbussche.info/2019/named-entity-recognition-with-pytorch-transformers/)

Experiment on NER task using Huggingface state-of-the-art Natural Language Models

## Installation

### Prerequisites

* Python ≥ 3.6

### Provision a Virtual Environment

Create and activate a virtual environment (conda)

```
conda create --name py36_transformers-ner python=3.6
source activate py36_transformers-ner
```

If `pip` is configured in your conda environment, 
install dependencies from within the project root directory
```
pip install -r requirements.txt
``` 

### Data Pre-processing

#### Download the data
The current `BC5CDR` dataset is available as IOB format. Small modifications should be applied 
to the files so they can be processed by BERT NER (space separated elements, etc.). 
We will first download the files and then transform them

Download the files at:
```bash
mkdir data-input
curl -o data-input/devel.tsv https://raw.githubusercontent.com/cambridgeltl/MTL-Bioinformatics-2016/master/data/BC5CDR-IOB/devel.tsv
curl -o data-input/train.tsv https://raw.githubusercontent.com/cambridgeltl/MTL-Bioinformatics-2016/master/data/BC5CDR-IOB/train.tsv
curl -o data-input/test.tsv https://raw.githubusercontent.com/cambridgeltl/MTL-Bioinformatics-2016/master/data/BC5CDR-IOB/test.tsv

```

To transform the data in a BERT NER compatible format, execute the following command:
```bash
python ./preprocess/generate_dataset.py --input_train_data data-input/train.tsv --input_dev_data data-input/devel.tsv --input_test_data data-input/test.tsv --output_dir data-input/
```

The script ouputs two files `train.txt` and `test.txt` that will be the input of the NER pipeline.

### Download pre-trained model and run the NER task
#### BERT
Pre-trained models of BERT are automatically fetched by HuggingFace's transformers library.
To execute the NER pipeline, run the following scripts:
```bash
python ./run_ner.py --data_dir ./data --model_type bert --model_name_or_path bert-base-cased --output_dir ./output --labels ./data/labels.txt --do_train --do_predict --max_seq_length 256 --overwrite_output_dir --overwrite_cache
```
The script will output the results and predictions in the output directory.

#### SciBERT
Download and unzip the model, vocab and its config. Rename config file to config.json as expected from the script.
```bash
curl -Ol https://s3-us-west-2.amazonaws.com/ai2-s2-research/scibert/pytorch_models/scibert_scivocab_cased.tar
tar -xvf scibert_scivocab_cased.tar -C scibert_scivocab_cased
cd scibert_scivocab_cased/
tar -zxvf weights.tar.gz
mv bert_config.json config.json
rm weights.tar.gz
```
To execute the NER pipeline, run the following scripts:
```bash
python ./run_ner.py --data_dir ./data --model_type bert --model_name_or_path scibert_scivocab_cased --output_dir ./output --labels ./data/labels.txt --do_train --do_predict --max_seq_length 256 --overwrite_output_dir --overwrite_cache
```
The script will output the results and predictions in the output directory.

#### SpanBERT
Download and unzip the model, vocab and its config. Rename config file to config.json as expected from the script.
Note that SpanBERT does not come with its own `vocab.txt` file. Instead it reuses the same as BERT-large-cased model
```bash
curl -Ol https://dl.fbaipublicfiles.com/fairseq/models/spanbert_hf_base.tar.gz
mkdir spanbert_hf_base
tar -zxvf spanbert_hf_base.tar.gz -C spanbert_hf_base
cd spanbert_hf_base
curl -Ol https://raw.githubusercontent.com/pyvandenbussche/transformers-ner/master/data/bert_large_cased_vocab.txt
mv bert_large_cased_vocab.txt vocab.txt
```
To execute the NER pipeline, run the following scripts:
```bash
python ./run_ner.py --data_dir ./data --model_type bert --model_name_or_path spanbert_hf_base --output_dir ./output --labels ./data/labels.txt --do_train --do_predict --max_seq_length 256 --overwrite_output_dir --overwrite_cache
```
The script will output the results and predictions in the output directory.