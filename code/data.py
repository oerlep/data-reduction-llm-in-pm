import pm4py
import pandas as pd

# Prevents an error in the DataFrame
pd.options.mode.chained_assignment = None


# Clear overview of the flow of processes with nodes and arcs
# Returns the textual representation for the LLM
def show_petri_net(log):
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(log)
    pm4py.view_petri_net(net, initial_marking, final_marking)
    return pm4py.llm.abstract_petri_net(net, initial_marking, final_marking, False)

# Returns the textual representation of the Directed-Follows Graph (DFG)
def get_textual_dfg(log):
    # dfg, start, end = pm4py.discover_dfg(log)
    # pm4py.view_dfg(dfg, start, end)
    return pm4py.llm.abstract_dfg(log, response_header=False)

# Save visual of DFG
def save_dfg(log, output='save.png'):
    dfg, start, end = pm4py.discover_dfg(log)
    pm4py.save_vis_dfg(dfg, start, end, f'{file_path}/images/{output}')

# Get textual DFG from first N lines of log file
# Saves visual when save parameter is set to True
def get_dfg_from_n(log, n, save_img=False, save_text=False, file='save411'):
    log = log.head(n)
    if save_img:
        save_dfg(log, f'{file}-{n}-logs.png')
    if save_text:
        f = open(f'{file_path}/{file}-{n}-logs.txt', 'w')
        f.write(get_textual_dfg(log))
    return get_textual_dfg(log)

def get_complete_dfg(log, save_img=False, save_text=False, file='save411'):
    if save_img:
        save_dfg(log, f'{file}-complete.png')
    if save_text:
        f = open(f'{file_path}/{file}-complete.txt', 'w')
        f.write(get_textual_dfg(log))
    return get_textual_dfg(log)


if __name__ == '__main__':
    # Array of files to process, without their suffixes
    files = ['411', '412', '413', '421', '422']

    for file in files:
        # Directory where the files are found
        dir_path = f'FilteredFiles/{file}.xes'
        
        # Amount of input logs the output models are based on
        log_counts = [5, 10, 20, 50, 100, 1000, 10000, 100000]
        
        # Directory of the output files
        file_path = 'testData'
        
        # Read the .xes file and converts them to event logs
        logs = pm4py.read_xes(dir_path)
        
        for log_amount in log_counts:
            # Saves the DFG in the directory indicated for each input logs amount
            get_dfg_from_n(logs, log_amount, save_img=True, save_text=True, file=file)
        
        # Finally saves the DFG based on the complete set of input logs
        get_complete_dfg(logs, save_img=True, save_text=False, file=file)
