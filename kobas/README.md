# Docker of kobas

This docker contains an Ubuntu 14.04 system and pre-installed kobas. Provides an environment for running kobas in instance.

### Running method
---

To build the docker image locally, just run:

```
./build [your image name]
# example: ./build readline/kobas
```

---

To start a container for kobas analysis, run:
```
# Run it in a interactive mode
docker run -it -v /path/to/your/files:/path/to/mount/your/files readline/kobas /bin/bash
```

---

# Assistance scripts:

### /opt/dbPrepare.sh

To download required sqlite3 database for your analysis. It requires the organism code which you can find in the db.list. This is essential for kobas analysis.

```bash
/opt/dbPrepare.sh ko
```

### /opt/blastdbPrepare.sh

To download fasta file for your analysis and make blastdb. It requires the organism code which you can find in the db.list

You can run blast in the docker, but you'd better run blast in a parallel multi-node environment, out side of docker. If so, this step can skip for kobas analysis.

### Infomations about kobas

version kobas2.0-20150126

> KOBAS 2.0 is an update of KOBAS (KEGG Orthology Based Annotation System). KOBAS is the first software to identify statistically significantly enriched pathways using hypergeometric test. It has been successfully used in pathway analysis in plants, animals and bacteria.

> KOBAS 2.0, which annotates an input set of genes with pathways, diseases, and GO terms based on mapping to genes with known annotation. It allows for both ID mapping and cross-species sequence similarity mapping. It then performs statistical tests to identify statistically significantly enriched pathways, diseases, and GO terms. KOBAS 2.0 incorporates knowledge across over 2969 species from 6 pathway databases (KEGG PATHWAY, PID, BioCarta (from PID), Reactome, BioCyc, and PANTHER), 5 human disease databases (OMIM, KEGG DISEASE, FunDO, GAD, and NHGRI GWAS Catalog), and Gene Ontology.

[kobas paper](http://www.ncbi.nlm.nih.gov/pubmed/21715386)

