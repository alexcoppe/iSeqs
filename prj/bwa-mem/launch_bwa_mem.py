#!/usr/bin/env python

import os
from subprocess import call
import argparse


def main():
    parser = argparse.ArgumentParser(description="Apply exome mapping in multiple samples")
    parser.add_argument('-s', '--sconsdir', action='store', type=str, help="Path to directory containing SConstruct and settings.py files", default=".")
    args = parser.parse_args()
    for f in os.listdir(os.getcwd()):
        if os.path.isdir(f):
            os.chdir(f)
            project = f
            sample = f

            sconstruct = os.path.join(args.sconsdir, "SConstruct")
            settings = os.path.join(args.sconsdir, "settings.py")

            command = "scons -f {} projectName={} sampleName={}".format(sconstruct, project, sample)

            call(["cp", sconstruct, "."])
            call(["cp", settings, "."])
            os.system(command)
            os.chdir("..")


if __name__ == "__main__":
    main()
