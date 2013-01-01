for i in `seq 2 1 8`;do
#for i in 2;do
	#echo $i
	rm flags.dat
	cat base.dat >> flags.dat
	echo "-om "$i >> flags.dat
	cat tail.dat >> flags.dat

	make
       	./benchmark -f flags.dat >> ../log/$i.nmi.log

	cd ../

	python2 SeedDrivenDete.py >> ./log/$i.log
	#python2 ./lfm/LFM.py >> ./log/$i.log
	#python2 ./gce/GCE.py >> ./log/$i.log

	cd ./evaluations/mutual3
	make
	#python2 NMI.py >> $i.nmi.log
	echo "i ="$i": " >> ../../log/$i.nmi.log
	./mutual true.dat result.dat >> ../../log/$i.nmi.log

	cd ../../benchmark_LFR_OC_UU

done
