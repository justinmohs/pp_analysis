variablename=$1
sqrts=$2
for observable in 'y' 'xF' 'mpt'
do
  cd $variablename'_'$sqrts'/'$observable
  pdflatex --jobname=$variablename'_'$observable '../../unite.tex'
  cd ../..
done
