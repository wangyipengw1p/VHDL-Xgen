library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_unsigned.all;

library work;
use work.ALU_components_pack.all;

entity binary_to_BCD is
   
   port ( 
          binary_in : in  std_logic_vector(7 downto 0);  -- binary input width
          BCD_out   : out std_logic_vector(9 downto 0)        -- BCD output, 10 bits [2|4|4] to display a 3 digit BCD value when input has length 8
        );
end binary_to_BCD;

architecture structural of binary_to_BCD is 
  
begin  

process(binary_in)
variable stack :std_logic_vector(17 downto 0);
begin

stack := (others => '0');
stack(10 downto 3) := binary_in;

for i in 0 to 4 loop
    if stack(11 downto 8) > 4 then
        stack(11 downto 8) := stack(11 downto 8) + 3;
    end if;
    if stack(15 downto 12) > 4 then
        stack(15 downto 12) := stack(15 downto 12) + 3;
    end if;
    stack(17 downto 1) := stack(16 downto 0);
end loop;
 BCD_out <= stack(17 downto 8);
end process;



end structural;
