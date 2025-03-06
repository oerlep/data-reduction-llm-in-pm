# Towards Data-Efficient Large Language Model Explanations for Process Mining

This repository contains all relevant data and results as presented in the paper 'Towards Data-Efficient Large Language Model Explanations for Process Mining', submitted to the [BPM 2025 Conference](https://www.bpm2025seville.org/).

In the <em>code</em> section, the used algorithms for the data pre-processing and explanation-judgment generation can be found. The textual representations as used in the main algorithm can be found in the <em>data</em> section.
The <em>results</em> section is split per experiment as found in [1]. Each experiment folder contains a .txt file containing an overview of the given scores per amount of input log size. Furthermore, all generated explanations and judgments per process model can be found in the corresponding folders. The name of the files are in the format of <em>[experiment]-[log_amount]-[run_number].md</em>.

## Running locally
### Windows
1. Clone the repository locally.
2. Paste your API token from [the LLaMA API website](https://www.llamaapi.com/en/dashboard/api-token) in line 6 of ``code/main.py``.
3. Make sure you have the required packages installed.
```cmd
pip install openai re pm4py pandas
```
4. Run the code.
```cmd
python code/main.py
```

### Linux
1. Clone the repository locally.
2. Paste your API token from [the LLaMA API website](https://www.llamaapi.com/en/dashboard/api-token) in line 6 of ``code/main.py``.
3. Make sure you have the required packages installed.
```bash
sudo apt install openai re pm4py pandas
```
4. Run the code.
```bash
python code/main.py
```

Please note that running the code might take a while due to the large amount of API requests made to the LLaMA API.



[1] Bemthuis, Rob; M. (Martijn) Koot; Mes, M.R.K. (Martijn); F.A. (Faiza) Bukhsh; Iacob, M.E. (Maria-Eugenia) et. al. (2021): Data underlying the paper: An agent-based process mining architecture for emergent behavior analysis. Version 2. 4TU.ResearchData. dataset. https://doi.org/10.4121/12708839.v2
