# QAM signal generation
Example from Beijing IC Design Contest for College Student, digital track, 2019, problem C

> The specific instruction of the problem of the contest will be uploaded soon


See what the tool can do for you.

First, in the folder `ex2`, creat a vsh file, whose content is
```
gen clk_gen -i clk rst -o clkd_25 clkd_500
add clk_gen clk_div 25 500
gen m_seq_gen -i clk rst -o m_seq
add m_seq_gen reg
gen mapping -i clk rst m_seq -o ab_sig 3
add mapping counter 4
gen qam_gen -i clk rst ab_sig 3 -o qam_sig 14
add qam_gen reg
# add qam_gen blk_rom_gen -f <where the ip exists>
top qam_TOP -i clk rst -o qam_sig 14
tb qam_TOP -q 50 -pr
```


Then command
```
vxgen
```

Then console out put should be like this with no warning and no error
```
>vxgen
>>> gen clk_gen -i clk rst -o clkd_25 clkd_500

>>> add clk_gen clk_div 25 500

>>> gen m_seq_gen -i clk rst -o m_seq

>>> add m_seq_gen reg

>>> gen mapping -i clk rst m_seq -o ab_sig 3

>>> add mapping counter 4

>>> gen qam_gen -i clk rst ab_sig 3 -o qam_sig 14

>>> add qam_gen reg

>>> top qam_TOP -i clk rst -o qam_sig 14

>>> tb qam_TOP -q 50 -pr
>>> Done
```

Finally, change the connection of the clk in the `qam_TOP` file. (we need to do this because entity `m_seq_gen` needs clkd_500, `mapping` and `qam_gen` need clkd_25. But the tool can only connect them to clk)

We notice that changing the clk connection in the generated vhd file will be easy, while describing them in shell may be difficault.

The role of the tool has ended. We can focus on our core logic!