#!/bin/bash
cd /opt/kobas*/seq_pep &&
wget http://kobas.cbi.pku.edu.cn/download/seq_pep/$1.pep.fasta.gz &&
gunzip $1.db.gz &&
makeblastdb -in $1.pep.fasta -dbtype prot

