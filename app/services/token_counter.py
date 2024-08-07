import tiktoken





TOKEN_LIMIT = 20000


#"gpt-4o": "o200k_base",
#"gpt-4": "cl100k_base",
#"gpt-3.5-turbo": "cl100k_base",
#"gpt-3.5": "cl100k_base",  # Common shorthand
#"gpt-35-turbo": "cl100k_base",  # Azure deployment name
# embeddings
#"text-embedding-ada-002": "cl100k_base",
#"text-embedding-3-small": "cl100k_base",
#"text-embedding-3-large": "cl100k_base",

## this uses the new gpt4-o models token limit
ENCODING_NAME = "o200k_base"



def count_tokens(content: str) -> int:
    encoding = tiktoken.get_encoding(ENCODING_NAME)
    tokens = encoding.encode(content)
    num_tokens = len(tokens)
    return num_tokens

def check_token_limit(content: str, filename: str) -> tuple:
    num_tokens = count_tokens(content)
    if num_tokens > TOKEN_LIMIT:
        print(f"Warning: '{filename}' has {num_tokens} tokens, which exceeds the limit of {TOKEN_LIMIT} tokens.")
    return num_tokens, num_tokens <= TOKEN_LIMIT