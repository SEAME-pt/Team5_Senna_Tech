ssh root@10.21.220.158 "python3 /home/pipeline_vini/main.py /home/models/yolo26n_seg_640.hef /home/models/yolo26n_v5.hef  --remote" | DISPLAY=:1 ffplay -f mjpeg -i -

