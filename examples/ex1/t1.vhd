--------------------------------------------------
-- Creat time: 2019-05-31 22:05:12
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
entity t1 is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	data	: in	std_logic_vector(7 downto 0);
	t1_t2	: out	std_logic_vector(15 downto 0);
	t1_t3	: out	std_logic_vector(3 downto 0)
);
end entity;

architecture behaviral of t1 is

signal count10: unsigned(3 downto 0);
begin
-- counter 10
process(clk,rst)
begin
    if rising_edge(clk) then
        if rst = '0' then 
            count10 <= (others => '0');
        else 
			count10 <= count + 1;
			if count10 = 10 then count10 <= to_unsigned(1, 4); end if;
        end if;
    end if;
end process;


end architecture;
