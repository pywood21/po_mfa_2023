## Simultaneous cell-by-cell recognition and microfibril angle determination in Japanese hardwoods by polarized optical microscopy combined with semantic segmentation

-----

#### **Author**: 

Yusuke Kita<sup>1</sup>, Titis Setiyobudi<sup>1</sup>, Tatsuya Awano<sup>1</sup>, Arata Yoshinaga<sup>1</sup>, Junji Sugiyama<sup>1</sup>

#### **Affiliation**: 

1. Division of Forest and Biomaterials Science, Kyoto University, Kyoto, 606-8502, Japan

#### **Link to paper**

DOI : [https://doi.org/10.1007/s10570-023-05351-0](https://doi.org/10.1007/s10570-023-05351-0)

#### **Link to full-text access to a view-only version**

https://rdcu.be/dfYhr

-----

### 1. Brief Introduction

Hardwood species have flourished in the recent evolutionary history of angiosperms and exhibit pronounced diversity in cell anatomy, such as cell arrangement, cell type, ultrastructure, and cellulose microfibril angle (Calquist 2001). Optimization of the mass transportation and load-bearing functions of wood can be realized by complex combinations of these structural features (Berglund and Burgert 2018). To decipher species-by-species structural optimization strategies, multiscale wood cell structures should ideally be measured simultaneously. However, methodological restrictions have hampered progress in this respect. <br>

In this work, we aimed to develop new methodological framework to achieve simultaneous measurements of MFA and cell anatomical parameters for clarifying wood species dependent survival  and environmental adaptation strategies in cellular resolution, and to applied it to Japanese hard wood species characterized by various anatomical features. To achieve the above purpose, we utilized and combined polarization optical microscopy (POM)-based MFA imaging (Abraham & Elbaum 2013; Kita & Sugiyama 2021; Kita et al. 2022), deep learning-based semantic segmentation (Guo et al. 2018), and image analysis techniques specialized in measurements of wood cell anatomical parameters (e.g. Prendin et al. 2017). In addition, POM results were verified by XRD-based MFA measurement (Donaldson 2008) and their methodological perspectives are discussed.<br>



##### References

- Abraham Y, Elbaum R (2013) Quantification of microfibril angle in secondary cell walls at subcellular resolution by means of polarized light microscopy. New Phytol 197: 1012-1019.
- Berglund LA, Burgert I (2018) Bioinspired wood nanotechnology for functional materials. Adv Mater 30:1704285.
- Carlquist S (2001) Comparative wood anatomy: systematic, ecological, and evolutionary aspects of dicotyledon wood. Springer, Berlin.
- Donaldson L (2008) Microfibril angle: measurement, variation and relationships – a review. IAWA J 29:345–386.
- Guo Y, Liu Y, Georgiou T, Lew MS (2018) A review of semantic segmentation using deep neural networks. Int J Multimed Inf Retr 7:87–93.
- Kita Y, Sugiyama J (2021) Wood identification of two anatomically similar Cupressaceae species based on two-dimensional microfibril angle mapping. Holzforschung 75: 591-602.
- Kita Y, Awano T, Yoshinaga A, Sugiyama J (2022) Intra-annual fluctuation in morphology and microfibril angle of tracheids revealed by novel microscopy-based imaging. 17: e0277616.
- Prendin LA, Petit G, Carrer M, Fonti P, Bjorklund J, von Arx G (2017) New research perspectives from a novel approach to quantify tracheid wall thickness. Tree Physiol 37: 976-983.

&nbsp;

----

### 2. Main results

#### Comparison of two methodologies, POM and XRD

<img src="./Figs/Fig1.PNG" style="zoom:75%;" />

This figure corresponds to a scatter plot, regression line of MFA measured by POM (x-axis) and XRD (y-axis). Our results clarified that MFA obtained by the both methodologies well coincide with each other within the wide range. Considering this result and their theoretical backgrounds, advantages and limitations of the both methods are discussed in our paper.

&nbsp;

#### Cell-by-cell MFA measurement and visualization by POM

<img src="./Figs/Fig2.PNG" style="zoom:75%;" />

This section introduces what POM-based MFA imaging can do in evaluation of hardwood cell anatomy. The above figures exemplify the results of MFA imaging applied to one of diffuse-porous hardwood species, *Acer nipponicum*. Each figure corresponds to (a) its MFA map in latewood side, expanded to (b) a fiber, (c) axial parenchyma surrounding a vessel element, (d) vessel element and (e) axial parenchyma located at an annual ring boundary (terminal axial parenchyma), respectively.<br>

Cell-by-cell MFA measurement clearly shows large MFA variations depending on wood cell species. General trends are following: fibers have lower MFA, vessel elements and axial parenchyma tend to be higher MFA. This result is reasonable considering functional differentiation and roles of each cell species. Interestingly, axial parenchyma has different layer compositions or MFA values depending on their positions, around vessel element or earlywood-latewood boundary.<br>In our paper, the same kind of analysis is also applied to ring-porous *Quercus serrata* in addition to *Acer nipponicum*.

&nbsp;

#### Relationships between MFA and CWT

<img src="./Figs/Fig4.PNG" style="zoom:75%;" />

Combined with measurements of by POM and of cell anatomical parameters by image analysis, the both relationships can be evaluated and discussed. In this work, we targeted MFA and CWT, which largely contribute to mechanical strengths of living trees, and performed their simultaneous evaluation in some representative specimens (angiosperms without vessels, with ring-porous and diffuse-porous). <br>

The above example corresponds to (a) a MFA map, (b) intra-annual fluctuations of MFA and CWT, and (c) a scatter plot of MFA vs CWT in vesselless *Trochodendron aralioides*, respectively. The body of this species mainly consisted of trachieds and its transverse section clearly shows softwood-like earlywood-latewood transition within its annual ring. The scatter plot clarified negative correlation (thicker CWT, lower MFA) between them and this result imply that trachieds achieve role-exchanging through cell structure optimization in nano and micro scales. We performed the similar analysis in the other wood species with ring-porous and diffuse porous, and our study demonstrated vessel-porosity  and wood species dependency of MFA and CWT relationship.<br>

&nbsp;

-----

### 3. About this repository

This repository contains all programing codes used in this work. Using these codes, the followings can be achieved if data is appropriately collected.<br> 

1. Microfibril angle measurements from wood cross sections
   (see [class_funcs](https://github.com/pywood21/po_mfa_2023/tree/main/src/class_func/POM))
2. Automatic quantitative measurements of wood cell anatomical parameters such as cell area, lumen radial diameter, cell wall thickness, etc.
   (see [class_funcs](https://github.com/pywood21/po_mfa_2023/tree/main/src/class_func/Segmentation)))
3. Microfibril angle measurements using single crystal Xray diffractometer
   (see [class_funcs](https://github.com/pywood21/po_mfa_2023/tree/main/src/class_func/Xray))

The details of how to use each class functions are exemplified by jupyter notebooks used in our work (see [jupyter_notebooks](https://github.com/pywood21/po_mfa_2023/tree/main/src/jupyter_notebooks)).<br>

&nbsp;

----

### 4. Required apparatus for data collection

Required apparatus for data collection are listed below.<br>

1. Polarized optical microscope equipped with a quarter wave plate, interference plate<sup>*1</sup> and scientific CMOS camera.
2. Graphical processing unit for semantic segmentation tasks (if pretrained model is already prepared, this is not necessary)
3. single crystal Xray diffractometer

Details of the apparatus we used (manufactures, experimental conditions, etc.) are described in our paper (see [our_paper](https://doi.org/10.1007/s10570-023-05351-0)). Details of the experimental procedure is well documented in our previous work (see [our_previous_paper](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0277616)).

&nbsp;

#### **Note**

*1) Interference filter is required due to the selection of appropriate incident light source wavelength for a quarter waveplate.





 



