# Disease Detection from Chest X-RAYs
The project uses the standard [NIH Chest X-Ray dataset](https://www.kaggle.com/datasets/nih-chest-xrays/data) as well as privately aquired radiology reports. The repo consists of the following:
1. sortfile.py: A program to classify the reports and associated images into 1 of the 16 categories based on regualr expression matching
2. A VGG based classifier
3. A CBAM based classifier
4. a GradCAM model in order to create a heat map to better visualize the X-Ray
