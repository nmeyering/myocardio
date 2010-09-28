set term svg;
set output "data/weight_plot.svg"
set xlabel "Days since <min-date>"
set ylabel "Weight/kg"
f(x)=a*x+b
a=0
b=0
fit f(x) "<myfile>" using 1:2 via a,b
plot "<myfile>" using 1:2 title "Body weight" with points, \
	f(x) title "Linear approximation" with line
