from openai import OpenAI
import re

client = OpenAI(
    # Update api_key as found in https://console.llamaapi.com/ under 'Api Keys'
    api_key='',
    base_url='https://api.llama-api.com'
)


def explanation_api_call(prompt, filename=None, logs=None, experiment_repeat=None):
    """
    This function executes the API call to LLaMA 3.3 70B to explain a given process model.
    When parameters filename, logs and experiment_repeat are given, the LLaMA response is saved as .md file.
    Parameter filename is the name of the input data and is included in the output file.
    Parameter logs is the number of input logs the prompt is based on.
    Parameter experiment_repeat is the numerical trace, based on the number of repeats per input log amount.
    The function returns the LLaMA response.
    """
    r = client.chat.completions.create(
        model='llama3.3-70b',
        max_tokens=1800,
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    ).choices[0].message.content
    if filename and logs != None and experiment_repeat != None:
        try:
            m = open(f'results/paperSubmission/{filename}/explanations/{filename}-{logs}-{experiment_repeat}.md', 'w')
            m.write(r)
        except:
            print(f"Unexpected error writing explanation {filename} with {logs} logs, run {experiment_repeat}.")
    return r

def judgment_api_call(prompt_to_evaluate,
                        response_to_evaluate,
                        complete_pm,
                        filename=None, logs=None, experiment_repeat=None):
    """
    This function executes the API call to LLaMA 3.3 70B to give a judgment of an explanation.
    Parameter prompt_to_evaluate is the prompt the given explanation was based upon.
    Parameter response_to_evaluate is the explanation given by the LLM based on prompt_to_evaluate.
    Parameter complete_pm is the complete process model which the given explanation is compared to.
    When parameters filename, logs and experiment_repeat are given, the LLaMA response is saved as .md file.
    Parameter filename is the name of the input data and is included in the output file.
    Parameter logs is the number of input logs the prompt is based on.
    Parameter experiment_repeat is the numerical trace, based on the number of repeats per input log amount.
    The function returns the LLaMA response.
    """
    r = client.chat.completions.create(
        model='llama3.3-70b',
        max_tokens=9999,
        messages=[
            {
                'role': 'user',
                'content': make_judgment_prompt(prompt_to_evaluate,
                                             response_to_evaluate,
                                             complete_pm)
            }
        ]
    ).choices[0].message.content
    if filename and logs != None and experiment_repeat != None:
        try:
            m = open(f'results/paperSubmission/{filename}/judgments/{filename}-{logs}-{experiment_repeat}.md', 'w')
            m.write(r)
        except:
            print(f'Unexpected error writing judgment {filename} with {logs} logs, run {experiment_repeat}.')
    return r

def make_explanation_prompt(process_model):
    """
    This function returns the prompt used to generate an explanation on a given process model.
    Parameter process_model is the textual representation of the process model.
    """
    return f"""
        You are an expert in the field of process mining. 
        Given the following directed-follows graph, provide a clear 
        and concise explanation of the process flow. 
        {process_model} 
        Give a detailed explanation of the general business process, 
        with technical details such as sequences, parallel activities 
        and loops or conditions. Also mention any possible bottlenecks 
        or anomales in the data, as well as possible improvements 
        to enhance the business process. 
        
        Explain the process with technical details, highlighting 
        sequences, parallel activities and any loops or conditions 
        where applicable. Also mention any possible bottlenecks 
        or anomalies in the data.
    """

def make_judgment_prompt(pm_to_evaluate, response_to_evaluate, complete_pm):
    """
    This function returns the prompt used to generate a judgment on a given explanation.
    Parameter pm_to_evaluate is the textual representation of the process model the
    explanation is based upon.
    Parameter response_to_evaluate is the generated explanation by LLaMA.
    Parameter complete_pm is the textual representation of the complete process model
    which the generated explanation should be compared to.
    """
    return f"""
        An LLM has given an explanation of a process model based on a 
        limited amount of event log data. Evaluate the quality of the 
        explanation provided by the LLM compared to an explanation that 
        can be given based on the complete process model based on the following 
        3 quality metrics with scoring criteria. *Completeness* 1-3: Fails to 
        mention major elements (key activities, transitions or loops). 4-6: 
        Mentions some major elements but lacks detail or critical aspects. 7-9: 
        Covers most elements accurately, with minor omissions. 10: Fully 
        accurate explanation of all aspects. *Process Improvements* 1-3: Suggestions are 
        irrelevant, vague or inaccurate. 4-6: Some relevant suggestions but 
        lack completeness. 7-9: Actionable and relevant improvements with minor 
        omissions. 10: Precise, well-defined and actionable suggestions. 
        *Bottlenecks* 1-3: Fails to identify major bottlenecks or makes 
        incorrect claims. 4-6: Identifies some bottlenecks but misses key ones 
        or lacks detail. 7-9: Identifies most bottlenecks accurately with 
        minor omissions. 10: Accurately identifies all bottlenecks with 
        clear and detailed explanations. 
        Assign a rating on a scale of 1 (very bad) to 10 (perfect) 
        for each metric. Use the definitions above to guide your scoring. 
        Calculate the overall score as average of the metrics, presented in the format: 
        --[overall score]/10-- (include the minus signs).  
        The process model given to the LLM is as follows: {pm_to_evaluate} 
        The explanation given by the LLM is as follows: {response_to_evaluate} 
        The complete process model is as follows: {complete_pm} 
        Give an output stating the score of the metrics Completeness, 
        Improvements and Bottlenecks, with the Overall Score in the format 
        --[overall score]/10--.
    """


if __name__ == '__main__':
    # Array of the files used in the experiment, without suffixes
    file_names = ['411', '412', '413', '421', '422']

    # Directory in which the files are located
    file_directory = 'testData'
    
    # Different amount of input logs the process models are based on
    log_numbers = [5, 10, 20, 50, 100, 1000, 10000, 100000, 'complete']
    
    # Number of explanation-judgment pairs that are generated per input logs per file
    experiment_repeats = 5
    
    for file_name in file_names:
        # Dictionary where average scores per input logs are stored in
        overall = {}

        # Array of textual representations based on the amount of input logs
        files_to_evaluate = [open(f'{file_directory}/{file_name}-{l}-logs.txt', 'r').read() for l in log_numbers]
        
        # File that contains all obtained scores and average scores
        f = open(f'results/paperSubmission/{file_name}/{file_name}.txt', 'a')
        
        for i in range(len(log_numbers)):
            # Per input logs amount, an array of the obtained scores is made
            grade_list = []
            
            for j in range(experiment_repeats):
                """
                The judgment_api_call function is called to generate a judgment. One of the parameters of the
                function is the explanation_api_call function, which generates the explanation.
                The judgment is stored in variable judgment for further processing.
                """
                judgment = judgment_api_call(files_to_evaluate[i],
                                        explanation_api_call(make_explanation_prompt(files_to_evaluate[i]),
                                                        file_name, log_numbers[i], j),
                                        files_to_evaluate[-1],
                                        file_name, log_numbers[i], j)
                
                """
                The final score in the judgment is given in the form of --[score]/10--, which is extracted using
                a regular expression. When a wrong format type is generated, an error is raised and the errorous
                response is saved in a seperate folder. Most often, the result can be handled manually after the
                algorithm has finished.
                """
                try:
                    grade_list.append(float(re.search(r"--(?:\(|\[)?(.*?)(?:\)|\])?/10--", judgment).group(1)))
                except:
                    print(f"Wrong format type in overall score ({file_name}-{log_numbers[i]}-{j})")
                    f.write(f"Wrong format type in overall score ({file_name}-{log_numbers[i]}-{j}) \n")
                    h = open(f'results/paperSubmission/errorResponses/{file_name}-{log_numbers[i]}-{j}.md', 'w')
                    try:
                        h.write(judgment)
                    except:
                        print(f'Unexpected error writing error file {file_name} with {i} logs, run {j}.')
            
            """
            The results for the input logs amount are printed and stored in the general file f. The dictionary
            overall is updated with the average grade rounded to 2 decimals. The exception is typically raised
            when all runs of the input logs amount return a wrong format in the final score. In practice,
            this rarely happens.
            """
            print(f"#Log {log_numbers[i]}: {grade_list}")
            f.write(f"{log_numbers[i]} {str(grade_list)} \n")
            try:
                overall[log_numbers[i]] = round(sum(grade_list) / len(grade_list), 2)
            except:
                print(f"Error, most likely divide by 0 due to errorous responses in {file_name} {log_numbers[i]}.")
                f.write(f"Error, most likely divide by 0 due to errorous responses. Otherwise idk in {file_name} {log_numbers[i]}.")
        
        # Per file, the average scores per input logs amount are printed and stored in general file f.
        print(f"Overall scores for {file_name}: {overall}")
        f.write(f"Average scores: {str(overall)} \n")
