variablename=$1
for observable in 'y' 'xF' 'mpt'
do
  cd $variablename'_17.27'/$observable
  pdflatex --jobname=$variablename'_'$observable '../../unite.tex'
  cd ../..
done
