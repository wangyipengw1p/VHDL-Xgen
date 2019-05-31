--------------------------------------------------
-- Creat time: 2019-05-31 22:07:27
-- Platform: Linux
-- Engineer: wangyipeng
-- University
-- Version
--------------------------------------------------



library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_signed.all;
use IEEE.numeric_std.all;


library work;
use work.testVXGen_pkg.all;
entity t2 is
port(
	clk	: in	std_logic;
	t1_t2	: in	std_logic_vector(15 downto 0);
	rst	: in	std_logic;
	t2_t4	: out	std_logic_vector(7 downto 0);
);
end entity;

architecture behaviral of t2 is


-- signals for clk div 5
signal clk_d5 : std_logic;
signal div5count:unsigned(2.0 downto 0);
signal div5_clkp, div5_clkn, div5_clkp_n, div5_clkn_n: std_logic;
begin

-- clk div 5
p_reg_clkdiv5:process(clk,rst)
begin
    if rising_edge(clk) then
        if rst = '0' then 
            div5count <= (others => '0');
			div5_clkp <= '0';
        else 
			div5_clkp <= div5_clkp_n;
			div5count <= div5count + 1;
			if div5count = 5 then div5count <= to_unsigned(1,2.0); end if;
        end if;
    end if;
end process;
n_reg_clkdiv5:process(clk,rst)
begin
    if falling_edge(clk) then
        if rst = '0' then 
            div5_clkn <= '0';
        else 
			div5_clkn <= div5_clkn_n;
        end if;
    end if;
end process;

comb:process(div5_clkn, div5_clkp, div5count)
begin
	div5_clkn_n <= div5_clkn;
	div5_clkp_n <= div5_clkp;
	if div5count = 5 then div5_clkp_n <= not div5_clkp; end if;
	if div5count = (5 - 1) / 2 then div5_clkn_n <= not div5_clkn; end if;
end process;

clk_d5 <= div5_clkp xor div5_clkn;





end architecture;