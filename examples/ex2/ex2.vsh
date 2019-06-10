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