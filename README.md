# VHDL-Xgen
[![build status](https://img.shields.io/badge/build-pass-brightgreen.svg)](https://img.shields.io/badge/build-pass-brightgreen.svg)
[![test status](https://img.shields.io/badge/test-undergoing-blue.svg)](https://img.shields.io/badge/test-undergoing-blue.svg)



VHDL auto generation tool, Targetting Synchronous, Top-down design flow. Support only one entity per file.

## Build
Python file does not need to build. The main file is `src/vxgen.py`. For convience, command
```
cd $VHDL-Xgen-dir 
sh setup.sh
```
Done. Then command following to test if you've done things correctly.
```
vxgen version
```

## Usage
```
vxgen <func> {<args>}
```

## [gen](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#generation)  [add](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#add-components) [top](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#top-gen)  [tb](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#testbench-gen)  [pkg](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#package-gen)  [version](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#version)
## Function
>  If not specified:
> * \<folder\> will be the current folder.
> * Auto-connect will connect the port with the same name.
> * \<filename\> is treated equally with \<entityname\>.
> * register will be positive triggered
> * reset will be synchoronous negative-rst.
### Generation
``` 
vxgen gen <entitypath> {-i <name> <width> ...} {-o <name> <width> ...} {-io <name> <width> ...} 
```
Generate the templete ```.vhd``` file based on ```<VXGEN-PATH>/conf/title.conf``` and ```libaray.conf```
  - Comment in .conf using '**#**' if you don't want to generate the items and libraries in the vhd file.
  - remember to add a ```<space>``` behind item name to assign content. 
  - `Time` `Platform`will be auto completed. If ```Engineer``` is not specified vxgen will use <usrname>.
  - If \<width\> is not specified, default value is 1

**example of usage**
```
vxgen gen test -i clk rst data 8 -o data_out 16     # test.vhd will be generated
vxgen gen test -i clk -o data 8 -i rst -io bus 16   # -i -o -io can exist anywhere
vxgen gen test.vhd  -i clk rst -o output            # test.vhd will be generated
vxgen gen test.txt                                  # test.txt.vhd will be generated
vxgen gen ~/work-dir/test                           # add full path, '.vhd' can still be omitted; no ports;
```
  
### Add code framworks or components
```
vxgen add <filename> <component> {<args>} {-f <folder>}
```


| component | description |
|  :-: | ------------- |
| counter | Counter named "count&lt;countNum&gt;" is added to &lt;filename&gt;, which will count from 1 to &lt;countNum&gt; and reset to 0. |
| div_clk | Divided the clk by &lt;div&gt; and named the out put clk like "clkd_10" "clkd_3" etc. |
| FSM | Create the FSM framwork. \<args\> can be one number, where states like s0 s1 ... will be generated. One can also specify state names in \<args\> |
| reg | Create reg framework as indicated by ps(positive triggered,sync reset) na(negative triggered,asynchronous reset) pa ns. Default ps |
| \<component\> | The tool will check first in the current folder for the component and add. If not exists, the tool will then find in lib. if -n is specified, the tool will not do the auto instantiation and connection. |

*<filename> should not contain path
*Script will be generated in \<filename\> for counter, clk_div, fsm and reg.
*Remember to name the \<component\> with '_' to indicate that it's not the first level entity.
*the auto connection will connect port with the signals or ports witn same name and width. If not exist, the tool will generate signals for component. Especially if the signals or ports exists but width miss-mach, the tool will rename the signal like signalx, signalxx, signalxxx etc.

**example of usage**
```
vxgen add test.vhd counter 200 4    #add two counters, 'test.vhd' is also accepted
vxgen add test div_clk 3 20         #add a even div clk and a odd div clk
vxgen add test fsm 5
vxgen add test fsm  idle work play study
vxgen add test reg                  # add a positive triggered, sync reset reg
vxgen add test reg ps na            # add two regs
vxgen add test testcomponent        # add component from current folder (which means 'testcomponent.vhd' exists in work folder
vxgen add test binary_to_sg.vhd     # add component from lib, vhd file will be copied; 'binary_to_sg.vhd' is also accepted 
```

  
### Top gen
```
vxgen top {<topName>} {-c <components>} {-u <components>] {-i ... -o ... -io ...} {-n} {-f <folder>}
```

args | discription
:-: | --
{\<topName\>} | Specify the name. Default: "\<current-folder\>_TOP".
{-n} | Do not auto connect.
{-f <folder>} | Default : current.
{-c <components>} | include the \<components\>, which is placed in folder
{-u <components>} | Do not include the \<components\>, which means add all components left in folder
{-i ... -o ... -io ...} | io ports for Top entity
  
**example of usage**

Generate top, including entity1 entity2, specify the ports and do the auto connection
```
vxgen top toptop.vhd -c entity1 entity2.vhd -i clk rst -o data  #you can choose whether to add '.vhd'
```
Generate the top named '<currend-folder>_TOP.vhd', add all vhd entities in folder as component and do the auto connection
  
```
vxgen top                               #easy      
```

Generate the top named 'proj_TOP.vhd', specify the ports, add entities in the folder other than sub_component1 sub_component2 and do not do the auto connection

```
vxgen top proj_TOP -i clk rst -o d_out -i d_in -u sub_component1 sub_component2 -n              #declear io anywhere
```
*Do not command -u -c -n more than once. It'll raise error!*

### Testbench gen
```
vxgen tb <entityname> {-q <clkFrequency>} {-d <dutycycle>} {-diff} {-pr/-nr} {-rt <rst-time>}
```

args | discription
:-: | --
\<entityname\> | name
{-q \<clkFrequency\>} | Unit: MHz. Default: 100MHz
{-d \<dutycycle\>} | Unit: %. Default: 50%
{-pn} | Diffrencial clk. Name: "clkn" "clkp"
{-pr/-nr} | Positive reset/ negative reset. **Default: neg-reset**
{-rt \<rst-time\>} | Unit: ns; Default: 1 clk cycle
  
Generate the testbench for specific entity. clock is created named "clk", whose frequency is set to &lt;clkFrequency&gt; MHz (default 100MHz). If -d is specified, the clk dutycycle is set to &lt;dutucycle&gt; (default 50%). If -pn is specified, differencial clk will be generated and named "clkp" and clkn". Reset is auto generated named "rst". If -pr is specified, it will be positive reset, otherwise, default setting is negative reset. Reset will last for &lt;rst-time&gt; (default one clk cycle), and inverted.

**example of usage**

Generate tb_test.vhd with 100Mhz clk and nagative rst.
```
vxgen tb test                     # easy
```
generated tb_test.vhd and 50Mhz differencial clk with 25% duty cycle, rst <= '0', '1' after 20 ns
```
vxgen tb test.vhd -q 50 -d 25 -diff -rt 20    
```
  
### Package gen
```
vxgen pkg <pkg_name> {-a} {-f <folder>}
```

args | discription
:-: | --
<pkg_name> | name
{-a} | Add work lib and this pkg to all file in the folder
{-f <folder>} | Default: current
  
Generated pkg framework named &lt;pkg_name&gt; (default "pkg"). If -a is specified, all file in the folder will add work library as will as this pkg.


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
