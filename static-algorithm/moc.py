import matplotlib.pyplot as plt
import numpy as np
import os

low, high = 2, 10
alpha = 0.03263156979782538
x = np.linspace(2.1, 9.9, 1000)

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(x, (high - x) ** (-1 - alpha), "r", label="high")
axs[0, 0].plot(x, (x - low) ** (-1 - alpha), "g", label="low")

axs[0, 1].plot(x, (high - x), "r", label="high")
axs[0, 1].plot(x, (x - low), "g", label="low")
# axs[0].plot(x, (high - x) ** (-1 - alpha) + (x - low) ** (-1 - alpha), "b", label="l")

x = np.linspace(0.00001, 1, 1000)
axs[1, 0].plot(x, x ** (-1), "r", label="x^-1")

if not os.path.exists("output"):
    os.makedirs("output")

plt.savefig(f"output/length.png")

# for i in range(1, 5):
#     words = np.pow(np.log(x), i)
#     low = np.exp(-np.pow(np.log(x), i))
#     high = np.exp(np.pow(np.log(x), i))
#
#     fig, axs = plt.subplots(2, 2)
#
#     axs[0, 0].plot(x, low, "r")
#     axs[0, 0].set_title("Low")
#
#     axs[0, 1].plot(x, high, "g")
#     axs[0, 1].set_title("High")
#
#     axs[1, 0].plot(x, words)
#     axs[1, 0].set_title("Words")
#
#     fig.suptitle(f"Plot {i}")
#
#     if not os.path.exists("output"):
#         os.makedirs("output")
#
#     plt.savefig(f"output/plot_{i}.png")
