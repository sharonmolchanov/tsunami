"""Run the 'slipgen' fortran application.

To compile the slipgen application do the following:

> cd /Users/sharon/code/SlipGen
> /Users/sharon/anaconda3/bin/gfortran -o slipgen slipgen.f90
> cp slipgen <the location of this module>
"""
import numpy as np
import subprocess as sbp


def run_slipgen(length, width, ln, wn, k, mean_slip, show_output=False):
    """Run the slipgen code.
    
    Args:
        length, width (int, int): length and width of the fault
        ln, wn (int, int): discretization in strike and dip direction
        k (float): K-value
        mean_slip (np.array): Description of the deterministic part (mean) of the slip.
        show_output (bool, optional): Show the output of the code (default to False).
        
    Retrun:
        X, Y, Z (np.array) X, Y and Z are 2D arrays of shape ln, wn ...
    """
    with open("slipgen.in", "w") as f:
        f.write("{}\t{}\n".format(length, width))
        f.write("{}\t{}\n".format(ln, wn))
        f.write("{}\n".format(k))
        f.write("{}\t{}\n".format(*mean_slip.shape))
        for ms in mean_slip:
            f.write("\t".join(["{:.3}".format(i) for i in ms])+"\n")

    try:
        out = sbp.run(
            ["slipgen"],
            env={"DYLD_FALLBACK_LIBRARY_PATH":"/Users/sharon/anaconda3/lib/"},
            check=True, stdout=sbp.PIPE, stderr=sbp.PIPE
        )
    except Exception as status:
        raise Exception(status.stderr.decode())
    
    if show_output:
        print(out.stdout.decode())
        
    result = np.loadtxt("slipgen.txt")
    X = result[:, 0].reshape(ln, wn)
    Y = result[:, 1].reshape(ln, wn)
    Z = result[:, 2].reshape(ln, wn)
    
    return X, Y, Z