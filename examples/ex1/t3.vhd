--------------------------------------------------
-- Creat time: 2019-05-31 22:08:39
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
entity t3 is
port(
	clk	: in	std_logic;
	rst	: in	std_logic;
	t1_t3	: in	std_logic_vector(3 downto 0);
	t3_t4	: out	std_logic_vector(7 downto 0)
);
end entity;

architecture behaviral of t3 is
type state_type is (s0, s1, s2, s3, s4, s5, s6, s7, s8, s9);
-- signals for FSM
signal current_state, next_state: state_type;

begin

-- FSM
FSM_reg:process(clk,rst)
begin
    if rising_edge(clk) then
        if rst = '0' then 
			current_state <= $default_state;		
        else 
			current_state <= next_state;
        end if;
    end if;
end process;

FSM_comb:process(current_state)
begin
	next_state <= current_state;
	case current_state is

		when s0 =>
			
		when s1 =>
			
		when s2 =>
			
		when s3 =>
			
		when s4 =>
			
		when s5 =>
			
		when s6 =>
			
		when s7 =>
			
		when s8 =>
			
		when s9 =>
			
	end case;
end process;

end architecture;
