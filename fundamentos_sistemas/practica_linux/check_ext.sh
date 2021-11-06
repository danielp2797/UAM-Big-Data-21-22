#!/bin/bash
######################################################
#Input: extension de archivo (sin punto)
#Output: listado de archivos
#Descrip: imprime los archivos del dir actual con la extension de entrada
######################################################

dir=$pwd*
exten=$1
if [ $# -lt 1 ]; then
	echo "No extension provided..."
else

for file in $dir*; do
	file_exten=${file##*.}
    if [[ $exten == $file_exten ]];then
        echo $file
    fi
done
fi
