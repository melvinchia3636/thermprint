from . import print
from . import preview
from . import qrcode

router = print.router  # not used directly; routes registered via each module
