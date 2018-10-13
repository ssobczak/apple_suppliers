#!/usr/bin/env bash

rm -rf docs/*

jupyter nbconvert *.ipynb --output-dir docs

ls docs | grep -v 'index.html' | \
perl -e 'print "<html><body><ul>"; while(<>) { chop $_; print "<li><a href=\"./$_\">$_</a></li>";} print "</ul></body></html>"' > docs/index.html
