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

entity m_seq_gen is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	m_seq	: out	std_logic
);
end entity;

architecture behaviral of m_seq_gen is

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