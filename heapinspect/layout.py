from heapinspect.auxiliary.ezcolor import color
from heapinspect.auxiliary.utils import terminal_size
from colorama import Fore, Back, Style

# from termcolor import colored

class HeapShower(object):
    '''Print heap and arena information in detailed mode.

    Args:
        hi (HeapInspector or HeapRecord): HeapInspector or HeapRecord.
        relative (bool): Show relative addresses.
        w_limit_size (int): Data size limit.
    '''

    def __init__(self, hi, relative=False, w_limit_size=8):
        self.hi = hi
        self.record = hi.record
        self.relative = relative
        self.w_limit_size = w_limit_size

    def update(self):
        '''Update the HeapRecord.
        '''
        self.record = self.hi.record

    @property
    def heap_chunks(self):
        '''str: formated heapchunks str.
        '''
        return self.chunks(self.record.heap_chunks, 'heapchunks')

    @property
    def fastbins(self):
        '''str: formated fastbins str.
        '''
        return self.indexed_chunks(self.record.fastbins, 'fastbins')

    @property
    def unsortedbins(self):
        '''str: formated unsortedbins str.
        '''
        return self.chunks(self.record.unsortedbins, 'unsortedbins')

    @property
    def smallbins(self):
        '''str: formated smallbins str.
        '''
        return self.indexed_chunks(self.record.smallbins, 'smallbins', -1)

    @property
    def largebins(self):
        '''str: formated largebins str.
        '''
        return self.indexed_chunks(self.record.largebins, 'largebins', -0x3f)

    @property
    def tcache_chunks(self):
        '''str: formated tcache chunks str.
        '''
        return self.indexed_chunks(self.record.tcache_chunks, 'tcache')

    def chunks(self, chunks, typ=''):
        lines = []
        if not self.relative:
            lines.append(self.banner(typ))
            for chunk in chunks:
                lines.append(self.chunk(chunk))
        else:
            lines.append(self.banner('relative ' + typ))
            for chunk in chunks:
                lines.append(self.rela_chunk(chunk))
        return '\n'.join(lines)

    def indexed_chunks(self, chunk_dict, typ='', align=0):
        lines = []
        if not self.relative:
            lines.append(self.banner(typ))
            for index in sorted(chunk_dict.keys()):
                chunks = chunk_dict[index]
                lines.append(self.banner_index(typ, index + align))
                for chunk in chunks:
                    if typ == 'largebins':
                        lines.append(self.large_chunk(chunk))
                    else:
                        lines.append(self.chunk(chunk))
        else:
            lines.append(self.banner('relative ' + typ))
            for index in sorted(chunk_dict.keys()):
                lines.append(self.banner_index('relative ' + typ, index + align))
                chunks = chunk_dict[index]
                for chunk in chunks:
                    if typ == 'largebins':
                        lines.append(self.rela_large_chunk(chunk))
                    else:
                        lines.append(self.rela_chunk(chunk))
        return '\n'.join(lines)

    def banner(self, banner):
        w, h = terminal_size()
        return '{:=^{width}}'.format('  {}  '.format(banner), width=w)

    def banner_index(self, banner, index):
        return '{:}[{:}]:'.format(banner, index)

    def chunk(self, chunk):
        return "chunk({:#x}): prev_size={:<8} size={:<#8x} fd={:<#15x} bk={:<#15x}".format(
            chunk._addr, self.w_limit(chunk.prev_size), chunk.size, chunk.fd, chunk.bk)

    def large_chunk(self, chunk):
        return "chunk({:#x}): prev_size={:<8} size={:<#8x} fd={:<#15x} bk={:<#15x} fd_nextsize={:<#15x} bk_nextsize={:<#15x}".format(
            chunk._addr,
            self.w_limit(chunk.prev_size),
            chunk.size,
            chunk.fd,
            chunk.bk,
            chunk.fd_nextsize,
            chunk.bk_nextsize)

    def rela_chunk(self, chunk):
        return "chunk({:<13}): prev_size={:<8} size={:<#8x} fd={:<13} bk={:<13}".format(
            self.rela_str(chunk._addr),
            self.w_limit(chunk.prev_size),
            chunk.size,
            self.rela_str(chunk.fd),
            self.rela_str(chunk.bk))

    def rela_large_chunk(self, chunk):
        return "chunk({:<13}): prev_size={:<8} size={:<#8x} fd={:<13} bk={:<13} fd_nextsize={:<13} bk_nextsize={:<13}".format(
            self.rela_str(chunk._addr),
            self.w_limit(chunk.prev_size),
            chunk.size,
            self.rela_str(chunk.fd),
            self.rela_str(chunk.bk),
            self.rela_str(chunk.fd_nextsize),
            self.rela_str(chunk.bk_nextsize))

    def relative_addr(self, addr):
        mapname = self.whereis(addr)
        if mapname in self.record.bases:
            return (mapname, addr - self.record.bases[mapname])
        else:
            return ('', addr)

    def rela_str(self, addr):
        result = self.relative_addr(addr)
        if result[0]:
            return result[0] + '+' + hex(result[1])
        else:
            return hex(addr)

    def w_limit(self, addr):
        result = hex(addr)
        if len(result) > self.w_limit_size:
            return result[0:6] + '..'
        return result

    def whereis(self, addr):
        for mapname in self.record.ranges:
            lst = self.record.ranges[mapname]
            for r in lst:
                if r[0] <= addr < r[1]:
                    return mapname
        return ''


class PrettyPrinter(object):
    '''Pretty Printer for HeapInspector.

    Note:
        With the shortage of not able to show enough infomation.
        Use HeapShower for detailed infomation.
    Args:
        hi (HeapInspector or HeapRecord): HeapInspector or HeapRecord.
        relative (bool): Show relative addresses.
    '''

    def __init__(self, hi, relative=False):
        self.hi = hi
        self.record = hi.record
        self.relative = relative

    def update(self):
        '''Update the HeapRecord.
        '''
        self.record = self.hi.record

    @property
    def fastbins(self):
        '''str: pretty formated fastbins str.
        '''
        lines = []
        header_fmt = color.green('({size:#x})    fastbins[{index}] ')
        for index in sorted(self.record.fastbins.keys()):
            size = 2 * self.record.size_t * (index + 2)
            chunks = self.record.fastbins[index]
            tail = ''
            for chunk in chunks:
                tail += "-> " + color.blue("{:#x} ".format(chunk._addr))
            line = header_fmt.format(size=size, index=index) + tail
            if tail != '':
                lines.append(line)
        return '\n'.join(lines)

    @property
    def unsortedbins(self):
        '''str: pretty formated unsortedbins str.
        '''
        head = color.magenta('unsortedbins: ')
        tail = ''
        for chunk in self.record.unsortedbins:
            tail += '<-> ' + color.blue("{:#x} ".format(chunk._addr))
        if tail == '':
            tail = color.blue('None')
        return head + tail

    @property
    def smallbins(self):
        '''str: pretty formated smallbins str.
        '''
        lines = []
        header_fmt = color.green('({size:#x})    smallbins[{index}] ')
        for index in sorted(self.record.smallbins.keys()):
            size = 2 * self.record.size_t * (index + 1)
            chunks = self.record.smallbins[index]
            tail = ''
            for chunk in chunks:
                tail += "<-> " + color.blue("{:#x} ".format(chunk._addr))
            line = header_fmt.format(size=size, index=index - 1) + tail
            if tail != '':
                lines.append(line)
        return '\n'.join(lines)

    @property
    def largebins(self):
        '''str: pretty formated largebins str.
        '''
        lines = []
        header_fmt = color.green('largebins[{index}] ')
        for index in sorted(self.record.largebins.keys()):
            size = 2 * self.record.size_t * (index + 1)
            chunks = self.record.largebins[index]
            tail = ''
            for chunk in chunks:
                tail += "<-> " + \
                        color.blue(
                            "{:#x}".format(chunk._addr) +
                            color.green("({:#x}) ".format(chunk.size & ~0b111))
                        )
            line = header_fmt.format(size=size, index=index - 0x3f) + tail
            if tail != '':
                lines.append(line)
        return '\n'.join(lines)

    @property
    def tcache_chunks(self):
        '''str: pretty formated tcache chunks str.
        '''
        lines = []
        header_fmt = color.yellow('({size:#x})    entries[{index}] ')
        for index in sorted(self.record.tcache_chunks.keys()):
            size = 4 * self.record.size_t + index * 0x10
            chunks = self.record.tcache_chunks[index]
            tail = ''
            for chunk in chunks:
                tail += "-> " + color.blue("{:#x} ".format(
                    chunk._addr + 2 * self.record.size_t))
            line = header_fmt.format(size=size, index=index) + tail
            if tail != '':
                lines.append(line)

        return '\n'.join(lines)

    @property
    def all(self):
        '''str: pretty formated all infomation of heap.
        '''
        lines = [self.banner('HeapInspect', 'green')]
        lines.append(self.basic)
        lines.append(self.fastbins)
        lines.append(self.smallbins)
        lines.append(self.largebins)
        lines.append(self.tcache_chunks)
        lines.append(
            color.magenta('top: ') +
            color.blue('{:#x}'.format(self.record.main_arena.top))
        )
        lines.append(
            color.magenta('last_remainder: ') +
            color.blue('{:#x}'.format(self.record.main_arena.last_remainder))
        )
        lines.append(self.unsortedbins)
        return '\n'.join(lines)

    @property
    def basic(self):
        return '''libc_version:{}
arch:{}
tcache_enable:{}
libc_base:{}
heap_base:{}'''.format(
            color.yellow(self.record.libc_version),
            color.yellow(self.record.arch),
            color.yellow(self.record.tcache_enable),
            color.blue(hex(self.record.libc_base)),
            color.blue(hex(self.record.heap_base))
        )

    def banner(self, msg, color1='white'):
        w, h = terminal_size()
        return color.__getattr__(color1)(
            '{:=^{width}}'.format('  {}  '.format(msg), width=w))


# Got this from https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal-in-python
# Yay pretty colors!
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class DiagramHeap(HeapShower):
    """
    Output the heap information provided by a HeapInspector object in a
    user-friendly way
    """

    def __int__(self, hi):
        super().__init__(hi)

    def draw_chunk(self, chunk, d_up_arrow, d_down_arrow, is_even, draw_red, large_chunk=False):
        """
        Draws a single chunk of memory, according to the diagram in the draw_single_bin method
        """
        output = ""
        down_arrow = "\u2193"
        up_arrow = "\u2191"

        if d_up_arrow:
            output += f"           {up_arrow}         \n"
        output += f"    Chunk:0x{chunk._addr:x}     \n"
        output += "+----------------------------+\n"
        output += "/ {0:<5} bytes |  A | M |  P  /\n".format(hex(chunk.size))
        output += "\\----------------------------\\\n"
        output += "/ FWD Ptr: {0:<18}/\n".format(hex(chunk.fd))
        output += "\\----------------------------\\\n"
        output += "/ BCK Ptr: {0:<18}/\n".format(hex(chunk.bk))
        output += "\\----------------------------\\\n"

        if large_chunk:
            output += "/ FWD NEXT SIZE: {0:<18}/\n".format(hex(chunk.fd_nextsize))
            output += "\\----------------------------\\\n"
            output += "/ BCK NEXT SIZE: {0:<18}/\n".format(hex(chunk.bk_nextsize))
            output += "\\----------------------------\\\n"

        prev_size = hex(chunk.prev_size)
        if len(prev_size) > 14:
            prev_size = prev_size[0:14]
        output += "/ Prev_size: {0:<16}/\n".format(prev_size)
        output += "+----------------------------+\n"

        if d_down_arrow:
            output += f"           {down_arrow}         \n"

        if draw_red:
            print(Fore.RED + output)
        elif is_even:
            print(Fore.GREEN + output)
        else:
            print(Fore.LIGHTGREEN_EX + output)
        print(Style.RESET_ALL)

    def draw_single_bin(self, bin, is_even, large_bin=False, d_up_arrow=True):
        """
        Draws fastbin[0] or smallbin[3] or whatever it is given, not all bins of a type
        Outputs the given memory bin looking something like this
                            ^
                            |
                            |
                    Address in Memory
                +--------------------------+
                /  Size  |  A  |  M  |  P  /
                \--------------------------\
                /      Forward Pointer     /
                \--------------------------\
               /     Backward Pointer     /
                \--------------------------\
                /      Previous Size       /
                +--------------------------+
                            |
                            |
                          -----
                           ---
                            -
        Will look different for the large bin
        Bin is a list of chunks
        """

        addrs_in_bin = [chunk._addr for chunk in bin]
        corrupted_double_free = not len(addrs_in_bin) == len(set(addrs_in_bin))


        for i, chunk in enumerate(bin):
            d_down_arrow = True
            if i == len(bin) - 1:
                d_down_arrow = False
            self.draw_chunk(chunk, d_up_arrow, d_down_arrow, is_even, corrupted_double_free, large_bin)

    def draw_bin_type(self, bin_dict: dict, type_bin: str, large_bin=False, d_up_arrow=True):
        """
        Draws all bins of a given type, such as fastbin or largebin
        int -> [chunks]
        """

        if bin_dict.keys():
            print(f"{bcolors.OKGREEN}" + "-=" * 15 + " " + type_bin + " " + "-=" * 15 + f"{bcolors.ENDC}")
        else:
            print(f"{bcolors.OKCYAN}" + "-=" * 15 + " " + type_bin + " " + "-=" * 15 + f"{bcolors.ENDC}")

        for i, bin in enumerate(bin_dict.keys()):
            addrs_in_bin = [chunk._addr for chunk in bin_dict[bin]]
            corrupted_double_free = not len(addrs_in_bin) == len(set(addrs_in_bin))

            if corrupted_double_free:
                print(Fore.RED + f"{type_bin}[{i}]")
                self.draw_single_bin(bin_dict[bin], True, large_bin, d_up_arrow)
            elif i % 2 == 0:
                print(Fore.GREEN + f"{type_bin}[{i}]")
                self.draw_single_bin(bin_dict[bin], True, large_bin, d_up_arrow)
            else:
                print(Fore.LIGHTGREEN_EX + f"{type_bin}[{i}]")
                self.draw_single_bin(bin_dict[bin], False, large_bin, d_up_arrow)

    def output(self):
        self.draw_bin_type(self.hi.record.fastbins, "fastbins", d_up_arrow=False)
        self.draw_bin_type(self.hi.record.unsortedbins, "unsortedbins")
        self.draw_bin_type(self.hi.record.smallbins, "smallbins")
        self.draw_bin_type(self.hi.record.largebins, "largebins", True)
        self.draw_bin_type(self.hi.record.tcache_chunks, "tcachebins", d_up_arrow=False)
