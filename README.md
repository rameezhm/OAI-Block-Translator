# OAI-Block-Translator

Sometimes line-by-line translation using LLMs like GPT-3.5 can have poor results due to lack of context. This program seeks to provide a GUI that can allow you to enter multiple lines so that translation can be provided with full context, while also returning a line-by-line result.

## Configuration

Place your OpenAI key in the OPENAI_KEY file in the base directory of this project. 



The prompt that the program uses is stored in the BASE_PROMPT file in the base directory of this project. You can use the default provided or modify it to fit your preferences. Note that the program assumes that the response is in JSON format, so make sure you include an instruction in the prompt to return a JSON result. [See here for more details about JSON mode.](https://platform.openai.com/docs/guides/text-generation/json-mode)

## Usage

Install dependencies with
```bash
pip install -r requirements.txt
```
Then just run the program with
```bash
python main.py
```
Fill in the text box with the line you want to translate, using the "Add Line" button for each new line you want to add. Hit the "Submit" button to get the translated result.
