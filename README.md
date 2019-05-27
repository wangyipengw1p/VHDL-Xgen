# VHDL-Xgen
VHDL auto generation tool, Targetting Synchronous, Top-down design flow. Support only one entity per file.

```Still developing```

## Function
### Generation from templete
``` 
vxgen gen <entityname> {-f <folder>}
```
Generate the templete ```.vhd``` file based on ```<VXGEN-PATH>/templete/title.conf``` and ```libaray.conf```
  - Comment in .conf using '**#**' if you don't want to generate the items and libraries in the vhd file.
  - remember to add a ```<space>``` behind item name to assign content. 
  - Time will be auto completed. If ```Engineer``` is not specified vxgen will use <usrname>.
  
### Add components
```
vxgen add <filename> <component-name> {<args>} {-f <folder>}
```
Add components to existing vhd file.  ```<component-name> {<args>}``` could be:
  - ```counter <countNum>```
  - ```divclk <div>```
  - ```FSM <#states> {moore}```
  - ```reg <type>``` ```<type>: -p -n -a -s```
  - ```<lib-filename> {-n}```
 Notes:
 
|component | description
|counter | counter named "count<countNum>" is added to <filename>, which will count from 1 to <countNum> and reset to 0.|
|divclk | divided the clk by <div> and named the out put clk like "clk1" "clk2" etc.|
|FSM | Create the FSM with <#states> states. "moore" will let the FSM be moore-typed, otherwise it'll be mealy-typed.|
|reg | Create reg as indicated by -p(positive triggered) -n(negative triggered) -a(asynchronous reset) -s(sync reset).|
|<lib-filename> | copy the entity in the lib , include and auto-connect them in the <filename>. if -n is specified the tool will not do the auto connection.|
  
### Top gen
```
vxgen top {-n <topName>} {-og} {-f <folder>}
```
Auto generation & connection for Top entities. 
First the tool will find generate the framwork of the top entity named by <topName>(default "TOP"). If "-og" is specified, only generation will be done. Otherwise, the tool will find first in the <folder>(default current folder) for the file named "*_TOP.conf". And connect the port as indicated in the file. If no such file, the tool will include all entities, whose name does not include **'_'**(underline) connect the the port with same name **(recommand)**, and only generate the signal for the ports left, which means that they are not connected.
If there's already been a file named "*_TOP.vhd", the tool will only do the auto connection work.
**It's recommand to name all clock as "clk" and connect disired clk manually after auto connection. Other logics should be added manually.**

### Testbench gen
```
vxgen tb <entityname> {<clkFrequency>} {-d <dutycycle>} {-pn} {-pr}{-rt <rst-time>}
```
Generate the testbench for specific entity. clock is created named "clk", whose frequency is set to <clkFrequency> MHz (default 100MHz). If -d is specified, the clk dutycycle is set to <dutucycle> (default 50%). If -pn is specified, differencial clk will be generated and named "clkp" and clkn". Reset is auto generated named "rst". If -pr is specified, it will be positive reset, otherwise, default setting is negative reset. Reset will last for <rst-time> (default one clk cycle), and inverted.
  
### pkg gen
```
vxgen pkg <pkg_name> {-a} {-f <folder>}
```
Generated pkg named <pkg_name> (default "pkg"). If -a is specified, all file in the folder will add work library as will as this pkg.

### Notes
- Please write one entiey per file and assign same name for file. In this tool, <entityname> is treated equally with <filename>.
- Please name the first-level entities (which are to be included by top entities) with out **'_'** , or it'll be treated as second-level entities and ignore when auto-connecting in the top module.
- It's recommanded to integrate the IP cores at last, cus their names always contain '_'.
- It's recommand to name all clock as "clk" and connect disired clk manually after auto connection for TOP.

------------------
