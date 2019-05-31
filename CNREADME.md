# VHDL-Xgen

[![build status](https://img.shields.io/badge/build-pass-brightgreen.svg)](https://img.shields.io/badge/build-pass-brightgreen.svg)
[![test status](https://img.shields.io/badge/test-pass%20basic-blue.svg)](https://img.shields.io/badge/test-pass%20basic-blue.svg)

VHDL 自动生成工具,面相同步电路，自顶向下流程设计。

## 编译
Python 文件不需要编译，但需要你安装了Python环境，主文件是 `src/vxgen.py`. 

**Linux**

终端输入
```
cd $VHDL-Xgen-dir 
sh setup.sh
```
搞定！

再次打开终端，看看现在是否能够使用
```
vxgen version
```
如果你看到提示信息说明你已经可以正常使用以下功能了。
**Windows**

我们需要cmd. 如果你对系统比较了解，请打开 [`setup_win.cmd`](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/setup_win.cmd) [`setenv_win.cmd`](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/data/setenv_win.cmd) 看看我写了什么。当然你也可以以自己习惯的方式配置 :)

请尽量将仓库文件夹存储在安全位置，不要移动。如果移动，你可能需要重新运行
```
右键-以管理员方式打开setup_win.cmd
```
搞定！
打开cmd看看是否能够使用
```
vxgen version
```
如果你看到提示信息说明你已经可以正常使用以下功能了。
## 仓库文件结构
folder | explanition
:--: | --
master | 包含 README 和 setup files
src | 主要代码
data | 包含重要数据 **请不要更改**
conf | 配置默认文件头和library
lib | 你可以在这里添加你自己的lib，使用add功能作为component添加
examples | 一些例子



## 使用
```
vxgen <func> {<args>}
```
------------------

## 代码规范要求
* 关键字**小写**
* 主entity需要写在文件末尾
* 请使用 `end entity <entityname>`不要只写 `end <entityname>`.
-------------------

## [gen](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#generation)  &#160;&#160;&#160;&#160;[add](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#add-components) &#160;&#160;&#160;&#160;[top](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#top-gen)  &#160;&#160;&#160;&#160;[tb](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#testbench-gen) &#160; &#160;&#160;&#160;[pkg](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#package-gen)  &#160;&#160;&#160;&#160;[version](https://github.com/wangyipengw1p/VHDL-Xgen/blob/master/README.md#version)

## Generation
``` 
vxgen gen <filename> {-i <name> <width> ...} {-o <name> <width> ...} {-io <name> <width> ...} 
```
依据```<VXGEN-PATH>/conf/title.conf``` 和 ```libaray.conf``` 的配置生成VHDL文件框架
  - 在conf文件中请使用'**#**'来注释
  - `Time` `Platform`会自动生成， 如果 ```Engineer``` 没有设置，将使用系统用户名
  - 如果 \<width\> 没有指明，默认1, 也就是`std_logic`. 目前port种类只支持 `std_logic` 和 `std_logic_vector`
  
**例**
```
vxgen gen test -i clk rst data 8 -o data_out 16     # 生成了test.vhd
vxgen gen test -i clk -o data 8 -i rst -io bus 16   # -i -o -io 可以乱序，或者重复出现
vxgen gen test.vhd  -i clk rst -o output            # 这里生了test.vhd
vxgen gen test.txt                                  # 而这里生成了test.txt.vhd
vxgen gen ~/work-dir/test                           # 可以写绝对路径, '.vhd' 可以省略，没有ports
```
  
## 添加代码框架和component
```
vxgen add <filename> <component> {<args>} {-f <folder>}
```


| component | description |
|  :-: | ------------- |
| counter | 在文件中添加信号名为“counter$数”的计数器，计数器重置为0，工作时从1到#，可添加多个 |
| clk_div | 在文件中添加时钟分频，生成信号名为例如 "clkd_10" "clkd_3" ，奇偶分频均支持自动生成，可添加多个|
| fsm | 在文件中添加有限状态机，如果\<arg\>是一个数字，将会自动生成例如s0 s1 ...的状态，否则将会用你指明的名字命名状态。当然了工具只会添加代码框架，核心逻辑还需要你来完成 |
| reg | 添加D触发器的代码框架，参数可选择 `ps`(positive triggered,sync reset) `na`(negative triggered,asynchronous reset) `pa` `ns`. 默认 `ps` ，可添加多个|
| \<component\> | 添加component，工具会现在当前目录中寻找，如果没有的话会在lib中寻找并复制到当前目录。-n 会使工具不进行自动连接 |

* <filename> 不应包含路径，事实上路径会被工具忽略。正确做法是用-f指明。当然还是推荐者在当前目录工作。
* counter, clk_div, fsm and reg 都是在文件中生成代码，而添加component只是实例化和链接。
* 工具会自动连接名字相同而且位宽相同的端口，如果没有找到同名端口，工具会添加一个signal，如果名字相同位宽不同，工具会重命名component的端口并添加signal（重命名会在原有名称后面加x，直到不重名） 
* 前面提到工具目前只支持`std_logic` 和 `std_logic_vector`。用户自定义类型会被视作  `std_logic`。特殊的，类似`unsigned(7 downto 0)` 的port会被视为 `std_logic_vector(7 downto 0)`
* 工具在自动连接的时候暂时没有考虑`in` `out` 属性，因为我懒，略略略
* 注意：工具目前只支持`downto`形式的位宽声明

**example of usage**
```
vxgen add test.vhd counter 200 4    # 添加两个counter
vxgen add test div_clk 3 20         # 添加一个奇数分频时钟，一个偶数分频时钟
vxgen add test fsm 5
vxgen add test fsm  idle work play study
vxgen add test reg                  # add a positive triggered, sync reset reg
vxgen add test reg ps na            # 添加两个dff
vxgen add test testcomponent        # 天价当前文件夹中的'testcomponent.vhd'作为component
vxgen add test binary_to_sg.vhd     # 从库中添加'binary_to_sg.vhd'作为component
```

  
## Top gen
```
vxgen top {<topName>} {-c <components>} {-u <components>] {-i ... -o ... -io ...} {-n} {-f <folder>}
```

args | discription
:-: | --
{\<topName\>} | 默认 "\<current-folder\>_TOP".
{-n} | 不自动连接
{-f <folder>} | 更改目录，默认当前目录
{-c <components>} | 添加指定的component
{-u <components>} | 添加除了指定文件，当前目录下所有可以作为component的entity，作为top的component
{-i ... -o ... -io ...} | 指定top文件端口
  
* 工具会自动排除名字中有tb,TOP,pkg的.vhd文件
* 不能同时或者多次使用-c和-u，工具会报错
  
**例**

top包含 entity1 entity2, 指定了端口并且自动连接
```
vxgen top toptop.vhd -c entity1 entity2.vhd -i clk rst -o data  #you can choose whether to add '.vhd'
```
一句话生成top文件，爽不爽？生成默认名称'<currend-folder>_TOP.vhd'的top文件,添加所有合适文件作为component，并且自动连接
  
```
vxgen top                               #easy      
```

添加除了 sub_component1 sub_component2 的目录下其他合适文件，不作实例化和连接

```
vxgen top proj_TOP -i clk rst -o d_out -i d_in -u sub_component1 sub_component2 -n              #io可以出现多次，-c-u不行
```


## Testbench gen
```
vxgen tb <entityname> {-q <clkFrequency>} {-d <dutycycle>} {-diff} {-pr/-nr} {-rt <rst-time>}
```

args | discription
:-: | --
\<entityname\> | 名字
{-q \<clkFrequency\>} | 时钟频率 单位: MHz. 默认: 100MHz
{-d \<dutycycle\>} | 占空比 单位: %. 默认: 50%
{-pn} | 添加差分时钟，命名为"clkn" "clkp"
{-pr/-nr} | 高电平有效或者低电平有效 默认ns
{-rt \<rst-time\>} | Unit: ns; Default: 1 clk cycle
  
* 工具会自动添加clk和rst信号，如果你不想要，那就删了吧

**例**

一句话生成testbench，爽不爽？
```
vxgen tb test                     # easy
```
testbench添加50MHz差分时钟，25%占空比 (rst <= '0', '1' after 20 ns) will be generated.
```
vxgen tb test.vhd -q 50 -d 25 -diff -rt 20    
```
## Package gen
```
vxgen pkg <pkg_name> {-a} {-f <folder>}
```

args | discription
:-: | --
<pkg_name> | pkg的名字，默认当前文件夹名称_pkg.vhd
{-a} | 在文件下所有文件添加这个pkg
{-f <folder>} | Default: current
  


## Version
```
vxgen version
```
版本信息

## Help
```
vxgen help
```
帮助信息，很有用的！


