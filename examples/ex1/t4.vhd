--------------------------------------------------
-- Creat time: 2019-05-31 22:09:29
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
entity t4 is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	t2_t4	: in	std_logic_vector(7 downto 0);
	t3_t4	: in	std_logic_vector(7 downto 0);
	d_out	: out	std_logic_vector(3 downto 0)
);
end entity;

architecture behaviral of t4 is
component t5 is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	t2_t4	: in	std_logic_vector(7 downto 0);
	t5_o	: in	std_logic;
);
end component;




signal t5_o: std_logic;
begin
inst_t5:t5 port map(
	rst	=> rst,
	t2_t4	=> t2_t4,
	t5_o	=> t5_o,
	clk	=> clk
);




process(clk,rst)
begin
    if rising_edge(clk) then
        if rst = '0' then 
            
        else 

        end if;
    end if;
end process;
end architecture;
