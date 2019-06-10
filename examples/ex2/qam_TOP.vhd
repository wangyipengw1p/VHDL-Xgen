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

entity qam_TOP is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	qam_sig	: out	std_logic_vector(13 downto 0)
);
end entity;

architecture behaviral of qam_TOP is
component qam_gen is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	ab_sig	: in	std_logic_vector(2 downto 0);
	qam_sig	: out	std_logic_vector(13 downto 0)
);
end component;
component m_seq_gen is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	m_seq	: out	std_logic
);
end component;
component mapping is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	m_seq	: in	std_logic;
	ab_sig	: out	std_logic_vector(2 downto 0)
);
end component;
component clk_gen is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	clkd_25	: out	std_logic;
	clkd_500	: out	std_logic
);
end component;

signal clkd_25: std_logic;
signal clkd_500: std_logic;
signal m_seq: std_logic;
signal ab_sig: std_logic_vector(2 downto 0);
begin
inst_qam_gen:qam_gen port map(
	clk	=> clk,
	rst	=> rst,
	ab_sig	=> ab_sig,
	qam_sig	=> qam_sig
);

inst_m_seq_gen:m_seq_gen port map(
	clk	=> clk,						-- TODO: change the second 'clk' to 'clkd_500'
	rst	=> rst,
	m_seq	=> m_seq
);

inst_mapping:mapping port map(
	clk	=> clk,						-- TODO: change the second 'clk' to 'clkd_25'
	rst	=> rst,
	m_seq	=> m_seq,
	ab_sig	=> ab_sig
);

inst_clk_gen:clk_gen port map(
	clk	=> clk,						-- TODO: change the second 'clk' to 'clkd_25'
	rst	=> rst,
	clkd_25	=> clkd_25,
	clkd_500	=> clkd_500
);


end architecture;