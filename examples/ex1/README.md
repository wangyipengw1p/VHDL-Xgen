Files in this folder are generated under a floder called `testVXGen`. And command with:
```
vxgen gen t1 -i clk rst data 8 -o t1_t2 16 t1_t3 4
vxgen gen t2 -i clk t1_t2 16 -o t2_t4 8 -i rst
vxgen gen t3 -i clk rst t1_t3 4 -o t3_t4 8
vxgen gen t4 -i clk rst t2_t4 8 t3_t4 8 -o d_out 4
vxgen top -i clk rst data 8 -o d_out 4
vxgen pkg -a
vxgen add t1.vhd counter 10
vxgen add t2.vhd clk_div 5
vxgen add t3 fsm 10
vxgen add t4 reg
vxgen gen t5 -i clk rst t2_t4 8 -o t5_o
vxgen add t4 t5
```
