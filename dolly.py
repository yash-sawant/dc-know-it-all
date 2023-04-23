import torch
from transformers import pipeline
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline

class Dolly:
  def __init__(self):
    # generate_text = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")
    generate_text = pipeline(model="databricks/dolly-v2-3b", torch_dtype=torch.bfloat16,
                            trust_remote_code=True, device_map="auto", return_full_text=True)

    # template for an instrution with no input
    prompt = PromptTemplate(
        input_variables=["instruction"],
        template="{instruction}")

    # template for an instruction with input
    prompt_with_context = PromptTemplate(
        input_variables=["instruction", "context"],
        template="{instruction}\n\nInput:\n{context}")

    hf_pipeline = HuggingFacePipeline(pipeline=generate_text)
    self.llm_chain = LLMChain(llm=hf_pipeline, prompt=prompt)
    self.llm_context_chain = LLMChain(llm=hf_pipeline, prompt=prompt_with_context)

  def ask(self, ques):
    return self.llm_chain.predict(instruction=ques).lstrip()


  def ask_with_context(self, ques, context):
    return self.llm_context_chain.predict(instruction=ques, context=context).lstrip()