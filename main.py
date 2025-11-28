#
# ______ _____ ____________      __                      _____           _
# | ___ \  __ \| ___ \  _  \    / _|                    /  ___|         | |
# | |_/ / |  \/| |_/ / | | |___| |_ ___ _ __   ___ ___  \ `--. _   _ ___| |_ ___ _ __ ___
# | ___ \ | __ |  __/| | | / _ \  _/ _ \ '_ \ / __/ _ \  `--. \ | | / __| __/ _ \ '_ ` _ \
# | |_/ / |_\ \| |   | |/ /  __/ ||  __/ | | | (_|  __/ /\__/ / |_| \__ \ ||  __/ | | | | |
# \____/ \____/\_|   |___/ \___|_| \___|_| |_|\___\___| \____/ \__, |___/\__\___|_| |_| |_|
#                                                               __/ |
#                                                              |___/
#
#
# author:       Omer Shraibshtein
# personal-id:  205984271
# version:      very much beta (and probably last...)
# date:         25/11/2025
#
# description:  pythonic tool to detect BGP hijack attacks. can also help to investigate data attributes related
#               to BGP as-path to some destination IP address, with metrics like: delay to target, raw traceroute
#               data-plane and control-plane as-paths.

from detection.dashboard.app import run_app

if __name__ == '__main__':
    run_app()
