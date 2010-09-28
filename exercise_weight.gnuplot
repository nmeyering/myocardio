set term svg;
set xlabel "Days since <min-date>"
set ylabel "Weight"
plot "<myfile>" using 1:2
min_y = GPVAL_DATA_Y_MIN
max_y = GPVAL_DATA_Y_MAX
set yrange [min_y:max_y+0.5]
set output "data/exercise_weight.svg"
plot "<myfile>" using 1:2 title "" with boxes
replot
