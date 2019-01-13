# print file path list in directory
find `pwd` -type f -exec echo {} \; > list.txt

# add label 0 to the end
sed "s/$/ 0/" list.txt > file_list.txt 

