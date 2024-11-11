<p align="center">
<img src="ETBX.ico" alt="ETBX Icon">

</p>

<h1 align="center"> Express-Tuberculosis-Buster 
</h1>

*A desktop application that automates Pulmonary Tuberculosis screening in digital Chest X-rays.*

![Language](https://img.shields.io/badge/language-Python-blue)
![Kivy](https://img.shields.io/badge/framework-Kivy-blue)
![Version](https://img.shields.io/badge/version-1.2-blue)
![License](https://img.shields.io/badge/license-MIT-blue)
<br><br>
# Introduction

Tuberculosis (TB) is a serious infectious disease that remains a significant global health challenge. Early and accurate diagnosis is crucial for effective treatment and disease management. This project aims to develop a Computer-Aided Diagnosis (CAD) system to assist healthcare professionals in the diagnosis of Pulmonary TB


The primary objectives of this project are:
- To design and implement a robust CAD system for the detection and classification of TB from digital Chest X-rays.
- To evaluate the performance of the CAD system and compare it to the accuracy of human experts in TB diagnosis.
- To explore the potential of the CAD system to improve the accessibility and efficiency of TB diagnosis

<br>

# Overview 

ETBX is an offline desktop application that was developed using Kivy, an open-source Python GUI framework. The system is trained on two datasets:
the "Chest X-ray Masks and Labels" for segmentation and "Tuberculosis (TB) Chest X-ray Database" from Kaggle for classification. U-Net Segmentation Model and Efficient-Net B3 were used to analyze the images. The system also leverages Gradient weighted Class Activation Mapping (Grad-CAM) to visualize 
heatmaps on x-ray images.  
<br>

# Features 
<img src="assets\upload-img.png"/>

* Upload and scan x-ray images. Choose a .JPG, .PNG., or a DICOM file to process. 


* Once the image is processed, the classfication and the confidence level of the learning model is displayed. Different images of the x-ray can be toggled between: the original, isolated, and heatmapped version. A full view mode is also available in which an enlarged original and heatmapped scan image is placed side-by-side. Results can be annotated. 

* Save and view patients' scan results. Scan results can be either saved to a patient previously entered into the system or to a new patient. Patient records can also be reviewed 
after saving and the option to export a scan result as 
PDF is also given. 

<br><br>

# Installation 
1. Go to the following link: https://github.com/LoremIpsum-Group/Express-Tuberculosis-Buster/releases/tag/v1.2
2. Once loaded, under assets, click on the Express Tuberculosis Buster exe file to download. 
3. After downloading, it will open up the application setup.
   Click "I accept the agreement" to proceed.
4. Enter LoremIpsum124 in the password field in order to proceed and check the desktop shortcut option if wanted. Wait for the setup to install the application. 
5. Once successfully finished, click Finish to exit setup or click the Launch option to open the application right away.
6. After the application is done loading, the Login page will be presented. Enter doctor and apple for the username and password, respectively. 

