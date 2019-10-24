mv mdin/* .
mv movie/* .
head -1 md.movie-0.03-8 >md.movie-0.03-8.xyz
tac md.movie-0.03-8 | awk '!flag; /Frame/{flag = 1};' | tac >> md.movie-0.03-8.xyz
for f in `ls *.xyz`; do head -2 $f >$f.header; done;

tar cvzf pt-5.tar.gz md.in-5-* md.movie-5-*.xyz
tar cvzf pt-5.header.tar.gz md.movie-5-*.xyz.header
