# rtp_vp8_extractor

this script will export vp8 from pcap file. this file can played by ffplay or other player.

this file format is `ivf`, you can see [this](https://wiki.multimedia.cx/index.php?title=IVF)

## Environment And Dependency

- [x] python3
- [x] tshark

## How to use it

+ prepare vp8 pcap, and run `pip3 install tshark`
+ install wireshark, find `tshark` position
+ run script, and fill args, like this: 
    ```python
  python3 rtp_vp8_extractor.py --width=480 --height=640 --fps=30 --source=C:\Users\test\Desktop\test.pcap --udp_port=12264 --tshark=D:\Capture\Wireshark\tshark.exe --out_path=C:\test\hpng\Desktop\
    ```
## Plan

- [x] python script 
- [ ] wireshark lua plugin



## Reference

+ [https://wiki.multimedia.cx/index.php?title=IVF](https://wiki.multimedia.cx/index.php?title=IVF)