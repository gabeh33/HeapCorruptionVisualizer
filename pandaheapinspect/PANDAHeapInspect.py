import argparse
from heapinspect.core import *
from pandare import Panda
from heapinspect.auxiliary.utils import terminal_size
from colorama import Fore, Back, Style
from heapinspect.layout import DiagramHeap

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='HeapInspect.py',
        description='''Use PANDA to inspect the heap usage of a given binary.
                       Author:gabeh33 (forked from lacraig2)
                       Github:https://github.com/gabeh33/HeapCorruptionVisualizer''')
    parser.add_argument('--raw', action='store_true', help='Show more detailed chunk info')
    parser.add_argument('--rela', action='store_true', help='Show relative detailed chunk info')
    parser.add_argument('--pretty', action='store_true', help='Output heap info with colors')
    parser.add_argument('--script', help='Name of executable in /scripts to execute on the guest machine')
    parser.add_argument('--diagram', action='store_true', help='Output the heap info in '
                                                               'the form of a diagram, default is True')
    parser.add_argument('--all', action='store_true', help='Output heap info on all processes, not just the target')
    args = parser.parse_args()

    panda = Panda(generic="x86_64")
    skip_first = True  # Skip the first malloc hook, it's outputting nonsense and throws errors



    def call_hook():
        @panda.hook_symbol("libc-", "malloc")
        def hook(cpu, tb, h):
            process = panda.get_process_name(cpu)
            try:
                global pid, args, skip_first

                if args.script:
                    target = args.script
                else:
                    target = "simple"

                output_all = args.all
                if process != target and not output_all:
                    h.enabled = False
                    print(f"Caught libc:malloc in {process}, not the target process so exiting...")
                    # return
                elif skip_first and not output_all:
                    print(f"Skipping first hook in {process}...")
                elif target == process:
                    width, height = terminal_size()
                    print(Fore.GREEN + "\n" + "__--" * round(width/12) +
                          f" Caught libc:malloc in {process}, target process " + "__--" * round(width/12) + Style.RESET_ALL)
                else:
                    print(f"\nCaught libc:malloc in {process}, outputting information on all processes" )

                arena_info = {"main_arena_offset": 4111432, "tcache_enable": True}
                hi = HeapInspector(0, panda=panda, arena_info=arena_info)
                if args.diagram:
                    if output_all:
                        hs = HeapShower(hi)
                        dh = DiagramHeap(hs)
                        dh.output()
                    elif process == target:
                        if skip_first:
                            skip_first = False
                            return
                        hs = HeapShower(hi)
                        dh = DiagramHeap(hs)
                        dh.output()
                elif args.raw:
                    if output_all:
                        hs = HeapShower(hi)
                        print(hs.fastbins)
                        print(hs.unsortedbins)
                        print(hs.smallbins)
                        print(hs.largebins)
                        print(hs.tcache_chunks)
                    elif target == process:
                        if skip_first:
                            skip_first = False
                            return
                        hs = HeapShower(hi)
                        print(hs.fastbins)
                        print(hs.unsortedbins)
                        print(hs.smallbins)
                        print(hs.largebins)
                        print(hs.tcache_chunks)
                elif args.pretty:
                    if output_all:
                        pp = PrettyPrinter(hi)
                        print(pp.all)
                    elif target == process:
                        if skip_first:
                            skip_first = False
                            return
                        pp = PrettyPrinter(hi)
                        print(pp.all)
                elif args.rela:
                    if output_all:
                        hs = HeapShower(hi)
                        hs.relative = True
                        print(hs.fastbins)
                        print(hs.unsortedbins)
                        print(hs.smallbins)
                        print(hs.largebins)
                        print(hs.tcache_chunks)
                    elif process == target:
                        if skip_first:
                            skip_first = False
                            return
                        hs = HeapShower(hi)
                        hs.relative = True
                        print(hs.fastbins)
                        print(hs.unsortedbins)
                        print(hs.smallbins)
                        print(hs.largebins)
                        print(hs.tcache_chunks)
                else:
                    if output_all:
                        hs = HeapShower(hi)
                        dh = DiagramHeap(hs)
                        dh.output()
                    elif process == target:
                        if skip_first:
                            skip_first = False
                            return
                        hs = HeapShower(hi)
                        dh = DiagramHeap(hs)
                        dh.output()
            except Exception as e:
                print(f"Error while trying to output heap info for {panda.get_process_name(cpu)}, exiting...")
                raise e
            # h.enabled = False


    @panda.queue_blocking
    def drive_guest():
        panda.revert_sync("root")
        if args.script:
            print("Running analysis on: " + args.script)
        else:
            print("Running analysis on: Simple")
        print("ATTEMPTING TO COPY TO GUEST")
        panda.copy_to_guest("/host/scripts/", absolute_paths=True, timeout=50)
        print("CALLING HOOK")
        call_hook()
        if args.script:
            target = args.script
        else:
            target = "simple"
        print(f"ATTEMPTING TO RUN PROGRAM: {target}")
        print(panda.run_serial_cmd(f"/host/scripts/{target}", timeout=1000))
        print(Style.RESET_ALL)
        panda.end_analysis()

    panda.run()
