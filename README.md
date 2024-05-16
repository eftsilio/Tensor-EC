# Tensor-EC: A Tensor-Based Formalization of the Event Calculus

Tensor-EC is an open-source tensor formalization of the [Event Calculus](https://en.wikipedia.org/wiki/Event_calculus) (EC), optimized for data stream reasoning.

# License

Tensor-EC comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions; see the [GNU Lesser General Public License v3 for more details](http://www.gnu.org/licenses/lgpl-3.0.html).

# File Description

Symbolic-EC is the symbolical implementation of EC and is written in XSB Prolog. You will need to install XSB Prolog 5.0.0 in your system before running this code.

Tensor-EC is implemented in Python and is tensted under Python 3.11.4, NumPy 1.25.2 and SciPy 1.10.1. A subset of the public dataset of Brest is provided as a csv file and can be found in the folder `./examples/maritime/brest/data/dynamic_data'. The first time you will run the code, you need to unzip the file found in the aforemetnioned directory.

To run the source code of each method you have to enter the corresponding directory, \`./symbolic-EC' for the logic implementation of EC and `./Tensor-EC' for the tensor method, open a terminal and type the following command:

```python
$ python3 run-exps.py```

The results will be saved in the following directories for each method:
- Symbolic-EC: `./examples/maritime/data/results/symbolic-EC'
- Tensor-EC: ./examples/maritime/data/results/Tensor-EC'

# Documentation

- Tsilionis E., Artikis A. and Paliouras G., [A Tensor-Based Formalization of the Event Calculus](https://cer.iit.demokritos.gr/publications/papers/2024/tensor-EC.pdf). In International Joint Conference on Artificial Intelligence (IJCAI), 2024.

# Related Software
- [RTEC](https://github.com/aartikis/RTEC): RTEC is an Event Calculus implementation optimised for stream reasoning.
