# Docker of strelka

This docker contains an CentOS 6.6 system and pre-installed strelka. Provides an environment for running strelka in instance.

### Running method
---

To build the docker image locally, just run:

```
./build [your image name]
# example: ./build readline/strelka
```

---

To start a container for strelka analysis, run:
```
# Run it in a interactive mode
docker run -it -v /path/to/your/files:/path/to/mount/your/files readline/strelka /bin/bash
```

### Automatic running tool
```
./dockerStrelka.py -h
Usage: dockerStrelka.py [options]

Options:
  -h, --help            show this help message and exit
  -n NORMALBAM, --normal=NORMALBAM
                        Normal sample bam file.
  -t TUMORBAM, --tumor=TUMORBAM
                        Tumor sample bam file.
  -r REFFA, --ref=REFFA
                        Reference fasta file.
  -o OUTPATH, --output=OUTPATH
                        Output dir.
  -c CONFIG, --config=CONFIG
                        Strelka config file, if not given, use default config.
  -m MODE, --mode=MODE  WGS or WES. [default=WES]. -c and -m conflicks. If -c
                        given, -m would be ignored.
  -p THREADS, --threads=THREADS
                        Threads to use. [default=4]
  -d DOCKER, --docker=DOCKER
                        Docker image to use.

```

Example:
```
../dockerStrelka.py -n NA12891_dupmark_chr20_region.bam -t NA12892_dupmark_chr20_region.bam -r chr20_860k_only.fa -o test -m WGS -p 24 -d centos/strelka
```

---
### Infomations about Strelka

version 1.0.14

[Strelka paper](http://www.ncbi.nlm.nih.gov/pubmed/22581179)


