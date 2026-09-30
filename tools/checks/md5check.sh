# Checks site PDFs against Zenodo MD5s. Input: a text file of "<md5>  <ID>" lines (from the coordinating instance, which can reach Zenodo). Run from repo root: sh tools/checks/md5check.sh zenodo_md5.txt
while read m id; do f=research/pdf/$id.pdf; got=$(md5sum "$f" | cut -d' ' -f1); [ "$got" = "$m" ] && echo "OK   $id" || echo "DIFF $id site=$got zenodo=$m"; done < "$1"
