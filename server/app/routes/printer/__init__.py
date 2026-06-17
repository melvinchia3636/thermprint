from . import print
from . import preview
from . import qrcode
from . import calendar

router = print.router  # not used directly; routes registered via each module
