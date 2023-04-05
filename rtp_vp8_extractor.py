# Copyright [2023-04-05] [nikohpng <hepingadjust@163.com>]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import pyshark
import argparse


def write_header(f: io.FileIO, width: int, height: int, nb_frames: int, fourcc: str):
    # byte 0-3     signature: 'DKIF'
    f.write("DKIF".encode())
    # byte 4-5     version (should be 0)
    f.write(int(0).to_bytes(2, 'little'))
    # byte 6-7     length of header in bytes
    f.write(int(32).to_bytes(2, 'little'))
    # bytes 8-11   codec FourCC (e.g., 'VP80')
    f.write(fourcc.encode())
    # bytes 12-13  width in pixels
    f.write(width.to_bytes(2, 'little'))
    # bytes 14-15  height in pixels
    f.write(height.to_bytes(2, 'little'))
    # bytes 16-23  time base denominator
    # bytes 20-23  time base numerator
    # f.write(int(4294968296).to_bytes(8, 'little'))
    f.write(int(30).to_bytes(4, 'little'))
    f.write(int(1).to_bytes(4, 'little'))
    # bytes 24-27  number of frames in file
    f.write(int(nb_frames).to_bytes(4, 'little'))
    # bytes 28-31  unused
    f.write(int(0).to_bytes(4, 'little'))


def write_frame(f: io.FileIO, pts: int, packet: bytes):
    # bytes 0-3    size of frame in bytes (not including the 12-byte header)
    f.write(len(packet).to_bytes(4, 'little'))
    # bytes 4-11   64-bit presentation timestamp
    f.write(pts.to_bytes(8, 'little'))
    f.write(packet)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--width', type=int, help='vp8 video width pixel', required=True)
    parser.add_argument('--height', type=int, help='vp8 video height pixel', required=True)
    parser.add_argument('--fps', type=int, help='vp8 video fps', required=True)
    parser.add_argument('--source', type=str, help='vp8 pcap file', required=True)
    parser.add_argument('--udp_port', type=int, help='vp8 source udp port', required=True)
    parser.add_argument('--tshark', type=str, help='tshark.exe position', required=True)
    parser.add_argument('--out_path', type=str, help='output ivr file', required=True)

    args = parser.parse_args()

    width = args.width    # video frame width
    height = args.height  # video frame height
    fps = args.fps        # video frame rate
    num_frames = 0        # number of video frames

    path = args.source
    cap = pyshark.FileCapture(path, tshark_path=args.tshark, include_raw=True, use_json=True,
                              decode_as={'udp.port=={0}'.format(args.udp_port): 'rtp'})

    frames: bytes = bytes()

    with open('{0}\\output.ivf'.format(args.out_path), 'wb') as f:
        write_header(f, width, height, 0, "VP80")
        for packet in cap:
            rtp_raw = bytes.fromhex(packet.rtp_raw.value)
            if 'VP8' in packet and (rtp_raw[1] & 0x80) == 0x80:
                # print(dir(packet["RTP"].timestamp.int_value()))
                # print(dir(packet['VP8']))
                frames += bytes.fromhex(packet.vp8_raw.value)[4:]
                write_frame(f, num_frames, frames)
                num_frames = num_frames+1
                frames = bytes()
            elif (rtp_raw[1] & 0x80) == 0:
                frames += bytes.fromhex(packet.vp8_raw.value)[4:]
    with open('{0}\\output.ivf'.format(args.out_path), 'r+b') as f:
        write_header(f, width, height, num_frames, "VP80")
