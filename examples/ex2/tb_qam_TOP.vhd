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

entity tb_qam_TOP is
end entity;

architecture behaviral of tb_qam_TOP is
component qam_TOP is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	qam_sig	: out	std_logic_vector(13 downto 0)
);
end component;

signal clk, rst: std_logic;
signal qam_sig: std_logic_vector(1 downto 0);
begin
inst_qam_TOP:qam_TOP port map(
	clk	=> clk,
	rst	=> rst,
	qam_sig	=> qam_sig
);


process
begin
	clk <= '1';
	wait for 10.0 ns;
	clk <= '0';
	wait for 10.0 ns;
end process;
rst <='1', '0' after 20.0 ns;
end architecture;