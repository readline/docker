# Install required softwares
apt-get update &&
apt-get install --yes wget python python-dev python-pip perl libreadline6 libreadline6-dev gfortran sqlite openjdk-7-jre sqlite3 libsqlite3-dev openjdk-7-jre libxt-dev &&

cd /opt &&

wget http://mirror.bjtu.edu.cn/cran/src/base/R-3/R-3.2.0.tar.gz &&
tar zxvf R-3.2.0.tar.gz &&
rm R-3.2.0.tar.gz &&
cd R-3.2.0 &&
./configure --enable-R-shlib &&
make &&
make install &&
cd .. &&
rm -rf R-3.2.0 &&

pip install PySQLite &&
pip install BioPython &&
pip install rpy2 &&
echo "source(\"http://bioconductor.org/biocLite.R\")" > qvalue.R &&
echo "biocLite(\"qvalue\")">>qvalue.R &&
Rscript qvalue.R &&
rm qvalue.R &&

wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.30/ncbi-blast-2.2.30+-x64-linux.tar.gz &&
tar zxvf ncbi-blast-2.2.30+-x64-linux.tar.gz &&
mv ncbi-blast-2.2.30+/bin/makeblastdb ncbi-blast-2.2.30+/bin/blastx ncbi-blast-2.2.30+/bin/blastp /bin/ &&
rm -rf ncbi-blast-2.2.30+-x64-linux.tar.gz ncbi-blast-2.2.30+ &&

wget http://kobas.cbi.pku.edu.cn/download/kobas-2.1.1.tar.gz http://kobas.cbi.pku.edu.cn/download/sqlite3/organism.db.gz http://kobas.cbi.pku.edu.cn/download/sqlite3/ko.db.gz &&
tar zxvf kobas-2.1.1.tar.gz &&
rm kobas-2.1.1.tar.gz &&
gunzip organism.db.gz ko.db.gz &&
mv organism.db ko.db kobas-2.1.1/sqlite3/ &&
cp /opt/kobas-2.1.1/doc/kobasrc /root/.kobasrc &&
sed -i 's/kobas_home\ =/kobas_home \=\/opt\/kobas-2\.1\.1/g' ~/.kobasrc &&
sed -i 's/blast_home\ =/blast_home \=\/bin/g' ~/.kobasrc &&
export PATH=/opt/kobas-2.1.1/scripts/:$PATH
export PYTHONPATH=/opt/kobas-2.1.1/src:$PYTHONPATH
rm /opt/install.sh

