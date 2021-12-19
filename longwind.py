import glob
import logging
import numpy as np
import os
import shutil
import sox
import sys
import tempfile
import tqdm


def concatenate(dir_path, n_files_per_chunk=50):
    logging.getLogger("sox").setLevel(logging.ERROR)
    dir_path = os.path.abspath(dir_path)
    glob_regexp = os.path.join(dir_path, "*.wav")
    file_list = sorted([
        path for path in glob.glob(glob_regexp)
        if os.path.exists(path)
        and os.access(path, os.R_OK)
        and os.path.splitext(path)[1][1:] in sox.core.VALID_FORMATS
    ])
    n_files = len(file_list)
    n_stages = int(np.ceil(np.log(n_files)/np.log(n_files_per_chunk)))
    in_file_list = file_list
    out_file_list = []
    file_combiner = sox.Combiner()

    tmpdirname = os.path.join(os.path.split(dir_path)[0], "longwind_temp")
    if os.path.exists(tmpdirname):
        shutil.rmtree(tmpdirname)
    os.makedirs(tmpdirname)
    print("Longwind temporary directory: {}".format(tmpdirname))

    for stage_id in range(n_stages):
        print("{}   LONG-WINDING: STAGE {:d} OF {:d}   {}".format(
            "*" * 15, 1+stage_id, n_stages, "*" * 15))
        n_chunks = 1 + len(in_file_list)//n_files_per_chunk
        for chunk_id in tqdm.tqdm(range(n_chunks)):
            chunk_start = n_files_per_chunk * chunk_id
            chunk_stop = n_files_per_chunk * (1+chunk_id)
            chunk = in_file_list[chunk_start:chunk_stop]
            chunk_name = "longwind_stage-{:d}_segment-{:09d}.wav".format(
                1+stage_id, chunk_id)
            chunk_path = os.path.join(tmpdirname, chunk_name)
            out_file_list.append(chunk_path)
            file_combiner.build(chunk, chunk_path, "concatenate")
        in_file_list = out_file_list
        out_file_list = []
    assert len(in_file_list)==1
    print("DONE.")
    print("Output WAV file is available at: {}".format(in_file_list[0]))


if __name__ == "__main__":
    dir_path = sys.argv[1]
    concatenate(dir_path)
