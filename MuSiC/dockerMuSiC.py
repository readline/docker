#!/usr/bin/env python
# dockerMuSiC.py
# version 1.0
# Kai Yu
# https://github.com/readline
# 150518
##############################################
import os,sys
from optparse import OptionParser

def main():
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-b", "--bamlist", dest="bamlist",help="Bamlist file path")
    parser.add_option("-a", "--bampath", dest="bampath",help="Bampath accord with the bamlist")
    parser.add_option("-m", "--maf", dest="maf",help="Maf file path")
    parser.add_option("-r", "--roi", dest="roi",help="Roi file path")
    parser.add_option("-f", "--ref", dest="ref",help="Reference fasta path")
    parser.add_option("-n", "--ndepth", dest="ndepth",type='int',default=14,help="Normal min depth [default=14]")
    parser.add_option("-t", "--tdepth", dest="tdepth",type='int',default=8,help="Tumor min depth [default=8]")
    parser.add_option("-q", "--mapq", dest="mapq",type='int',default=1,help="Min mapq [default=1]")
    parser.add_option("-p", "--threads", dest="threads",type='int',default=1,help="Num of threads [default=1]")
    parser.add_option("-o", "--prefix", dest="prefix",help="Output path prefix")
    parser.add_option("-d", "--docker", dest="docker",help="Docker image name")

    (options, args) = parser.parse_args()
    if not options.bamlist or not options.maf or not options.roi or not options.ref \
        or not options.prefix or not options.docker or not options.bampath:
        parser.error("Incorrect argument, please check.")
    if os.path.exists(options.prefix):
        tmpquery = raw_input('Output path exists, enter Y to continue:').upper()
        if tmpquery == 'Y':
            pass
        else:
            sys.exit('Abort!')
    print 'Preparing files...'
    os.system('mkdir -p %s' %options.prefix)
    os.system('cp %s %s/tmp%d.bamlist' %(options.bamlist, options.prefix, os.getpid()))
    os.system('cp %s %s/tmp%d.maf' %(options.maf, options.prefix, os.getpid()))
    os.system('cp %s %s/tmp%d.roi' %(options.roi, options.prefix, os.getpid()))
    os.system('cp %s %s/tmp%d.ref' %(options.ref, options.prefix, os.getpid()))
    savefile = open('%s/run_music.sh'%options.prefix, 'w')
    savefile.write('echo Docker-MuSiC start at `date`,`hostname`. &&\n')
    savefile.write('cd /data &&\n')
    savefile.write('mkdir -p music/roi_covgs music/gene_covgs &&\n')
    savefile.write('echo [`date`] Run genome music bmr calc-covg. &&\n')
    savefile.write('''genome music bmr calc-covg \
--roi-file tmp%d.roi \
--reference-sequence tmp%d.ref \
--bam-list tmp%d.bamlist \
--output-dir music \
--normal-min-depth %d \
--tumor-min-depth %d \
--min-mapq %d &&\n''' %(os.getpid(),os.getpid(),os.getpid(),options.ndepth,options.tdepth,options.mapq))
    savefile.write('echo [`date`] Run genome music bmr calc-bmr. &&\n')
    savefile.write('''genome music bmr calc-bmr \
--roi-file tmp%d.roi \
--reference-sequence tmp%d.ref \
--bam-list tmp%d.bamlist \
--output-dir music \
--bmr-groups 2 \
--maf-file tmp%d.maf &&\n''' %(os.getpid(),os.getpid(),os.getpid(),os.getpid()))
    savefile.write('echo [`date`] Run genome music smg. &&\n')
    savefile.write('''genome music smg \
--gene-mr-file music/gene_mrs \
--output-file music/%s.smg \
--processors %d &&\n''' %(options.prefix.split('/')[-1], options.threads))
    savefile.write('echo [`date`] Clean up work dir. &&\n')
    savefile.write('rm tmp%d.* &&\n'%os.getpid())
    savefile.write('echo Docker-MuSiC finish at `date`,`hostname`.\n')
    savefile.close()

    cmd = 'docker run --rm -v %s:/data -v %s:%s %s sh /data/run_music.sh' \
        %(os.path.abspath(options.prefix),os.path.abspath(options.bampath), 
          os.path.abspath(options.bampath), options.docker)
    print cmd
    tmp = os.popen(cmd)

    print 'Mission submitted to docker container:\n%s'%tmp.readline().rstrip()

if __name__ == '__main__':
    main()
