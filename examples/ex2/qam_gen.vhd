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

entity qam_gen is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	ab_sig	: in	std_logic_vector(2 downto 0);
	qam_sig	: out	std_logic_vector(13 downto 0)
);
end entity;

architecture behaviral of qam_gen is

begin

process(clk,rst)
begin
    if rising_edge(clk) then
        if rst = '0' then 
            
        else 

        end if;
    end if;
end process;
end architecture;