from settings import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
import os

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5),save_as=None):
    if not(isinstance(estimator, list)):
        estimator = [].append(estimator)

    fig = plt.figure(figsize=(8,len(estimator)*4),dpi=100)
    fig.canvas.set_window_title("Learning curve")

    for est in estimator:
        n = len(fig.axes)
        for i in range(n):
            fig.axes[i].change_geometry(n + 1, 1, i + 1)
        fig.add_subplot(n + 1, 1, n + 1)
        fig.subplots_adjust(hspace = 1)

        plt.title(est.name)
        if ylim is not None:
            plt.ylim(*ylim)
        plt.xlabel("Training examples")
        plt.ylabel("Score")
        train_sizes, train_scores, test_scores = learning_curve(
            est.clf, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        plt.grid()

        plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
        plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1, color="g")
        plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
                label="Training score")
        plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")

        plt.legend(loc="best")
    path = os.path.join(FIGURES_DIR, "Learning curve" + save_as)
    plt.savefig(path)

def plot_predictions_per_label(data, labels,save_as):
    algs = data.pop(0)[2:]

    fig = plt.figure()
    fig.canvas.set_window_title("Predictions per Algorithm/Label")
    ax = fig.add_subplot(111)
    N = len(labels)

    results_final = np.zeros((len(labels), len(algs)))
    for entry in data:
        entry = entry[2:]
        for i in range(0, len(entry)):
            results_final[labels.index(entry[i])][i] += 1
    ## necessary variables
    ind = np.arange(N)                # the x locations for the groups
    width = 0.10                      # the width of the bars

    ## the bars
    i = 0
    for alg in algs:
        rects1 = ax.bar(ind + width*i,
                        results_final[:,algs.index(alg)],
                        width,
                        label=alg)
        i+=1

    # axes and labels
    ax.set_xlim(-width,len(ind)+width)
    #ax.set_ylim(0,10)
    ax.set_ylabel('#Users')
    ax.set_title('Classification p/Algorithm')
    xTickMarks = [label for label in labels]
    ax.set_xticks(ind+width)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=10)

    ## add a legend
    ax.legend()

    #plt.show()
    path = os.path.join(FIGURES_DIR, "Prediciton-Alg_label" + save_as)
    plt.savefig(path)


def plot_predictions_per_alg(data, labels,save_as):
    algs = data.pop(0)[2:]

    fig = plt.figure()
    fig.canvas.set_window_title("Predictions per Label/Algorithms")
    ax = fig.add_subplot(111)
    N = len(algs)

    results_final = np.zeros((len(labels), len(algs)))
    for entry in data:
        entry = entry[2:]
        for i in range(0, len(entry)):
            results_final[labels.index(entry[i])][i] += 1
    ## necessary variables
    ind = np.arange(N)  # the x locations for the groups
    width = 0.10  # the width of the bars

    ## the bars
    i = 0
    for label in labels:
        rects1 = ax.bar(ind + width * i,
                        results_final[labels.index(label),:],
                        width,
                        label=label)
        i += 1

    # axes and labels
    ax.set_xlim(-width, len(ind) + width)
    # ax.set_ylim(0,10)
    ax.set_ylabel('#Users')
    ax.set_title('Classification p/Algorithm')
    xTickMarks = [alg for alg in algs]
    ax.set_xticks(ind + width)
    xtickNames = ax.set_xticklabels(xTickMarks)
    plt.setp(xtickNames, rotation=45, fontsize=10)

    ## add a legend
    ax.legend()

    #plt.show()
    path = os.path.join(FIGURES_DIR, "Prediciton-Label_Alg" + save_as)
    plt.savefig(path)


if __name__ == "__main__":
    pass