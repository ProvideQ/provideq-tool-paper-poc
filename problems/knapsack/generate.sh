# Used to call https://github.com/JorikJooken/knapsackProblemInstances
for n in {3..10}; do
    for i in {1..10}; do
        c=$(($n * 10)) # Capacity
        g=$(($n / 2 + 1)) # Classes
        f=0.5
        eps=0.01
        s=$(($c / 3)) # Amount of "small" items
        mkdir -p $n;
        echo "$n\n$c\n$g\n$f\n$eps\n$s";
        echo -e "$n\n$c\n$g\n$f\n$eps\n$s" | ./generatorExecutable > $n/n_${n}_c_${c}_f_${f}_eps_${eps}_s_${s}_i_${i}.txt
    done
done