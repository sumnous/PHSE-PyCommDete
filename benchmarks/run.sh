for i in `seq 0.10 0.05 0.90`;do
#for i in 0.1;do
	#echo $i
	rm parameters.dat
	cat base.dat >> parameters.dat
	echo $i >> parameters.dat
	cat tail.dat >> parameters.dat

	make
       	./benchmark

	cd ../

	python2 SeedDrivenDete.py >> ./log/$i.log

	cd ./evaluations/mutual3
	#python2 NMI.py >> $i.nmi.log
	echo "i ="$i": " >> ../../log/$i.nmi.log
	./mutual true.dat result.dat >> ../../log/$i.nmi.log

	cd ../../benchmarks

done
