#!/bin/bash
gawk -F',' '{
  listen[$1][$2] = 1
}
END {
  for (key in listen) {
    print key " " length(listen[key]) > "ex_2.tmp"
  }
}' samples_formatted.txt

sort --numeric-sort -k2 -r ex_2.tmp | head -n 10
rm ex_2.tmp
