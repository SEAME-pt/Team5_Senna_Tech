ssh root@10.21.220.158 "HAILO_MONITOR=1 python3 /home/pipeline/main.py /home/pipeline/yolo26n_seg_640.hef /home/pipeline/yolo26n_v4.hef --virtual --no-display" | DISPLAY=:1 ffplay -f mjpeg -i -
