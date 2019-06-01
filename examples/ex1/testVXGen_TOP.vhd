--------------------------------------------------
-- Creat time: 2019-05-31 22:21:20
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
entity testVXGen_TOP is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	data	: in	std_logic_vector(7 downto 0);
	d_out	: out	std_logic_vector(3 downto 0)
);
end entity;

architecture behaviral of testVXGen_TOP is
component t4 is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	t2_t4	: in	std_logic_vector(7 downto 0);
	t3_t4	: in	std_logic_vector(7 downto 0);
	d_out	: out	std_logic_vector(3 downto 0)
);
end component;
component t3 is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	t1_t3	: in	std_logic_vector(3 downto 0);
	t3_t4	: out	std_logic_vector(7 downto 0)
);
end component;
component t1 is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	data	: in	std_logic_vector(7 downto 0);
	t1_t2	: out	std_logic_vector(15 downto 0);
	t1_t3	: out	std_logic_vector(3 downto 0)
);
end component;
component t2 is
port(
	clk	: in	std_logic;
	t1_t2	: in	std_logic_vector(15 downto 0);
	rst	: in	std_logic;
	t2_t4	: out	std_logic_vector(7 downto 0)
);
end component;

signal t2_t4: std_logic_vector(7 downto 0);
signal t1_t2: std_logic_vector(15 downto 0);
signal t1_t3: std_logic_vector(3 downto 0);
signal t3_t4: std_logic_vector(7 downto 0);
begin
inst_t4:t4 port map(
	rst	=> rst,
	t2_t4	=> t2_t4,
	t3_t4	=> t3_t4,
	d_out	=> d_out,
	clk	=> clk
);

inst_t3:t3 port map(
	rst	=> rst,
	t1_t3	=> t1_t3,
	t3_t4	=> t3_t4,
	clk	=> clk
);

inst_t1:t1 port map(
	rst	=> rst,
	t1_t3	=> t1_t3,
	t1_t2	=> t1_t2,
	data	=> data,
	clk	=> clk
);

inst_t2:t2 port map(
	rst	=> rst,
	t2_t4	=> t2_t4,
	t1_t2	=> t1_t2,
	clk	=> clk
);


end architecture;
