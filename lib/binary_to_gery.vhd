
entity norm_to_gery is
generic(width:integer:=8);
port(
	din:in std_logic_vector(width-1 downto 0);
	dout:out std_logic_vector(width-1 downto 0);
end entity;
architecture norm_to_grey of norm_to_grey is begin
	dout<=din xor('0' & din(width-1 downto 1));


process(din)
variable tempd:std_logic;
begin

for i in width-1 downto 0 loop 
	tempd:='0';
	for j in width-1 downto i loop
		tempd:=tempd xor din(j);
	end loop;
	dout(i)<=tempd;
end loop;

end process;
end architecture;
