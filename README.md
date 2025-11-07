# Cloud Enabled Tuberculosis Diagnosis System using Convolutional Neural Network (CNN)
<img src="img/tuberculosis_image.jpg">

> Tuberculosis (TB) is a chronic lung disease that occurs due to bacterial infection and is one the top ten leading causes of death. Accurate and early detection of TB is very important, otherwise, it could be life-threatening. We have detected TB reliably from the chest X-ray images using image preprocessing, data augmentation, image segmentation, and Support Vector classification techniques.

> Several public databases were used to create a database of 1800TB infected and 3700 normal chest X- ray images for this study. Our methodology also makes use of Image Enhancement Techniques for enhancing the blurred image for improving accuracy. The entire prediction is presented as a web Based UI which makes the model available to the common people. The entire model is deployed on the cloud for the larger computational power.

## <h2>Get Started with </h2>

```bash
https://github.com/Rohini-Viswanathan/Tuberculosis-Diagnosis-System-using-CNN
```

## <h3>Dataset Description</h3>
Researchers from Qatar University and the University of Dhaka, with collaborators from Malaysia, have developed a chest X-ray image database for TB and Normal cases. The dataset includes 700 publicly accessible TB images and 3500 normal images. An additional 2800 TB images are available for download from the NIAID TB portal upon agreement. The     collaboration involves medical experts from Hamad Medical Corporation and Bangladesh.

## <h3>Project Structure</h3>

* `notebooks` : Jupyter notebooks for data exploration, preprocessing, and model training.
* ``README.md`` : Project documentation.

## <h2>Installation</h2>
To run this project locally, follow these steps:
1. **Clone this Repository** :
   ```bash
   https://github.com/Rohini-Viswanathan/Tuberculosis-Diagnosis-System-using-CNN
   ```

2. **Install Python** :
   
   Windows
   ```bash
   https://www.python.org/downloads/
   ```
   
4. **Create a virtual environment** :
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   
5. **Install required pip libraries**
   * OpenCV  
   * TensorFlow
   * Keras
   * scikit-learn
   ```bash
   pip install <above packages name>
   ```
6. **Install Cloud python library**
   * Streamlit

7. Open the Jupyter notebook to run the Project
   ```bash
   jupyter notebook
   ```
   
## <h2>Evaluation Metrics</h2>

* Precision: The proportion of true positive predictions among all positive predictions.
* Recall: The proportion of true positive predictions among all actual positives.
* F1-Score: The harmonic mean of precision and recall.
* ROC-AUC: The area under the receiver operating characteristic curve.
    
## <h2>Acknowledgements</h2>

Download the Dataset from the Kaggle
```
https://www.kaggle.com/datasets/tawsifurrahman/tuberculosis-tb-chest-xray-dataset
```

## <h2>Licence</h2>
[MIT license](LICENSE)
