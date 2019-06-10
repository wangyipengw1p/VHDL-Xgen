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

entity mapping is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	m_seq	: in	std_logic;
	ab_sig	: out	std_logic_vector(2 downto 0)
);
end entity;

architecture behaviral of mapping is

signal count4: unsigned(1 downto 0);
begin
-- counter 4
process(clk,rst)
begin
    if rising_edge(clk) then
        if rst = '0' then 
            count4 <= (others => '0');
        else 
			count4 <= count4 + 1;
			if count4 = 4 then count4 <= to_unsigned(1, 2); end if;
        end if;
    end if;
end process;


end architecture;