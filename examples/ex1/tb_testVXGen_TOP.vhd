--------------------------------------------------
-- Creat time: 2019-05-31 22:23:59
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
entity tb_testVXGen_TOP is
end entity;

architecture behaviral of tb_testVXGen_TOP is
component testVXGen_TOP is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	data	: in	std_logic_vector(7 downto 0);
	d_out	: out	std_logic_vector(3 downto 0);
);
end component;

signal clk, rst: std_logic;
signal d_out: std_logic_vector(3 downto 0);
signal data: std_logic_vector(7 downto 0);
begin
inst_testVXGen_TOP:testVXGen_TOP port map(
	rst	=> rst,
	d_out	=> d_out,
	data	=> data,
	clk	=> clk
);


clk <= not clk after 5 ns;
rst <= '0', '1' after 10 ns;
end architecture;