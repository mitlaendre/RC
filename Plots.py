import numpy as np
import matplotlib.pyplot as plt
import Differential_Equation
from joblib import Parallel, delayed
import random

def universal_Data_Plot(data,labels = None,title = "", verbosity = 3):
    if len(data.shape) > 2:
        print("Data is not in 2D array form")
        return
    if data.shape[0] > data.shape[1]:
        data = data.T       #The data should be "longer" than the dimensions. This helps with universality
    if labels == None:
        labels = {"X Axis", "Y Axis", "Z Axis"}

    if verbosity >= 1:
        color = plt.cm.rainbow(np.linspace(0, 1, data.shape[0]))
        for i, c in enumerate(color):
            plt.plot(data[i], c=c,label=labels[i],title=title)
        plt.show()

    if data.shape[0] == 1:          #1D data
        print()
    elif data.shape[0] == 2:        #2D data
        plt.figure()
        plt.plot(data[0], data[1], lw=0.5)
        plt.xlabel(labels[0])
        plt.ylabel(labels[1])
        plt.title(title)
        plt.grid(True)
        plt.show()
    elif data.shape[0] == 3:        #3D data
        ax = plt.figure().add_subplot(projection='3d')
        ax.plot(*data.T, lw=0.5)
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        ax.set_zlabel(labels[2])
        ax.set_title(title)
        plt.show()
    else:                           #Multidim data
        print()





def compare_3dData_3dPlot(ground_truth, prediction):
    ax = plt.figure().add_subplot(projection='3d')
    ax.plot(*ground_truth.T, lw=0.5, label="ground truth")
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_zlabel("Z Axis")

    ax.plot(*prediction.T, lw=0.5, label="prediction")

    plt.legend()
    plt.show()
    return

def compare_3dData_2dPlot(ground_truth, prediction):
    plt.plot(np.transpose(ground_truth)[0], "r-", label="x")
    plt.plot(np.transpose(ground_truth)[1], "g-", label="y")
    plt.plot(np.transpose(ground_truth)[2], "b-", label="z")
    plt.plot(np.transpose(prediction)[0], "r--", label="Prediction x")
    plt.plot(np.transpose(prediction)[1], "g--", label="Prediciton y")
    plt.plot(np.transpose(prediction)[2], "b--", label="Prediciton z")
    plt.show()
    return


def plot_W_out(arr,row_labels,col_labels):
    fig, ax = plt.subplots()

    # Create the heatmap
    ax.imshow(np.abs(arr), cmap='hot')

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_yticks(np.arange(len(row_labels)))

    # ... and label them with the respective list entries
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            ax.text(j, i, arr[i, j],ha="center", va="center", color="w")

    ax.set_title("W_out matrix")
    fig.tight_layout()
    plt.show()
    return

def histogram_W_out(W_out,labels,cutoff_small_weights = 0.):

    i = W_out.shape[0]+1
    while i < W_out.shape[1]:
        delete = True
        for j in range(W_out.shape[0]):
            if abs(W_out[j,i]) > cutoff_small_weights:
                delete = False
        if delete:
            W_out = np.delete(W_out, i, axis=1)
            labels = np.delete(labels, i, axis=0)
        else: i+=1

    combinators = W_out.shape[1]  # its the input  dimension of W_out (larger)
    dimensions = W_out.shape[0]  # its the output dimension of W_out (smaller)

    if combinators != len(labels): return
    y_pos = np.arange(W_out.shape[1])

    #make the coloring
    colors = np.full((dimensions,combinators),'b')

    #scaled to biggest component
    fig, axs = plt.subplots(1, dimensions)
    fig.set_figheight(7.)
    fig.set_figwidth(6.)

    for dimension in range(dimensions):
        axs[dimension].barh(y_pos, W_out[dimension, :], color=colors[dimension])
        axs[dimension].set_yticks(y_pos)
        axs[dimension].set_yticklabels(labels)
        axs[dimension].set_ylim(combinators-0.5, -.5)
        axs[dimension].set_xlabel("Pred. " + str(labels[1+dimension]))
        axs[dimension].grid()
    plt.show()


    #scaled to (-1,+1)
    fig, axs = plt.subplots(1, dimensions)
    fig.set_figheight(7.)
    fig.set_figwidth(6.)

    for dimension in range(dimensions):
        axs[dimension].barh(y_pos, W_out[dimension, :], color=colors[dimension])
        axs[dimension].set_yticks(y_pos)
        axs[dimension].set_yticklabels(labels)
        axs[dimension].set_ylim(combinators - 0.5, -.5)
        axs[dimension].set_xlim(-1.05,1.05)
        axs[dimension].set_xlabel("Pred. " + str(labels[1 + dimension]))
        axs[dimension].grid()
    plt.show()


    return


#unfinished; example run below
def bifurcate_plot(fix_param: float, n_skip: int, n_shown_iter: int, step: int = 1, param_interval_min: float = 0.0, param_interval_max: float = 0.1):
    interval = np.linspace(param_interval_min, param_interval_max, step)
    def func(atadott):
        diffegy = Differential_Equation.Chua(a=atadott, b=fix_param)
        kezdo = [random.randrange(-1,1),random.randrange(-1,1),random.randrange(-1,1)]
        data = diffegy.generate_data(x0=kezdo, n_timepoints=n_skip + n_shown_iter, dt=0.1)
        X = data[n_skip:, 0]
        Y = data[n_skip:, 1]
        Z = data[n_skip:, 2]
        A = np.full(n_shown_iter - 1, atadott)
        return (X,Y,Z,A)

    res = Parallel(n_jobs=20)(delayed(func)(atadott) for atadott in interval)

    As = np.array([])
    Xs = np.array([])
    Ys = np.array([])
    Zs = np.array([])
    for i in range(len(res)):
        As = np.append(As,res[i][3])
        Xs = np.append(Xs,res[i][0])
        Ys = np.append(Ys, res[i][1])
        Zs = np.append(Zs, res[i][2])

    dpi = 180
    plt.plot(As, Xs, ls='', marker=',', color='black')
    plt.xlim(param_interval_min, param_interval_max)
    plt.savefig('bifurcation_' + str(param_interval_min) + '-' + str(param_interval_max) + '_x_' + str(step) + '.png',dpi=dpi)
    plt.plot(As, Ys, ls='', marker=',', color='black')
    plt.xlim(param_interval_min, param_interval_max)
    plt.savefig('bifurcation_' + str(param_interval_min) + '-' + str(param_interval_max) + '_y_' + str(step) + '.png',dpi=dpi)
    plt.plot(As, Zs, ls='', marker=',', color='black')
    plt.xlim(param_interval_min, param_interval_max)
    plt.savefig('bifurcation_' + str(param_interval_min) + '-' + str(param_interval_max) + '_z_' + str(step) + '.png',dpi=dpi)

    return
    #bifurcate_plot(seed = 14,n_skip= 100000,n_iter= 100, r_min=6, r_max=14,step=200)
