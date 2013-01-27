for i in `seq 0.10 0.05 0.95`;do
#for i in 0.05;do
	#echo $i
	rm flags.dat
	cat base.dat >> flags.dat
	echo "-mu "$i >> flags.dat
	cat tail.dat >> flags.dat

	make
       	./benchmark -f flags.dat

	cd ../

	python2 SeedDrivenDete.py >> ./log/$i.log
	#python2 GCE.py >> ./log/$i.log
	#python2 LFM.py >> ./log/$i.lfm.log
	
	cd ./evaluations/mutual3
	#python2 NMI.py >> $i.nmi.log
	echo "i ="$i": " >> ../../log/nmi.log
	./mutual true.dat result.dat >> ../../log/nmi.log
	#./mutual true.dat result_GCE.dat >> ../../log/nmi.log
	#./mutual true.dat result_LFM.dat >> ../../log/nmi.lfm.log

	cd ../../benchmark_LFR_OC_UU

done
