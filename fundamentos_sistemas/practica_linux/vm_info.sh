#!/bin/sh
# imprime la fecha y una linea de guiones:
# para un mejor trazado de las ejecuciones con cron (ejercicio 13)
echo --------------------------------------------
echo $(date +"%Y-%m-%d-% %H:%M")
echo --------------------------------------------
echo
# solucion al ejercicio 5
cat /proc/cpuinfo | grep "model name" | head -n 1
echo
free --giga #info de memoria
echo
df -H / #info de espacio en disco libre para la part /
echo
