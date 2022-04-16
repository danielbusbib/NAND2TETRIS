load,
output-file MaxTest.out,
compare-to MaxTest.cmp,
output-list RAM[8000]%D2.6.1 RAM[8001]%D2.6.1 RAM[8002]%D2.6.1 RAM[8003]%D2.6.1 RAM[8004]%D2.6.1 RAM[8005]%D2.6.1 RAM[8006]%D2.6.1 RAM[8007]%D2.6.1;

repeat 1000000 {
  vmstep;
}

output;
