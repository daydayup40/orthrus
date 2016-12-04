'''
Gdb-Orthrus
'''

try:
    import gdb
except ImportError as e:
    raise ImportError("This script must be run in GDB: ", str(e))

import os
import json
import re

# ARCH = ""
# COMPILER = ""
# PC = ""
# BP = ""
# SP = ""
#
# class SupportBreakpoint (gdb.Breakpoint):
#     def __init__(self, location, observe_frame, arguments):
#         gdb.Breakpoint.__init__(self, location, gdb.BP_BREAKPOINT)
#         self._observe_frame = observe_frame
#         self._arguments = arguments
#
#     def stop (self):
#         for key, value in self._arguments:
#             val = gdb.parse_and_eval(key)
#             if val != value:
#                 return False
#         return True
#
# class CanaryBreakpoint(gdb.Breakpoint):
#     def __init__(self, canary_addr, observe_frame):
#         gdb.Breakpoint.__init__(self, "*(long*)" + hex(canary_addr), gdb.BP_WATCHPOINT, gdb.WP_WRITE, True)
#         self._observe_frame = observe_frame
#
#     def stop(self):
#         frame = gdb.newest_frame()
#         while True:
#             if not frame:
#                 break
#             if frame.name() and self._observe_frame in frame.name():
#                 if not self._validAccess(frame.pc()):
#                     return True
#             frame = frame.older()
#         return False
#
#     def _validAccess(self, pc):
#         disasm = ""
#         if "x86_64" in ARCH and "gcc" in COMPILER:
#             disasm = gdb.execute("x/i " + hex(pc) + "-13", False, True)
#         elif "i386" in ARCH and "gcc" in COMPILER:
#             disasm = gdb.execute("x/i " + hex(pc) + "-9", False, True)
#         elif "x86_64" in ARCH and "clang" in COMPILER:
#             disasm = gdb.execute("x/i " + hex(pc) + "-14", False, True)
#         elif "i386" in ARCH and "clang" in COMPILER:
#             disasm = gdb.execute("x/i " + hex(pc) + "-10", False, True)
#
#         if ("%gs:" in disasm) or ("%fs:" in disasm):
#             return True
#         return False
    
# class GdbOrthrus(gdb.Command):
#     _cmdstr = "orthrus"
#
#     def __init__(self, outjson):
#         gdb.Command.__init__(self, self._cmdstr, gdb.COMMAND_OBSCURE)
#         self.outfile = outjson
#         self.gdb_dict = {}
        
    # def _platformInfo(self):
    #     arch = ""
    #     pc = ""
    #     bp = ""
    #     sp = ""
    #
    #     data = gdb.execute("show architecture", False, True)
    #     if "x86-64" in data:
    #         arch = "x86_64"
    #         pc = "$rip"
    #         bp = "$rbp"
    #         sp = "$rsp"
    #     else:
    #         arch = "i386"
    #         pc = "$eip"
    #         bp = "$ebp"
    #         sp = "$esp"
    #
    #     #TODO: Check which compiler was used
    #     compiler = "clang"
    #
    #     return (arch, compiler, pc, bp, sp)
    #
    # def _isStackCheckFail(self):
    #     frame = gdb.newest_frame()
    #     while True:
    #         if not frame:
    #             break
    #         if frame.name() and "__stack_chk_fail" in frame.name():
    #             return True
    #         frame = frame.older()
    #
    #     return False
    #
    # def _getTopUserCodeFrame(self):
    #     frame = gdb.newest_frame()
    #     while True:
    #         if not frame.is_valid():
    #             break
    #         if frame.find_sal().symtab:
    #             filename =frame.find_sal().symtab.filename
    #             for dirpath, dirnames, filenames in os.walk('./'):
    #                 for fn in filenames:
    #                     if os.path.basename(filename) == fn:
    #                         return frame
    #         frame = frame.older()
    #
    #     return None
    #
    # def _getProgArgs(self):
    #     cmd_args = gdb.execute("show args", False, True)
    #     cmd_args = cmd_args[cmd_args.find("\""):]
    #     cmd_args = cmd_args[1:-3]
    #
    #     return cmd_args
    #
    # def _getCanaryAddr(self, frame):
    #     global COMPILER
    #     re_clang = re.compile("mov\s+(%gs|%fs):.+?\n.+?cmp\s+(?P<offset>-?0x[0-9a-zA-Z]+)\(")
    #     re_gcc = re.compile("mov\s+(?P<offset>-?0x[0-9a-zA-Z]+)\(.+?\n.+?(xor)\s+(%gs|%fs):")
    #     disasm = ""
    #     pc = frame.pc()
    #     #print (hex(pc))
    #     #print (ARCH)
    #     bp = gdb.parse_and_eval(BP)
    #     #print (hex(int(bp)))
    #
    #     disasm = gdb.execute("disass", False, True)
    #
    #     match = re_clang.search(disasm)
    #     if not match:
    #         COMPILER = "gcc"
    #         match = re_gcc.search(disasm)
    #
    #     if match:
    #         offset = match.group("offset")
    #         #print (offset)
    #         if "-" in offset:
    #             return ((-1 * int(offset[1:], 16)) + int(bp))
    #         else:
    #             return (int(offset[1:], 16) + int(bp))
    #     else:
    #         print ("No match")
        
            
#         if "x86_64" in ARCH:
#             disasm = gdb.execute("x/i " + hex(pc) + "-20", False, True)
#         else:
#             disasm = gdb.execute("x/i " + hex(pc) + "-17", False, True)
            
        
#         tmp = disasm[disasm.find("mov"):]
#         tmp = tmp[tmp.find(" "):tmp.find("(")].lstrip(" ")
#         if "-" in tmp:
#             return ((-1 * int(tmp[1:], 16)) + int(bp))
#         else:
#             return (int(tmp[1:], 16) + int(bp))


        # return None
    
    # def _getExploitableInfo(self):
    #     info =  "GDB exploitable info:\n" + gdb.execute("exploitable", False, True)
    #     gdb.execute("set disassembly-flavor att", False, True)
    #
    #     return info
    #
    # def _updateExploitableHash(self, exploitable_info):
    #     exploitable_info = exploitable_info.splitlines()
    #     tmp = gdb.execute("exploitable", False, True).splitlines()
    #     gdb.execute("set disassembly-flavor att", False, True)
    #
    #     exploitable_info[3] = tmp[2]
    #
    #     return "".join(exploitable_info)
    #
    # def _describeLocals(self, frame, sp, fa_offset):
    #     local_vars = gdb.execute("info locals", False, True).splitlines()
    #     print ("This frame has " + str(len(local_vars)) + " object(s):")
    #     for loc_var in local_vars:
    #         loc_var = loc_var[:loc_var.find(" = ")]
    #         addr = gdb.execute("p &" + loc_var, False, True)
    #         addr = int(addr[addr.find("0x"):-1], 16)
    #         size = gdb.execute("p sizeof(" + loc_var + ")", False, True)
    #         size = int(size[size.find("= ") + 2:-1])
    #
    #         overflow_str = ""
    #         if frame == gdb.newest_frame():
    #             if (addr - sp + size) == fa_offset:
    #                 overflow_str = " <== Memory access overflows this variable"
    #             print ("["+ str(addr - sp) + "," + str(addr - sp + size) + "] '" + loc_var + "'" + overflow_str)
    #             overflow_str = ""
    #         else:
    #             if (addr - sp + size) == fa_offset:
    #                 overflow_str = " <== Memory access overflows this variable"
    #             print ("["+ str(addr - sp) + "," + str(addr - sp + size) + "] '" + loc_var + "'" + overflow_str)
    #             overflow_str = ""
    #
    # def _printStackLocation(self, fa_addr):
    #     frame_no = 0
    #     frame = gdb.newest_frame()
    #     frame.select()
    #     while True:
    #         if not frame or not frame.is_valid():
    #             break
    #         bp = int(gdb.parse_and_eval(BP))
    #         sp = int(gdb.parse_and_eval(SP))
    #         pc = frame.pc()
    #         if int(fa_addr) < int(bp):
    #             print ("Address " + hex(fa_addr) + " is located in stack at offset " + str(fa_addr - (sp)) + " in frame")
    #             print (gdb.execute("bt " + str(frame_no + 1), False, True).splitlines()[-1])
    #             self._describeLocals(frame, sp, fa_addr - sp)
    #             return
    #         frame = frame.older()
    #         frame.select()
    #         frame_no += 1
    #
    # def _printHeapLocation(self, fa_addr):
    #     print ("no information")
    #
    # def _printFault(self, fa_addr, isStack):
    #     pid = "0"
    #     re_pid = re.compile("\s+process\s(?P<pid>[0-9]+?)\s")
    #     inferior = gdb.execute("info inferior", False, True)
    #     match = re_pid.search(inferior)
    #     if match:
    #         pid = match.group("pid")
    #
    #     pc = int(gdb.parse_and_eval(PC))
    #     bp = int(gdb.parse_and_eval(BP))
    #     sp = int(gdb.parse_and_eval(SP))
    #
    #     print ("==" + pid + "==ERROR: GenericGdb:" )
    #     print ("Faulting mem location is " + hex(fa_addr) + ", pc is " + hex(pc) + ", sp is " + hex(sp) + ", bp is " + hex(bp))
    #     print ("AccessViolation: WRITE of size 4 at " + hex(fa_addr))
    #
    #     if isStack:
    #         self._printStackLocation(fa_addr)
    #     else:
    #         self._printHeapLocation(fa_addr)
    #
    #     bt = "\nProgram back trace:\n"
    #     bt += gdb.execute("bt", False, True)
    #     print (bt)
    #
    # def _incompleteBackTrace(self):
    #     frame = gdb.newest_frame()
    #     while True:
    #         if not frame:
    #             break
    #         if frame.name() is None:
    #             return True
    #         frame = frame.older()
    #
    #     return False
    #
    # def invoke(self, argstr, from_tty):
    #     global ARCH, COMPILER, PC, BP, SP
    #     ARCH, COMPILER, PC, BP, SP = self._platformInfo()
    #     #print ("Arch: " + ARCH + " Compiler:" + COMPILER + " PC: " + PC + " BP: " + BP + " SP: " + SP)
    #
    #     exploitable_info = self._getExploitableInfo()
    #     #print (exploitable_info)
    #
    #     cmd_args = self._getProgArgs()
    #     #print (cmd_args)
    #
    #     frame = self._getTopUserCodeFrame()
    #     if not frame:
    #         print("Error: Couldn't find top user code frame!")
    #         return
    #     frame.select()
    #
    #     isStack = False
    #     fa_addr = 0
    #
    #     if self._isStackCheckFail():
    #         isStack = True
    #
    #         observe_frame = frame.name()
    #         #print ("Frame: " + observe_frame)
    #         fa_addr = self._getCanaryAddr(frame)
    #
    #         #print ("Canary: " + hex(fa_addr))
    #         CanaryBreakpoint(fa_addr, observe_frame)
    #
    #         gdb.execute("run " + cmd_args, False, True)
    #
    #         if self._incompleteBackTrace():
    #             #print ("Stack trace incomplete")
    #             frame2 = self._getTopUserCodeFrame()
    #             #print ("New Top frame: " + frame2.name())
    #             frame2.select()
    #             args = gdb.execute("info args", False, True)
    #             arguments = {}
    #             for arg in args.splitlines():
    #                 tmp = arg.split(" = ")
    #                 arguments[tmp[0]] = tmp[1]
    #
    #             location = frame2.find_sal().symtab.filename + ":" + str(frame2.find_sal().line)
    #             #print (location)
    #             SupportBreakpoint(location, observe_frame, arguments)
    #             gdb.execute("run " + cmd_args, False, True)
    #
    #         gdb.execute("set " + PC + "=" + PC + "-1")
    #         self._updateExploitableHash(exploitable_info)
    #
    #     self._printFault(fa_addr, isStack)
    #     main_info = gdb.execute("info line main", False, True)
    #     print ("Main function: " + main_info)
    #     print (exploitable_info)
    #
    #     gdb.newest_frame().select()
    # def invoke(self):

class GdbOrthrus(gdb.Function):
    """JSONify core dump via GDB python plugin. Takes jsonfile as arg"""

    _re_gdb_bt = re.compile(r"""
                        ^\#(?P<frame_no>[0-9]+)\s*
                        ((?P<address>0x[A-Fa-f0-9]+)\s*)?
                        (in\s(?P<func>[A-Za-z0-9_:\-\?<>,]+)\s*
                        (?P<paramlist>\([A-Za-z0-9_\=\-:\&\,\s\*]*\))\s*)?
                        (at\s*(?P<file>[A-Za-z0-9_\.\-]*):(?P<line>[0-9]+)\s*)?
                        ((\s)?\((?P<module>.+?)\+(?P<offset>0x[A-Fa-f0-9]+)\))?
                        """, re.MULTILINE | re.VERBOSE)
    _re_gdb_exploitable = re.compile(r".*Description: (?P<desc>[\w|\s]+).*"
                                     r"Short description: (?P<shortdesc>[\w|\s\(\)\/]+).*"
                                     r"Hash: (?P<hash>[0-9A-Za-z\.]+).*"
                                     r"Exploitability Classification: (?P<class>[A-Z_]+).*"
                                     r"Explanation: (?P<explain>[\w|\s|\.|\/,]+).*"
                                     r"Other tags: (?P<other>[\w|\s,\(\)\/]+).*",
                                     re.DOTALL)

    def __init__(self):
        super(GdbOrthrus, self).__init__("jsonify")
        self.gdb_dict = {}

    def invoke(self, jsonfile):
        self.jsonfile = jsonfile.string()

        ## Get and parse backtrace
        bt_string = gdb.execute("bt", False, True)
        bt_dict = {}
        for match in self._re_gdb_bt.finditer(bt_string):
            frame_no, address, func, paramlist, filename, line, module, offset = \
                match.group("frame_no", "address", "func", "paramlist", "file", "line", "module", "offset")
            frame_str = "frame{}".format(frame_no)

            bt_dict[frame_str] = {"frame_no": frame_no, "address": address, "function": func, "func_params": paramlist }

            if filename and line:
                bt_dict[frame_str]['file'] = filename
                bt_dict[frame_str]['line'] = line
            if module and offset:
                bt_dict[frame_str]['module'] = module
                bt_dict[frame_str]['offset'] = offset
        self.gdb_dict['backtrace'] = bt_dict
        self.gdb_dict['debug'] = bt_string


        # Parse fault address and exploitable output
        self.gdb_dict['fault_addr'] = gdb.execute('printf "%#lx", $_siginfo._sifields._sigfault.si_addr', False, True)
        exp_string = gdb.execute('exploitable', False, True)
        match = self._re_gdb_exploitable.match(exp_string)
        if match is not None:
            exp_dict = {}
            exp_dict['description'] = match.group("desc").rstrip()
            exp_dict['short_desc'] = match.group("shortdesc").rstrip()
            exp_dict['hash'] = match.group("hash").rstrip()
            exp_dict['classification'] = match.group("class").rstrip()
            exp_dict['explanation'] = match.group("explain").rstrip()
            exp_dict['tags'] = match.group("other").rstrip()
            self.gdb_dict['exploitable_info'] = exp_dict

        with open(self.jsonfile, 'w') as fp:
            json.dump(self.gdb_dict, fp, indent=4)
        return True

GdbOrthrus()