from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from app.core.config import settings
from huggingface_hub import login
from accelerate import disk_offload

class LLMModule:
    def __init__(self, model_name="meta-llama/Llama-3.2-1B", max_context=1000):
        login(token=settings.HF_TOKEN)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, low_cpu_mem_usage=True,  offload_state_dict = True).cpu()
        disk_offload(model=self.model, offload_dir="alpha")
        self.pipeline = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        self.max_context = max_context
        self.history = []
    
    def add_to_history(self, user_input: str):
        self.history.append(user_input)
        if len(self.history) > self.max_context:
            self.history.pop(0)
    
    def generate_response(self, user_query: str) -> str:
        self.add_to_history(user_query)
        context = " ".join(self.history)
        response = self.pipeline(context, max_length=200, num_return_sequences=1)[0]["generated_text"]
        self.history.append(response)
        return response
