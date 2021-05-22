""" Send remote commands to a sigle or multiple Quasar STB
    Utils
"""

__author__ = "Mattiolo Paolo Valentino"
__copyright__ = "2016 EDP Progetti S.r.l."
__credits__ = []
__license__ = "Proprietary"
__version__ = "1.0.0"
__maintainer__ = "Mattiolo Poalo"
__email__ = "paolo.mattiolo@edp-progetti.it"
__status__ = "Production"


import os
import platform

from traceback import format_exc, print_exc

def log(msg):
    try:
        if not isinstance(msg, str):
            string = str(msg)
        print("[Change setup]: %s "  % msg)
    except:
        print_exc()


def isUp(hostname):

    response = os.system("ping -c 1 %s >/dev/null" % hostname)

    isUpBool = False
    if response == 0:
        isUpBool = True

    return isUpBool