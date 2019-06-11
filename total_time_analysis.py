import tools as tls

import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta

if __name__ == "__main__":

    data_path = "./data/"
    data_files = ["2014-maschile-ledro.xls",
                  "2014-maschile-ledro.xls",
                  "2018-maschile-ledro.xls"]
    #
    times = np.zeros((0,))
    #
    for df in data_files:
        times = np.hstack((times,
        tls.read_times_xls(data_path+df,"TEMPO_UFFICIALE")))

    data_files = ["2016-maschile-ledro.csv",
                  "2017-maschile-ledro.csv"]

    for df in data_files:
        times = np.hstack((times,tls.read_ledro_csv_format(data_path+df)["total"]))

    fig, ax = plt.subplots(2,1)

    bins = np.arange(3480,7500,60)

    values = ax[0].hist(times,bins)

    plt.sca(ax[0])
    plt.xticks(bins, [])
    plt.grid(axis='x')
    plt.title('num of samples ='+str(times.shape[0]))


    res = ax[1].hist(times,bins, density=True,
                           cumulative=True)
    plt.sca(ax[1])

    xlabels = [str(timedelta(seconds=t)) for t in bins]


    plt.xticks(bins, xlabels, rotation=60)

    expected_percentile = [.7,.8]
    ylabels = [str(p) for p in expected_percentile]
    plt.yticks(expected_percentile, ylabels)

    plt.grid()

    plt.show()
