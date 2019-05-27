# VHDL-Xgen
VHDL auto generation tool, Targetting Synchronous, Top-down design flow. Support only one entity per file.

```Still developing```

## Function
### Generation from templete
``` 
vxgen gen {<path>} <entityname>
```
Generate the templete ```.vhd``` file based on ```<VXGEN-PATH>/templete/title.conf``` and ```libaray.conf```
  - Comment in .conf using '**#**' if you don't want to generate the items and libraries in the vhd file.
  - remember to add a ```<space>``` behind item name to assign content. 
  - Time will be auto completed. If ```Engineer``` is not specified vxgen will use <usrname>.
  
### Add components
```
vxgen add <file-name> <component-name> {<args>}
```
Add components to existing vhd file.
- default path of the <filename> will be current folder.
-  ```<component-name> {<args>}``` could be:
  - ```counter <countNum>```
  - ```divclk <div>```
  - ```<filename> <whether_auto_connect>```
  - ```To be filled```
  
 
### Top gen
```
vxgen top {-n <topName>} {-m <mode>} {-f <folder>}
```
Auto generation & connection for Top entities.


### Testbench gen
```
vxgen tb <filename> {<clkFrequency>} {<rstPN>} {-d <dutycycle>} {-pn} {-rt <rst-time>}
```

### Notes

------------------
