
# VHDL-Xgen
[![build status](https://img.shields.io/badge/build-pass-brightgreen.svg)](https://img.shields.io/badge/build-pass-brightgreen.svg)
[![test status](https://img.shields.io/badge/test-pass%20basic-blue.svg)](https://img.shields.io/badge/test-pass%20basic-blue.svg)

#### [中文版](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/CNREADME.md) 

VHDL auto generation tool, Targetting Synchronous, Top-down design flow.

## Build
Python file does not need to build. The main file is `src/vxgen.py`. 

**Linux**

For convience, command
```
cd $VHDL-Xgen-dir 
sh setup.sh
```
Done. 

Then re-open the terminal and command following to test if you've done things correctly.
```
vxgen version
```
**Windows**

We need to use cmd. If you know something, make sure to open [`setup_win.cmd`](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/setup_win.cmd) [`setenv_win.cmd`](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/data/setenv_win.cmd) and check :)

Please move the master folder to some safe place on your disk and try NOT to move it.
```
run setup_win.cmd as admin
```
Done.
Then re-open the cmd and command following to test if you've done things correctly.
```
vxgen version
```
## File Structure
folder | explanition
:--: | --
master | Contains README and setup files
src | Main python script 
data | Contain vital data for this tool **DO NOT modify**
conf | library and title configuration [more](https://github.com/wangyipengw1p/VHDL-Xgen#generation)
lib | You can add your own vhd here and add as component [more](https://github.com/wangyipengw1p/VHDL-Xgen#add-code-framworks-or-components)
examples | Some example usages


------------------

## Syntex requirement
* Use **lower case** for keyword.
* Main entity should be at the end of the file.
* Use `end entity <entityname>` instead of just `end <entityname>`.
-------------------

## [gen](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#generation)  &#160;&#160;&#160;&#160;[add](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#add-components) &#160;&#160;&#160;&#160;[top](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#top-gen)  &#160;&#160;&#160;&#160;[tb](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#testbench-gen) &#160; &#160;&#160;&#160;[pkg](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#package-gen)  &#160;&#160;&#160;&#160;[version](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#version)

## Generation
``` 
vxgen gen <filename> {-i <name> <width> ...} {-o <name> <width> ...} {-io <name> <width> ...} 
```
Generate the templete ```.vhd``` file based on ```<VXGEN-PATH>/conf/title.conf``` and ```libaray.conf```
  - Comment in .conf using '**#**' if you don't want to generate the items and libraries in the vhd file.
  - `Time` `Platform`will be auto completed. If ```Engineer``` is not specified \<usrname\> in os will be added.
  - If \<width\> is not specified, default value is 1, which is `std_logic`. Currently, this tool only supports `std_logic` and `std_logic_vector` for signal type.

**example of usage**
```
vxgen gen test -i clk rst data 8 -o data_out 16     # test.vhd will be generated
vxgen gen test -i clk -o data 8 -i rst -io bus 16   # -i -o -io can exist anywhere
vxgen gen test.vhd  -i clk rst -o output            # test.vhd will be generated
vxgen gen test.txt                                  # test.txt.vhd will be generated
vxgen gen ~/work-dir/test                           # add full path, '.vhd' can still be omitted; no ports;
```
  
## Add code framworks or components
```
vxgen add <filename> <component> {<args>} {-f <folder>}
```


| component | description |
|  :-: | ------------- |
| counter | Counter named "count$countNum;" is added to &lt;filename&gt;, which will count from 1 to &lt;countNum&gt; and reset to 0. |
| clk_div | Divided the clk by &lt;div&gt; and named the out put clk like "clkd_10" "clkd_3" etc. |
| fsm | Create the FSM framwork. \<args\> can be one number, where states like s0 s1 ... will be generated. One can also specify state names in \<args\> |
| reg | Create reg framework as indicated by ps(positive triggered,sync reset) na(negative triggered,asynchronous reset) pa ns. Default ps |
| \<component\> | The tool will check first in the current folder for the component and add. If not exists, the tool will then find in lib. if `-n` is specified, the tool will not do the auto instantiation and connection. |

* \<filename\> should not contain path
* Script will be generated **in** \<filename\> for counter, clk_div, fsm and reg. 
* The auto connection will connect port(in component) with the signals or ports (in master file) with the **same name and width**. If not exist, the tool will generate signals for component. Especially if the signals or ports exists but width miss-mach, the tool will add renamed the signal like signalx, signalxx, signalxxx etc.
* As indicated above, currently, this tool only supports `std_logic` and `std_logic_vector` for signal type. For example,  types like `record` or user defined type will be treadted as `std_logic`; Types like `unsigned(7 downto 0)` will be treated as `std_logic_vector(7 downto 0)`
* `in` `out` is not considered while connecting the ports. (Because I think its unnecessary)
* Only `downto` format is supported currently for port connection. 

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

  
## Top gen
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

## Testbench gen
```
vxgen tb <entityname> {-q <clkFrequency>} {-d <dutycycle>} {-diff} {-pr/-nr} {-rt <rst-time>}
```

args | discription
:-: | --
\<entityname\> | name
{-q \<clkFrequency\>} | Unit: MHz. Default: 100MHz
{-d \<dutycycle\>} | Unit: %. Default: 50%
{-diff} | Diffrencial clk. Name: "clkn" "clkp"
{-pr/-nr} | Positive reset/ negative reset. **Default: neg-reset**
{-rt \<rst-time\>} | Unit: ns; Default: 1 clk cycle
  
Generate the testbench for specific entity. clock is created named "clk", whose frequency is set to &lt;clkFrequency&gt; MHz (default 100MHz). If -d is specified, the clk dutycycle is set to &lt;dutucycle&gt; (default 50%). If -diff is specified, differencial clk will be generated and named "clkp" and clkn". Reset is auto generated named "rst". If -pr is specified, it will be positive reset, otherwise, default setting is negative reset. Reset will last for &lt;rst-time&gt; (default one clk cycle), and inverted.

**example of usage**

Generate tb_test.vhd with 100Mhz clk and nagative rst.
```
vxgen tb test                     # easy
```
generated tb_test.vhd and 50Mhz differencial clk with 25% duty cycle. Reset (rst <= '0', '1' after 20 ns) will be generated.
```
vxgen tb test.vhd -q 50 -d 25 -diff -rt 20    
```
## Package gen
```
vxgen pkg <pkg_name> {-a} {-f <folder>}
```

args | discription
:-: | --
<pkg_name> | name
{-a} | Add work lib and this pkg to all file in the folder
{-f <folder>} | Default: current
  
Generated pkg framework named &lt;pkg_name&gt; (default "pkg"). If -a is specified, all file in the folder will add work library as will as this pkg.


## Version
```
vxgen version
```
Check if you've succeffully installed the VHDL-Xgen.

## Help
```
vxgen help
```
Print help message.


