import tools as tls

import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta

import pandas

def plot_probability_fractions(nicola):
    data_path = "./data/"
    data_files = ["2018-maschile-ledro.xls"]
    #

    times = {"total" : np.zeros((0,)),
             "swim" : np.zeros((0,)),
             "t1" : np.zeros((0,)),
             "bike" : np.zeros((0,)),
             "t2" : np.zeros((0,)),
             "run" : np.zeros((0,))}
    #
    matches = {"total" : "TEMPO_UFFICIALE",
               "swim" : "trs",
               "t1" : "tr1",
               "bike" : "trb",
               "t2" : "tr2",
               "run" : "trr"}

    for df in data_files:
        print(df)
        for key, v in matches.items():
            times[key] = np.hstack((times[key],
                                    tls.read_times_xls(data_path+df,v)))

    data_files = ["2016-maschile-ledro.csv",
                  "2017-maschile-ledro.csv"]

    for df in data_files:
        print(df)
        for key, v in matches.items():
            times[key] = np.hstack((times[key],
                                    tls.read_ledro_csv_format(data_path+df)[key]))


    keys = ["swim","t1","bike","t2","run"]


    fig, ax = plt.subplots(2,5)


    f = tls.get_time_evaluation_formulas()
    d = tls.get_distances()

    p = {}

    p["swim"] = np.arange(60,180,5)
    p["t1"] = np.arange(60,300,20)
    p["bike"] = np.flip(np.arange(25,34,.5))
    p["t2"] = np.arange(60,200,10)
    p["run"] = np.arange(200,390,10)

    bins = []

    for k in keys:
        bins.append(f[k](d[k],p[k]))

    nicola_bin_id = {}

    for b, k in zip(bins,keys):
        nicola_bin_id[k] = int((np.floor(nicola[k]-b[0])/(b[1]-b[0])))

    for pic in range(5):

        n0, b0, p0 = ax[0,pic].hist(times[keys[pic]],bins[pic])
        n1, b1, p1 = ax[1,pic].hist(times[keys[pic]],bins[pic],
                       density=True,cumulative=True)
        p0[nicola_bin_id[keys[pic]]].set_fc('r')
        plt.sca(ax[0,pic])
        plt.title(keys[pic])
        plt.xticks(bins[pic], [])
        plt.grid(axis='x')

        plt.sca(ax[1,pic])
        xlabels = [str(timedelta(seconds=int(t))) for t in p[keys[pic]]]
        bins_time = [str(timedelta(seconds=int(t))) for t in bins[pic]]
        if (keys[pic]=="bike"):
            xlabels = [str(t) for t in p[keys[pic]]]

        plt.xticks(bins[pic], xlabels,rotation = "vertical")
        plt.grid(axis='x')
        p1[nicola_bin_id[keys[pic]]].set_fc('r')

        data_to_write = {}

        data_to_write["pace-"+keys[pic]] = xlabels[:-1]
        data_to_write["finishers-"+keys[pic]] = n0
        data_to_write["percentile-"+keys[pic]] = n1
        data_to_write["time-"+keys[pic]] = bins_time[:-1]

        df = pandas.DataFrame(data_to_write)
        df.to_csv("./ledroman-partial-"+keys[pic]+".cvs", sep=',',index=False)



    plt.show()


if __name__ == "__main__":


    keys = ["swim","t1","bike","t2","run"]

    paces = tls.get_expected_pace()

    distances = tls.get_distances()

    formulas = tls.get_time_evaluation_formulas()

    n_times = tls.evaluate_times(paces,distances,formulas)

    print(str(timedelta(seconds=int(n_times["total"]))))

    plot_probability_fractions(n_times)
