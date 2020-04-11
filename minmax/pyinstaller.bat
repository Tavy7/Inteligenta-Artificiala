@echo off
color a
python-3.7.6.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
echo "hatz"
tree
@echo on