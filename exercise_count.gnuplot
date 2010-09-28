set term svg;
set output "data/exercise_count.svg"
set xlabel "Days since <min-date>"
set ylabel "Number of exercises"
set yrange [2:9]
plot "<myfile>" using 1:2 title "" with points
min_y = GPVAL_DATA_Y_MIN
max_y = GPVAL_DATA_Y_MAX
f(x) = mean_y
fit f(x) '<myfile>' using 1:2 via mean_y
set label 1 gprintf("Minimum = %g", min_y) at 2, min_y-0.3
set label 2 gprintf("Maximum = %g", max_y) at 2, max_y+0.3
set label 3 gprintf("Mean = %g", mean_y) at 2, max_y+0.55
plot min_y with filledcurves y1=mean_y lt 1 lc rgb "#bbbbdd", \
max_y with filledcurves y1=mean_y lt 1 lc rgb "#bbddbb", \
'<myfile>' u 1:2 title "" w p pt 7 lt 1 ps 1
