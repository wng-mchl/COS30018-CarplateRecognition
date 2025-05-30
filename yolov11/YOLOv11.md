--README for YOLOv11--

1. Head into the yolov11.ipynb notebook and follow the steps there, cell by cell.

2. First, mount a drive with dataset pictures within it, change the path to suit setup. 

3. Define the ROOT_DIR variable for later use.

4. Install Ultralytics, this will take a while to download.

5. In this cell, first define the path to the weights you wish to train. Set the path to the YAML file of choice too, this is also preset. The preset one is the most recently trained best.pt weights file. After that, tweak parameters to your liking.

6. Lastly, run the last cell to save the best weights off the Colab runtime. Specify the last argument to the path of your Drive folder you wish to save your weights in.