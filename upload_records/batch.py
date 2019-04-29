import subprocess as sp


def execute(cmd):
    popen = sp.Popen(cmd, stdout=sp.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise sp.CalledProcessError(return_code, cmd)


if __name__ == "__main__":
    datasets = [("adm2", "bd42375f-0983-4e4f-9602-806eb2c26401", ["B", "C", "D", "E", "F", "G"])]
        #                                                           "H", "I", "J", "K", "L"
        # ,"M", "N", "O", "P", "Q", "R", "S", "T", "U","V", "W", "X", "Y", "Z"])]

    for dataset in datasets:
        for letter in dataset[2]:
            cmd = "concatenate_record {} gfw-files --prefix 2018_update/results/{}/{}/".format(dataset[1], letter, dataset[0]).split()
            for path in execute(cmd):
                print(path, end="")
