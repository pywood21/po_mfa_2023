### Simultaneous cell-by-cell recognition and microfibril angle determination in Japanese hardwoods by polarized optical microscopy combined with semantic segmentation

-----

**Author**: 

Yusuke Kita<sup>1</sup>, Titis Setiyobudi<sup>1</sup>, Tatsuya Awano<sup>1</sup>, Arata Yoshinaga<sup>1</sup>, Junji Sugiyama<sup>1</sup>

**Affiliation**: 

1. Division of Forest and Biomaterials Science, Kyoto University, Kyoto, 606-8502, Japan

**Link to paper**

add link here.

-----

#### 1. Brief Introduction





#### 2. Main results





-----

#### 3. About this repository

This repository contains all programing codes used in this work. Using these codes, the followings can be achieved if data is appropriately collected.<br> 

1. Microfibril angle measurements from wood cross sections
   (see [class_funcs](https://github.com/pywood21/po_mfa_2023/tree/main/src/class_func/POM))
2. Automatic quantitative measurements of wood cell anatomical parameters such as cell area, lumen radial diameter, cell wall thickness, etc.
   (see [class_funcs](https://github.com/pywood21/po_mfa_2023/tree/main/src/class_func/Segmentation)))
3. Microfibril angle measurements using single crystal Xray diffractometer
   (see [class_funcs](https://github.com/pywood21/po_mfa_2023/tree/main/src/class_func/Xray))



#### 4. Required apparatus for data collection

Required apparatus for data collection are listed below.

1. Polarized optical microscope equipped with a quarter wave plate, interference plate<sup>*1</sup> and scientific CMOS camera.
2. Graphical processing unit for semantic segmentation tasks (if pretrained model is already prepared, this is not necessary)
3. single crystal Xray diffractometer



**Note**

*1) Interference filter is required due to the selection of appropriate incident light source wavelength for a quarter waveplate.





 



