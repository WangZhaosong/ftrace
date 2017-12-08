import re
from ftrace.common import ParserError
from .register import register_parser
from .binder import parse_binder_cmd
from collections import namedtuple

TRACEPOINT = 'binder_return'

__all__ = [TRACEPOINT]

#binder_return: cmd=0x80287203 BR_REPLY

BinderReturnBase = namedtuple(TRACEPOINT,
    [
    'cmd',
    'rv',
    ]
)

class BinderReturn(BinderReturnBase):
    __slots__ = ()
    def __new__(cls, cmd, rv):

            cmd = parse_binder_cmd (int (cmd, base=16))

            return super(cls, BinderReturn).__new__(
                cls,
                cmd=cmd,
                rv=rv
            )

binder_ioctl_pattern = re.compile(
    r"""
    cmd=(0x[0-9a-f]+)\s+
    BR_([A-Z]+)
    """,
    re.X|re.M
)

@register_parser
def binder_return(payload):
    """Parser for `binder_return`"""
    try:
        match = re.match(binder_ioctl_pattern, payload)
        if match:
            match_group_dict = match.groupdict()
            return BinderReturn(match.group(1), match.group(2))
    except Exception, e:
        raise ParserError(e.message)
