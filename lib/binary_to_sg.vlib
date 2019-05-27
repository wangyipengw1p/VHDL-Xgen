-------------------------------------------------------------------------------
-- Title      : binary_to_sg.vhd 
-- Project    : Keyboard VLSI Lab
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
-- Description: 
-- 	            Simple Look-Up-Table	
-- 		
--
-------------------------------------------------------------------------------

library ieee; 
use ieee.numeric_std.all; 
use ieee.std_logic_1164.all; 
use std.textio.all;  
use ieee.std_logic_textio.all;


entity binary_to_sg is
    port (
	     binary_in : in unsigned(3 downto 0);
	     sev_seg   : out unsigned(7 downto 0)
	 );
end binary_to_sg;

architecture binary_to_sg_arch of binary_to_sg is
begin
process(binary_in)
begin
    case binary_in is
        when "0000" => 
            sev_seg <= "00000010"; -- "0"     
        when "0001" => 
            sev_seg <= "10011110"; -- "1" 
        when "0010" => 
            sev_seg <= "00100100"; -- "2" 
        when "0011" => 
            sev_seg <= "00001100"; -- "3" 
        when "0100" => 
            sev_seg <= "10011000"; -- "4" 
        when "0101" => 
            sev_seg <= "01001000"; -- "5" 
        when "0110" => 
            sev_seg <= "01000000"; -- "6" 
        when "0111" => 
            sev_seg <= "00011110"; -- "7" 
        when "1000" => 
            sev_seg <= "00000000"; -- "8"     
        when "1001" => 
            sev_seg <= "00001000"; -- "9" 
        when others => 
            sev_seg <= "01100000"; -- E
    end case;
end process;


end binary_to_sg_arch;
