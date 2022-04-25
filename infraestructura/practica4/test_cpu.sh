
echo --------------------------------------------- >> test_cpu.txt
echo $(date) >> test_cpu.txt
echo --------------------------------------------- >> test_cpu.txt
sysbench --threads=3 cpu run >>test_cpu.txt
