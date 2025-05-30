This is a README file for setup of TensorFlow Model Garden's EfficientDet-D0

1. python -m venv env_name
On Windows: env_name\Scripts\activate

Set up the virtual environment and activate it. If running into security issue while activating the environment, use

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

to allow the environment to be activated.

2. Before starting, install required libraries:
pip install --upgrade pip
pip install tensorflow==2.10.0
pip install tf-slim
pip install opencv-python
pip install matplotlib
pip install pandas
pip install lxml
pip install Cython
pip install contextlib2
pip install pillow
pip install pycocotools
pip install numpy==1.24.4

3. Clone the TensorFlow models repository:
git clone https://github.com/tensorflow/models.git
cd models/research

4. Compile and Install the Object Detection API

# From models/research/
protoc object_detection/protos/*.proto --python_out=.

# Install the package
cp object_detection/packages/tf2/setup.py .
pip install -e .

5. Test the installation:
python -c "from object_detection.utils import label_map_util"

if no errors, installation was successful.

6. Setting up dataset, it should be in this directory layout
dataset/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── annotations/
│   ├── instances_train.json
│   ├── instances_val.json
│   ├── instances_test.json
│   └── label_map.pbtxt


also create a label.pbtxt file with:
item {
  id: 1
  name: 'carplate'
}

*IMPORTANT SO IT WILL RUN PROPERLY*

7. Convert the dataset
python create_coco_tf_record.py \
  --logtostderr \
  --train_image_dir=.../images/train \
  --val_image_dir=.../images/val \
  --test_image_dir=.../images/test \
  --train_annotations_file=.../annotations/instances_train.json \
  --val_annotations_file=.../annotations/instances_val.json \
  --testdev_annotations_file=.../annotations/instances_test.json \
  --output_dir=.../tfrecord \
  --include_masks=False

8. Edit the pipeline.config file and the filepaths inside it, such as train_input_reader and eval_input_reader. Point pipeline.config to the config file included in GitHub.

9. Finally, run training with(filepaths are just examples) :
python models/research/object_detection/model_main_tf2.py `
--model_dir="C:..\checkpoint" ` #output folder
--pipeline_config_path="C:...\pipeline.config" `
--alsologtostderr ` 
--checkpoint_every_n=1000 

and evaluation with (filepaths are just examples):

python models/research/object_detection/model_main_tf2.py `
  --pipeline_config_path="C:\Users\maxmi\Documents\Swinburne\DEGREE\Y2S1\COS30018 INTELLIGENT SYSTEMS\tensorflow-model-maker-test\models\research\efficientdet_d0_coco17_tpu-32\pipeline.config" `
  --model_dir="...\checkpoint" `
  --checkpoint_dir="C:\Users\maxmi\Documents\Swinburne\DEGREE\Y2S1\COS30018 INTELLIGENT SYSTEMS\tensorflow-model-maker-test\tf-garden\model_directory_results\checkpoint" `
  --run_once=True `
  --alsologtostderr


9. Install TensorBoard and point it to train and eval folders with contain event files to monitor metrics with graphs (OPTIONAL)

The images will have to be provided yourselves, together with the tfrecord conversion and json annotations. the provided paths are just examples


