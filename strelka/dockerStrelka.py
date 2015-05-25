#!/usr/bin/env python
# =============================================================================
# Filename: dockerStrelka.py
# Version: 
# Author: Kai Yu - finno@live.cn
# https://github.com/readline
# Last modified: 2015-05-25 22:03
# Description: 
# 
# =============================================================================
import os,sys
from optparse import OptionParser

def main():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-n","--normal", dest="normalbam",help="Normal sample bam file.")
    parser.add_option("-t","--tumor", dest="tumorbam",help="Tumor sample bam file.")
    parser.add_option("-r","--ref", dest="reffa",help="Reference fasta file.")
    parser.add_option("-o","--output", dest="outpath",default="strelka_output",help="Output dir.")
    parser.add_option("-c","--config", dest="config",default="",help="Strelka config file, if not given, use default config.")
    parser.add_option("-m","--mode", dest="mode",default="WES",help="WGS or WES. [default=WES]. -c and -m conflicks. If -c given, -m would be ignored.")
    parser.add_option("-p","--threads", dest="threads", type='int',default=4, help="Threads to use. [default=4]")
    parser.add_option("-d","--docker",dest="docker",default='', help="Docker image to use.")
    (options, args) = parser.parse_args()

    if not options.normalbam or not options.tumorbam or not options.reffa:
        parser.error("Required arguments missed, please check!")


    if os.path.exists(options.normalbam+'.bai') == True:
        normalbai = options.normalbam+'.bai'
    elif os.path.exists(options.normalbam[:-1] + 'i') == True:
        normalbai = options.normalbam[:-1] + 'i'
    else:
        parser.error("Bam files should be indexed.")


    if os.path.exists(options.tumorbam+'.bai') == True:
        tumorbai = options.tumorbam+'.bai'
    elif os.path.exists(options.tumorbam[:-1] + 'i') == True:
        tumorbai = options.tumorbam[:-1] + 'i'
    else:
        parser.error("Bam files should be indexed.")


    if os.path.exists(options.reffa+'.fai') == True:
        reffai = options.reffa+'.fai'
    else:
        parser.error("Ref fasta file should be indexed.")


    if os.path.exists(options.outpath) == True:
        parser.error("Output dir exists. Please change it.")
    else:
        os.system("mkdir -p %s" %options.outpath)


    if options.config != '':
        os.system('cp %s %s' %(options.config, options.outpath+'/config.ini'))
        config = '/data/config.ini'
    else:
        if options.mode == 'WES':
            config = '/opt/strelka/etc/strelka_config_bwa_WES.ini'
        elif options.mode == 'WGS':
            config = '/opt/strelka/etc/strelka_config_bwa_WGS.ini'
        else:
            parser.error("Illegal argument -m.")

    if options.docker == '':
        parser.error("Docker image not given.")

    
    os.system('ln %s %s/normal.bam' %(options.normalbam, options.outpath))
    os.system('ln %s %s/normal.bam.bai' %(normalbai, options.outpath))

    os.system('ln %s %s/tumor.bam' %(options.tumorbam, options.outpath))
    os.system('ln %s %s/tumor.bam.bai' %(tumorbai, options.outpath))
    
    os.system('ln %s %s/ref.fa' %(options.reffa, options.outpath))
    os.system('ln %s %s/ref.fa.fai' %(reffai, options.outpath))

    if options.config != '':
        os.system('ln %s %s/config.ini' %(options.config, options.outpath))

    writefile = open('%s/run_strelka.sh'%options.outpath,'w')
    writefile.write('export PATH=/opt/strelka/bin:$PATH\n')
    writefile.write('echo Strelka start at `date`, `hostname` &&\n')
    writefile.write('configureStrelkaWorkflow.pl --tumor /data/tumor.bam --normal /data/normal.bam --ref /data/ref.fa --config %s --output-dir /data/strelka &&\n'%config)
    writefile.write('make -C /data/strelka -j %d &&\n'%options.threads)
    writefile.write('rm /data/*.bam /data/*.bai /data/ref.fa* &&')
    writefile.write('mv /data/strelka/results /data/ &&\n')
    writefile.write('rm -rf /data/strelka &&\n')
    writefile.write('echo Strelka finish at `date`, `hostname` \n')
    writefile.close()

    cmd = 'docker run --rm -v %s:/data %s sh /data/run_strelka.sh' %(os.path.abspath(options.outpath), options.docker)
    print cmd
    os.system(cmd)

if __name__ == '__main__':
    main()

    
        

