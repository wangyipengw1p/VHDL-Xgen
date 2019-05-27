# VHDL-Xgen
VHDL auto generation tool, Targetting Synchronous, Top-down design flow. Support only one entity per file.

```Still developing```

## Usage
```
vxgen <func> {<args>}
```

* [gen](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#generation-from-templete)
* [add](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#add-components)
* [top](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#top-gen) 
* [tb](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#testbench-gen) 
* [pkg](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#package-gen) 
* [clear](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#clear)
* [version](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#version)
## Function
>  If not specified:
> * \<folder\> will be the current folder.
> * Auto-connect will connect the port with the same name.
> * \<filename\> is treated equally with \<entityname\>.
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
vxgen add <filename> <component> {<args>} {-f <folder>}
```
 
| component | description |
|  :-: | ------------- |
| counter | Counter named "count&lt;countNum&gt;" is added to &lt;filename&gt;, which will count from 1 to &lt;countNum&gt; and reset to 0. |
| divclk | Divided the clk by &lt;div&gt; and named the out put clk like "clk1" "clk2" etc. |
| FSM | Create the FSM with &lt;#states&gt; states. "moore" will let the FSM be moore-typed, otherwise it'll be mealy-typed. |
| reg | Create reg as indicated by -p(positive triggered) -n(negative triggered) -a(asynchronous reset) -s(sync reset). |
| &lt;lib-name&gt; | Copy the entity in the lib , include and auto-connect them in the &lt;filename&gt;. if -n is specified the tool will not do the auto connection. |
  
### Top gen
```
vxgen top {<topName>} {-n} {-f <folder>}
```

args | discription
:-: | --
{\<topName\>} | Specify the name. Default: "TOP".
{-n} | Do not auto connect.
{-f <folder>} | Default : current.
  
Auto generation & connection for Top entities. 
First the tool will find generate the framwork of the top entity named by &lt;topName&gt;(default "TOP"). If "-n" is specified, only generation will be done. Otherwise, the tool will find first in the <folder>(default current folder) for the file named "\*_TOP.conf". And connect the port as indicated in the file. If no such file, the tool will include all entities, whose name does not include '&apos;	_&apos;	(underline) connect the the port with same name **(recommand)**, and only generate the signal for the ports left, which means that they are not connected.
If there's already been a file named "\*_TOP.vhd", the tool will only do the auto connection work.
**It's recommand to name all clock as "clk" and connect disired clk manually after auto connection. Other logics should be added manually.**

### Testbench gen
```
vxgen tb <entityname> {<clkFrequency>} {-d <dutycycle>} {-pn} {-pr} {-rt <rst-time>}
```

args | discription
:-: | --
\<entityname\> | name
{\<clkFrequency\>} | Unit: MHz. Default: 100MHz
{-d \<dutycycle\>} | Unit: %. Default: 50%
{-pn} | Diffrencial clk. Name: "clkn" "clkp"
{-pr} | Positive reset. Default: neg-reset
{-rt \<rst-time\>} | Default: 1 clk cycle
  
Generate the testbench for specific entity. clock is created named "clk", whose frequency is set to &lt;clkFrequency&gt; MHz (default 100MHz). If -d is specified, the clk dutycycle is set to &lt;dutucycle&gt; (default 50%). If -pn is specified, differencial clk will be generated and named "clkp" and clkn". Reset is auto generated named "rst". If -pr is specified, it will be positive reset, otherwise, default setting is negative reset. Reset will last for &lt;rst-time&gt; (default one clk cycle), and inverted.
  
### Package gen
```
vxgen pkg <pkg_name> {-a} {-f <folder>}
```

args | discription
:-: | --
<pkg_name> | name
{-a} | Add work lib and this pkg to all file in the folder
{-f <folder>} | Default: current
  
Generated pkg named &lt;pkg_name&gt; (default "pkg"). If -a is specified, all file in the folder will add work library as will as this pkg.

### Clear
```
vxgen clear {-f <folder>}
```
The tool till generate log and some mark commented at the first line of each file. Clear them using this command. Note that after this command the behaviour of the tool is not guaranteed. So make sure that you finish the creation process before running this command.

### Version
```
vxgen version
```
Check if you've succeffully installed the VHDL-Xgen.

## Notes
- Please write one entiey per file and assign same name for file. In this tool, &lt;entityname&gt; is treated equally with &lt;filename&gt;.
- Please name the first-level entities (which are to be included by top entities) with out **'_'** , or it'll be treated as second-level entities and ignore when auto-connecting in the top module.
- It's recommanded to integrate the IP cores at last, cus their names always contain '_'.
- It's recommand to name all clock as "clk" and connect disired clk manually after auto connection for TOP.

------------------
