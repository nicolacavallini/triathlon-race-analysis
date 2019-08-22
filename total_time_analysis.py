import tools as tls

import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta

import pandas


if __name__ == "__main__":

    data_path = "./data/"
    data_files = ["2014-maschile-ledro.xls",
                  "2015-maschile-ledro.xls",
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

    print(times.shape)

    fig, ax = plt.subplots(2,1)

    bins = np.arange(3480,7500,60)

    values = ax[0].hist(times,bins)

    # print(values[0].shape)
    # print(bins[:-1].shape)

    time_str = [str(timedelta(seconds=int(t))) for t in bins]

    # np.savetxt("probability-density.csv", values[0], delimiter=",")
    # np.savetxt("probability-bins.csv", values[0], delimiter=",")

    plt.sca(ax[0])
    plt.xticks(bins, [])
    plt.grid(axis='x')
    plt.title('num of samples ='+str(times.shape[0]))


    res = ax[1].hist(times,bins, density=True,
                           cumulative=True)
    plt.sca(ax[1])

    xlabels = [str(timedelta(seconds=int(t))) for t in bins]

    df = pandas.DataFrame(data={"finishers": values[0], "percentile": res[0], "total-time": time_str[:-1]})
    df.to_csv("./ledroman-total.csv", sep=',',index=False)

    plt.xticks(bins, xlabels, rotation=60)

    expected_percentile = [.7,.8]
    ylabels = [str(p) for p in expected_percentile]
    plt.yticks(expected_percentile, ylabels)

    plt.grid()

    plt.show()
