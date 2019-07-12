""" Some basic undocumented CLI behavior. Have fun! """

if __name__ == "__main__":
    import os
    import sys

    if sys.argv[1] == "new":
        from .new import new

        fn = "new.pptx" if len(sys.argv) < 3 else sys.argv[2]
        w = 13.333 if "-w" not in sys.argv else sys.argv[sys.argv.index("-w") + 1]
        h = 7.5 if "-h" not in sys.argv else sys.argv[sys.argv.index("-h") + 1]
        new(fn, slidesize=(w, h))

    if sys.argv[1] == "convert" or sys.argv[1] == "c":
        from .convert import dir2pptx, dir2zip, pptx2dir, zip2dir, zip2pptx, pptx2zip

        fn, ext = os.path.splitext(sys.argv[2])

        if ext == "":
            if os.path.isdir(fn):
                frm = "dir"
            elif os.path.exists(fn + ".pptx"):
                frm = "pptx"
            elif os.path.exists(fn + ".zip"):
                frm = "zip"
        else:
            frm = ext[1:]

        if "-to" not in sys.argv:
            if frm == "pptx" or frm == "zip":
                to = "dir"
            elif frm == "dir":
                to = "pptx"
        else:
            to = sys.argv[sys.argv.index("-to") + 1]
            if to == "ppt":
                to = "pptx"

        func = {
            "dirpptx": dir2pptx,
            "dirzip": dir2zip,
            "pptxdir": pptx2dir,
            "zipdir": zip2dir,
            "zippptx": zip2pptx,
            "pptxzip": pptx2zip,
        }[frm + to]

        if frm == "dir":
            func(fn)
        else:
            func(fn + "." + frm)
