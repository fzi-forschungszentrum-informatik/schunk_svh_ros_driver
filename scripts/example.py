#!/usr/bin/env python3
################################################################################
# Copyright 2022 FZI Research Center for Information Technology
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
"""
Control the Schunk SVH's joints with a graphical slider

This is a small helper to manually test the SVH with ROS2-control.  It provides
a minimal GUI with a single slider that changes the SVH's state between a
`fist` and a `full spread`.  It assumes a running `joint_trajectory_controller`
for all joints.
"""
import numpy as np
from tkinter import Tk, Scale
import rclpy
from rclpy.node import Node
import subprocess
import sys

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class SVH(Node):
    def __init__(self):
        super().__init__('svh_gui')

        # Check the available ROS2 nodes for a joint trajectory controller.
        # It's either called /left_hand or /right_hand.
        nodes = subprocess.check_output("ros2 node list", stderr=subprocess.STDOUT, shell=True)
        nodes = nodes.decode("utf-8").split('\n')
        if "/left_hand" in nodes:
            controller = "/left_hand"
            joint_prefix = "Left_Hand"
        elif "/right_hand" in nodes:
            controller = "/right_hand"
            joint_prefix = "Right_Hand"
        else:
            rclpy.shutdown()
            print("No suitable hand controller found.")
            sys.exit(0)

        # Control the hand with publishing joint trajectories.
        self.publisher = self.create_publisher(
            JointTrajectory, f'{controller}/joint_trajectory', 10)

        # Configuration presets
        self.joint_names = [
            f'{joint_prefix}_Thumb_Flexion',
            f'{joint_prefix}_Thumb_Opposition',
            f'{joint_prefix}_Index_Finger_Distal',
            f'{joint_prefix}_Index_Finger_Proximal',
            f'{joint_prefix}_Middle_Finger_Distal',
            f'{joint_prefix}_Middle_Finger_Proximal',
            f'{joint_prefix}_Ring_Finger',
            f'{joint_prefix}_Pinky',
            f'{joint_prefix}_Finger_Spread',
        ]
        self.fist = [0.6, 0.6, 0.7, 0.7, 0.7, 0.7, 0.6, 0.6, 0.3]
        self.full_spread = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5]

    def gui(self):
        """ A GUI with a single slider for opening/closing the SVH """
        self.percent = 100
        self.window = Tk()
        self.window.title('Schunk SVH')
        self.slider = Scale(self.window, from_=self.percent, to=0)
        self.slider.set(self.percent)
        self.slider.bind("<ButtonRelease-1>", self.slider_changed)
        self.slider.pack()
        self.window.mainloop()

    def slider_changed(self, event):
        self.publish(self.slider.get())
        rclpy.spin_once(self, timeout_sec=0)

    def publish(self, opening):
        """ Publish a new joint trajectory with an interpolated state

        We scale linearly with opening=[0,1] between `fist` and `full_spread`.
        """
        jpos = opening * np.array(self.full_spread) + \
            (self.percent - opening) * np.array(self.fist)
        jpos = jpos / self.percent
        msg = JointTrajectory()
        msg.joint_names = self.joint_names
        jtp = JointTrajectoryPoint()
        jtp.positions = jpos.tolist()
        jtp.time_from_start = Duration(sec=2)
        msg.points.append(jtp)
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    svh = SVH()
    svh.gui()
    svh.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()