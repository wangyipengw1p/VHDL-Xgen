--------------------------------------------------
-- Creat time: 2019-06-10 22:15:19
-- Platform: Windows
-- Engineer: Jacob
-- University
-- Version
--------------------------------------------------



library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_signed.all;
use IEEE.numeric_std.all;

entity clk_gen is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	clkd_25	: out	std_logic;
	clkd_500	: out	std_logic
);
end entity;

architecture behaviral of clk_gen is

-- signals for clk div 25
signal clk_d25 : std_logic;
signal div25count:unsigned(4 downto 0);
signal div25_clkp, div25_clkn, div25_clkp_n, div25_clkn_n: std_logic;
-- signals for clk div 500
signal clk_d500, clk_d500_n : std_logic;
signal div500count:unsigned(8 downto 0);
begin

-- clk div500
counter_reg_clkdiv500:process(clk,rst)
begin
    if rising_edge(clk) then
        if rst = '0' then 
            div500count <= (others => '0');
			clk_d500 <= '0';
        else 
			div500count <= div500count + 1;
			if div500count = 500 then 
				div500count <= to_unsigned(1,8); 
				clk_d500 <= clk_d500_n;
			end if;
        end if;
    end if;
end process;
comb_clkdiv500:process(div500count, clk_d500)
begin
	clk_d500_n <= clk_d500;
	if div500count = 500 then  clk_d500_n <= not clk_d500; end if;
end process;


-- clk div 25
p_reg_clkdiv25:process(clk,rst)
begin
    if rising_edge(clk) then
        if rst = '0' then 
            div25count <= (others => '0');
			div25_clkp <= '0';
        else 
			div25_clkp <= div25_clkp_n;
			div25count <= div25count + 1;
			if div25count = 25 then div25count <= to_unsigned(1,4); end if;
        end if;
    end if;
end process;
n_reg_clkdiv25:process(clk,rst)
begin
    if falling_edge(clk) then
        if rst = '0' then 
            div25_clkn <= '0';
        else 
			div25_clkn <= div25_clkn_n;
        end if;
    end if;
end process;

comb:process(div25_clkn, div25_clkp, div25count)
begin
	div25_clkn_n <= div25_clkn;
	div25_clkp_n <= div25_clkp;
	if div25count = 25 then div25_clkp_n <= not div25_clkp; end if;
	if div25count = (25 - 1) / 2 then div25_clkn_n <= not div25_clkn; end if;
end process;

clk_d25 <= div25_clkp xor div25_clkn;


end architecture;