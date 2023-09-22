#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from PIL import Image
import keras
# from keras.utils.np_utils import to_categorical
from tensorflow.keras.layers import BatchNormalization
from keras.utils import to_categorical
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout


# In[2]:


get_ipython().system('pip install keras.utils.np_utils')



# In[3]:


parent_folder_path = r"D:\SIH MODEL\archive (18)\IMG_CLASSES"


# In[4]:


# create empty lists to store the image paths and their corresponding class labels
image_paths = []
class_labels = []

# create an empty dictionary to store the class label to subfolder name mappings
class_label_map = {}


# In[5]:


# loop through each subfolder in the parent folder
for subfolder_name in os.listdir(parent_folder_path):
    # get the starting number of the subfolder name
    class_label = int(subfolder_name.split(".")[0]) - 1
    
    # add the class label and subfolder name to the dictionary
    class_label_map[class_label] = subfolder_name.split(".")[1].split(" ")[1]
    
    # loop through each image file in the subfolder
    subfolder_path = os.path.join(parent_folder_path, subfolder_name)
    for image_name in os.listdir(subfolder_path):
        # get the full path to the image file
        image_path = os.path.join(subfolder_path, image_name)
        
        # append the image path and class label to the lists
        image_paths.append(image_path)
        class_labels.append(class_label)


# In[6]:


# create a pandas DataFrame from the image paths and class labels
data = {"image_path": image_paths, "class_label": class_labels}
df = pd.DataFrame(data)

# print the class label map
class_label_map


# In[7]:


df


# In[8]:


# Define the directory containing the image dataset
data_dir = '/path/to/dataset'

# Get the list of subdirectories in the dataset directory (each subdirectory corresponds to a class)
class_names = os.listdir(parent_folder_path)

# Loop over the subdirectories and count the number of files in each one
for class_name in class_names:
    class_dir = os.path.join(parent_folder_path, class_name)
    num_images = len(os.listdir(class_dir))
    print("Class {}: {} images".format(class_name, num_images))


# In[9]:


fig, ax1 = plt.subplots(1, 1, figsize= (10, 5))
df['class_label'].value_counts().plot(kind='bar', ax=ax1)


# In[10]:


# Plot pie chart of train_df
df['class_label'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Distribution of Labels in DataFrame')
plt.legend(df['class_label'].unique())
plt.show()


# In[11]:


max_images_per_class = 2000

# Group by label column and take first max_images_per_class rows for each group
df = df.groupby("class_label").apply(lambda x: x.head(max_images_per_class)).reset_index(drop=True)


# In[12]:


fig, ax1 = plt.subplots(1, 1, figsize= (10, 5))
df['class_label'].value_counts().plot(kind='bar', ax=ax1)


# In[13]:


import concurrent.futures
import tensorflow as tf

# Allow gpu usage
gpus = tf.config.experimental.list_physical_devices('GPU')
print(gpus)
try:
    tf.config.experimental.set_memory_growth = True
except Exception as ex:
    print(e)


# In[14]:


import multiprocessing

# Get the number of CPU cores available
max_workers = multiprocessing.cpu_count()
max_workers


# In[15]:


# Define a function to resize image arrays
def resize_image_array(image_path):
    return np.asarray(Image.open(image_path).resize((100,75)))

# Use concurrent.futures to parallelize the resizing process
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Use executor.map to apply the function to each image path in the DataFrame
    image_arrays = list(executor.map(resize_image_array, df['image_path'].tolist()))

# Add the resized image arrays to the DataFrame
df['image'] = image_arrays
del image_arrays
df


# In[16]:


# for the visulization of dataset
n_samples = 4
fig, m_axs = plt.subplots(10, n_samples, figsize = (4*n_samples, 3*7))
for n_axs, (type_name, type_rows) in zip(m_axs, df.sort_values(['class_label']).groupby('class_label')):
    n_axs[0].set_title(type_name)
    for c_ax, (_, c_row) in zip(n_axs, type_rows.sample(n_samples, random_state=1234).iterrows()):
        c_ax.imshow(c_row['image'])
        c_ax.axis('off')


# In[17]:


df['image'].map(lambda x: x.shape).value_counts()


# In[18]:


from keras.preprocessing.image import ImageDataGenerator

# Create an ImageDataGenerator object with the desired transformations
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest')


# In[19]:


# Create an empty dataframe to store the augmented images
augmented_df = pd.DataFrame(columns=['image_path', 'class_label', 'image'])

# Loop through each class label and generate additional images if needed
for class_label in df['class_label'].unique():
    # Get the image arrays for the current class
    image_arrays = df.loc[df['class_label'] == class_label, 'image'].values
    
    # Calculate the number of additional images needed for the current class
    num_images_needed = max_images_per_class - len(image_arrays)
    
    # Generate augmented images for the current class
    if num_images_needed > 0:
        # Select a random subset of the original images
        selected_images = np.random.choice(image_arrays, size=num_images_needed)
        
        # Apply transformations to the selected images and add them to the augmented dataframe
        for image_array in selected_images:
            # Reshape the image array to a 4D tensor with a batch size of 1
            image_tensor = np.expand_dims(image_array, axis=0)
            
            # Generate the augmented images
            augmented_images = datagen.flow(image_tensor, batch_size=1)
            
            # Extract the augmented image arrays and add them to the augmented dataframe
            for i in range(augmented_images.n):
                augmented_image_array = augmented_images.next()[0].astype('uint8')
                augmented_df = augmented_df.append({'image_path': None, 'class_label': class_label, 'image': augmented_image_array}, ignore_index=True)
    
    # Add the original images for the current class to the augmented dataframe
    original_images_df = df.loc[df['class_label'] == class_label, ['image_path', 'class_label', 'image']]
    augmented_df = augmented_df.append(original_images_df, ignore_index=True)

# Group the augmented dataframe by the 'label' column and filter out extra images
df = augmented_df.groupby('class_label').head(max_images_per_class)

del augmented_df

# Use the augmented dataframe for further processing
df = df.sample(frac=1, random_state=42).reset_index(drop=True)


# In[20]:


df.groupby('class_label').size()


# In[21]:


# Count the number of images in each class
class_counts = df['class_label'].value_counts().sort_index()

# Print the number of images in each class
print("Dataset Summary")
print("-" * 50)
print(f"{'Class Label':<15} {'Class Name':<30} {'Count':<10}")
print("-" * 50)
for class_label, class_name in class_label_map.items():
    count = class_counts[class_label]
    print(f"{class_label:<15} {class_name:<30} {count:<10}")
print("-" * 50)
print(f"{'Total':<45} {sum(class_counts):<10}")


# In[22]:


features=df.drop(columns=['class_label','image_path'],axis=1)
target=df['class_label']


# In[23]:


target.head()


# In[24]:


print(target.shape,features.shape)


# In[25]:


x_train_o, x_test_o, y_train_o, y_test_o = train_test_split(features, target, test_size=0.20,random_state=1234)


# In[26]:


x_train_o


# In[27]:


x_train = np.asarray(x_train_o['image'].tolist())
x_test = np.asarray(x_test_o['image'].tolist())

x_train_mean = np.mean(x_train)
x_train_std = np.std(x_train)

x_test_mean = np.mean(x_test)
x_test_std = np.std(x_test)

x_train = (x_train - x_train_mean)/x_train_std
x_test = (x_test - x_test_mean)/x_test_std


# In[28]:


# Perform one-hot encoding on the labels

y_train = to_categorical(y_train_o,num_classes = 10)
y_test = to_categorical(y_test_o,num_classes = 10)


# In[29]:


x_train, x_validate, y_train, y_validate = train_test_split(x_train, y_train, test_size = 0.1, random_state = 2)


# In[30]:


# Reshape image in 3 dimensions (height = 75px, width = 100px , canal = 3)
x_train = x_train.reshape(x_train.shape[0], *(75, 100, 3))
x_test = x_test.reshape(x_test.shape[0], *(75, 100, 3))
x_validate = x_validate.reshape(x_validate.shape[0], *(75, 100, 3))


# In[31]:


num_classes = 10
from keras.optimizers import SGD
input_shape = (75,100,3)

from tensorflow.keras.applications.resnet import preprocess_input as resnet_preprocess_input
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

# DenseNet121
model = Sequential()
model.add(DenseNet121(include_top=False, weights='imagenet', input_shape=input_shape))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

opt = SGD(lr=0.001, momentum=0.9)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])


# In[32]:


learning_rate_reduction = ReduceLROnPlateau(monitor='val_acc',
                                            patience=3,
                                            verbose=1,
                                            factor=0.5,
                                            min_lr=0.00001)


# In[33]:


# # Fit the model
epochs = 5
batch_size=150
history = model.fit(x=x_train,
                    y=y_train,
                    epochs=epochs,
                    batch_size=batch_size,
                    validation_data=(x_validate,y_validate),
                    callbacks=learning_rate_reduction)


# In[36]:


from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, cohen_kappa_score

# Calculate evaluation metrics
accuracy = accuracy_score(np.argmax(y_test, axis=1), y_pred)
precision = precision_score(np.argmax(y_test, axis=1), y_pred, average='macro')
recall = recall_score(np.argmax(y_test, axis=1), y_pred, average='macro')
f1 = f1_score(np.argmax(y_test, axis=1), y_pred, average='macro')

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-score: {f1:.4f}")


# In[41]:


from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image


# In[73]:


model.save("Skin_SIH.h5")


# In[76]:


def pred(img_path1):
    target_size = (75, 100)  # Set the target size to match DenseNet121's input size
    channels = 3  # Number of color channels

    img = image.load_img(img_path1, target_size=target_size)
    img_array1 = image.img_to_array(img)

# Ensure the image has the correct number of channels
    if img_array1.shape[-1] != channels:
        raise ValueError(f"Input image should have {channels} channels, but got {img_array1.shape[-1]} channels.")

# Expand the dimensions of the image and preprocess it
    img_array1 = np.expand_dims(img_array1, axis=0)
    img_array1 = preprocess_input(img_array1)
    predictions = model.predict(img_array1)
    top_class_index = np.argmax(predictions)
    top_class_label = top_class_index  # Assuming class labels are integers
    top_class_score = predictions[0, top_class_index]

    print(f"Top predicted class: {top_class_label} with score: {top_class_score:.2f}")

    


# In[82]:


po=r"D:\SIH MODEL\archive (18)\IMG_CLASSES\6. Benign Keratosis-like Lesions (BKL) 2624\ISIC_0025743.jpg"


# In[83]:


pred(po)


# In[ ]:




